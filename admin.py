# admin.py

import streamlit as st
from firebase_config import get_db_reference
import datetime

def admin_app():
    st.title("Admin Login")

    # Admin credentials
    admin_username = "cyborg"
    admin_password = "cyborg123"

    # Input fields for admin credentials
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    # Login button
    if st.button("Login"):
        if username == admin_username and password == admin_password:
            st.success("Login successful!")
            st.write("Navigating to Admin Dashboard...")
            show_admin_dashboard()
        else:
            st.error("Invalid credentials")

def show_admin_dashboard():
    st.title("Admin Dashboard")

    # Input field for student ID
    student_id = st.text_input("Enter Student ID")

    # Submit button
    if st.button("Submit"):
        st.write("Submit button pressed")

        # Try Firebase connection and query
        try:
            db_ref = get_db_reference()
            st.write("Connected to Firebase")

            # Query the student data using the provided student ID
            st.write(f"Looking for student ID: {student_id}")
            student_data = db_ref.child('students').order_by_child('ID').equal_to(student_id).get()

            # Check if we got any results
            if student_data:
                st.write("Student data found")
                student_data = list(student_data.values())[0]

                # Display student information
                st.write("Student Information:")
                st.write(f"Name: {student_data.get('Name')}")
                st.write(f"Program: {student_data.get('Program')}")
                st.write(f"Section: {student_data.get('Section')}")
                st.success("Attendance confirmed.")

                # Save the attendance record without the student ID
                save_attendance(student_data)
            else:
                st.error("Student ID not found")
                st.write("No student data returned from Firebase")

        except Exception as e:
            st.error(f"Error accessing Firebase: {str(e)}")
            st.write("Debug info:", e)

# Function to save attendance
def save_attendance(student_data):
    try:
        db_ref = get_db_reference()
        now = datetime.datetime.now().isoformat()

        # Check data being saved
        st.write("Saving attendance record", student_data)

        # Push attendance record into the attendance_records collection
        attendance_ref = db_ref.child('attendance_records').push({
            'Name': student_data['Name'],
            'Program': student_data['Program'],
            'Section': student_data['Section'],
            'Timestamp': now,
            'recordId': db_ref.child('attendance_records').push().key
        })

        st.success("Attendance saved successfully.")

    except Exception as e:
        st.error(f"Error saving attendance: {str(e)}")
        st.write("Detailed error:", e)
