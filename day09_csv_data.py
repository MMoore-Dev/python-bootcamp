# Day 9 — CSV Files and Data Ingestion
# Python Bootcamp 

import csv
import oee_utils
from datetime import datetime

def load_production_data(filepath):
    """
    Load production records from a CSV file.

    Args:
        filepath (str): Path to the CSV file

    Returns:
        list: List of dictionaries, one per production record
    """
    records = []
    try:
        with open(filepath, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                records.append({
                    "date":        row["date"],
                    "machine":     row["machine"],
                    "shift":       row["shift"],
                    "actual_run":  int(row["actual_run"]),
                    "planned":     int(row["planned"]),
                    "units":       int(row["units"]),
                    "good_units":  int(row["good_units"]),
                    "defect_code": row["defect_code"]
                })
    except FileNotFoundError:
        print(f"[ERROR] File not found: {filepath}")
    except KeyError as e:
        print(f"[ERROR] Missing column in CSV: {e}")
    return records


def process_records(records):
    """
    Calculate OEE for each production record.

    Args:
        records (list): List of production record dictionaries

    Returns:
        list: Records with oee and status fields added
    """
    processed = []
    for record in records:
        try:
            avail  = oee_utils.calculate_availability(record["actual_run"], record["planned"])
            perf   = oee_utils.calculate_performance(record["units"], record["planned"])
            qual   = oee_utils.calculate_quality(record["good_units"], record["units"])
            oee    = oee_utils.calculate_oee(avail, perf, qual)
            status = oee_utils.classify_oee(oee)

            record["oee"]    = oee
            record["status"] = status
            processed.append(record)

        except (ValueError, ZeroDivisionError) as e:
            print(f"  [SKIP] {record.get('machine','?')} {record.get('date','?')}: {e}")

    return processed


def print_summary(processed):
    """Print a fleet OEE summary from processed records."""
    report_time = datetime.now().strftime("%Y-%m-%d %H:%M")

    print("=" * 54)
    print(f"  FLEET OEE SUMMARY — {report_time}")
    print("=" * 54)

    machine_oee = {}
    for record in processed:
        m = record["machine"]
        if m not in machine_oee:
            machine_oee[m] = []
        machine_oee[m].append(record["oee"])

    for machine, oee_list in machine_oee.items():
        avg = sum(oee_list) / len(oee_list)
        status = oee_utils.classify_oee(avg)
        print(f"  {machine:<22} Avg OEE: {avg*100:.1f}%  [{status}]")

    print("=" * 54)
    print(f"  Total records processed: {len(processed)}")
    print("=" * 54)


# --- Main ---
if __name__ == "__main__":
    records   = load_production_data("sample_data.csv")
    processed = process_records(records)
    print_summary(processed)