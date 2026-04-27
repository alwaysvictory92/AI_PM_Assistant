import streamlit as st
import plotly.express as px
from database import get_tasks
from analytics import tasks_to_dataframe, analyze_sprint_plan

st.set_page_config(page_title="Sprint Planning", page_icon="🏃", layout="wide")

st.title("🏃 Sprint Planning Assistant")

st.write(
    "This module helps project managers review active tasks, team workload, and sprint planning recommendations."
)

tasks = get_tasks()
df = tasks_to_dataframe(tasks)

if df.empty:
    st.warning("No tasks available. Add tasks first from the Task Manager page.")
else:
    sprint_result = analyze_sprint_plan(df)

    st.subheader("Team Workload")

    workload = sprint_result["workload"]

    if workload.empty:
        st.info("No active workload. All tasks may be completed.")
    else:
        st.dataframe(workload, use_container_width=True)

        fig = px.bar(
            workload,
            x="Assignee",
            y="Total_Effort",
            title="Sprint Workload by Assignee"
        )
        st.plotly_chart(fig, use_container_width=True)

    st.divider()

    st.subheader("Sprint Candidate Tasks")

    sprint_tasks = sprint_result["sprint_tasks"]

    if sprint_tasks.empty:
        st.success("No active tasks remaining for sprint planning.")
    else:
        display_cols = [
            "Title",
            "Assignee",
            "Priority",
            "Status",
            "Deadline",
            "Effort Points"
        ]
        st.dataframe(sprint_tasks[display_cols], use_container_width=True)

    st.divider()

    st.subheader("Sprint Planning Recommendations")

    for rec in sprint_result["recommendations"]:
        st.info(rec)

    st.divider()

    st.subheader("Planning Logic")

    st.write("""
    The sprint planning assistant reviews:
    - active tasks that are not completed
    - workload by assignee
    - total effort points
    - high-priority tasks
    - blocked tasks
    
    This helps the project manager decide what should be included in the next sprint.
    """)