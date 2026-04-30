# Day 6 — Dictionaries and File I/O
# Python Bootcamp

# --- Production Records ---
production_data = [
    {"machine": "CNC Mill #4", "actual_run": 437, "planned": 480, "units": 842, "good_units": 821},
    {"machine": "Press #2", "actual_run": 390, "planned": 480, "units": 760, "good_units": 741},
    {"machine": "Assembly Line A", "actual_run": 465, "planned": 480, "units": 910, "good_units": 906},
    {"machine": "Assembly Line B", "actual_run": 310, "planned": 480, "units": 620, "good_units": 589},
]

def calculate_oee(record, target_rate=1.8):
    """
    Calculate OEE from a production record dictionary.

    Args: 
        record(dict): Production data from one machine
        target_rate(float): Units per minute target. Default 1.8.
    
    Returns:
        tuple(oee float, status str)
    """

    avail = record["actual_run"] / record["planned"]
    perf  = record["units"] / (record["planned"] * target_rate)
    qual  = record["good_units"] / record["units"]
    oee   = avail * perf * qual

    if oee >= 0.85:
        status = "World Class"
    elif oee >= 0.70:
        status = "Acceptable"
    else:
        status = "Below Threshold"

    return oee, status

# --- Generate Report ---
report_lines = []
report_lines.append("=" * 50)
report_lines.append(" OEE FLEET REPORT - Day Shift")
report_lines.append("=" * 50)

for record in production_data:
    oee, status = calculate_oee(record)
    line = f" {record['machine']:<22} OEE: {oee*100:.1f}% [{status}]"
    report_lines.append(line)

report_lines.append("=" * 50)

# --- Print to Console ---
for line in report_lines:
    print(line)

# --- Write to File ---
with open("oee_report.txt", "w") as f:
    for line in report_lines:
        f.write(line + "\n")

print("\nReport saved to oee_report.txt") 