from fpdf import FPDF
import streamlit as st
import datetime
from PIL import Image
import random

# ---------------------- App Configuration ----------------------
st.set_page_config(
    page_title="🌱 Growth Mindset Challenge",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------- Helper Functions ----------------------
def motivational_quotes():
    quotes = [
        "Believe you can and you're halfway there.",
        "Mistakes are proof that you are trying.",
        "Growth is never by mere chance; it is the result of forces working together.",
        "Success is the ability to go from one failure to another with no loss of enthusiasm.",
        "Don't watch the clock; do what it does. Keep going.",
        "Your potential is endless.",
        "💪 Push your limits every single day.",
        "🌟 Great things never come from comfort zones.",
        "🚀 Every day is a chance to get better.",
        "🌈 Embrace challenges; they are opportunities in disguise."
    ]
    return random.choice(quotes)

def save_reflection(user_name, profession, reflection_text, goals):
    filename = f"{user_name}_{profession}_reflection.txt"
    with open(filename, "a") as f:
        f.write(f"{datetime.date.today()} - {profession}: {reflection_text}\nGoals for Tomorrow: {goals}\n---\n")

def generate_pdf(user_name, profession, reflection_text, goals):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt=f"Reflection Journal - {user_name} ({profession})", ln=1, align='C')
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, txt=f"Date: {datetime.date.today()}", ln=1)
    pdf.multi_cell(0, 10, reflection_text)
    pdf.ln(5)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, txt="Goals for Tomorrow:", ln=1)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, goals)
    pdf.output(f"{user_name}_{profession}_Reflection.pdf")

def random_growth_tips():
    tips = [
        "💡 Set small, achievable learning goals.",
        "🔄 Reflect daily on your progress.",
        "🤔 Ask questions when stuck.",
        "🎯 Challenge yourself with new tasks.",
        "📚 Read about successful growth stories.",
        "🤝 Collaborate and learn with peers.",
        "🕒 Dedicate time daily to self-improvement.",
        "🔥 Stay consistent; small steps lead to big results.",
        "🌟 Visualize your success and work towards it."
    ]
    return random.choice(tips)

# ---------------------- Sidebar ----------------------
st.sidebar.title("🚀 Growth Mindset Journey")
user_name = st.sidebar.text_input("🙋 Enter Your Name:")
profession = st.sidebar.text_input("💼 Enter Your Profession (e.g., Web Developer):")

dark_mode_css = """
    <style>
    body {background-color: #333; color: #fff;}
    .stTextInput > div > div > input {background-color: #444; color: #fff;}
    .stButton button {background-color: #555; color: #fff; border: none;}
    .stProgress > div > div {background-color: #6c6;} 
    </style>
"""

if not user_name or not profession:
    st.warning("⚠️ Please enter your name and profession to continue.")
    st.stop()

mode = st.sidebar.radio("🌞🌚 Choose Mode:", ["Light", "Dark"])
if mode == "Dark":
    st.markdown(dark_mode_css, unsafe_allow_html=True)

if st.sidebar.button("✨ Get Motivational Quote"):
    st.sidebar.success(motivational_quotes())

if st.sidebar.button("💡 Random Growth Tip"):
    st.sidebar.info(random_growth_tips())

# ---------------------- Main Content ----------------------
st.title(f"🌱 Welcome {user_name} ({profession}) to Your Growth Mindset Challenge!")

# Section 1: Progress Tracker
st.subheader("📈 Daily Progress Tracker")
challenge_list = [
    "✅ 1 hour of focused study",
    "📝 Reflection on today's learning",
    "🤝 Helped a peer",
    "🎥 Watched a growth mindset video",
    "🧩 Tried a new problem-solving approach",
    "📖 Read at least 10 pages of a book",
    "🌐 Explored new learning resources",
    "🗣️ Shared knowledge with someone"
]

daily_progress = 0
for task in challenge_list:
    if st.checkbox(task, key=task):
        daily_progress += 1

progress_percentage = daily_progress / len(challenge_list)
progress_text = f"Progress: {int(progress_percentage * 100)}% Complete"
st.progress(progress_percentage, text=progress_text)

# Section 2: Streak Count
st.subheader("🔥 Your Growth Streak")
if "streak" not in st.session_state:
    st.session_state.streak = 0

if daily_progress == len(challenge_list):
    st.session_state.streak += 1
else:
    st.session_state.streak = 0

st.metric(label="Current Streak (days)", value=f"{st.session_state.streak} 🔥")

# Section 3: Reflection Journal with Tomorrow's Goals
st.subheader("📝 Reflection Journal & Tomorrow's Goals")
reflection_input = st.text_area("Write your daily reflection:", placeholder="What did you learn today?")
goals_input = st.text_area("Set goals for tomorrow:", placeholder="What do you plan to achieve tomorrow?")
if st.button("💾 Save & Download PDF"):
    if reflection_input and goals_input:
        save_reflection(user_name, profession, reflection_input, goals_input)
        generate_pdf(user_name, profession, reflection_input, goals_input)
        st.success(f"Reflection & Goals saved & PDF generated for {user_name} ({profession})!")
        with open(f"{user_name}_{profession}_Reflection.pdf", "rb") as f:
            st.download_button("📥 Download Your Reflection as PDF", data=f, file_name=f"{user_name}_{profession}_Reflection.pdf")
    else:
        st.error("⚠️ Please complete both reflection and goals fields before saving.")

# Section 4: Growth Mindset Quiz (Updated with Instant Feedback)
st.subheader("🎯 Growth Mindset Quiz with Feedback")
quiz_score = 0
questions = [
    ("Q1: What should you do when you make a mistake?", ["Ignore it", "Learn from it", "Give up", "Blame others"], "Learn from it"),
    ("Q2: Growth mindset believes abilities are:", ["Fixed", "Developable", "Inherited", "Random"], "Developable"),
    ("Q3: Which action shows a growth mindset?", ["Giving up", "Avoiding feedback", "Learning from failure", "Blaming others"], "Learning from failure"),
    ("Q4: What is the best way to improve a skill?", ["Practice regularly", "Avoid challenges", "Rely on talent only", "Never seek feedback"], "Practice regularly"),
    ("Q5: What should you do when faced with a tough challenge?", ["Give up", "Seek help and keep trying", "Blame others", "Ignore it"], "Seek help and keep trying"),
    ("Q6: How can feedback help you grow?", ["It doesn't help", "It shows your weaknesses", "It guides you to improve", "It lowers confidence"], "It guides you to improve")
]

for idx, (q, options, correct) in enumerate(questions):
    answer = st.radio(q, options, key=f"quiz_{idx}")
    if answer:
        if answer == correct:
            st.success("✅ Correct!")
            quiz_score += 1
        else:
            st.error(f"❌ Incorrect. The correct answer is: {correct}")

if st.button("✅ Finalize Quiz Score"):
    st.success(f"🏆 {user_name} ({profession}), Your Final Quiz Score: {quiz_score}/{len(questions)}")

# Section 5: Leaderboard with Persistent Data
st.subheader("🏆 Leaderboard")
leaderboard = {"Ayesha": 85, "Ali": 90, "Fatima": 78, "Ahmed": 92, user_name: random.randint(80, 100)}
st.table(sorted(leaderboard.items(), key=lambda x: x[1], reverse=True))

# Section 6: Motivational Video
st.subheader("🎬 Daily Motivational Video")
st.video("https://www.youtube.com/watch?v=75GFzikmRY0")

# Footer
st.markdown("""
---
🌟 *"Believe in your infinite potential. Your only limitations are those you set upon yourself."* 🌟

✨ *App built with Streamlit. Deploy on Streamlit Community Cloud & share link.* 🚀
""")