import pandas as pd
from datetime import date

def generate_project_insights(df):
    if df.empty:
        return {
            "health_score": 0,
            "health_status": "No Data",
            "completion_rate": 0,
            "blocked_count": 0,
            "high_priority_count": 0,
            "assignee_summary": pd.DataFrame(),
            "insights": []
        }

    df = df.copy()

    total_tasks = len(df)
    completed_tasks = len(df[df["Status"] == "Completed"])
    blocked_count = len(df[df["Status"] == "Blocked"])
    high_priority_count = len(df[
        (df["Priority"] == "High") &
        (df["Status"] != "Completed")
    ])

    completion_rate = round((completed_tasks / total_tasks) * 100, 2)

    assignee_summary = df.groupby("Assignee").agg(
        Total_Tasks=("ID", "count"),
        Completed_Tasks=("Status", lambda x: (x == "Completed").sum()),
        Active_Tasks=("Status", lambda x: (x != "Completed").sum()),
        Total_Effort=("Effort Points", "sum")
    ).reset_index()

    health_score = completion_rate

    if blocked_count > 0:
        health_score -= blocked_count * 10

    if high_priority_count > 0:
        health_score -= high_priority_count * 5

    health_score = max(0, round(health_score, 2))

    if health_score >= 80:
        health_status = "Healthy"
    elif health_score >= 50:
        health_status = "Needs Attention"
    else:
        health_status = "Critical"

    insights = []

    insights.append(f"The project completion rate is {completion_rate}%.")

    if blocked_count > 0:
        insights.append(f"There are {blocked_count} blocked tasks affecting productivity.")
    else:
        insights.append("No blocked tasks are currently affecting the project.")

    if high_priority_count > 0:
        insights.append(f"{high_priority_count} high-priority tasks are still incomplete.")
    else:
        insights.append("No incomplete high-priority tasks detected.")

    most_loaded = assignee_summary.sort_values(
        by="Total_Effort",
        ascending=False
    ).head(1)

    if not most_loaded.empty:
        name = most_loaded.iloc[0]["Assignee"]
        effort = most_loaded.iloc[0]["Total_Effort"]
        insights.append(f"{name} currently has the highest workload with {effort} effort points.")

    return {
        "health_score": health_score,
        "health_status": health_status,
        "completion_rate": completion_rate,
        "blocked_count": blocked_count,
        "high_priority_count": high_priority_count,
        "assignee_summary": assignee_summary,
        "insights": insights
    }

def analyze_sprint_plan(df):
    if df.empty:
        return {
            "workload": pd.DataFrame(),
            "overloaded_members": [],
            "sprint_tasks": pd.DataFrame(),
            "recommendations": []
        }

    df = df.copy()

    active_tasks = df[df["Status"] != "Completed"]

    workload = active_tasks.groupby("Assignee").agg(
        Task_Count=("ID", "count"),
        Total_Effort=("Effort Points", "sum")
    ).reset_index()

    overloaded_members = workload[workload["Total_Effort"] > 12]["Assignee"].tolist()

    sprint_tasks = active_tasks.sort_values(
        by=["Priority", "Deadline"],
        ascending=[True, True]
    )

    recommendations = []

    if len(overloaded_members) > 0:
        recommendations.append(
            f"Some team members may be overloaded: {', '.join(overloaded_members)}."
        )
        recommendations.append(
            "Consider redistributing tasks to balance workload across the team."
        )
    else:
        recommendations.append("No major workload imbalance detected.")

    high_priority = active_tasks[active_tasks["Priority"] == "High"]

    if len(high_priority) > 0:
        recommendations.append(
            f"There are {len(high_priority)} high-priority active tasks that should be considered for the next sprint."
        )

    blocked = active_tasks[active_tasks["Status"] == "Blocked"]

    if len(blocked) > 0:
        recommendations.append(
            f"{len(blocked)} blocked tasks should be resolved before sprint commitment."
        )

    return {
        "workload": workload,
        "overloaded_members": overloaded_members,
        "sprint_tasks": sprint_tasks,
        "recommendations": recommendations
    }

def analyze_project_risks(df):
    if df.empty:
        return {
            "risk_score": 0,
            "risk_level": "No Data",
            "risks": [],
            "recommendations": []
        }

    df = df.copy()
    df["Deadline"] = pd.to_datetime(df["Deadline"], errors="coerce").dt.date
    today = date.today()

    risks = []
    recommendations = []
    risk_score = 0

    overdue_tasks = df[
        (df["Deadline"] < today) &
        (df["Status"] != "Completed")
    ]

    blocked_tasks = df[df["Status"] == "Blocked"]
    high_priority_tasks = df[
        (df["Priority"] == "High") &
        (df["Status"] != "Completed")
    ]

    incomplete_tasks = df[df["Status"] != "Completed"]

    if len(overdue_tasks) > 0:
        risk_score += len(overdue_tasks) * 20
        risks.append(f"{len(overdue_tasks)} task(s) are overdue.")
        recommendations.append("Review overdue tasks immediately and adjust deadlines or resources.")

    if len(blocked_tasks) > 0:
        risk_score += len(blocked_tasks) * 25
        risks.append(f"{len(blocked_tasks)} task(s) are blocked.")
        recommendations.append("Resolve blockers by assigning owners and removing dependencies.")

    if len(high_priority_tasks) > 0:
        risk_score += len(high_priority_tasks) * 10
        risks.append(f"{len(high_priority_tasks)} high-priority task(s) are still incomplete.")
        recommendations.append("Focus team effort on high-priority unfinished tasks.")

    if len(incomplete_tasks) > len(df) * 0.6:
        risk_score += 20
        risks.append("More than 60% of tasks are still incomplete.")
        recommendations.append("Reassess project timeline and reduce scope if needed.")

    if risk_score >= 80:
        risk_level = "High Risk"
    elif risk_score >= 40:
        risk_level = "Medium Risk"
    elif risk_score > 0:
        risk_level = "Low Risk"
    else:
        risk_level = "On Track"

    if not risks:
        risks.append("No major project risks detected.")
        recommendations.append("Continue monitoring progress and maintaining current workflow.")

    return {
        "risk_score": risk_score,
        "risk_level": risk_level,
        "risks": risks,
        "recommendations": recommendations
    }

def prioritize_tasks(df):
    if df.empty:
        return df

    priority_score = {
        "High": 30,
        "Medium": 20,
        "Low": 10
    }

    status_score = {
        "Blocked": 25,
        "In Progress": 15,
        "To Do": 10,
        "Completed": -50
    }

    df = df.copy()
    df["Deadline"] = pd.to_datetime(df["Deadline"], errors="coerce").dt.date

    today = date.today()

    scores = []

    for _, row in df.iterrows():
        score = 0

        score += priority_score.get(row["Priority"], 0)
        score += status_score.get(row["Status"], 0)

        if pd.notnull(row["Deadline"]):
            days_left = (row["Deadline"] - today).days

            if days_left < 0:
                score += 40
            elif days_left <= 2:
                score += 30
            elif days_left <= 5:
                score += 20
            elif days_left <= 10:
                score += 10

        try:
            effort = int(row["Effort Points"])
            if effort >= 8:
                score += 10
        except:
            pass

        scores.append(score)

    df["Priority Score"] = scores

    df["Recommendation"] = df["Priority Score"].apply(
        lambda x: "Immediate Focus" if x >= 70
        else "High Focus" if x >= 50
        else "Medium Focus" if x >= 30
        else "Low Focus"
    )

    return df.sort_values(by="Priority Score", ascending=False)

def tasks_to_dataframe(tasks):
    columns = [
        "ID",
        "Title",
        "Description",
        "Assignee",
        "Priority",
        "Status",
        "Deadline",
        "Effort Points",
        "Created At"
    ]

    return pd.DataFrame(tasks, columns=columns)


def calculate_metrics(df):
    if df.empty:
        return {
            "total": 0,
            "completed": 0,
            "in_progress": 0,
            "overdue": 0,
            "progress": 0
        }

    total = len(df)
    completed = len(df[df["Status"] == "Completed"])
    in_progress = len(df[df["Status"] == "In Progress"])

    df["Deadline"] = pd.to_datetime(df["Deadline"], errors="coerce").dt.date
    today = date.today()

    overdue = len(df[
        (df["Deadline"] < today) &
        (df["Status"] != "Completed")
    ])

    progress = round((completed / total) * 100, 2) if total > 0 else 0

    return {
        "total": total,
        "completed": completed,
        "in_progress": in_progress,
        "overdue": overdue,
        "progress": progress
    }