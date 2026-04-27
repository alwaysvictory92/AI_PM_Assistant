import streamlit as st

st.set_page_config(
    page_title="AI Project Assistant",
    page_icon="🤖",
    layout="wide"
)

st.title("🚀 AI-Powered SDLC Automation & Project Management System")

st.write("""
This application is an AI-powered system designed to automate and support the Software Development Life Cycle (SDLC). 
It transforms meeting inputs into structured project outputs including requirements, user stories, and tasks, 
while also providing intelligent project insights and resource management.
""")

st.subheader("🚀 System Capabilities")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    ### 🧠 Software Engineering Module
    - AI-generated meeting minutes from audio
    - Automated requirements extraction
    - User story generation
    - AI-powered documentation
    - End-to-end SDLC automation
    """)

with col2:
    st.markdown("""
    ### 📊 Software Project Management Module
    - Task generation and assignment (AI-driven)
    - Resource management (Junior, Mid, Senior roles)
    - Task prioritization and tracking
    - Risk analysis and mitigation insights
    - Project health and performance analytics
    """)

st.subheader("🔄 Intelligent Workflow")

st.markdown("""
**Meeting Input → AI Processing → SDLC Outputs**

- 🎤 Meeting Audio Upload  
- 📝 Transcription & Meeting Minutes  
- 📌 Requirements & User Stories Extraction  
- 📋 Task Generation & Assignment  
- 📊 Project Tracking & Insights  

This system bridges the gap between **project discussions and actionable development workflows**.
""")

st.subheader("📦 System Modules")

col3, col4 = st.columns(2)

with col3:
    st.markdown("""
    #### 🧠 Software Engineering Module
    - Project tracking dashboard  
    - Automated documentation  
    - AI project insight assistant  
    - Requirement & user story generation  
    """)

with col4:
    st.markdown("""
    #### 📊 Software Project Management Module
    - Task planning and assignment  
    - Task prioritization  
    - Progress tracking  
    - Risk awareness and analytics  
    """)

st.write("Use the sidebar to navigate between pages.")