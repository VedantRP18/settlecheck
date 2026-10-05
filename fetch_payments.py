import os, csv, sys, razorpay
from datetime import datetime

key_id = os.environ.get("RAZORPAY_KEY_ID")
key_secret = os.environ.get("RAZORPAY_KEY_SECRET")
if not key_id or not key_secret:
    sys.exit("Set RAZORPAY_KEY_ID and RAZORPAY_KEY_SECRET first (see README).")

client = razorpay.Client(auth=(key_id, key_secret))

# Razorpay returns at most 100 payments per request, so keep asking for the next page.
items, skip = [], 0
while True:
    batch = client.payment.all({"count": 100, "skip": skip})["items"]
    items.extend(batch)
    if len(batch) < 100:
        break
    skip += 100
captured = [p for p in items if p["status"] == "captured"]

os.makedirs("data", exist_ok=True)
with open("data/payments.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["payment_id", "date", "amount_paise"])
    for p in captured:
        date = datetime.fromtimestamp(p["created_at"]).strftime("%Y-%m-%d")
        w.writerow([p["id"], date, p["amount"]])

print(f"Fetched {len(items)} payments, saved {len(captured)} captured ones to data/payments.csv")
