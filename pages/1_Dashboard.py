import streamlit as st
import plotly.express as px
from database import get_tasks
from analytics import tasks_to_dataframe, calculate_metrics

st.set_page_config(page_title="Dashboard", page_icon="📊", layout="wide")

st.title("📊 Project Dashboard")

tasks = get_tasks()
df = tasks_to_dataframe(tasks)

metrics = calculate_metrics(df)

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Total Tasks", metrics["total"])
col2.metric("Completed", metrics["completed"])
col3.metric("In Progress", metrics["in_progress"])
col4.metric("Overdue", metrics["overdue"])
col5.metric("Progress", f"{metrics['progress']}%")

st.divider()

if df.empty:
    st.warning("No task data available yet.")
else:
    col_left, col_right = st.columns(2)

    with col_left:
        st.subheader("Task Status Distribution")
        status_counts = df["Status"].value_counts().reset_index()
        status_counts.columns = ["Status", "Count"]

        fig_status = px.pie(
            status_counts,
            names="Status",
            values="Count",
            title="Tasks by Status"
        )

        st.plotly_chart(fig_status, use_container_width=True)

    with col_right:
        st.subheader("Workload by Assignee")
        workload = df["Assignee"].value_counts().reset_index()
        workload.columns = ["Assignee", "Tasks"]

        fig_workload = px.bar(
            workload,
            x="Assignee",
            y="Tasks",
            title="Tasks Assigned per Team Member"
        )

        st.plotly_chart(fig_workload, use_container_width=True)

    st.subheader("Task Table")
    st.dataframe(df, use_container_width=True)