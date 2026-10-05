import csv, os, sys

sys.stdout.reconfigure(encoding="utf-8")  # so symbols like the rupee sign don't crash Windows

with open("data/issues.csv", newline="", encoding="utf-8") as f:
    issues = list(csv.DictReader(f))

# The only reasons the AI is allowed to pick from
REASONS = {
    "MISSING_IN_BANK": "payment not yet settled, settlement delayed, or the bank entry was dropped",
    "AMOUNT_MISMATCH": "gateway fee or tax deducted, partial refund, or a data entry error",
    "DUPLICATE_IN_BANK": "settlement posted twice, or the bank file was imported twice",
    "NOT_IN_PAYMENTS": "bank credit with no matching Razorpay payment: a payment from another source, a wrong ID, or a test entry",
}

def template_explain(i):
    diff = int(i["difference_paise"]) / 100
    return (f"{i['issue_type']}: difference of Rs {diff:+.2f}. "
            f"Possible causes: {REASONS.get(i['issue_type'], 'unclear')}. "
            f"Check this payment manually.")

client = None
if os.environ.get("ANTHROPIC_API_KEY"):
    import anthropic
    client = anthropic.Anthropic()

def ai_explain(i):
    prompt = (
        "You help a small shop owner understand payment mismatches.\n"
        f"Issue: {i}\n"
        f"Allowed likely causes: {REASONS.get(i['issue_type'], 'unclear')}\n"
        "Explain in under 40 words, in plain English, what probably happened "
        "and one thing to check. Amounts are in paise (100 paise = Rs 1). "
        "If you are unsure, say 'unclear' instead of guessing."
    )
    msg = client.messages.create(
        model="claude-sonnet-5-5",
        max_tokens=200,
        messages=[{"role": "user", "content": prompt}],
    )
    return msg.content[0].text.strip()

lines = []
for i in issues:
    try:
        text = ai_explain(i) if client else template_explain(i)
    except Exception as e:
        text = template_explain(i) + f" (AI unavailable: {e})"
    lines.append(f"{i['payment_id']}: {text}")

report = "\n\n".join(lines)
print(report)
with open("data/report.txt", "w", encoding="utf-8") as f:
    f.write(report)
