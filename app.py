import streamlit as st
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="Gradify - GPA Calculator",
    page_icon="🎓",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .gpa-result {
        background-color: #f0f8ff;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
        margin: 1rem 0;
    }
    .subject-table {
        background-color: #f9f9f9;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Header
    st.markdown('<h1 class="main-header">🎓 Gradify - GPA & CGPA Calculator</h1>', unsafe_allow_html=True)
    st.write("Calculate your GPA and CGPA")
    
    # Sidebar with information
    with st.sidebar:
        st.header("ℹ️ About")
        st.write("""
        This app calculates GPA and CGPA based on the DS grading system.
        
        **Grading Scale:**
        - A: 85-100 (4.0)
        - A-: 80-84 (3.7)
        - B+: 75-79 (3.3)
        - B: 70-74 (3.0)
        - C+: 65-69 (2.7)
        - C: 60-64 (2.3)
        - D+: 55-59 (2.0)
        - D: 50-54 (1.7)
        - F: Below 50 (0.0)
        """)
        
        st.header("📊 Instructions")
        st.write("""
        1. Enter number of subjects
        2. Input marks and credit hours
        3. View GPA calculation
        4. Add previous record for CGPA
        """)
    
    # Main content
    tab1, tab2, tab3 = st.tabs(["📝 Enter Marks", "📊 GPA Calculation", "🎯 CGPA Calculation"])
    
    with tab1:
        st.header("Enter Your Marks")
        
        # Input: number of subjects
        num_subjects = st.number_input(
            "Number of subjects:", 
            min_value=1, 
            max_value=20, 
            step=1,
            help="Enter the total number of subjects in this semester"
        )
        
        # Initialize session state for subjects
        if 'subjects_data' not in st.session_state:
            st.session_state.subjects_data = []
        
        subjects_data = []
        
        # Create input form for each subject
        st.markdown("### Subject Details")
        for i in range(num_subjects):
            st.markdown(f"#### Subject {i+1}")
            col1, col2, col3 = st.columns([2, 1, 1])
            
            with col1:
                subject_name = st.text_input(f"Subject Name", value=f"Subject {i+1}", key=f"name{i}")
            
            with col2:
                marks = st.number_input(
                    f"Marks (0-100)", 
                    min_value=0, 
                    max_value=100, 
                    value=70,
                    key=f"marks{i}"
                )
            
            with col3:
                credit_hours = st.number_input(
                    f"Credit Hours", 
                    min_value=0.5, 
                    max_value=5.0, 
                    value=3.0, 
                    step=0.5,
                    key=f"credit{i}"
                )
            
            subjects_data.append({
                'name': subject_name,
                'marks': marks,
                'credits': credit_hours
            })
        
        st.session_state.subjects_data = subjects_data
    
    with tab2:
        st.header("GPA Calculation")
        
        if 'subjects_data' in st.session_state and st.session_state.subjects_data:
            # Grade point conversion function (DS Grading System)
            def get_grade_point(mark):
                if mark >= 85:
                    return 4.0, "A"
                elif mark >= 80:
                    return 3.7, "A-"
                elif mark >= 75:
                    return 3.3, "B+"
                elif mark >= 70:
                    return 3.0, "B"
                elif mark >= 65:
                    return 2.7, "C+"
                elif mark >= 60:
                    return 2.3, "C"
                elif mark >= 55:
                    return 2.0, "D+"
                elif mark >= 50:
                    return 1.7, "D"
                else:
                    return 0.0, "F"
            
            # Calculate GPA
            total_quality_points = 0
            total_credit_hours = 0
            
            results_data = []
            
            for subject in st.session_state.subjects_data:
                grade_point, letter_grade = get_grade_point(subject['marks'])
                quality_points = grade_point * subject['credits']
                
                total_quality_points += quality_points
                total_credit_hours += subject['credits']
                
                results_data.append({
                    'Subject': subject['name'],
                    'Marks': subject['marks'],
                    'Credit Hours': subject['credits'],
                    'Grade': letter_grade,
                    'Grade Points': grade_point,
                    'Quality Points': round(quality_points, 2)
                })
            
            # Calculate GPA
            if total_credit_hours > 0:
                gpa = total_quality_points / total_credit_hours
                
                # Display results in a table
                st.markdown("### 📋 Results Summary")
                df_results = pd.DataFrame(results_data)
                st.dataframe(df_results, use_container_width=True)
                
                # Display GPA
                st.markdown("### 🎓 GPA Result")
                st.markdown(f"""
                <div class="gpa-result">
                    <h3 style="margin:0; color: #1f77b4;">Your GPA: {gpa:.2f}/4.0</h3>
                    <p style="margin:0.5rem 0 0 0;">Total Credit Hours: {total_credit_hours}</p>
                    <p style="margin:0;">Total Quality Points: {total_quality_points:.2f}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Performance message
                if gpa >= 3.7:
                    st.success("🎉 Excellent Performance! Keep up the great work!")
                elif gpa >= 3.0:
                    st.info("👍 Good Performance! You're doing well!")
                elif gpa >= 2.0:
                    st.warning("💪 Satisfactory Performance! Room for improvement.")
                else:
                    st.error("📚 Needs Improvement! Consider seeking academic support.")
                
                # Store GPA for CGPA calculation
                st.session_state.current_gpa = gpa
                st.session_state.current_credits = total_credit_hours
                
            else:
                st.error("Please enter at least one subject with credit hours.")
        else:
            st.info("👆 Please go to the 'Enter Marks' tab and add your subjects first.")
    
    with tab3:
        st.header("CGPA Calculation")
        
        st.write("Calculate your Cumulative GPA by including previous academic records.")
        
        col1, col2 = st.columns(2)
        
        with col1:
            prev_cgpa = st.number_input(
                "Previous CGPA:",
                min_value=0.0,
                max_value=4.0,
                value=3.0,
                step=0.01,
                help="Your CGPA from previous semesters"
            )
        
        with col2:
            prev_credits = st.number_input(
                "Previous Total Credit Hours:",
                min_value=0.0,
                value=60.0,
                step=1.0,
                help="Total credit hours completed before this semester"
            )
        
        if st.button("Calculate CGPA", type="primary"):
            if 'current_gpa' in st.session_state and 'current_credits' in st.session_state:
                current_gpa = st.session_state.current_gpa
                current_credits = st.session_state.current_credits
                
                if prev_credits > 0:
                    # Calculate CGPA
                    total_quality_points = (prev_cgpa * prev_credits) + (current_gpa * current_credits)
                    total_combined_credits = prev_credits + current_credits
                    cgpa = total_quality_points / total_combined_credits
                    
                    st.markdown("### 📈 CGPA Result")
                    st.markdown(f"""
                    <div class="gpa-result">
                        <h3 style="margin:0; color: #1f77b4;">Your Updated CGPA: {cgpa:.2f}/4.0</h3>
                        <p style="margin:0.5rem 0 0 0;">Previous CGPA: {prev_cgpa:.2f}</p>
                        <p style="margin:0;">Current Semester GPA: {current_gpa:.2f}</p>
                        <p style="margin:0;">Previous Credits: {prev_credits}</p>
                        <p style="margin:0;">Current Credits: {current_credits}</p>
                        <p style="margin:0;">Total Credits: {total_combined_credits}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Progress comparison
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Previous CGPA", f"{prev_cgpa:.2f}")
                    with col2:
                        st.metric("Updated CGPA", f"{cgpa:.2f}", 
                                 delta=f"{cgpa - prev_cgpa:+.2f}")
                        
                else:
                    st.info("Enter your previous CGPA and total credit hours to calculate your updated CGPA.")
            else:
                st.warning("Please calculate your current GPA first in the 'GPA Calculation' tab.")

if __name__ == "__main__":
    main()
