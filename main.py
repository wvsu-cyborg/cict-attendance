# main.py

import streamlit as st

def main():
    st.title("Online Attendance System")

    option = st.selectbox("Select a side", ("Admin", "Viewer"))

    if option == "Admin":
        import admin
        admin.admin_app()
    elif option == "Viewer":
        import viewer
        viewer.viewer_app()

if __name__ == "__main__":
    main()
