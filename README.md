# 🚀 AI-Assisted Software Project Management System

## 📌 Project Overview
This project is an **AI-assisted Software Project Management System** developed using **Streamlit and Groq AI**. It enhances traditional project management by integrating AI into planning, resource allocation, risk analysis, and project monitoring.

The system transforms project requirements into structured tasks and provides intelligent insights to support decision-making.

---

## 🎯 Objectives
- Automate project planning and task generation  
- Improve resource allocation using AI  
- Support risk identification and mitigation  
- Provide real-time project monitoring and insights  
- Enhance decision-making with AI assistance  

---

## 🔧 Key Features

### 📋 Task Management
- Create, edit, and delete tasks  
- Track status, priority, deadlines, and effort  
- Tasks structured as Work Breakdown Structure (WBS)  

### 👥 Resource Management
- Add team members (PM, Developers, QA)  
- Define skill levels (Junior, Mid, Senior)  
- Assign tasks to resources  

### 🤖 AI Integration
- AI-assisted task generation from requirements  
- AI-based task assignment  
- AI-powered risk analysis  
- AI project insights and recommendations  

### 📊 Project Dashboard
- Monitor project progress  
- Visualize task completion and performance  
- Supports Monitoring & Control phase  

### 📘 Documentation Module
- Stores:
  - Project description  
  - Meeting minutes  
  - Requirements  
  - User stories  

---

## 🏗️ System Architecture
- **Frontend**: Streamlit  
- **Backend**: Python  
- **AI Layer**: Groq AI (LLM + Whisper)  
- **Database**: SQLite  

---

## 🗄️ Database Tables
- `tasks`  
- `resources`  
- `meeting_minutes`  
- `project_description`  
- `requirements`  
- `user_stories`  

---

## ⚙️ Technologies Used
- Python  
- Streamlit  
- Groq AI  
- SQLite  
- Pandas  

---

## ▶️ How to Run the Project

### 1️⃣ Clone Repository
```bash
git clone https://github.com/your-username/AI_PM_Assistant.git
cd AI_PM_Assistant
python -m venv venv
pip install -r requirements.txt
GROQ_API_KEY=your_api_key_here
streamlit run app.py
