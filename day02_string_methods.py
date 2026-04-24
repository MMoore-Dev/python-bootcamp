# Day 2 — Strings, Methods, Operators
# Python Bootcamp

machine = "cnc mill #4"
shift = "Day Shift"
planned = 480
actual = 437
units_produced = 842
target_units = 900

# Clean and format the machine name
machine_clean = machine.strip().title()

#Calculate metrics
availability = actual / planned
performance = units_produced / target_units
complete_hours = actual // 60
remaining_mins = actual % 60

# Evaluate against target
meeting_target = availability >= 0.90

print("=" * 42)
print(" SHIFT OPERATIONS REPORT ")
print("=" * 42)
print(f" Machine : {machine_clean}")
print(f" Shift : {shift}")
print(f" Run Time : {complete_hours}h {remaining_mins}m")
print(f" Availability : {availability * 100:.1f}%")
print(f" Performance : {performance * 100:.1f}%")
print("=" * 42)