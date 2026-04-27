from dotenv import load_dotenv
import os
from groq import Groq
import json
import tempfile
from database import get_full_project_context, get_resources

load_dotenv()


def get_groq_client():
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        return None
    return Groq(api_key=api_key)


def transcribe_audio_with_groq(uploaded_file):
    client = get_groq_client()

    if not client:
        return "Groq API key is missing. Please set GROQ_API_KEY in your environment."

    suffix = "." + uploaded_file.name.split(".")[-1]

    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_audio:
        temp_audio.write(uploaded_file.read())
        temp_audio_path = temp_audio.name

    try:
        with open(temp_audio_path, "rb") as audio_file:
            transcription = client.audio.transcriptions.create(
                file=audio_file,
                model="whisper-large-v3"
            )

        return transcription.text

    except Exception as e:
        return f"Audio transcription failed: {e}"


def generate_meeting_minutes_from_transcript(transcript):
    client = get_groq_client()

    if not client:
        return "Groq API key is missing. Please set GROQ_API_KEY in your environment."

    prompt = f"""
You are an AI meeting minutes assistant.

Convert the transcript below into professional software project meeting minutes.

Include:
1. Meeting Summary
2. Key Discussion Points
3. Decisions Made
4. Risks / Issues
5. Action Items
6. Next Steps

Transcript:
{transcript}
"""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": "You generate structured software project meeting minutes."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.3,
            max_tokens=900
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"Meeting minutes generation failed: {e}"


def extract_project_data_from_minutes(minutes):
    client = get_groq_client()

    if not client:
        return {"error": "Groq API key is missing."}

    resources = get_resources()

    if resources:
        resource_context = "\n".join([
            f"- Name: {r[1]}, Role: {r[2]}, Skill Level: {r[3]}, Availability: {r[5]}"
            for r in resources
        ])
    else:
        resource_context = "No resources available. Use Unassigned."

    prompt = f"""
You are an AI software requirements analyst.

From the meeting minutes below, extract structured software project data.

Return ONLY raw valid JSON.
Do not include markdown.
Do not include explanations.
Do not include code fences.
Use double quotes for all keys and string values.
Return one JSON object only with this exact structure:

{{
  "project_description": "short project description",
  "requirements": [
    {{
      "type": "Functional or Non-Functional",
      "text": "requirement text",
      "priority": "Low, Medium, or High"
    }}
  ],
  "user_stories": [
    {{
      "story": "As a [user], I want [feature], so that [benefit].",
      "acceptance_criteria": "clear acceptance criteria",
      "priority": "Low, Medium, or High"
    }}
  ],
  "tasks": [
    {{
      "title": "task title",
      "description": "task description",
      "assignee": "name of available resource or Unassigned",
      "priority": "Low, Medium, or High",
      "status": "To Do",
      "deadline": "2026-04-30",
      "effort_points": 3
    }}
  ]
}}

Rules:
- Only generate tasks for a software project following SDLC.
- Tasks should be practical development, design, testing, deployment, documentation, or security tasks.
- Assign each task to the most suitable available resource based on role and skill level.
- Use only names listed in Available Project Resources.
- If no suitable resource exists, use "Unassigned".
- Do not invent names.
- Prefer development tasks to developers.
- Prefer testing tasks to QA Tester.
- Prefer design tasks to UI/UX Designer.
- Prefer security tasks to Security Analyst.
- Prefer planning tasks to Project Manager or Business Analyst.
- Prefer procurement/budget tasks to Procurement Manager or Accountant.
- Use realistic effort points from 1 to 13.
- Return JSON only.

Available Project Resources:
{resource_context}

Meeting Minutes:
{minutes}
"""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": "You extract software requirements, user stories, and SDLC tasks as valid JSON only."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.2,
            max_tokens=1800
        )

        raw_output = response.choices[0].message.content.strip()

        raw_output = raw_output.replace("```json", "").replace("```", "").strip()

        start = raw_output.find("{")
        end = raw_output.rfind("}") + 1

        if start != -1 and end != -1:
            clean_json = raw_output[start:end]
        else:
            clean_json = raw_output

        return json.loads(clean_json)

    except json.JSONDecodeError:
        return {
            "error": "AI response was not valid JSON.",
            "raw_output": raw_output
        }

    except Exception as e:
        return {"error": f"Project data extraction failed: {e}"}


def build_project_context(df, metrics):
    saved_context = get_full_project_context()

    if df.empty:
        task_context = "No project tasks are available yet."
    else:
        task_lines = []
        for _, row in df.iterrows():
            task_lines.append(
                f"- {row['Title']} | Assignee: {row['Assignee']} | "
                f"Priority: {row['Priority']} | Status: {row['Status']} | "
                f"Deadline: {row['Deadline']} | Effort: {row['Effort Points']}"
            )

        task_context = f"""
Project Metrics:
- Total tasks: {metrics['total']}
- Completed tasks: {metrics['completed']}
- In progress tasks: {metrics['in_progress']}
- Overdue tasks: {metrics['overdue']}
- Progress: {metrics['progress']}%

Tasks:
{chr(10).join(task_lines)}
"""

    requirements_text = "\n".join([
        f"- {r[0]} | {r[1]} | Priority: {r[2]}"
        for r in saved_context["requirements"]
    ])

    user_stories_text = "\n".join([
        f"- {s[0]} | Acceptance Criteria: {s[1]} | Priority: {s[2]}"
        for s in saved_context["user_stories"]
    ])

    return f"""
Project Description:
{saved_context["project_description"]}

Latest Meeting Minutes:
{saved_context["latest_minutes"]}

Requirements:
{requirements_text if requirements_text else "No requirements saved yet."}

User Stories:
{user_stories_text if user_stories_text else "No user stories saved yet."}

{task_context}
"""


def ask_groq_ai(question, df, metrics):
    client = get_groq_client()

    if not client:
        return "Groq API key is missing. Please set GROQ_API_KEY in your environment."

    project_context = build_project_context(df, metrics)

    prompt = f"""
You are an AI project management and software engineering assistant.
Answer only using the project data provided below.
Be concise, practical, and professional.

{project_context}

User question:
{question}
"""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful AI assistant for project tracking, documentation, and task analysis."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.3,
            max_tokens=500
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"AI request failed: {e}"


def generate_ai_documentation(df, metrics):
    client = get_groq_client()

    if not client:
        return "Groq API key is missing. Please set GROQ_API_KEY in your environment."

    project_context = build_project_context(df, metrics)

    prompt = f"""
You are an AI documentation assistant for a software project.

Using the project data below, generate a professional project documentation report.

The report must include:
1. Project Summary
2. Current Progress
3. Key Risks
4. Recommendations
5. Next Steps

Use clear headings and concise paragraphs.

Project Data:
{project_context}
"""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": "You generate professional software project documentation based only on provided project data."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.3,
            max_tokens=700
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"AI documentation generation failed: {e}"


def generate_ai_risk_analysis(df, metrics, extra_context=""):
    client = get_groq_client()

    if not client:
        return "Groq API key is missing. Please set GROQ_API_KEY in your environment."

    project_context = build_project_context(df, metrics)

    prompt = f"""
You are an AI project risk analyst.

Analyze the project data below and provide a professional risk analysis report.

Include:
1. Overall Risk Assessment
2. Key Risk Factors
3. Possible Impact
4. Mitigation Recommendations
5. Next Immediate Actions

Project Data:
{project_context}

Additional Manager Context:
{extra_context}
"""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": "You are a professional AI risk analyst for software projects."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.3,
            max_tokens=700
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"AI risk analysis failed: {e}"


def generate_ai_project_insights(df, insights_result, extra_context=""):
    client = get_groq_client()

    if not client:
        return "Groq API key is missing. Please set GROQ_API_KEY in your environment."

    task_data = df.to_string(index=False)

    prompt = f"""
You are an AI software project insight analyst.

Analyze the project productivity and health data below.

Provide a professional report with:
1. Overall Project Health
2. Productivity Analysis
3. Team Workload Observations
4. Key Concerns
5. Improvement Recommendations
6. Next Best Actions

Project Health Data:
- Health Score: {insights_result["health_score"]}
- Health Status: {insights_result["health_status"]}
- Completion Rate: {insights_result["completion_rate"]}%
- Blocked Tasks: {insights_result["blocked_count"]}
- Incomplete High Priority Tasks: {insights_result["high_priority_count"]}

Task Data:
{task_data}

Additional Context:
{extra_context}
"""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": "You are a professional AI analyst for software project productivity and health."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.3,
            max_tokens=800
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"AI project insight generation failed: {e}"