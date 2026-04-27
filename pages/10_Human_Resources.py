import streamlit as st
import pandas as pd
from database import add_resource, get_resources

st.set_page_config(page_title="Human Resources", page_icon="👥", layout="wide")

st.title("👥 Human Resources")

st.write("Add project resources that can later be assigned to tasks.")

roles = [
    "Project Manager",
    "Business Analyst",
    "Junior Software Developer",
    "Mid-Level Software Developer",
    "Senior Software Developer",
    "QA Tester",
    "UI/UX Designer",
    "Security Analyst",
    "DevOps Engineer",
    "Accountant",
    "Procurement Manager"
]

skill_levels = ["Junior", "Mid", "Senior", "Lead", "Specialist"]

availability_options = ["Available", "Partially Available", "Unavailable"]

with st.form("resource_form"):
    name = st.text_input("Resource Name")
    role = st.selectbox("Role", roles)
    skill_level = st.selectbox("Skill Level", skill_levels)
    hourly_rate = st.number_input("Hourly Rate", min_value=0.0, value=25.0, step=5.0)
    availability = st.selectbox("Availability", availability_options)

    submitted = st.form_submit_button("Add Resource")

    if submitted:
        if not name.strip():
            st.error("Resource name is required.")
        else:
            add_resource(name, role, skill_level, hourly_rate, availability)
            st.success("Resource added successfully.")

st.divider()

st.subheader("Available Project Resources")

resources = get_resources()

if not resources:
    st.warning("No resources added yet.")
else:
    df = pd.DataFrame(
        resources,
        columns=[
            "ID",
            "Name",
            "Role",
            "Skill Level",
            "Hourly Rate",
            "Availability",
            "Created At"
        ]
    )

    st.dataframe(df, use_container_width=True)