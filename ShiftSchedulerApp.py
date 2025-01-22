import streamlit as st
import pandas as pd


# Function to shift elements in a list to the right
def shift_right(lst):
    if not lst:  # Check if the list is empty
        return lst
    return [lst[-1]] + lst[:-1]


# Function to create the first row of the schedule
def get_first_row(days, shifts, days_per_person):
    count_days = 0
    distribution_list = []
    for i in range(days * shifts):
        if i % shifts == 0 and count_days < days_per_person:
            distribution_list.append(1)
            count_days += 1
        else:
            distribution_list.append(0)
    return distribution_list


# Streamlit app
st.title("Event Shift Scheduler")

# Input: List of names
names_input = st.text_area("Enter list of names (comma-separated):")
names = [name.strip() for name in names_input.split(",") if name.strip()]

# Input: Total number of days for the event
total_days = st.number_input("Total number of days for event:", min_value=1)

# Input: Number of shifts
num_shifts = st.number_input("Select number of shifts:", min_value=1)

# Input: Max number of participants per day
min_participants_per_day = st.number_input("Min number of participants per day:", min_value=1)

# Input: Maximum days per person
days_per_person = st.number_input("Max days per person:", min_value=1)

# Button to generate the schedule
if st.button("Generate Schedule"):
    # Generate the schedule using the shift-right mechanism
    first_row = get_first_row(total_days, num_shifts, days_per_person)
    schedule = [first_row]
    previous_row = first_row
    skip = False
    for i in range(1, len(names)):
        if skip:
            schedule.append(first_row)
            skip = False
            continue
        current_row = shift_right(previous_row)
        if current_row[-1] == 1:
            previous_row = first_row
            skip = True
        else:
            previous_row = current_row
        schedule.append(current_row)

    for s in schedule:
        print(s)
    # Convert the schedule to a DataFrame
    schedule_df = pd.DataFrame(schedule, index=names)
    schedule_df.columns = [f"Day {day + 1} Shift {shift + 1}" for day in range(total_days) for shift in range(num_shifts)]

    # Replace 1 with '✔' and 0 with 'x'
    schedule_df = schedule_df.replace({1: '✔', 0: 'x'})

    # Display the schedule table
    st.write("### Event Schedule")
    st.dataframe(schedule_df)
