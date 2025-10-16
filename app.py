import streamlit as st

st.set_page_config(page_title="Gradify - GPA & CGPA Calculator", page_icon="🎓")

st.title("🎓 Gradify: GPA & CGPA Calculator")

st.write("Enter your subject marks to calculate your GPA and CGPA easily!")

num_subjects = st.number_input("Enter number of subjects:", min_value=1, max_value=20, step=1)

marks = []
total_grade_points = 0
total_credit_hours = 0

grade_scale = {
    (85, 100): (4.0, "A"),
    (80, 84): (3.7, "A-"),
    (75, 79): (3.3, "B+"),
    (70, 74): (3.0, "B"),
    (65, 69): (2.7, "B-"),
    (61, 64): (2.3, "C+"),
    (58, 60): (2.0, "C"),
    (55, 57): (1.7, "C-"),
    (50, 54): (1.0, "D"),
    (0, 49): (0.0, "F"),
}

st.subheader("Enter your marks and credit hours:")
for i in range(int(num_subjects)):
    col1, col2 = st.columns(2)
    with col1:
        mark = st.number_input(f"Marks for Subject {i+1}:", min_value=0, max_value=100, step=1)
    with col2:
        credit = st.number_input(f"Credit Hours for Subject {i+1}:", min_value=1, max_value=4, step=1)

    for (low, high), (gpa, grade) in grade_scale.items():
        if low <= mark <= high:
            marks.append((mark, gpa, grade, credit))
            total_grade_points += gpa * credit
            total_credit_hours += credit
            break

if total_credit_hours > 0:
    gpa = total_grade_points / total_credit_hours
    st.success
