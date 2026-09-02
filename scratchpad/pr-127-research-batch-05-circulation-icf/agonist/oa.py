#!/usr/bin/env python3
"""R10 rung: Unpaywall OA location lookup, logged."""
import sys
sys.path.insert(0, "scripts/research")
from retrieval_log import fetch
S = "session_2026-09-02-research-batch-05-circulation-icf"
for doi in sys.argv[1:]:
    p = fetch(f"https://api.unpaywall.org/v2/{doi}?email=jordan.a.elias@gmail.com",
              session=S, purpose=f"unpaywall OA locations for {doi}")
    print(f"\n=== {doi}")
    if not p:
        print("  no payload"); continue
    print("  is_oa:", p.get("is_oa"), "| status:", p.get("oa_status"))
    for loc in (p.get("oa_locations") or []):
        print("   -", loc.get("host_type"), "|", loc.get("version"), "|", loc.get("license"))
        print("     pdf:", loc.get("url_for_pdf"))
        print("     landing:", loc.get("url_for_landing_page"))
