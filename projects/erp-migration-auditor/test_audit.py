import csv, tempfile, unittest
from pathlib import Path
from audit import audit, load_rows

class MigrationTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.folder = Path(self.tmp.name)
    def csvfile(self, name, rows):
        path = self.folder / name
        with path.open("w", newline="", encoding="utf-8") as output:
            w = csv.DictWriter(output, fieldnames=["employee_id", "department", "salary"])
            w.writeheader()
            w.writerows(rows)
        return path
    def test_clean_migration(self):
        source = self.csvfile("source.csv", [{"employee_id":"E01","department":"HR","salary":"3000.00"}])
        target = self.csvfile("target.csv", [{"employee_id":"E01","department":"hr","salary":"3000"}])
        self.assertTrue(audit(source, target)["passed"])
    def test_detects_missing_and_changed_records(self):
        src = self.csvfile("src.csv", [
            {"employee_id":"E01","department":"IT","salary":"100"},
            {"employee_id":"E02","department":"HR","salary":"200"}])
        dst = self.csvfile("dst.csv", [{"employee_id":"E01","department":"IT","salary":"101"}])
        result = audit(src, dst)
        self.assertEqual(result["issue_counts"]["missing_in_target"], 1)
        self.assertEqual(result["issue_counts"]["mismatch_salary"], 1)
    def test_duplicate_invalid_and_blank(self):
        file = self.csvfile("bad.csv", [
            {"employee_id":"E01","department":"","salary":"-3"},
            {"employee_id":"E01","department":"HR","salary":"100"}])
        _, errors = load_rows(file)
        self.assertEqual({e.category for e in errors},
                         {"duplicate_id","missing_department","invalid_salary"})

if __name__ == "__main__": unittest.main()
