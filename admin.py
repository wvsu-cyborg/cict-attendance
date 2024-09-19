# admin.py

import streamlit as st
from firebase_config import get_db_reference
import datetime

def admin_app():
    st.title("Admin Login")

    # Admin credentials
    admin_username = "cyborg"
    admin_password = "cyborg123"

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == admin_username and password == admin_password:
            st.success("Login successful!")
            show_admin_dashboard()
        else:
            st.error("Invalid credentials")

def show_admin_dashboard():
    st.title("Admin Dashboard")

    student_id = st.text_input("Enter Student ID")
    if st.button("Submit"):
        db_ref = get_db_reference()
        student_data = db_ref.child('students').order_by_child('ID').equal_to(student_id).get()

        if student_data:
            student_data = list(student_data.values())[0]
            st.write("Student Information:")
            st.write(f"Name: {student_data.get('Name')}")
            st.write(f"Program: {student_data.get('Program')}")
            st.write(f"Section: {student_data.get('Section')}")
            st.success("Attendance confirmed.")
            # Save attendance
            save_attendance(student_id, student_data)
        else:
            st.error("Student ID not found")

def save_attendance(student_id, student_data):
    db_ref = get_db_reference()
    now = datetime.datetime.now().isoformat()
    attendance_ref = db_ref.child('attendance_records').push({
        'Name': student_data['Name'],
        'Program': student_data['Program'],
        'Section': student_data['Section'],
        'Timestamp': now,
        'recordId': db_ref.child('attendance_records').push().key
    })
