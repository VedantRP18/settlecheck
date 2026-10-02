import os, csv, razorpay
from datetime import datetime

client = razorpay.Client(auth=(os.environ["RAZORPAY_KEY_ID"],
                               os.environ["RAZORPAY_KEY_SECRET"]))

items = client.payment.all({"count": 100})["items"]
captured = [p for p in items if p["status"] == "captured"]

os.makedirs("data", exist_ok=True)
with open("data/payments.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["payment_id", "date", "amount_paise"])
    for p in captured:
        date = datetime.fromtimestamp(p["created_at"]).strftime("%Y-%m-%d")
        w.writerow([p["id"], date, p["amount"]])

print(f"Saved {len(captured)} captured payments to data/payments.csv")