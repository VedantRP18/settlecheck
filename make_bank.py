import csv

with open("data/payments.csv", newline="") as f:
    rows = list(csv.DictReader(f))

if len(rows) < 4:
    raise SystemExit("Need at least 4 payments first. Make more test payments.")

bank = [dict(r) for r in rows]

missing_id = bank[0]["payment_id"]          # first payment never arrives
bank = [r for r in bank if r["payment_id"] != missing_id]

bank[0]["amount_paise"] = str(int(bank[0]["amount_paise"]) - 2000)  # Rs 20 short
bank[1]["amount_paise"] = str(int(bank[1]["amount_paise"]) + 500)   # Rs 5 extra
bank.append(dict(bank[2]))                                          # duplicate entry

with open("data/bank.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["payment_id", "date", "amount_paise"])
    w.writeheader()
    w.writerows(bank)

print("Planted: 1 missing, 1 short, 1 extra, 1 duplicate")
print("Missing payment:", missing_id)