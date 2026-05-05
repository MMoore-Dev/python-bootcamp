# oee_utils.py
# Reusable OEE utility functions
# Python Bootcamp 

def calculate_availability(actual_run, planned_time):
    """Returns availability rate. Raises ValueError if planned_time is zero."""
    if planned_time == 0:
        raise ValueError("Planned time cannot be zero")
    return actual_run / planned_time

def calculate_performance(units, planned_time, target_rate=1.8):
    """Returns performance rate based on target units per minute."""
    if planned_time == 0:
        raise ValueError("Planned time cannot be zero")
    return units / (planned_time * target_rate)

def calculate_quality(good_units, total_units):
    """Returns quality rate. Raises ValueError if total_units is zero."""
    if total_units == 0:
        raise ValueError("Total units cannot be zero")
    return good_units / total_units

def calculate_oee(availability, performance, quality):
    """Returns OEE score as a float."""
    return availability * performance * quality

def classify_oee(oee, threshold=0.85):
    """Classifies OEE score against world class threshold."""
    if oee >= threshold:
        return "World Class"
    elif oee >= 0.70:
        return "Acceptable"
    else:
        return "Below Threshold"
    
def _test():
    """Quick self-test when file is run directly."""
    avail = calculate_availability(437, 480)
    perf  = calculate_performance(842, 480)
    qual  = calculate_quality(821, 842)
    oee   = calculate_oee(avail, perf, qual)
    print(f"Test OEE: {oee*100:.1f}% — {classify_oee(oee)}")

if __name__ == "__main__":
    _test()