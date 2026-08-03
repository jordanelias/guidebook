#!/usr/bin/env python3
"""
scripts/contamination_sampler.py — BPC contamination sampling utility (per governance/doctrine-recheck.md, A13 §7).

Implements the §3.1 stratified-deterministic sampling methodology adapted from
Stage 0.4 (workplan/co0007-contamination-sample.md).

The tool walks the BPC corpus, stratifies by topic group, selects N≥15 files
deterministically (first-alphabetical within each topic-group stratum), and
writes a sampling manifest with `disposition: PENDING` placeholders. The
recheck reviewer fills disposition by human classification.

Usage:
    python3 scripts/contamination_sampler.py                   # N=15, default seed
    python3 scripts/contamination_sampler.py --n 25            # N=25
    python3 scripts/contamination_sampler.py --output PATH     # custom output
    python3 scripts/contamination_sampler.py --recheck-id RC-001  # set recheck association

Exit codes: 0 = sample written; 2 = corpus not found.
"""

import argparse
import datetime
import glob
import math
import os
import sys

import yaml

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BPC_ROOT = os.path.join(REPO_ROOT, "references", "bpc")
RECHECK_DIR = os.path.join(REPO_ROOT, "data", "doctrine_recheck")


def discover_topic_groups(corpus_root: str) -> dict[str, list[str]]:
    """Walk corpus_root — return {topic_group: sorted_filenames_relative_to_topic}."""
    if not os.path.isdir(corpus_root):
        return {}
    groups: dict[str, list[str]] = {}
    for entry in sorted(os.listdir(corpus_root)):
        topic_dir = os.path.join(corpus_root, entry)
        if not os.path.isdir(topic_dir):
            continue
        files = sorted(
            f for f in os.listdir(topic_dir)
            if f.endswith(".md") and not f.startswith(".")
        )
        if files:
            groups[entry] = files
    return groups


def stratify_sample(
    groups: dict[str, list[str]], n: int
) -> list[tuple[str, str]]:
    """Allocate N samples across topic groups proportionally; select first-alphabetical
    within each group's stratum. Returns list of (topic_group, filename) tuples.

    Allocation rule:
    - Each group with ≥1 file gets ≥1 sample
    - Remaining samples allocated proportionally by population size, rounded
    """
    if not groups:
        return []

    total = sum(len(v) for v in groups.values())
    if n > total:
        # Sample everything if n > population
        return [(g, f) for g, files in groups.items() for f in files]

    # Initial allocation: 1 per group
    allocation = {g: 1 for g in groups}
    remaining = n - len(groups)
    if remaining < 0:
        # n < number of groups: rare; allocate 1 to the n largest groups
        sorted_groups = sorted(
            groups.items(), key=lambda kv: -len(kv[1])
        )
        return [(g, files[0]) for g, files in sorted_groups[:n]]

    # Proportional allocation of remaining
    excess_pool: dict[str, float] = {}
    for g, files in groups.items():
        # Each group's "extra" share is (population - 1) — already given 1
        share = max(0, len(files) - 1)
        excess_pool[g] = share
    excess_total = sum(excess_pool.values())
    if excess_total > 0:
        for g in groups:
            extra = math.floor(remaining * excess_pool[g] / excess_total)
            allocation[g] += extra

    # Top up any rounding shortfall by giving to largest groups
    while sum(allocation.values()) < n:
        sorted_groups = sorted(
            groups.items(), key=lambda kv: -len(kv[1])
        )
        for g, files in sorted_groups:
            if allocation[g] < len(files):
                allocation[g] += 1
                if sum(allocation.values()) >= n:
                    break

    # Cap at group population
    for g in groups:
        allocation[g] = min(allocation[g], len(groups[g]))

    # Select first-alphabetical from each group
    selected: list[tuple[str, str]] = []
    for g, files in groups.items():
        for fn in files[:allocation[g]]:
            selected.append((g, fn))
    return selected


def write_manifest(
    selected: list[tuple[str, str]],
    output_path: str,
    recheck_id: str,
    n: int,
) -> None:
    now = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M")
    samples = []
    for topic, fn in selected:
        samples.append({
            "recheck_id": recheck_id,
            "bpc_path": f"references/bpc/{topic}/{fn}",
            "topic_group": topic,
            "disposition": "PENDING",
            "disposition_rationale": "TBD by reviewer",
            "reviewer": "TBD",
            "review_date": now,
        })
    manifest = {
        "sample_date": now,
        "recheck_id": recheck_id,
        "sample_size_requested": n,
        "sample_size_actual": len(selected),
        "stratification_method": "first-alphabetical within topic group; "
                                 "proportional allocation with floor=1 per group",
        "samples": samples,
    }
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        yaml.dump(
            manifest, f, default_flow_style=False,
            sort_keys=False, allow_unicode=True
        )


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--n", type=int, default=15,
                    help="sample size (default 15; minimum 15)")
    ap.add_argument("--seed", type=int, default=0,
                    help="(reserved for future tie-breaking; current methodology "
                         "is deterministic, no randomness)")
    ap.add_argument("--corpus-root", default=None,
                    help=f"override default {BPC_ROOT}")
    ap.add_argument("--output", default=None,
                    help="override default sample output path")
    ap.add_argument("--recheck-id", default="RC-PENDING",
                    help="recheck_id this sample belongs to (default RC-PENDING)")
    args = ap.parse_args()

    if args.n < 15:
        print(
            f"WARNING: n={args.n} is below the methodology minimum (15). "
            f"Proceeding anyway."
        )

    corpus_root = args.corpus_root or BPC_ROOT
    if not os.path.isdir(corpus_root):
        print(f"ERROR: corpus root not found: {corpus_root}")
        return 2

    groups = discover_topic_groups(corpus_root)
    total_files = sum(len(v) for v in groups.values())
    print(
        f"Discovered {len(groups)} topic groups; {total_files} BPC files total"
    )

    if total_files < args.n:
        print(
            f"WARNING: corpus has only {total_files} files; sample size {args.n} "
            f"exceeds population. Sampling all files."
        )

    selected = stratify_sample(groups, args.n)
    print(f"Selected {len(selected)} files:")
    for topic, fn in selected:
        print(f"  {topic}/{fn}")

    if args.output:
        out_path = args.output
    else:
        date_tag = datetime.datetime.utcnow().strftime("%Y-%m-%d")
        out_path = os.path.join(RECHECK_DIR, f"sample_{date_tag}.yaml")

    write_manifest(selected, out_path, args.recheck_id, args.n)
    print(f"\nSampling manifest written: {os.path.relpath(out_path, REPO_ROOT)}")
    print(
        f"Recheck reviewer: classify each sampled BPC's disposition (CLEAN / "
        f"AMBIGUOUS / STUB / MERGED) and update the manifest."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
