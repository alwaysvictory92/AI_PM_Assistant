import streamlit as st
import plotly.express as px
from database import get_tasks
from analytics import tasks_to_dataframe, generate_project_insights
from ai_helper import generate_ai_project_insights

st.set_page_config(page_title="Project Insights", page_icon="📈", layout="wide")

st.title("📈 Productivity and Project Insights")

st.write(
    "This module provides a high-level view of project productivity, workload, and overall project health."
)

tasks = get_tasks()
df = tasks_to_dataframe(tasks)

if df.empty:
    st.warning("No tasks available. Add tasks first from the Task Manager page.")
else:
    insights_result = generate_project_insights(df)

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Project Health", insights_result["health_status"])
    col2.metric("Health Score", insights_result["health_score"])
    col3.metric("Completion Rate", f"{insights_result['completion_rate']}%")
    col4.metric("Blocked Tasks", insights_result["blocked_count"])

    st.divider()

    st.subheader("Team Productivity Summary")

    assignee_summary = insights_result["assignee_summary"]
    st.dataframe(assignee_summary, use_container_width=True)

    col_left, col_right = st.columns(2)

    with col_left:
        fig_effort = px.bar(
            assignee_summary,
            x="Assignee",
            y="Total_Effort",
            title="Effort Points by Assignee"
        )
        st.plotly_chart(fig_effort, use_container_width=True)

    with col_right:
        fig_tasks = px.bar(
            assignee_summary,
            x="Assignee",
            y=["Completed_Tasks", "Active_Tasks"],
            title="Completed vs Active Tasks by Assignee"
        )
        st.plotly_chart(fig_tasks, use_container_width=True)

    st.divider()

    st.subheader("Key Productivity Insights")

    for insight in insights_result["insights"]:
        st.info(insight)

    st.divider()

    st.subheader("Project Health Logic")

    st.write("""
    The project health score is calculated using:
    - completion rate
    - blocked tasks
    - incomplete high-priority tasks
    - team workload distribution
    
    This provides a quick overview of whether the project is healthy, needs attention, or is critical.
    """)
    st.divider()

    st.subheader("🤖 AI-Powered Project Insight Report")

    extra_context = st.text_area(
        "Add extra project context for AI analysis",
        placeholder="Example: The client changed requirements, one developer is unavailable, or testing is delayed."
    )

    if st.button("Generate AI Project Insights"):
        with st.spinner("AI is analyzing project health and productivity..."):
            ai_report = generate_ai_project_insights(df, insights_result, extra_context)

        st.subheader("AI Project Insight Report")
        st.markdown(ai_report)