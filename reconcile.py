import csv
from collections import Counter

def load(path):
    with open(path, newline="") as f:
        return list(csv.DictReader(f))

payments = load("data/payments.csv")
bank = load("data/bank.csv")

expected = {r["payment_id"]: int(r["amount_paise"]) for r in payments}
bank_counts = Counter(r["payment_id"] for r in bank)

bank_amount = {}
for r in bank:
    bank_amount.setdefault(r["payment_id"], int(r["amount_paise"]))

issues = []

for pid, amt in expected.items():
    if pid not in bank_counts:
        issues.append((pid, "MISSING_IN_BANK", amt, 0, -amt))
        continue
    if bank_amount[pid] != amt:
        issues.append((pid, "AMOUNT_MISMATCH", amt, bank_amount[pid], bank_amount[pid] - amt))
    if bank_counts[pid] > 1:
        extra = amt * (bank_counts[pid] - 1)
        issues.append((pid, "DUPLICATE_IN_BANK", amt, amt * bank_counts[pid], extra))

for pid in bank_counts:
    if pid not in expected:
        issues.append((pid, "NOT_IN_PAYMENTS", 0, bank_amount[pid], bank_amount[pid]))

print(f"Checked {len(expected)} payments, found {len(issues)} issues\n")
for pid, kind, exp, act, diff in issues:
    print(f"{pid:8} {kind:18} expected Rs {exp/100:>8.2f}  bank Rs {act/100:>8.2f}  difference Rs {diff/100:+.2f}")

with open("data/issues.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["payment_id", "issue_type", "expected_paise", "bank_paise", "difference_paise"])
    w.writerows(issues)