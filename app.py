import streamlit as st
import PyPDF2
import pandas as pd
import random
import json
import os

# -------------------------------
# 🎨 BACKGROUND
# -------------------------------
def set_bg(c1, c2):
    st.markdown(f"""
    <style>
    .stApp {{
        background: linear-gradient(to right, {c1}, {c2});
        color: white;
    }}
    </style>
    """, unsafe_allow_html=True)

# -------------------------------
# 💾 STORAGE
# -------------------------------
def load_data(file):
    if os.path.exists(file):
        with open(file, "r") as f:
            return json.load(f)
    return {}

def save_data(data, file):
    with open(file, "w") as f:
        json.dump(data, f)

users = load_data("users.json")

# -------------------------------
# 📌 SESSION STATE
# -------------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "role" not in st.session_state:
    st.session_state.role = ""

if "interview_stage" not in st.session_state:
    st.session_state.interview_stage = 1

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# -------------------------------
# 📄 PDF
# -------------------------------
def extract_text_from_pdf(file):
    text = ""
    reader = PyPDF2.PdfReader(file)
    for p in reader.pages:
        if p.extract_text():
            text += p.extract_text()
    return text.lower()

# -------------------------------
# 🧠 JOB ROLES
# -------------------------------
job_roles = {
    "Python Developer": ["python", "sql", "django"],
    "Java Developer": ["java", "spring"],
    "Web Developer": ["html", "css", "javascript"],
    "Data Analyst": ["excel", "sql"],
    "Tester": ["testing", "selenium"],
    "HR": ["communication", "recruitment"]
}

# -------------------------------
# 🧠 SKILLS
# -------------------------------
def extract_skills(text):
    all_skills = sum(job_roles.values(), [])
    return list(set([s for s in all_skills if s in text]))

def match_skills(candidate, required):
    matched = list(set(candidate) & set(required))
    missing = list(set(required) - set(candidate))
    score = (len(matched)/len(required))*100 if required else 0
    return matched, missing, score

# -------------------------------
# 🎤 QUESTIONS
# -------------------------------
def get_questions(role):
    return {
        "Python Developer": ["What is Python?", "Explain OOP", "What is Django?", "List vs Tuple?", "Exception handling?", "API?", "Project?", "Pandas?", "Database?", "Decorators?"],
        "Java Developer": ["What is Java?", "OOP?", "JVM?", "JDK vs JRE?", "Spring?", "Threads?", "Project?", "Exception?", "JDBC?", "Collections?"],
        "Web Developer": ["HTML?", "CSS?", "JS?", "DOM?", "Flexbox?", "React?", "Responsive?", "Project?", "API?", "Hosting?"],
        "Data Analyst": ["SQL?", "Excel?", "Cleaning?", "Visualization?", "Power BI?", "Python?", "Project?", "Dashboard?", "Joins?", "Data mining?"],
        "Tester": ["Testing?", "Manual vs Auto?", "Test case?", "Bug life cycle?", "Selenium?", "Regression?", "Project?", "Unit test?", "Integration?", "Black box?"],
        "HR": ["HR role?", "Recruitment?", "Conflict?", "Leadership?", "Team?", "Engagement?", "Strength?", "Weakness?", "Why HR?", "Experience?"]
    }.get(role, [])

def get_personality_questions():
    return [
        "How do you handle stress?",
        "Team experience?",
        "Handling failure?",
        "Motivation?",
        "Time management?"
    ]

# -------------------------------
# 🤖 CHATBOT RESPONSE
# -------------------------------
def get_ai_response(msg):
    msg = msg.lower()

    if "skill" in msg:
        return "Focus on core technical skills, practice daily, and build projects."
    elif "interview" in msg:
        return "Practice mock interviews, improve communication, and prepare common questions."
    elif "resume" in msg:
        return "Keep your resume clear, add projects, and highlight your strengths."
    elif "job" in msg:
        return "Choose a role, learn required skills, and apply consistently."
    elif "improve" in msg:
        return "Identify weak areas and work on them regularly."
    elif "hello" in msg or "hi" in msg:
        return "Hello! 😊 How can I help you today?"
    else:
        return "Keep learning, practicing, and building projects to grow your career."

# -------------------------------
# 🌐 MENU
# -------------------------------
menu = st.sidebar.selectbox("Menu", [
    "Home",
    "Register",
    "Login",
    "Recruiter Access",
    "Candidate Dashboard",
    "Recruiter Dashboard",
    "Mock Interview",
    "AI Chatbot"
])

# Logout
if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.session_state.role = ""

# -------------------------------
# 🏠 HOME
# -------------------------------
if menu == "Home":
    set_bg("#4facfe","#00f2fe")
    st.title("💼 Smart Hiring System")

# -------------------------------
# 📝 REGISTER
# -------------------------------
elif menu == "Register":
    set_bg("#43e97b","#38f9d7")
    u=st.text_input("Username")
    p=st.text_input("Password",type="password")

    if st.button("Register"):
        u=u.lower().strip()
        users[u]=p
        save_data(users,"users.json")
        st.success("Registered Successfully")

# -------------------------------
# 🔐 LOGIN
# -------------------------------
elif menu == "Login":
    set_bg("#fa709a","#fee140")
    u=st.text_input("Username")
    p=st.text_input("Password",type="password")

    if st.button("Login"):
        u=u.lower().strip()
        if u in users and users[u]==p:
            st.session_state.logged_in=True
            st.session_state.role="candidate"
            st.success("Login Successful")
        else:
            st.error("Invalid Credentials")

# -------------------------------
# 👨‍💼 RECRUITER ACCESS
# -------------------------------
elif menu == "Recruiter Access":
    set_bg("#30cfd0","#330867")
    if st.button("Enter Recruiter Dashboard"):
        st.session_state.logged_in=True
        st.session_state.role="recruiter"

# -------------------------------
# 👩‍🎓 CANDIDATE DASHBOARD
# -------------------------------
elif menu == "Candidate Dashboard":
    set_bg("#667eea","#764ba2")

    if st.session_state.role!="candidate":
        st.warning("Login first")
    else:
        role=st.selectbox("Job Role",list(job_roles.keys()))
        file=st.file_uploader("Upload Resume",type="pdf")

        if st.button("Analyze"):
            text=extract_text_from_pdf(file)
            skills=extract_skills(text)

            matched,missing,score=match_skills(skills,job_roles[role])

            st.write("Score:",score)
            st.progress(int(score))

            df=pd.DataFrame({
                "Role":[role],
                "Score":[score],
                "Required":[", ".join(job_roles[role])],
                "Matched":[", ".join(matched)],
                "Missing":[", ".join(missing)]
            })

            st.dataframe(df)

            csv=df.to_csv(index=False)
            st.download_button("Download Score Sheet",csv,"candidate_score.csv")

# -------------------------------
# 👨‍💼 RECRUITER DASHBOARD
# -------------------------------
elif menu == "Recruiter Dashboard":
    set_bg("#ff9a9e","#fad0c4")

    if st.session_state.role!="recruiter":
        st.warning("Access recruiter")
    else:
        role=st.text_input("Job Role")
        skills=st.text_input("Skills (comma separated)")
        req=[s.strip().lower() for s in skills.split(",") if s]

        files=st.file_uploader("Upload Resumes",type="pdf",accept_multiple_files=True)

        if st.button("Analyze"):
            data=[]
            for f in files:
                text=extract_text_from_pdf(f)
                skills=extract_skills(text)
                m,miss,score=match_skills(skills,req)

                data.append({
                    "Candidate":f.name,
                    "Score":score,
                    "Required":", ".join(req),
                    "Matched":", ".join(m),
                    "Missing":", ".join(miss)
                })

            df=pd.DataFrame(data)
            st.dataframe(df)

            st.download_button("Download",df.to_csv(index=False),"scores.csv")

# -------------------------------
# 🎤 MOCK INTERVIEW (2 STEP)
# -------------------------------
elif menu == "Mock Interview":
    set_bg("#a18cd1","#fbc2eb")

    role=st.selectbox("Role",list(job_roles.keys()))

    if st.session_state.interview_stage==1:
        st.subheader("Technical Round")

        for i,q in enumerate(get_questions(role)):
            st.text_area(q,key=f"t{i}")

        if st.button("Next"):
            st.session_state.interview_stage=2

    else:
        st.subheader("Personality Round")

        for i,q in enumerate(get_personality_questions()):
            st.text_area(q,key=f"p{i}")

        if st.button("Submit"):
            score=random.randint(50,100)
            st.write("Final Score:",score)
            st.progress(score)

            st.write("Suggestions:")
            st.write("- Improve technical knowledge")
            st.write("- Improve communication")
            st.write("- Practice more")

            st.session_state.interview_stage=1

# -------------------------------
# 🤖 AI CHATBOT
# -------------------------------
elif menu == "AI Chatbot":
    set_bg("#84fab0","#8fd3f4")

    st.header("🤖 AI Career Assistant")

    file=st.file_uploader("Upload Score Sheet (Optional)",type=["csv"])

    if file:
        df=pd.read_csv(file)
        st.dataframe(df)

        avg=df["Score"].mean()

        if avg>70:
            st.success("You are job-ready 🎯")
        elif avg>=40:
            st.warning("Need improvement ⚠️")
        else:
            st.error("Need strong preparation ❗")

    st.subheader("💬 Chat with AI")

    user_input=st.text_input("Ask your question")

    if st.button("Send"):
        response=get_ai_response(user_input)

        st.session_state.chat_history.append(("You",user_input))
        st.session_state.chat_history.append(("AI",response))

    for sender,msg in st.session_state.chat_history:
        if sender=="You":
            st.markdown(f"**🧑 You:** {msg}")
        else:
            st.markdown(f"**🤖 AI:** {msg}")
