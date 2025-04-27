import streamlit as st
import pandas as pd
from auth import get_current_user
from data_manager import (
    get_my_publications, get_my_experiences, 
    add_publication, add_experience, get_feedback_summary
)

def faculty_dashboard():
    user = get_current_user()
    
    st.header("Faculty Profile Dashboard")
    
    tabs = st.tabs(["My Publications", "My Experience", "Feedback Summary"])
    
    # My Publications Tab
    with tabs[0]:
        st.write("### My Publications")
        publications = get_my_publications(user['username'])
        
        if not publications:
            st.info("You have not added any publications yet.")
        else:
            pub_df = pd.DataFrame(publications)
            pub_df = pub_df[['title', 'journal', 'year', 'doi']]
            st.dataframe(pub_df, use_container_width=True)
        
        st.write("### Add New Publication")
        
        with st.form("add_publication_form"):
            title = st.text_input("Title")
            journal = st.text_input("Journal Name")
            year = st.number_input("Year", min_value=1900, max_value=2100, value=2024)
            doi = st.text_input("DOI (Optional)")
            
            submit_pub = st.form_submit_button("Add Publication")
            
            if submit_pub:
                success, message = add_publication(
                    user['username'], title, journal, year, doi
                )
                if success:
                    st.success(message)
                    st.rerun()
                else:
                    st.error(message)
    
    # My Experience Tab
    with tabs[1]:
        st.write("### My Experiences")
        experiences = get_my_experiences(user['username'])
        
        if not experiences:
            st.info("You have not added any experiences yet.")
        else:
            for exp in experiences:
                with st.expander(f"{exp['role']} at {exp['institution']}", expanded=False):
                    st.write(f"**Duration:** {exp['duration']}")
                    st.write(f"**Description:** {exp['description']}")
        
        st.write("### Add New Experience")
        
        with st.form("add_experience_form"):
            institution = st.text_input("Institution Name")
            role = st.text_input("Role/Position")
            duration = st.text_input("Duration (e.g., 2018-2022)")
            description = st.text_area("Description")
            
            submit_exp = st.form_submit_button("Add Experience")
            
            if submit_exp:
                success, message = add_experience(
                    user['username'], institution, role, duration, description
                )
                if success:
                    st.success(message)
                    st.rerun()
                else:
                    st.error(message)
    
    # Feedback Summary Tab
    with tabs[2]:
        st.write("### Feedback Summary")
        feedback_summary = get_feedback_summary(user['username'])
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Average Rating", f"{feedback_summary['avg_rating']} / 5.0")
        with col2:
            st.metric("From Students", feedback_summary['student_count'])
        with col3:
            st.metric("From Dean", feedback_summary['dean_count'])
        
        st.write("### Comments Received")
        comments = feedback_summary['comments']
        
        if not comments:
            st.info("No comments received yet.")
        else:
            for comment in comments:
                with st.expander(f"Comment ({comment['semester']})", expanded=False):
                    st.write(f"**Rating:** {comment['rating']} / 5.0")
                    st.write(comment['comment'])
