"""CSV migration audit tool using synthetic examples only; no real HR data."""
from __future__ import annotations
import argparse, csv, json
from dataclasses import asdict, dataclass
from decimal import Decimal, InvalidOperation
from pathlib import Path

REQUIRED = ("employee_id", "department", "salary")

@dataclass(frozen=True)
class Issue:
    category: str
    employee_id: str
    detail: str

def load_rows(path: Path):
    records, issues = {}, []
    with path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None or not set(REQUIRED).issubset(reader.fieldnames):
            raise ValueError(f"CSV must contain: {', '.join(REQUIRED)}")
        for row_number, row in enumerate(reader, start=2):
            key = (row.get("employee_id") or "").strip()
            if not key:
                issues.append(Issue("missing_id", "", f"line {row_number}"))
                continue
            if key in records:
                issues.append(Issue("duplicate_id", key, f"line {row_number}"))
                continue
            department = (row.get("department") or "").strip()
            if not department:
                issues.append(Issue("missing_department", key, f"line {row_number}"))
            try:
                salary = Decimal((row.get("salary") or "").strip())
                if not salary.is_finite() or salary < 0: raise InvalidOperation()
            except (InvalidOperation, ValueError):
                issues.append(Issue("invalid_salary", key, f"line {row_number}"))
                salary = None
            records[key] = {"department": department.casefold(), "salary": salary}
    return records, issues

def audit(source: Path, target: Path) -> dict:
    old, source_issues = load_rows(source)
    new, target_issues = load_rows(target)
    issues = [*source_issues, *target_issues]
    for key in sorted(set(old) - set(new)):
        issues.append(Issue("missing_in_target", key, "record not migrated"))
    for key in sorted(set(new) - set(old)):
        issues.append(Issue("unexpected_in_target", key, "new record not in source"))
    for key in sorted(set(old) & set(new)):
        for field in ("department", "salary"):
            if old[key][field] != new[key][field]:
                issues.append(Issue("mismatch_" + field, key, f"{field} differs"))
    return {"source_rows_unique": len(old), "target_rows_unique": len(new),
        "passed": len(issues) == 0,
        "issue_counts": {cat: sum(x.category == cat for x in issues)
                         for cat in sorted({x.category for x in issues})},
        "issues": [asdict(x) for x in issues]}

def main():
    p = argparse.ArgumentParser(description="Audit legacy and target ERP CSV exports")
    p.add_argument("source", type=Path)
    p.add_argument("target", type=Path)
    p.add_argument("--report", type=Path)
    args = p.parse_args()
    result = audit(args.source, args.target)
    output = json.dumps(result, indent=2)
    print(output)
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(output + "\n", encoding="utf-8")
    return 0 if result["passed"] else 1

if __name__ == "__main__": raise SystemExit(main())
