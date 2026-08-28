import streamlit as st
import pandas as pd
from utils.roundtable_solver import generate_roundtable_schedule
from utils.data_loader import parse_schedule_grid

st.set_page_config(page_title="Roundtable Planning", layout="wide")
st.title("Roundtable Planning")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Moderator Schedule Grid")
    mod_df = pd.DataFrame({
        "Name": [""], "Monday": [""], "Tuesday": [""], "Wednesday": [""], 
        "Thursday": [""], "Friday": [""], "Saturday": [""], "Sunday": [""]
    })
    edited_mods = st.data_editor(mod_df, num_rows="dynamic", key="rt_mod_grid")
    
    st.subheader("Global Settings")
    weekly_quota = st.number_input("Target roundtables per moderator (Weekly)", min_value=1, value=1)

with col2:
    st.subheader("Individual Roundtable Rules")
    rt_template = pd.DataFrame({
        "RT Name": ["RT 1", "RT 2", "RT 3"],
        "Min Mods": [4, 4, 4],
        "Max Mods": [8, 8, 8],
        "Allow Morning": [True, False, False],
        "Allow Midday": [True, True, True],
        "Allow Night": [False, False, True]
    })
    edited_rts = st.data_editor(rt_template, num_rows="dynamic", key="rt_rules_grid")

if st.button("Generate Roundtable Schedule", type="primary"):
    parsed_mods = parse_schedule_grid(edited_mods)
    valid_rts = edited_rts[edited_rts["RT Name"].str.strip() != ""].to_dict('records')
    
    if parsed_mods and valid_rts:
        days = list(set([m['day'] for m in parsed_mods]))
        
        with st.spinner("Calculating optimal mathematical schedule..."):
            result_df = generate_roundtable_schedule(parsed_mods, valid_rts, days, weekly_quota)
            
        if result_df is not None:
            st.success("Optimal Schedule Generated!")
            st.dataframe(result_df, use_container_width=True)
        else:
            st.error("Could not find a mathematically valid schedule.")
    else:
        st.error("Please enter data for both the schedule and the roundtable rules.")
