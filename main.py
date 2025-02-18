import streamlit as st
import requests

BASE_URL = "https://kabirtiwari.pythonanywhere.com"

st.title("Attendance UI")

# URL for attendance details
url = f"{BASE_URL}/attendencedetails"
response = requests.get(url=url)
data = response.json()

if not data:
    st.info("No attendance data available.")
else:
    # Extract unique values for filters
    network_names = list(set(entry['networkName'] for entry in data))
    class_names = list(set(entry['classname'] for entry in data))
    dates = list(set(entry['date'] for entry in data))

    # Sidebar filters
    st.sidebar.header("Filters")
    selected_network = st.sidebar.selectbox("Select Network Name", ["All"] + network_names)
    selected_class = st.sidebar.selectbox("Select Class Name", ["All"] + class_names)
    selected_date = st.sidebar.selectbox("Select Date", ["All"] + dates)

    # Filter data based on selections
    filtered_data = [entry for entry in data if 
                     (selected_network == "All" or entry['networkName'] == selected_network) and
                     (selected_class == "All" or entry['classname'] == selected_class) and
                     (selected_date == "All" or entry['date'] == selected_date)]

    if not filtered_data:
        st.write("No matching records found.")
    else:
        # Create a table
        table_data = {
            "User ID": [entry['userid'] for entry in filtered_data],
            "Network Name": [entry['networkName'] for entry in filtered_data],
            "Class Name": [entry['classname'] for entry in filtered_data],
            "Date": [entry['date'] for entry in filtered_data],
            "First Name": [entry['firstName'] for entry in filtered_data],
            "Last Name": [entry['lastName'] for entry in filtered_data],
            "Checkin Time": [entry['checkinTime'] for entry in filtered_data]
        }

        # Display the dynamic table
        st.table(table_data)
