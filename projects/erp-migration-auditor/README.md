# ERP Migration Auditor 🔎

An original Python **CSV migration quality gate** inspired by Ibrar's past ERP and legacy-data migration work. The included datasets are fictional; **no employer or employee records are exposed**.

### Implemented
- CSV schema and required-field validation, duplicate IDs, missing departments and negative/invalid salary detection.
- Source–target record reconciliation and changed-field checks.
- Currency-safe `decimal.Decimal` comparison, normalized department capitalization, JSON audit output.
- Nonzero process exit status for failed migrations, helpful for CI integration.
- Three unit tests and intentionally mismatched demonstration files.

### Run
```bash
python audit.py examples/legacy.csv examples/migrated.csv --report reports/audit.json
python -m unittest discover -v
```

The sample returns exit code 1 **by design**: one record was lost and one salary changed. For deployment: add encrypted data handling, per-field schema mapping, authentication, an audit trail and CI dashboards.
