import streamlit as st

def calculate_tlr(student_strength, faculty_quality, learning_resources, financial_support):
    """
    Calculate Teaching, Learning & Resources (TLR) based on sub-parameters.
    """
    return (0.4 * student_strength +
            0.3 * faculty_quality +
            0.2 * learning_resources +
            0.1 * financial_support)

def calculate_rp(research_papers, patents, funded_projects, phd_students):
    """
    Calculate Research and Professional Practice (RP) based on sub-parameters.
    """
    return (0.4 * research_papers +
            0.2 * patents +
            0.2 * funded_projects +
            0.2 * phd_students)

def calculate_go(placement_rate, higher_studies, median_salary, entrepreneurship):
    """
    Calculate Graduation Outcomes (GO) based on sub-parameters.
    """
    return (0.4 * placement_rate +
            0.2 * higher_studies +
            0.3 * median_salary +
            0.1 * entrepreneurship)

def calculate_oi(regional_diversity, gender_diversity, economic_diversity, facilities_access):
    """
    Calculate Outreach and Inclusivity (OI) based on sub-parameters.
    """
    return (0.3 * regional_diversity +
            0.3 * gender_diversity +
            0.2 * economic_diversity +
            0.2 * facilities_access)

def calculate_nirf_score(tlr, rp, go, oi, pp, weights):
    """
    Calculate the NIRF score based on the inputs and weights.
    """
    return (tlr * weights["TLR"] +
            rp * weights["RP"] +
            go * weights["GO"] +
            oi * weights["OI"] +
            pp * weights["Peer Perception"])

def nirf_score_calc():
    st.title("Calculate Overall Score")
 
    institute_type = st.selectbox(
        "Select the type of institute",
        ["Universities", "Engineering Institutions", "Management Institutions", "Medical Colleges", "Law Colleges", "Colleges", "Architecture Institutions", "Pharmacy Institutions", "Dental Colleges"]
    )
 
    weightages = {
        "Universities": {"TLR": 0.30, "RP": 0.30, "GO": 0.20, "OI": 0.10, "Peer Perception": 0.10},
        "Engineering Institutions": {"TLR": 0.30, "RP": 0.30, "GO": 0.20, "OI": 0.10, "Peer Perception": 0.10},
        "Management Institutions": {"TLR": 0.30, "RP": 0.25, "GO": 0.25, "OI": 0.10, "Peer Perception": 0.10},
        "Medical Colleges": {"TLR": 0.30, "RP": 0.30, "GO": 0.20, "OI": 0.10, "Peer Perception": 0.10},
        "Law Colleges": {"TLR": 0.30, "RP": 0.20, "GO": 0.25, "OI": 0.15, "Peer Perception": 0.10},
        "Colleges": {"TLR": 0.40, "RP": 0.15, "GO": 0.25, "OI": 0.10, "Peer Perception": 0.10},
        "Architecture Institutions": {"TLR": 0.30, "RP": 0.20, "GO": 0.25, "OI": 0.15, "Peer Perception": 0.10},
        "Pharmacy Institutions": {"TLR": 0.30, "RP": 0.30, "GO": 0.20, "OI": 0.10, "Peer Perception": 0.10},
        "Dental Colleges": {"TLR": 0.30, "RP": 0.20, "GO": 0.25, "OI": 0.15, "Peer Perception": 0.10}
    }

    # Collect inputs for NIRF calculations
    student_strength = st.number_input("Enter Student Strength (0-100):", min_value=0.0, max_value=100.0, step=0.1, value=90.0)
    faculty_quality = st.number_input("Enter Faculty Quality (0-100):", min_value=0.0, max_value=100.0, step=0.1, value=85.0)
    learning_resources = st.number_input("Enter Learning Resources (0-100):", min_value=0.0, max_value=100.0, step=0.1, value=80.0)
    financial_support = st.number_input("Enter Financial Support (0-100):", min_value=0.0, max_value=100.0, step=0.1, value=75.0)

    research_papers = st.number_input("Enter Research Papers Published (0-100):", min_value=0.0, max_value=100.0, step=0.1, value=70.0)
    patents = st.number_input("Enter Patents Filed/Granted (0-100):", min_value=0.0, max_value=100.0, step=0.1, value=65.0)
    funded_projects = st.number_input("Enter Funded Projects (0-100):", min_value=0.0, max_value=100.0, step=0.1, value=60.0)
    phd_students = st.number_input("Enter PhD Students Graduated (0-100):", min_value=0.0, max_value=100.0, step=0.1, value=55.0)

    placement_rate = st.number_input("Enter Placement Rate (0-100):", min_value=0.0, max_value=100.0, step=0.1, value=88.0)
    higher_studies = st.number_input("Enter Students Opting for Higher Studies (0-100):", min_value=0.0, max_value=100.0, step=0.1, value=75.0)
    median_salary = st.number_input("Enter Median Salary (0-100):", min_value=0.0, max_value=100.0, step=0.1, value=85.0)
    entrepreneurship = st.number_input("Enter Entrepreneurship Success Rate (0-100):", min_value=0.0, max_value=100.0, step=0.1, value=70.0)

    regional_diversity = st.number_input("Enter Regional Diversity (0-100):", min_value=0.0, max_value=100.0, step=0.1, value=78.0)
    gender_diversity = st.number_input("Enter Gender Diversity (0-100):", min_value=0.0, max_value=100.0, step=0.1, value=72.0)
    economic_diversity = st.number_input("Enter Economic Diversity (0-100):", min_value=0.0, max_value=100.0, step=0.1, value=70.0)
    facilities_access = st.number_input("Enter Facilities Access (0-100):", min_value=0.0, max_value=100.0, step=0.1, value=65.0)

    pp = st.number_input("Enter Peer Perception score (0-100):", min_value=0.0, max_value=100.0, step=0.1, value=75.0)

    # Ensure that the calculation is triggered only when the "Submit" button is clicked
    if st.button("Submit"):
        # Calculate the sub-scores
        tlr = calculate_tlr(student_strength, faculty_quality, learning_resources, financial_support)
        rp = calculate_rp(research_papers, patents, funded_projects, phd_students)
        go = calculate_go(placement_rate, higher_studies, median_salary, entrepreneurship)
        oi = calculate_oi(regional_diversity, gender_diversity, economic_diversity, facilities_access)

        # Calculate the final NIRF score
        overall_score = calculate_nirf_score(tlr, rp, go, oi, pp, weightages[institute_type])
        st.success(f"The overall NIRF score for {institute_type} is: {overall_score:.2f}")

