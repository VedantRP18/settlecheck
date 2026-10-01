import csv, os, random

random.seed(42)
os.makedirs("data", exist_ok=True)

# 20 fake payments
payments = []
for i in range(1, 21):
    payments.append({
        "payment_id": f"pay_{i:03d}",
        "date": f"2026-09-{random.randint(1, 28):02d}",
        "amount_paise": random.choice([49900, 99900, 150000, 250000]),
    })

# the bank starts as an exact copy
bank = [dict(p) for p in payments]

# now plant mistakes
bank = [r for r in bank if r["payment_id"] != "pay_004"]   # missing
for r in bank:
    if r["payment_id"] == "pay_009":
        r["amount_paise"] -= 2000   # short by Rs 20
    if r["payment_id"] == "pay_013":
        r["amount_paise"] += 500    # Rs 5 extra
bank.append(dict(bank[0]))          # pay_001 appears twice

def save(name, rows):
    with open(f"data/{name}", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["payment_id", "date", "amount_paise"])
        w.writeheader()
        w.writerows(rows)

save("payments.csv", payments)
save("bank.csv", bank)
print("Done: data/payments.csv and data/bank.csv created")