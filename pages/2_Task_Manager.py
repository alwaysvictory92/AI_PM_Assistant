import streamlit as st
import pandas as pd
from database import add_task, get_tasks, get_resources, update_task, delete_task
from analytics import tasks_to_dataframe

st.set_page_config(page_title="Task Manager", page_icon="📋", layout="wide")

st.title("📋 Task Manager")

st.write("Create, assign, edit, and track project tasks.")

resources = get_resources()

if resources:
    resource_names = [r[1] for r in resources]
else:
    resource_names = ["Unassigned"]

# ---------------- Add Task ----------------
st.subheader("Add New Task")

with st.form("task_form"):
    title = st.text_input("Task Title")
    description = st.text_area("Task Description")
    assignee = st.selectbox("Assignee", resource_names)
    priority = st.selectbox("Priority", ["Low", "Medium", "High"])
    status = st.selectbox("Status", ["To Do", "In Progress", "Completed", "Blocked"])
    deadline = st.date_input("Deadline")
    effort_points = st.number_input("Effort Points", min_value=1, max_value=20, value=3)

    submitted = st.form_submit_button("Add Task")

    if submitted:
        if title.strip() == "":
            st.error("Task title is required.")
        else:
            add_task(title, description, assignee, priority, status, deadline, effort_points)
            st.success("Task added successfully.")
            st.rerun()

st.divider()

# ---------------- View Tasks ----------------
st.subheader("Current Tasks")

tasks = get_tasks()
df = tasks_to_dataframe(tasks)

if df.empty:
    st.warning("No tasks found. Add your first task above.")
else:
    st.dataframe(df, use_container_width=True)

    st.divider()

    # ---------------- Edit Task ----------------
    st.subheader("Edit Existing Task")

    task_options = {
        f"{row['ID']} - {row['Title']}": row["ID"]
        for _, row in df.iterrows()
    }

    selected_task_label = st.selectbox("Select Task to Edit", list(task_options.keys()))
    selected_task_id = task_options[selected_task_label]

    selected_task = df[df["ID"] == selected_task_id].iloc[0]

    with st.form("edit_task_form"):
        edit_title = st.text_input("Task Title", value=selected_task["Title"])
        edit_description = st.text_area("Task Description", value=selected_task["Description"])
        edit_assignee = st.selectbox(
            "Assignee",
            resource_names,
            index=resource_names.index(selected_task["Assignee"]) if selected_task["Assignee"] in resource_names else 0
        )
        edit_priority = st.selectbox(
            "Priority",
            ["Low", "Medium", "High"],
            index=["Low", "Medium", "High"].index(selected_task["Priority"])
        )
        edit_status = st.selectbox(
            "Status",
            ["To Do", "In Progress", "Completed", "Blocked"],
            index=["To Do", "In Progress", "Completed", "Blocked"].index(selected_task["Status"])
        )
        edit_deadline = st.date_input(
            "Deadline",
            value=pd.to_datetime(selected_task["Deadline"]).date()
        )
        edit_effort_points = st.number_input(
            "Effort Points",
            min_value=1,
            max_value=20,
            value=int(selected_task["Effort Points"])
        )

        col1, col2 = st.columns(2)

        update_submitted = col1.form_submit_button("Update Task")
        delete_submitted = col2.form_submit_button("Delete Task")

        if update_submitted:
            update_task(
                selected_task_id,
                edit_title,
                edit_description,
                edit_assignee,
                edit_priority,
                edit_status,
                edit_deadline,
                edit_effort_points
            )
            st.success("Task updated successfully.")
            st.rerun()

        if delete_submitted:
            delete_task(selected_task_id)
            st.warning("Task deleted.")
            st.rerun()