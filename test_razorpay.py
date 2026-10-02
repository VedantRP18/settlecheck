import os, razorpay

client = razorpay.Client(auth=(os.environ["RAZORPAY_KEY_ID"],
                               os.environ["RAZORPAY_KEY_SECRET"]))

# Create one test order (like a fake invoice, no money moves)
order = client.order.create({
    "amount": 49900,        # in paise = Rs 499
    "currency": "INR",
    "receipt": "settlecheck_test_1",
})
print("Created order:", order["id"], order["amount"], order["status"])

# List recent test payments
payments = client.payment.all({"count": 10})
print("Payments found:", len(payments["items"]))