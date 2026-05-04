# Day 7 — Error Handling and Exception Management
# Python Bootcamp

def safe_calculate_oee(record):
    """
    Safely calculate OEE from a production record dictionary. 
    Handles missing fields, zero division, and type errors.

    Args:
        record(dict): Production data with keys:
                    actual_run, planned, units, good_units

    Returns: 
        tuple: (oee float or None, status str)
    """

    try:
        actual_run = record["actual_run"]
        planned = record["planned"]
        units = record["units"]
        good_units = record["good_units"]
        target = record.get("target_rate", 1.8)

        if planned == 0:
            raise ValueError("Planned time cannot be zero")
        if units == 0:
            raise ValueError("Units produced cannot be zero")
    
        avail = actual_run / planned
        perf = units / (planned * target)
        qual = good_units / units
        oee = avail * perf * qual

        if oee >= 0.85:
            status = "World Class"
        elif oee >= 0.70:
            status = "Acceptable"
        else:
            status = "Below Threshold"
    
        return oee, status

    except KeyError as e:
        print(f" [ERROR] Missing field: {e}")
        return None, "Error"
    except ValueError as e:
        print(f" [ERROR] Invalid value: {e}")
        return None, "Error"
    except TypeError as e:
        print(f" [ERROR] Type mismatch: {e}")
        return None, "Error"
    
# --- Test Data -- Includes intentionally bad records ---
production_data = [
    {"machine": "CNC Mill #4", "actual_run": 437, "planned": 480, "units": 842, "good_units": 821},
    {"machine": "Press #2",        "actual_run": 390, "planned": 480, "units": 760, "good_units": 741},
    {"machine": "Assembly Line A", "actual_run": 465, "planned": 0,   "units": 910, "good_units": 905},
    {"machine": "Weld Station B",  "actual_run": 310, "planned": 480, "units": 620},
    {"machine": "Drill Press #1",  "actual_run": "bad", "planned": 480, "units": 700, "good_units": 681},
]

# --- Process Report ---
print("=" * 52)
print(" OEE FLEET REPORT - WITH ERROR HANDLING")
print("=" * 52)

error_count = 0

for record in production_data:
    machine = record.get("machine", "Unknown Machine")
    oee, status = safe_calculate_oee(record)

    if oee is None: 
        error_count += 1
        print(f" {machine:<22} OEE: --- [{status}]")
    else:
        print(f" {machine:<22} OEE: --- {oee*100:.1f}% [{status}]")
        
print("=" * 52)
print(f"  Records processed : {len(production_data)}")
print(f"  Errors encountered: {error_count}")
print("=" * 52)