# Day 5 — Functions
# Python Bootcamp

def calculate_availability(actual_run, planned_time):
    """Returns the rate as a float"""
    return actual_run / planned_time

def calculate_performance(actual_unit, target_units):
    """Returns performance as a float"""
    return actual_unit / target_units

def calculate_quality(good_units, total_units):
    """Returns quality as a float"""
    return good_units / total_units

def calculate_oee(availability, performance, quality, threshold=0.85):
    """
    Calculate OEE and classify against threshold
    Args:
        availability (float): Availability rate
        performance (float): Performance rate
        quality (float): Quality rate
        threshold (float): World Class threshold. Default 0.85

    Returns:
        tuple: (one_score float, status str)
    """
    oee = availability * performance * quality
    if oee >= threshold:
        status = "World Class"
    elif oee >= 0.70:
        status = "Acceptable"
    else:
        status = "Below Threshold"
    return oee, status

def print_report(machine, shift, oee_score, status):
    """Print formatted oee shift report"""
    print("=" * 44)
    print(" OEE SHIFT REPORT ")
    print("=" * 44)
    print(f" Machine: {machine}")
    print(f" Shift: {shift}")
    print(f" OEE: {oee_score * 100:.1f}%")
    print(f" Status: {status}")
    print("=" * 44)

# --- Main Execution ---
machine = "CNC Mill #4"
shift = "Day Shift"

avail = calculate_availability(437, 480)
perf = calculate_performance(842, 900)
qual = calculate_quality(821, 842)

oee_score, oee_status = calculate_oee(avail, perf, qual)
print_report(machine, shift, oee_score, oee_status)