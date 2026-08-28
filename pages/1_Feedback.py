import streamlit as st
import pandas as pd
from utils.feedback_solver import schedule_feedback

st.set_page_config(page_title="Feedback Scheduling", layout="wide")
st.title("Feedback Scheduling")

st.write("Enter or paste your weekly schedules below. You can paste directly from your spreadsheet.")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Moderator Schedule")
    # Provide an empty template for the user to fill or paste over
    mod_template = pd.DataFrame([{"id": "", "day": "Monday", "shift": "Morning"}])
    edited_mods = st.data_editor(mod_template, num_rows="dynamic", key="mod_grid")

with col2:
    st.subheader("Overhead Schedule")
    oh_template = pd.DataFrame([{"id": "", "day": "Monday", "shift": "Morning", "opt_in": True}])
    edited_ohs = st.data_editor(oh_template, num_rows="dynamic", key="oh_grid")

if st.button("Generate Feedback Schedule", type="primary"):
    # Filter out empty rows
    valid_mods = edited_mods[edited_mods["id"].str.strip() != ""].to_dict('records')
    valid_ohs = edited_ohs[edited_ohs["id"].str.strip() != ""].to_dict('records')
    
    if valid_mods and valid_ohs:
        with st.spinner("Balancing workloads..."):
            result_df = schedule_feedback(valid_mods, valid_ohs)
            
        st.success("Assignment complete!")
        st.dataframe(result_df, use_container_width=True)
    else:
        st.error("Please enter schedule data for both Moderators and Overheads.")
