# day08_modules.py
import oee_utils
from datetime import datetime
import random

random.seed(42)

machines = ["CNC Mill #4", "Press #2", "Assembly Line A", "Weld Station B"]

report_time = datetime.now().strftime("%Y-%m-%d %H:%M")

print("=" * 52)
print(f"  OEE FLEET REPORT — {report_time}")
print("=" * 52)

for machine in machines:
    actual_run = random.randint(350, 475)
    units      = random.randint(600, 920)
    good_units = units - random.randint(0, 20)

    try:
        avail  = oee_utils.calculate_availability(actual_run, 480)
        perf   = oee_utils.calculate_performance(units, 480)
        qual   = oee_utils.calculate_quality(good_units, units)
        oee    = oee_utils.calculate_oee(avail, perf, qual)
        status = oee_utils.classify_oee(oee)
        print(f"  {machine:<22} OEE: {oee*100:.1f}%  [{status}]")
    except ValueError as e:
        print(f"  {machine:<22} [ERROR] {e}")

print("=" * 52)