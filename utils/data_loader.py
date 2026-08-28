import pandas as pd

def load_schedule_data(uploaded_file):
    """
    Reads a CSV from Streamlit and returns a list of dictionaries.
    Expected CSV columns: id, day, shift, (and opt_in for overheads)
    """
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        # Convert all column names to lowercase to prevent capitalization errors
        df.columns = [col.lower() for col in df.columns]
        return df.to_dict('records')
    return []
