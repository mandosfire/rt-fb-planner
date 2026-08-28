import streamlit as st
import pandas as pd
from utils.data_loader import load_schedule_data
from utils.feedback_solver import schedule_feedback

st.set_page_config(page_title="Feedback Scheduling", layout="wide")
st.title("Feedback Scheduling")

st.write("Upload the schedules to generate load-balanced feedback assignments.")

col1, col2 = st.columns(2)
with col1:
    mod_file = st.file_uploader("Moderators (CSV)", type="csv", key="mod_fb")
with col2:
    oh_file = st.file_uploader("Overheads (CSV)", type="csv", key="oh_fb")

if st.button("Generate Feedback Schedule", type="primary"):
    if mod_file and oh_file:
        mods = load_schedule_data(mod_file)
        ohs = load_schedule_data(oh_file)
        
        with st.spinner("Balancing workloads..."):
            result_df = schedule_feedback(mods, ohs)
            
        st.success("Assignment complete!")
        st.dataframe(result_df, use_container_width=True)
        
        csv_data = result_df.to_csv(index=False).encode('utf-8')
        st.download_button("Download CSV", data=csv_data, file_name="feedback_schedule.csv", mime="text/csv")
    else:
        st.error("Please upload both schedule files first.")
