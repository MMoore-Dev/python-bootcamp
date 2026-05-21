# Day 11 - Inheritance and Class Design 
# Python Bootcamp

from datetime import datetime

class MachineRecord:
    """ Base class for production shift records. """

    TARGET_RATE = 1.8
    OEE_THRESHOLD = 0.85

    def __init__(self, machine, shift, actual_run, planned, units, good_units):
        self.machine = machine
        self.shift = shift
        self.actual_run = actual_run
        self.planned    = planned
        self.units      = units
        self.good_units = good_units
    
    def availability(self):
        if self.planned == 0:
            raise ValueError("Planned time cannot be zero")
        return self.actual_run / self.planned

    def performance(self):
        return self.units / (self.planned * self.TARGET_RATE)

    def quality(self):
        if self.units == 0:
            raise ValueError("Units cannot be zero")
        return self.good_units / self.units

    def oee(self):
        return self.availability() * self.performance() * self.quality()

    def status(self):
        oee = self.oee()
        if oee >= self.OEE_THRESHOLD:
            return "World Class"
        elif oee >= 0.70:
            return "Acceptable"
        else:
            return "Below Threshold"
    
    def __str__(self):
        return (f"MachineRecord  | {self.machine:<22} | {self.shift:<5} | "
                f"OEE: {self.oee()*100:.1f}% [{self.status()}]")

class DowntimeRecord(MachineRecord):
    """MachineRecord extended with downtime tracking."""

    def __init__(self, machine, shift, actual_run, planned,
                 units, good_units, downtime_reason, downtime_minutes):
        super().__init__(machine, shift, actual_run, planned, units, good_units)
        self.downtime_reason  = downtime_reason
        self.downtime_minutes = downtime_minutes

    def downtime_rate(self):
        """Returns downtime as percentage of planned time."""
        return self.downtime_minutes / self.planned

    def __str__(self):
        base = super().__str__()
        return (f"{base}\n"
                f"               Downtime: {self.downtime_minutes}min "
                f"[{self.downtime_reason}] "
                f"({self.downtime_rate()*100:.1f}% of planned)")

class CriticalMachineRecord(MachineRecord):
    """MachineRecord with tighter OEE threshold for critical assets."""

    OEE_THRESHOLD = 0.90      # Override class variable

    def status(self):
        oee = self.oee()
        if oee >= self.OEE_THRESHOLD:
            return "On Target"
        elif oee >= 0.80:
            return "Watch — Approaching Limit"
        else:
            return "CRITICAL — Immediate Action Required"

    def __str__(self):
        return (f"[CRITICAL]     | {self.machine:<22} | {self.shift:<5} | "
                f"OEE: {self.oee()*100:.1f}% [{self.status()}]")
    
# --- Main ---
if __name__ == "__main__":

    # Standard records
    r1 = MachineRecord("CNC Mill #4",     "Day",   437, 480, 842, 821)
    r2 = MachineRecord("Assembly Line A", "Night", 465, 480, 910, 905)

    # Downtime record
    r3 = DowntimeRecord("Press #2", "Day", 390, 480, 760, 741,
                        "Mechanical Failure", 45)

    # Critical machine
    r4 = CriticalMachineRecord("Weld Station B", "Night", 310, 480, 620, 589)

    records = [r1, r2, r3, r4]

    print("=" * 62)
    print(f"  FLEET REPORT — {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 62)

    for record in records:
        print(record)
        print()

    # isinstance checks
    print("--- Type Checks ---")
    print(f"r3 is MachineRecord   : {isinstance(r3, MachineRecord)}")
    print(f"r3 is DowntimeRecord  : {isinstance(r3, DowntimeRecord)}")
    print(f"r1 is DowntimeRecord  : {isinstance(r1, DowntimeRecord)}")
    print(f"r4 is MachineRecord   : {isinstance(r4, MachineRecord)}")