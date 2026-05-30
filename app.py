import streamlit as st
import pandas as pd

DATA_FILE = "programs.csv"

# --- Load CSV ---
try:
    df = pd.read_csv(DATA_FILE)
except FileNotFoundError:
    df = pd.DataFrame(columns=[
        "Country", "University", "Program", "Level", "Field", "Funding",
        "Deadline", "IELTS", "GPA", "Application Status", "Email", "Link",
        "Notes", "Verified", "Deadline Status"
    ])

# --- Sidebar Inputs ---
st.sidebar.header("Add New Program")
country = st.sidebar.text_input("Country")
university = st.sidebar.text_input("University")
program = st.sidebar.text_input("Program")
level = st.sidebar.text_input("Level")
field = st.sidebar.text_input("Field")
funding = st.sidebar.text_input("Funding")
deadline = st.sidebar.text_input("Deadline")
ielts = st.sidebar.text_input("IELTS")
gpa = st.sidebar.text_input("GPA")
status = st.sidebar.selectbox("Application Status", ["Applied", "Accepted", "Rejected", "Preparing"])
email = st.sidebar.text_input("Email")
link = st.sidebar.text_input("Link")
notes = st.sidebar.text_area("Notes")
verified = st.sidebar.checkbox("Verified")

if st.sidebar.button("Save Program"):
    new_row = {
        "Country": country,
        "University": university,
        "Program": program,
        "Level": level,
        "Field": field,
        "Funding": funding,
        "Deadline": deadline,
        "IELTS": ielts,
        "GPA": gpa,
        "Application Status": status,
        "Email": email,
        "Link": link,
        "Notes": notes,
        "Verified": verified,
        "Deadline Status": ""
    }
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_csv(DATA_FILE, index=False)
    st.success("Program saved successfully ✅")

# --- Filters ---
st.sidebar.header("Filters")
selected_country = st.sidebar.multiselect("Filter by Country", df["Country"].dropna().unique())
selected_status = st.sidebar.multiselect("Filter by Status", df["Application Status"].dropna().unique())

filtered_df = df.copy()
if selected_country:
    filtered_df = filtered_df[filtered_df["Country"].isin(selected_country)]
if selected_status:
    filtered_df = filtered_df[filtered_df["Application Status"].isin(selected_status)]

# --- Color function ---
def color_status(val):
    if val == "Accepted":
        return "background-color: #c8f7c5"
    elif val == "Applied":
        return "background-color: #fff3b0"
    elif val == "Rejected":
        return "background-color: #ffc9c9"
    elif val == "Preparing":
        return "background-color: #cce5ff"
    return ""

# --- Main Table ---
st.subheader("📋 Saved Programs")
main_columns = [
    "Country", "University", "Program", "Level", "Field", "Funding",
    "Deadline", "IELTS", "GPA", "Application Status"
]
display_df = filtered_df[main_columns]

if "Application Status" in display_df.columns:
    st.dataframe(
      display_df.style.applymap(color_status, subset=["Application Status"]),
        width="stretch"
    )
else:
    st.dataframe(display_df, width="stretch")

# --- Details Table ---
st.subheader("📝 Program Details")
detail_columns = ["Email", "Link", "Notes", "Verified", "Deadline Status"]
detail_df = filtered_df[detail_columns]

with st.expander("Show Details"):
    st.dataframe(detail_df, width="stretch")

# --- Edit Program ---
st.subheader("✏️ Edit Program")
edit_list = df["Program"].dropna().astype(str).tolist()
if len(edit_list) > 0:
    selected_edit_program = st.selectbox("Select Program To Edit", edit_list)
    edit_index = df[df["Program"].astype(str) == selected_edit_program].index[0]
    selected_row = df.loc[edit_index]

    with st.expander("Open Edit Form"):
        edit_country = st.text_input("Edit Country", selected_row.get("Country", ""))
        edit_university = st.text_input("Edit University", selected_row.get("University", ""))
        edit_program = st.text_input("Edit Program Name", selected_row.get("Program", ""))
        edit_level = st.text_input("Edit Level", selected_row.get("Level", ""))
        edit_field = st.text_input("Edit Field", selected_row.get("Field", ""))
        edit_funding = st.text_input("Edit Funding", selected_row.get("Funding", ""))
        edit_deadline = st.text_input("Edit Deadline", selected_row.get("Deadline", ""))
        edit_ielts = st.text_input("Edit IELTS", selected_row.get("IELTS", ""))
        edit_gpa = st.text_input("Edit GPA", selected_row.get("GPA", ""))
        edit_status = st.selectbox(
            "Edit Application Status",
            ["Applied", "Accepted", "Rejected", "Preparing"],
            index=["Applied", "Accepted", "Rejected", "Preparing"].index(selected_row.get("Application Status", "Applied"))
        )
        edit_email = st.text_input("Edit Email", selected_row.get("Email", ""))
        edit_link = st.text_input("Edit Link", selected_row.get("Link", ""))
        edit_notes = st.text_area("Edit Notes", selected_row.get("Notes", ""))
        edit_verified = st.checkbox("Edit Verified", selected_row.get("Verified", False))

        if st.button("Save Changes"):
            df.at[edit_index, "Country"] = edit_country
            df.at[edit_index, "University"] = edit_university
            df.at[edit_index, "Program"] = edit_program
            df.at[edit_index, "Level"] = edit_level
            df.at[edit_index, "Field"] = edit_field
            df.at[edit_index, "Funding"] = edit_funding
            df.at[edit_index, "Deadline"] = edit_deadline
            df.at[edit_index, "IELTS"] = edit_ielts
            df.at[edit_index, "GPA"] = edit_gpa
            df.at[edit_index, "Application Status"] = edit_status
            df.at[edit_index, "Email"] = edit_email
            df.at[edit_index, "Link"] = edit_link
            df.at[edit_index, "Notes"] = edit_notes
            df.at[edit_index, "Verified"] = edit_verified
            df.to_csv(DATA_FILE, index=False)
            st.success("Changes saved successfully ✅")
