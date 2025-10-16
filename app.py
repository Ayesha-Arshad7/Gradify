import streamlit as st
import pandas as pd

# --- Page Config ---
st.set_page_config(
    page_title="Gradify | GPA & CGPA Calculator",
    page_icon="🎓",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- Logo and Title ---
st.image("assets/gradify_logo.png", width=180)
st.markdown("<h1 style='text-align:center; color:#4B9CD3;'>🎓 Gradify</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; font-size:18px;'>Your smart GPA & CGPA calculator</p>", unsafe_allow_html=True)
st.write("---")

# --- Input Section ---
st.subheader("📘 Enter Your Marks")

num_subjects = st.number_input("How many subjects do you have?", min_value=1, max_value=20, value=5, step=1)

marks = []
for i in range(num_subjects):
    mark = st.number_input(f"Marks for Subject {i+1}:", min_value=0, max_value=100, value=75)
    marks.append(mark)

# --- GPA Calculation Function ---
def get_grade_point(mark):
    if mark >= 85: return 4.0
    elif mark >= 80: return 3.7
    elif mark >= 75: return 3.3
    elif mark >= 70: return 3.0
    elif mark >= 65: return 2.7
    elif mark >= 60: return 2.3
    elif mark >= 55: return 2.0
    elif mark >= 50: return 1.7
    else: return 0.0

# --- Calculate GPA Button ---
if st.button("✨ Calculate GPA"):
    grade_points = [get_grade_point(m) for m in marks]
    gpa = sum(grade_points) / len(grade_points)
    st.success(f"🎯 Your GPA for this semester: **{gpa:.2f}**")

    # --- Optional CGPA Section ---
    st.write("---")
    st.subheader("📊 Calculate Your CGPA")

    total_semesters = st.number_input("Enter total semesters completed:", min_value=1, max_value=12, value=1)
    if total_semesters > 1:
        total_gpa = []
        for i in range(total_semesters):
            sem_gpa = st.number_input(f"GPA for Semester {i+1}:", min_value=0.0, max_value=4.0, value=gpa)
            total_gpa.append(sem_gpa)
        cgpa = sum(total_gpa) / len(total_gpa)
        st.success(f"🏆 Your CGPA: **{cgpa:.2f}**")

# --- Footer ---
st.write("---")
st.markdown(
    """
    <div style='text-align:center;'>
        <p style='font-size:15px;'>Made with ❤️ by <b>Ayesha Arshad</b></p>
        <p style='font-size:13px; color:gray;'>© 2025 Gradify | All rights reserved</p>
    </div>
    """,
    unsafe_allow_html=True
)
