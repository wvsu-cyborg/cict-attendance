# viewer.py

import streamlit as st
from firebase_config import get_db_reference

def viewer_app():
    st.title("Student Attendance Viewer")

    search_name = st.text_input("Search by Name")
    filter_program = st.selectbox("Filter by Program", ["All", "BLIS", "BSCS", "BSEMC", "BSIT"])
    filter_section = st.selectbox("Filter by Section", ["All", "A", "B"])

    if st.button("Search"):
        db_ref = get_db_reference()
        query = db_ref.child('students')
        
        if filter_program != "All":
            query = query.order_by_child('Program').equal_to(filter_program)
        if filter_section != "All":
            query = query.order_by_child('Section').equal_to(filter_section)
        
        results = query.get()
        
        if search_name:
            results = {k: v for k, v in results.items() if search_name.lower() in v.get('Name', '').lower()}

        if results:
            st.write("Student Attendance Records:")
            for student_id, data in results.items():
                st.write(f"Name: {data.get('Name')}")
                st.write(f"Program: {data.get('Program')}")
                st.write(f"Section: {data.get('Section')}")
                attendance = get_attendance(student_id)
                st.write(f"Attendance: {attendance}")
        else:
            st.write("No records found.")

def get_attendance(student_id):
    db_ref = get_db_reference()
    attendance_records = db_ref.child('attendance_records').order_by_child('Name').equal_to(
        db_ref.child('students').child(student_id).child('Name').get()).get()
    
    if attendance_records:
        attendance_list = [record['Timestamp'] for record in attendance_records.values()]
        return attendance_list
    return "No attendance records"
