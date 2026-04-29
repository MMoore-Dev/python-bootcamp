# Day 4 — Lists and Loops
# Python Bootcamp 

# --- Production Data ---
machines = ["CNC Mill #4", "Press #2", "Assembly Line A", "Weld Station B"]
oee_values = [0.82, 0.68, 0.91, 0.74]
defect_counts = [4, 11, 2, 7]

# --- Accumulators ---
total_oee = 0
critical_machines = []

# --- Process Each Machine ---
print("=" * 50)
print(" MACHINE PERFORMANCE REPORT")
print("=" * 50)

for i in range(len(machines)):
    oee = oee_values[i]
    defects = defect_counts[i]
    total_oee += oee

    if oee < 0.70:
        status = "CRITICAL"
        critical_machines.append(machines[i])
    elif oee >= 0.85: 
        status = "STRONG"
    else: 
        status = "MONITOR"

    print(f" {machines[i]:<22} OEE: {oee*100:.1f}% Defects: {defects:>2} [{status}]")

# --- Summary ---
avg_oee = total_oee / len(oee_values)
print("=" * 50)
print(f" Fleet Average OEE: {avg_oee * 100:.1f}%")
print(f" Critical Machines: {len(critical_machines)}")
for m in critical_machines:
    print(f"  →{m}")
print("=" * 50)