# Day 3 — Conditionals and Control Flow
# Python Bootcamp 

# --- Inputs ---
machine = "CNC Mill #4"
shift = "Day Shift"
availability = 0.88
performance = 0.79
quality = 0.95
defect_code = "DEF-004"
critical_codes = ["DEF-004", "DEF-007", "DEF-011"]

# --- OEE Calculations ---
oee = availability * performance * quality

# --- OEE Classification ---
if oee >= 0.85:
    oee_status = "World CLass"
elif oee >= 0.70:
    oee_status = "Acceptable"
else:
    oee_status = "Below Threshold"

# --- Defect Escalation ---
if defect_code in critical_codes:
    defect_status = "CRITICAL - Escalate Immediately"
else:
    defect_status = "Standard - Queue for review"

# --- Throughput Check ---
if availability < 0.90 or performance < 0.90:
    throughput_alert = True
else: 
    throughput_alert = False

print("=" * 44)
print(" SHIFT CONTROL REPORT ")
print("=" * 44)
print(f" Machine : {machine}")
print(f" Shift : {shift}")
print(f" OEE : {oee * 100:.1f}% [{oee_status}]")
print(f" Defect Code : {defect_code}")
print(f" Defect Status : {defect_status}")
print(f" Throughput Alert : {throughput_alert}")
print("=" * 44)