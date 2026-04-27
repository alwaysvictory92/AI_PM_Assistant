import streamlit as st
from database import (
    save_meeting_minutes,
    save_project_description,
    save_requirement,
    save_user_story,
    add_task
)
from ai_helper import (
    transcribe_audio_with_groq,
    generate_meeting_minutes_from_transcript,
    extract_project_data_from_minutes
)

st.set_page_config(page_title="Requirement Meeting", page_icon="🎤", layout="wide")

st.title("🎤 Requirement Meeting Minutes Generator")

st.write("Upload a meeting recording to generate requirements, user stories, and tasks.")

uploaded_file = st.file_uploader("Upload meeting audio", type=["mp3", "wav", "m4a"])

if uploaded_file:
    st.success("Audio uploaded successfully")

    if st.button("Process Meeting Recording"):

        with st.spinner("Transcribing audio..."):
            transcript = transcribe_audio_with_groq(uploaded_file)

        st.subheader("Transcript")
        st.write(transcript)

        with st.spinner("Generating meeting minutes..."):
            minutes = generate_meeting_minutes_from_transcript(transcript)

        st.subheader("Meeting Minutes")
        st.markdown(minutes)

        # Save meeting minutes
        save_meeting_minutes(transcript, minutes)

        with st.spinner("Extracting project data..."):
            extracted_data = extract_project_data_from_minutes(minutes)

        if "error" in extracted_data:
            st.error(extracted_data["error"])
            st.write(extracted_data.get("raw_output", ""))
        else:
            # Project Description
            description = extracted_data["project_description"]
            save_project_description(description)

            st.subheader("Project Description")
            st.write(description)

            # Requirements
            st.subheader("Requirements")
            for req in extracted_data["requirements"]:
                save_requirement(req["type"], req["text"], req["priority"])
                st.write(f"- ({req['type']}) {req['text']} [{req['priority']}]")

            # User Stories
            st.subheader("User Stories")
            for story in extracted_data["user_stories"]:
                save_user_story(
                    story["story"],
                    story["acceptance_criteria"],
                    story["priority"]
                )
                st.write(f"- {story['story']} [{story['priority']}]")

            # Tasks
            st.subheader("Generated Tasks")
            for task in extracted_data["tasks"]:
                add_task(
                    task["title"],
                    task["description"],
                    task["assignee"],
                    task["priority"],
                    task["status"],
                    task["deadline"],
                    task["effort_points"]
                )

                st.write(f"- {task['title']} ({task['priority']})")

            st.success("All data saved and tasks added to Task Manager")