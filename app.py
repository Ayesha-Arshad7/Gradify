import streamlit as st

st.set_page_config(page_title="Gradify", page_icon="🎓", layout="centered")

st.title("🎓 Gradify – GPA & CGPA Calculator")
st.write("Enter your marks and credit hours for each subject below:")

# Input: number of subjects
num_subjects = st.number_input("Number of subjects:", min_value=1, max_value=20, step=1)

marks = []
credits = []

# Get marks and credit hours for each subject
for i in range(num_subjects):
    col1, col2 = st.columns(2)
    with col1:
        mark = st.number_input(f"Marks for Subject {i+1} (0–100):", min_value=0, max_value=100, step=1, key=f"mark{i}")
    with col2:
        credit = st.number_input(f"Credit Hours for Subject {i+1}:", min_value=1.0, max_value=4.0, step=0.5, key=f"credit{i}")
    marks.append(mark)
    credits.append(credit)

# Grade point conversion
def grade_point(mark):
    if mark >= 85:
        return 4.0
    elif mark >= 80:
        return 3.7
    elif mark >= 75:
        return 3.3
    elif mark >= 70:
        return 3.0
    elif mark >= 65:
        return 2.7
    elif mark >= 60:
        return 2.3
    elif mark >= 55:
        return 2.0
    elif mark >= 50:
        return 1.7
    else:
        return 0.0

st.divider()
st.subheader("📘 Previous Academic Record")
prev_cgpa = st.number_input("Enter your previous CGPA:", min_value=0.0, max_value=4.0, step=0.01)
prev_credits = st.number_input("Enter total completed credit hours before this semester:", min_value=0.0, step=1.0)

st.divider()

if st.button("Calculate GPA & CGPA"):
    # GPA Calculation
    total_points = sum([grade_point(m) * c for m, c in zip(marks, credits)])
    total_credits = sum(credits)
    gpa = total_points / total_credits if total_credits > 0 else 0.0

    st.success(f"✅ GPA for this semester: **{gpa:.2f}**")

    # CGPA Calculation
    if prev_credits > 0:
        total_quality_points = (prev_cgpa * prev_credits) + (gpa * total_credits)
        total_combined_credits = prev_credits + total_credits
        cgpa = total_quality_points / total_combined_credits
        st.success(f"🎯 Updated CGPA: **{cgpa:.2f}**")
    else:
        st.info("Enter your previous CGPA and total credit hours to calculate your updated CGPA.")
