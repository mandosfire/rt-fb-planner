import streamlit as st
import pandas as pd
from utils.roundtable_solver import generate_roundtable_schedule

st.set_page_config(page_title="Roundtable Planning", layout="wide")
st.title("Roundtable Planning")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Moderator Schedule")
    mod_template = pd.DataFrame([{"id": "", "day": "Monday", "shift": "Morning"}])
    edited_mods = st.data_editor(mod_template, num_rows="dynamic", key="rt_mod_grid")
    
    st.subheader("Global Settings")
    weekly_quota = st.number_input("Target roundtables per moderator (Weekly)", min_value=1, value=1)

with col2:
    st.subheader("Individual Roundtable Rules")
    st.write("Define each roundtable, headcount limits, and which shifts are allowed to attend.")
    
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
    valid_mods = edited_mods[edited_mods["id"].str.strip() != ""].to_dict('records')
    valid_rts = edited_rts[edited_rts["RT Name"].str.strip() != ""].to_dict('records')
    
    if valid_mods and valid_rts:
        days = list(set([m['day'] for m in valid_mods]))
        
        with st.spinner("Calculating optimal mathematical schedule..."):
            result_df = generate_roundtable_schedule(valid_mods, valid_rts, days, weekly_quota)
            
        if result_df is not None:
            st.success("Optimal Schedule Generated!")
            st.dataframe(result_df, use_container_width=True)
        else:
            st.error("Could not find a mathematically valid schedule. Try adjusting your minimums or adding more roundtables.")
    else:
        st.error("Please enter data for both the schedule and the roundtable rules.")
