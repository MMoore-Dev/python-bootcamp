# day18_pipeline.py
# Full production data pipeline
# Python Bootcamp 

import pandas as pd
import os
from datetime import datetime

# Ingestion with validation
def ingest_data(filepath):
    """
    Load production CSV and perform basic validation.

    Args:
        filepath (str): Path to CSV file

    Returns:
        pd.DataFrame or None: Loaded DataFrame, None if failed
    """
    if not os.path.exists(filepath):
        print(f"[INGEST ERROR] File not found: {filepath}")
        return None
    df = pd.read_csv(filepath)
    required_columns = ["date", "machine", "shift",
                        "actual_run", "planned", "units",
                        "good_units", "defect_code"]
    missing = [col for col in required_columns if col not in df.columns]
    if missing:
        print(f"[INGEST ERROR] Missing columns: {missing}")
        return None
    print(f"[INGEST] Loaded {df.shape[0]} records × {df.shape[1]} columns")
    return df

# Cleaning 
def clean_data(df):
    """
    Clean and standardize production DataFrame.

    Args:
        df (pd.DataFrame): Raw production data

    Returns:
        pd.DataFrame: Cleaned DataFrame
    """
    initial_count = len(df)
    df["machine"]    = df["machine"].str.strip().str.title()
    df["shift"]      = df["shift"].str.strip().str.title()
    df["date"]       = pd.to_datetime(df["date"])
    df["actual_run"] = pd.to_numeric(df["actual_run"], errors="coerce")
    df["planned"]    = pd.to_numeric(df["planned"],    errors="coerce")
    df["units"]      = pd.to_numeric(df["units"],      errors="coerce")
    df["good_units"] = pd.to_numeric(df["good_units"], errors="coerce")
    df.dropna(subset=["actual_run", "planned", "units", "good_units"],
              inplace=True)
    df = df[df["planned"] > 0]
    df.drop_duplicates(inplace=True)
    print(f"[CLEAN] {len(df)} records retained, "
          f"{initial_count - len(df)} dropped")
    return df

# Transformation 
def transform_data(df, target_rate=1.8, oee_threshold=0.85):
    """
    Calculate OEE metrics and classify each record.

    Args:
        df (pd.DataFrame): Cleaned production data
        target_rate (float): Units per minute target
        oee_threshold (float): World class OEE threshold

    Returns:
        pd.DataFrame: DataFrame with OEE columns added
    """
    df = df.copy()
    df["availability"] = df["actual_run"] / df["planned"]
    df["performance"]  = df["units"] / (df["planned"] * target_rate)
    df["quality"]      = df["good_units"] / df["units"]
    df["oee"]          = (df["availability"] *
                          df["performance"] *
                          df["quality"])
    df["oee_status"] = df["oee"].apply(
        lambda oee: "World Class"    if oee >= oee_threshold
               else "Acceptable"     if oee >= 0.70
               else "Below Threshold"
    )
    print(f"[TRANSFORM] OEE range: "
          f"{df['oee'].min()*100:.1f}% — {df['oee'].max()*100:.1f}%")
    return df

# Analysis 
def analyze_data(df):
    """
    Generate fleet summary and performance rankings.

    Args:
        df (pd.DataFrame): Transformed production data

    Returns:
        dict: Analysis results
    """
    machine_summary = df.groupby("machine").agg(
        avg_oee         = ("oee", "mean"),
        min_oee         = ("oee", "min"),
        max_oee         = ("oee", "max"),
        record_count    = ("oee", "count"),
        below_threshold = ("oee_status",
                           lambda x: (x == "Below Threshold").sum())
    ).round(3).reset_index()

    shift_summary = df.groupby(["machine", "shift"])["oee"]\
                      .mean().round(3).reset_index()
    shift_summary.columns = ["machine", "shift", "avg_oee"]

    defect_summary = df[df["defect_code"] != "None"]\
                       ["defect_code"].value_counts().reset_index()
    defect_summary.columns = ["defect_code", "count"]

    print(f"[ANALYZE] {len(machine_summary)} machines | "
          f"{len(defect_summary)} defect codes")
    return {
        "machine_summary": machine_summary,
        "shift_summary":   shift_summary,
        "defect_summary":  defect_summary
    }

# Output
def generate_report(df, analysis, output_path="pipeline_report.txt"):
    """
    Write pipeline summary report to file.

    Args:
        df (pd.DataFrame): Transformed data
        analysis (dict): Analysis results
        output_path (str): Output file path
    """
    report_time     = datetime.now().strftime("%Y-%m-%d %H:%M")
    machine_summary = analysis["machine_summary"]

    lines = []
    lines.append("=" * 58)
    lines.append(f"  PRODUCTION PIPELINE REPORT — {report_time}")
    lines.append("=" * 58)
    lines.append(f"  Records analyzed : {len(df)}")
    lines.append(f"  Date range       : {df['date'].min().date()} "
                 f"→ {df['date'].max().date()}")
    lines.append(f"  Fleet avg OEE    : {df['oee'].mean()*100:.1f}%")
    lines.append("=" * 58)
    lines.append("  MACHINE PERFORMANCE RANKING")
    lines.append("-" * 58)

    ranked = machine_summary.sort_values("avg_oee", ascending=False)
    for _, row in ranked.iterrows():
        status = ("World Class"    if row["avg_oee"] >= 0.85
                  else "Acceptable" if row["avg_oee"] >= 0.70
                  else "Below Threshold")
        lines.append(
            f"  {row['machine']:<22} "
            f"Avg: {row['avg_oee']*100:.1f}%  "
            f"Min: {row['min_oee']*100:.1f}%  "
            f"[{status}]"
        )

    lines.append("=" * 58)

    with open(output_path, "w", encoding="utf-8") as f:
        for line in lines:
            f.write(line + "\n")

    for line in lines:
        print(line)

    print(f"\n[OUTPUT] Report saved → {output_path}")


# --- Run Pipeline ---
if __name__ == "__main__":
    print("\n🚀 Starting Production Data Pipeline\n")

    df = ingest_data("sample_data.csv")
    if df is None:
        print("Pipeline aborted — ingestion failed.")
    else:
        df       = clean_data(df)
        df       = transform_data(df)
        analysis = analyze_data(df)
        generate_report(df, analysis)

        print("\n✅ Pipeline complete.")