import pandas as pd

def map_time_to_shift(time_str):
    """Maps the specific timecodes to shift names. Adjust if times change."""
    time_str = str(time_str).strip()
    if time_str == "0730-1630":
        return "Morning"
    elif time_str == "1500-0000":
        return "Mid"
    elif time_str == "2330-0800":
        return "Night"
    return "OFF"

def parse_schedule_grid(df, is_overhead=False):
    """Melts a wide-format schedule matrix into a list of dictionaries."""
    records = []
    
    for index, row in df.iterrows():
        name = str(row.get("Name", "")).strip()
        if not name:
            continue
            
        for col in df.columns:
            # Skip non-day identifier columns
            if col in ["Name", "Opt-In for Feedback"]:
                continue
                
            cell_val = str(row[col]).strip().upper()
            if cell_val != "OFF" and cell_val != "NAN" and cell_val != "":
                shift_name = map_time_to_shift(row[col])
                
                if shift_name != "OFF":
                    record = {
                        'id': name,
                        'day': col, # Captures the column header (e.g., '17/08' or 'Monday')
                        'shift': shift_name
                    }
                    if is_overhead:
                        record['opt_in'] = row.get("Opt-In for Feedback", True)
                    records.append(record)
                    
    return records
