import streamlit as st
import pandas as pd
from utils.feedback_solver import schedule_feedback
from utils.data_loader import parse_schedule_grid

st.set_page_config(page_title="Feedback Scheduling", layout="wide")
st.title("Feedback Scheduling")

# Template matching your matrix format
template_data = {
    "Name": [""],
    "Monday": [""],
    "Tuesday": [""],
    "Wednesday": [""],
    "Thursday": [""],
    "Friday": [""],
    "Saturday": [""],
    "Sunday": [""]
}

col1, col2 = st.columns(2)

with col1:
    st.subheader("Moderator Schedule Grid")
    mod_df = pd.DataFrame(template_data)
    edited_mods = st.data_editor(mod_df, num_rows="dynamic", key="mod_grid")

with col2:
    st.subheader("Overhead Schedule Grid")
    oh_data = template_data.copy()
    oh_data["Opt-In for Feedback"] = [True]
    oh_df = pd.DataFrame(oh_data)
    edited_ohs = st.data_editor(oh_df, num_rows="dynamic", key="oh_grid")

if st.button("Generate Feedback Schedule", type="primary"):
    parsed_mods = parse_schedule_grid(edited_mods)
    parsed_ohs = parse_schedule_grid(edited_ohs, is_overhead=True)
    
    if parsed_mods and parsed_ohs:
        with st.spinner("Balancing workloads..."):
            result_df = schedule_feedback(parsed_mods, parsed_ohs)
        st.success("Assignment complete!")
        st.dataframe(result_df, use_container_width=True)
    else:
        st.error("Please paste valid schedule data.")
