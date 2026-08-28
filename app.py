import streamlit as st

st.set_page_config(page_title="Scheduling Hub", page_icon="📅", layout="wide")

st.title("Team Scheduling Hub")
st.write("Welcome to the scheduling app. Use the sidebar to navigate between tools:")

st.markdown("""
* **Feedback Scheduling:** Load-balances feedback sessions between Moderators and Overheads based on shift overlaps.
* **Roundtable Planning:** Uses mathematical constraints to perfectly schedule roundtable groups and quotas.
""")
