# Day 17 — Polymorphism and Advanced OOP
# Python Bootcamp | Operations Analyst Track

from abc import ABC, abstractmethod
from datetime import datetime


class ProductionRecord(ABC):
    """
    Abstract base class for all production record types.
    Subclasses must implement oee() and alert().
    """

    def __init__(self, machine, shift, actual_run, planned, units, good_units):
        self.machine    = machine
        self.shift      = shift
        self.actual_run = actual_run
        self.planned    = planned
        self.units      = units
        self.good_units = good_units

    @abstractmethod
    def oee(self):
        """Calculate and return OEE as a float."""
        pass

    @abstractmethod
    def alert(self):
        """Return alert string based on OEE performance."""
        pass

    def __str__(self):
        return (f"{self.__class__.__name__:<22} | {self.machine:<22} | "
                f"{self.shift:<5} | OEE: {self.oee()*100:.1f}%")

    def __repr__(self):
        return (f"{self.__class__.__name__}(machine={self.machine!r}, "
                f"shift={self.shift!r}, oee={self.oee():.3f})")


class StandardRecord(ProductionRecord):
    """Standard production shift record — 85% OEE threshold."""

    def oee(self):
        avail = self.actual_run / self.planned
        perf  = self.units / (self.planned * 1.8)
        qual  = self.good_units / self.units
        return avail * perf * qual

    def alert(self):
        oee = self.oee()
        if oee >= 0.85:
            return f"ON TARGET    | {self.machine} — {oee*100:.1f}%"
        elif oee >= 0.70:
            return f"MONITOR      | {self.machine} — {oee*100:.1f}%"
        else:
            return f"BELOW TARGET | {self.machine} — {oee*100:.1f}%"


class CriticalAssetRecord(ProductionRecord):
    """Critical asset record — 90% OEE threshold."""

    THRESHOLD = 0.90

    def oee(self):
        avail = self.actual_run / self.planned
        perf  = self.units / (self.planned * 1.8)
        qual  = self.good_units / self.units
        return avail * perf * qual

    def alert(self):
        oee = self.oee()
        if oee >= self.THRESHOLD:
            return f"ON TARGET    | [CRITICAL] {self.machine} — {oee*100:.1f}%"
        else:
            return f"ESCALATE NOW | [CRITICAL] {self.machine} — {oee*100:.1f}%"


class DowntimeRecord(ProductionRecord):
    """Production record with downtime tracking."""

    def __init__(self, machine, shift, actual_run, planned,
                 units, good_units, downtime_reason, downtime_minutes):
        super().__init__(machine, shift, actual_run, planned, units, good_units)
        self.downtime_reason  = downtime_reason
        self.downtime_minutes = downtime_minutes

    def oee(self):
        avail = self.actual_run / self.planned
        perf  = self.units / (self.planned * 1.8)
        qual  = self.good_units / self.units
        return avail * perf * qual

    def downtime_rate(self):
        return self.downtime_minutes / self.planned

    def alert(self):
        oee = self.oee()
        return (f"DOWNTIME     | {self.machine} — {oee*100:.1f}% | "
                f"{self.downtime_minutes}min [{self.downtime_reason}]")


# --- Main ---
if __name__ == "__main__":

    records = [
        StandardRecord("Assembly Line A", "Day",   465, 480, 910, 905),
        StandardRecord("Press #2",        "Night", 390, 480, 760, 741),
        CriticalAssetRecord("CNC Mill #4", "Day",  437, 480, 842, 821),
        CriticalAssetRecord("CNC Mill #4", "Night",410, 480, 800, 776),
        DowntimeRecord("Weld Station B", "Day", 310, 480, 620, 589,
                       "Mechanical Failure", 45),
    ]

    report_time = datetime.now().strftime("%Y-%m-%d %H:%M")

    print("=" * 62)
    print(f"  PRODUCTION ALERT REPORT — {report_time}")
    print("=" * 62)

    for record in records:
        print(f"  {record.alert()}")

    print()
    print("=" * 62)
    print("  FULL RECORD DETAIL")
    print("=" * 62)

    for record in records:
        print(f"  {record}")

    print()
    print("--- repr() output ---")
    for record in records:
        print(repr(record))