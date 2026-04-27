import streamlit as st
import plotly.express as px
import pandas as pd
from database import get_tasks
from analytics import tasks_to_dataframe, analyze_project_risks
from analytics import calculate_metrics
from ai_helper import generate_ai_risk_analysis

st.set_page_config(page_title="Risk Analysis", page_icon="⚠️", layout="wide")

st.title("⚠️ Project Risk Analysis")

st.write(
    "This module analyzes project risks based on overdue tasks, blocked tasks, unfinished high-priority tasks, and completion status."
)

tasks = get_tasks()
df = tasks_to_dataframe(tasks)

if df.empty:
    st.warning("No tasks available. Add tasks first from the Task Manager page.")
else:
    risk_result = analyze_project_risks(df)

    col1, col2 = st.columns(2)

    col1.metric("Overall Risk Level", risk_result["risk_level"])
    col2.metric("Risk Score", risk_result["risk_score"])

    st.divider()

    st.subheader("Identified Risks")

    for risk in risk_result["risks"]:
        st.error(risk)

    st.subheader("Recommended Mitigation Actions")

    for recommendation in risk_result["recommendations"]:
        st.success(recommendation)

    st.divider()

    st.subheader("Risk Factors Chart")

    overdue_count = len(df[
        (pd.to_datetime(df["Deadline"], errors="coerce").dt.date < pd.Timestamp.today().date()) &
        (df["Status"] != "Completed")
    ])

    blocked_count = len(df[df["Status"] == "Blocked"])

    high_priority_incomplete = len(df[
        (df["Priority"] == "High") &
        (df["Status"] != "Completed")
    ])

    chart_data = pd.DataFrame({
        "Risk Factor": [
            "Overdue Tasks",
            "Blocked Tasks",
            "Incomplete High Priority"
        ],
        "Count": [
            overdue_count,
            blocked_count,
            high_priority_incomplete
        ]
    })

    fig = px.bar(
        chart_data,
        x="Risk Factor",
        y="Count",
        title="Project Risk Factors"
    )
    st.divider()

    st.subheader("🤖 AI-Based Risk Analysis")

    extra_context = st.text_area(
        "Add any extra project context for AI analysis",
        placeholder="Example: The client changed requirements this week, one developer is unavailable, and testing has not started yet."
    )

    if st.button("Generate AI Risk Analysis"):
        metrics = calculate_metrics(df)

        with st.spinner("AI is analyzing project risks..."):
            ai_risk_report = generate_ai_risk_analysis(df, metrics, extra_context)

        st.subheader("AI Risk Report")
        st.markdown(ai_risk_report)

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Task Data Used for Risk Analysis")
    st.dataframe(df, use_container_width=True)