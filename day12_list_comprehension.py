# Day 12 — List Comprehensions and Pythonic Code
# Python Bootcamp 

from datetime import datetime


# --- Simulated Data ---
production_data = [
    {"machine": "CNC Mill #4",     "shift": "Day",   "actual_run": 437, "planned": 480, "units": 842, "good_units": 821},
    {"machine": "Press #2",        "shift": "Day",   "actual_run": 390, "planned": 480, "units": 760, "good_units": 741},
    {"machine": "Assembly Line A", "shift": "Night", "actual_run": 465, "planned": 480, "units": 910, "good_units": 905},
    {"machine": "Weld Station B",  "shift": "Night", "actual_run": 310, "planned": 480, "units": 620, "good_units": 589},
    {"machine": "Drill Press #1",  "shift": "Day",   "actual_run": 421, "planned": 480, "units": 798, "good_units": 780},
]


# --- OEE Calculations using comprehensions ---
def calc_oee(r):
    avail = r["actual_run"] / r["planned"]
    perf  = r["units"] / (r["planned"] * 1.8)
    qual  = r["good_units"] / r["units"]
    return avail * perf * qual


# List of OEE scores
oee_scores = [calc_oee(r) for r in production_data]

# Machine names only
machine_names = [r["machine"] for r in production_data]

# Records below threshold
below_threshold = [r for r in production_data if calc_oee(r) < 0.70]

# Alert strings for flagged machines
alerts = [
    f"ALERT: {r['machine']} OEE at {calc_oee(r)*100:.1f}%"
    for r in production_data
    if calc_oee(r) < 0.70
]

# Dictionary: machine → OEE score
oee_map = {r["machine"]: calc_oee(r) for r in production_data}

# Fleet checks
any_critical  = any(oee < 0.70 for oee in oee_scores)
all_on_target = all(oee >= 0.85 for oee in oee_scores)


# --- Report ---
report_time = datetime.now().strftime("%Y-%m-%d %H:%M")

print("=" * 54)
print(f"  PYTHONIC OEE REPORT — {report_time}")
print("=" * 54)

for i, (machine, oee) in enumerate(oee_map.items()):
    status = "World Class" if oee >= 0.85 else "Acceptable" if oee >= 0.70 else "Below Threshold"
    print(f"  {i+1}. {machine:<22} OEE: {oee*100:.1f}%  [{status}]")

print("=" * 54)
print(f"  Any critical machines : {any_critical}")
print(f"  All on target         : {all_on_target}")
print()

if alerts:
    print("  --- Active Alerts ---")
    for alert in alerts:
        print(f"  {alert}")
else:
    print("  No active alerts.")

print("=" * 54)