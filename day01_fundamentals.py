# Day 1 - Variables, Data Types, and Print
# Python Bootcamp  | Operations Analysts Track

machine_name = "CNC Mill #4"
shift = "Day Shift"
units_produced = 842
planned_production_time = 480 # minutes
actual_run_time = 437         # minutes 
availability = actual_run_time / planned_production_time

print("=" * 40)
print(" PRODUCTION LINE SUMMARY ")
print("=" * 40)
print(f" Machine : {machine_name}")
print(f" Shift : {shift}")
print(f" Units : {units_produced}")
print(f" Avail. : {availability * 100:.1f}%")
print("=" * 40)