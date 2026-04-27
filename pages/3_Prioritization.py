import streamlit as st
import plotly.express as px
from database import get_tasks
from analytics import tasks_to_dataframe, prioritize_tasks

st.set_page_config(page_title="Prioritization", page_icon="🎯", layout="wide")

st.title("🎯 AI-Assisted Task Prioritization")

st.write(
    "This module ranks tasks using priority, deadline urgency, task status, and effort points."
)

tasks = get_tasks()
df = tasks_to_dataframe(tasks)

if df.empty:
    st.warning("No tasks available. Add tasks first from the Task Manager page.")
else:
    prioritized_df = prioritize_tasks(df)

    st.subheader("Recommended Task Focus Order")

    display_cols = [
        "Title",
        "Assignee",
        "Priority",
        "Status",
        "Deadline",
        "Effort Points",
        "Priority Score",
        "Recommendation"
    ]

    st.dataframe(
        prioritized_df[display_cols],
        use_container_width=True
    )

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Recommendation Distribution")

        rec_counts = prioritized_df["Recommendation"].value_counts().reset_index()
        rec_counts.columns = ["Recommendation", "Count"]

        fig_rec = px.bar(
            rec_counts,
            x="Recommendation",
            y="Count",
            title="Task Focus Levels"
        )

        st.plotly_chart(fig_rec, use_container_width=True)

    with col2:
        st.subheader("Top Priority Tasks")

        top_tasks = prioritized_df.head(5)

        for _, row in top_tasks.iterrows():
            st.info(
                f"**{row['Title']}**  \n"
                f"Assignee: {row['Assignee']}  \n"
                f"Priority: {row['Priority']} | Status: {row['Status']}  \n"
                f"Score: {row['Priority Score']} — {row['Recommendation']}"
            )

    st.divider()

    st.subheader("How the Prioritization Works")

    st.write("""
    The system calculates a priority score using:
    - task priority level
    - deadline urgency
    - task status
    - effort points
    - overdue condition
    
    Higher scores indicate tasks that should receive earlier attention.
    """)