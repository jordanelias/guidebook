-- 065: rationale_ref becomes a typed pointer at the decision that authorises the edge.
--
-- OD-A (D-0175, owner ruling 2026-08-31) rules item_population_links SUBSTRATE
-- PROVISIONALLY: any edge a determination RELIES ON must be re-derived and carry a
-- rationale_ref in that determination's own migration.
--
-- Measured 2026-08-31, that obligation was unenforceable: rationale_ref is an
-- unconstrained INTEGER with NO foreign key, so it points at nothing and ANY integer
-- satisfies "carries a rationale_ref". Owner ruling 2026-09-01: it references the
-- DECISION that authorises the edge -- decisions.decision_id, which is TEXT. Hence a
-- type change, hence a rebuild: SQLite cannot alter a column's type or add a foreign
-- key in place.
--
-- Everything else is preserved deliberately and verified after: the PRIMARY KEY
-- (item_code, population_code, subtype), the applicability CHECK and its five-value
-- vocabulary (dbcore.check_values reads it, so losing it disarms db.py's refusal), the
-- populations and items foreign keys INCLUDING ON DELETE CASCADE, and both named
-- indexes. No view reads this table, so none needs dropping -- verified, not assumed.
--
-- rationale_ref stays NULLABLE. The 372 existing edges keep NULL: OD-A's debt is paid
-- where an edge is USED, not all at once, and making it NOT NULL would either forge 372
-- warrants or block the table entirely.

PRAGMA legacy_alter_table=OFF;

CREATE TABLE item_population_links__065 (
  item_code           TEXT NOT NULL,
  population_code     TEXT NOT NULL REFERENCES populations(population_code),
  subtype             TEXT NOT NULL DEFAULT '',  -- '' = no subtype; use empty string so PK works
  applicability       TEXT NOT NULL DEFAULT 'applies' CHECK(applicability IN (
                        'applies', 'applies_strictly', 'applies_loosely',
                        'context_dependent', 'does_not_apply'
                      )),
  rationale_ref       TEXT REFERENCES decisions(decision_id),
  created_at          TEXT,
  created_by_session  TEXT,
  PRIMARY KEY (item_code, population_code, subtype),
  FOREIGN KEY (item_code) REFERENCES items(item_code) ON DELETE CASCADE
);

-- CAST to TEXT is a formality: all 372 rows carry NULL, so nothing is converted.
INSERT INTO item_population_links__065
  (item_code, population_code, subtype, applicability, rationale_ref,
   created_at, created_by_session)
SELECT item_code, population_code, subtype, applicability,
       CAST(rationale_ref AS TEXT), created_at, created_by_session
FROM item_population_links;

DROP TABLE item_population_links;
ALTER TABLE item_population_links__065 RENAME TO item_population_links;

CREATE INDEX idx_ipl_pop  ON item_population_links(population_code);
CREATE INDEX idx_ipl_item ON item_population_links(item_code);

PRAGMA user_version = 65;
