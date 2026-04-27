import streamlit as st
from database import get_tasks
from analytics import tasks_to_dataframe, calculate_metrics
from ai_helper import ask_groq_ai

st.set_page_config(page_title="AI Chat", page_icon="🤖", layout="wide")

st.title("🤖 AI Project Assistant")

st.write("Ask questions about your project.")

tasks = get_tasks()
df = tasks_to_dataframe(tasks)
metrics = calculate_metrics(df)

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Input
user_input = st.chat_input("Ask a question about your project...")

if user_input:
    # User message
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.write(user_input)

    # AI response (fallback for now)
    response = ask_groq_ai(user_input, df, metrics)

    st.session_state.messages.append({"role": "assistant", "content": response})

    with st.chat_message("assistant"):
        st.write(response)