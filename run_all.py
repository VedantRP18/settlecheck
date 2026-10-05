"""Run the whole SettleCheck pipeline with one command:  py run_all.py"""
import subprocess, sys

STEPS = ["fetch_payments.py", "make_bank.py", "reconcile.py", "explain.py"]

for step in STEPS:
    print(f"\n=== {step} ===")
    if subprocess.run([sys.executable, step]).returncode != 0:
        sys.exit(f"\nStopped: {step} failed. Fix that, then run again.")
print("\nDone. See data/report.txt")
