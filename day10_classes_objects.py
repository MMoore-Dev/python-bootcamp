# Day 10 — Object Oriented Programming: Classes & Objects
# Python Bootcamp

import csv
from datetime import datetime

class MachineRecord:
     """Represents a single production shift record with OEE calculations."""

     def __init__(self, machine, shift, actual_run, planned, units, good_units):
          self.machine = machine
          self.shift = shift
          self.actual_run = actual_run
          self.planned = planned
          self.units = units
          self.good_units = good_units
        
     def availability(self):
          """Returns availability rate as float"""
          if self.planned == 0:
               raise ValueError("Planned time cannot be zero.")
          return self.actual_run / self.planned
     
     def performance(self, target_rate=1.8):
          """Returns performance rate as float"""
          return self.units / (self.planned * target_rate)
     
     def quality(self):
          """Returns quality rate as float"""
          if self.units == 0:
               raise ValueError("Units cannot be zero.")
          return self.good_units / self.units
     
     def oee(self):
          """Returns OEE as float"""
          return self.availability() * self.performance() * self.quality()
     
     def status(self, threshold=0.85):
          """Classifies OEE against threshold"""
          oee = self.oee()
          if oee >= threshold:
               return "World Class"
          elif oee >= 0.70:
               return "Acceptable"
          else:
               return "Below threshold"
          
     def __str__(self):
          return (f"MachineRecord | {self.machine:<22} | {self.shift:<5} | "
                  f"OEE: {self.oee()*100:.1f}% [{self.status()}]")
     
def load_records_from_csv(filepath):
     """Load production csv and return list of MachineRecord objects."""
     records = []
     try:
          with open(filepath, "r") as f:
               reader = csv.DictReader(f)
               for row in reader:
                    records.append(MachineRecord(
                         machine = row["machine"],
                         shift =  row["shift"],
                         actual_run = int(row["actual_run"]),
                         planned = int(row["planned"]),
                         units = int(row["units"]),
                         good_units = int(row["good_units"])
                    ))
     except FileNotFoundError:
          print(f"[ERROR] file not found: {filepath}")
     except KeyError as e:
          print(f"[ERROR] Missing column: {e}")
     return records

def print_fleet_report(records):
     """Print OEE summary grouped by machine"""
     report_time = datetime.now().strftime("%Y-%m-%d %H:%M")

     print("=" * 58)
     print(f"  FLEET OEE REPORT — {report_time}")
     print("=" * 58)

     # Group by machine
     machine_groups = {}
     for record in records:
        if record.machine not in machine_groups:
            machine_groups[record.machine] = []
        machine_groups[record.machine].append(record.oee())

     for machine, oee_list in machine_groups.items():
        avg_oee = sum(oee_list) / len(oee_list)
        if avg_oee >= 0.85:
            status = "World Class"
        elif avg_oee >= 0.70:
            status = "Acceptable"
        else:
            status = "Below Threshold"
        print(f"  {machine:<22} Avg OEE: {avg_oee*100:.1f}%  [{status}]")

        print("=" * 58)
        print(f"  Total records : {len(records)}")
        print(f"  Machines      : {len(machine_groups)}")
        print("=" * 58)


# --- Main ---
if __name__ == "__main__":
    records = load_records_from_csv("sample_data.csv")

    # Print first 5 records using __str__
    print("\n--- Sample Records ---")
    for record in records[:5]:
        print(record)

    # Full fleet report
    print()
    print_fleet_report(records)