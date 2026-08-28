import streamlit as st
import pandas as pd
from utils.data_loader import load_schedule_data
from utils.roundtable_solver import generate_roundtable_schedule

st.set_page_config(page_title="Roundtable Planning", layout="wide")
st.title("Roundtable Planning")

st.header("1. Upload Moderator Schedule")
mod_file = st.file_uploader("Moderator Schedule (CSV)", type="csv", key="mod_rt")

st.header("2. Rulesets & Settings")
col1, col2 = st.columns(2)

with col1:
    st.subheader("Global Settings")
    num_roundtables = st.number_input("Total roundtables for the week", min_value=1, value=5)
    weekly_quota = st.number_input("Target roundtables per moderator", min_value=1, value=1)
    
with col2:
    st.subheader("Roundtable Constraints")
    min_mods = st.number_input("Min Moderators per roundtable", min_value=1, value=4)
    max_mods = st.number_input("Max Moderators per roundtable", min_value=1, value=8)
    allowed_shifts = st.multiselect("Allowed Shifts", ["Morning", "Mid", "Night"], default=["Mid"])

if st.button("Generate Roundtable Schedule", type="primary"):
    if mod_file:
        mods = load_schedule_data(mod_file)
        days = list(set([m['day'] for m in mods]))
        
        settings = {
            'target_quota': weekly_quota,
            'min_mods': min_mods,
            'max_mods': max_mods,
            'allowed_shifts': allowed_shifts
        }
        
        with st.spinner("Calculating optimal mathematical schedule (this may take a moment)..."):
            result_df = generate_roundtable_schedule(mods, num_roundtables, days, settings)
            
        if result_df is not None:
            st.success("Optimal Schedule Generated!")
            st.dataframe(result_df, use_container_width=True)
            
            csv_data = result_df.to_csv(index=False).encode('utf-8')
            st.download_button("Download CSV", data=csv_data, file_name="roundtable_schedule.csv", mime="text/csv")
        else:
            st.error("Could not find a valid schedule with these constraints. Try lowering the minimums, raising the maximums, or adding more roundtables.")
    else:
        st.error("Please upload the moderator schedule first.")
