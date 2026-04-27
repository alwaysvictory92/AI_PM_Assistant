import streamlit as st
from database import get_tasks
from analytics import tasks_to_dataframe, calculate_metrics
from ai_helper import generate_ai_documentation
from database import get_full_project_context

st.set_page_config(page_title="Documentation", page_icon="📄", layout="wide")

st.title("📄 AI Documentation Generator")

st.write(
    "Generate professional project documentation using real AI and current project task data."
)

tasks = get_tasks()
df = tasks_to_dataframe(tasks)
metrics = calculate_metrics(df)

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Tasks", metrics["total"])
col2.metric("Completed", metrics["completed"])
col3.metric("Overdue", metrics["overdue"])
col4.metric("Progress", f"{metrics['progress']}%")

st.divider()

project_context = get_full_project_context()

st.subheader("📌 Project Description")
if project_context["project_description"]:
    st.write(project_context["project_description"])
else:
    st.info("No project description saved yet.")

st.subheader("✅ Requirements")
with st.expander("📋 Recorded Requirements", expanded=True):
    if project_context["requirements"]:

        functional = [r for r in project_context["requirements"] if r[0].lower() == "functional"]
        non_functional = [r for r in project_context["requirements"] if r[0].lower() == "non-functional"]

        st.markdown("### 🧩 Functional Requirements")
        if functional:
            for req in functional:
                st.write(f"- {req[1]} *(Priority: {req[2]})*")
        else:
            st.info("No functional requirements found.")

        st.markdown("### ⚙️ Non-Functional Requirements")
        if non_functional:
            for req in non_functional:
                st.write(f"- {req[1]} *(Priority: {req[2]})*")
        else:
            st.info("No non-functional requirements found.")

    else:
        st.info("No requirements saved yet.")

st.subheader("👤 User Stories")
if project_context["user_stories"]:
    for story in project_context["user_stories"]:
        st.write(f"- {story[0]}")
        st.caption(f"Acceptance Criteria: {story[1]} | Priority: {story[2]}")
else:
    st.info("No user stories saved yet.")

st.divider()

if df.empty:
    st.warning("No tasks available. Add tasks first from the Task Manager page.")
else:
    st.subheader("Project Data Used by AI")
    st.dataframe(df, use_container_width=True)

    if st.button("Generate AI Project Documentation"):
        with st.spinner("Generating AI documentation..."):
            ai_report = generate_ai_documentation(df, metrics)

        st.subheader("Generated Project Documentation")
        st.markdown(ai_report)