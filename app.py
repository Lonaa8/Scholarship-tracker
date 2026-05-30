import streamlit as st
import pandas as pd

DATA_FILE = "scholarship_programs.csv"

st.set_page_config(page_title="Scholarship Finder", layout="wide")

# Load data
try:
    df = pd.read_csv(DATA_FILE)
except FileNotFoundError:
    df = pd.DataFrame(columns=["Country", "Field", "Level", "University", "Program",
                               "Funding", "Deadline", "Email", "Link", "Notes", "IELTS", "GPA", "Application Status", "Verified"])

st.title("🎓 Scholarship Finder")
st.write("اینجا می‌تونی برنامه‌ها و بورسیه‌هایی که پیدا می‌کنی رو ذخیره و دسته‌بندی کنی")

# Sidebar: Add Program
st.sidebar.header("+ Add Program")
with st.sidebar.form("add_program"):
    country = st.text_input("Country")
    field = st.text_input("Field")
    level = st.selectbox("Level", ["Bachelor", "Master", "PhD"])
    university = st.text_input("University")
    program_name = st.text_input("Program name")
    funding = st.text_input("Funding")
    deadline = st.text_input("Deadline")
    email = st.text_input("Email")
    link = st.text_input("Official link")
    notes = st.text_area("Notes")
    ielts = st.text_input("IELTS")
    gpa = st.text_input("GPA")
    verified = st.checkbox("Verified", False)
    submitted = st.form_submit_button("Add Program")

    if submitted:
        new_row = {
            "Country": country, "Field": field, "Level": level, "University": university,
            "Program": program_name, "Funding": funding, "Deadline": deadline,
            "Email": email, "Link": link, "Notes": notes, "IELTS": ielts,
            "GPA": gpa, "Application Status": "Applied", "Verified": verified
        }
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        df.to_csv(DATA_FILE, index=False)
        st.success("Program added successfully ✅")

# Sidebar: Edit Program
st.sidebar.header("✏️ Edit Program")
edit_list = df["Program"].dropna().astype(str).tolist()
if len(edit_list) > 0:
    selected_program = st.sidebar.selectbox("Select Program To Edit", edit_list)
    edit_index = df[df["Program"].astype(str) == selected_program].index[0]
    selected_row = df.loc[edit_index]

    with st.sidebar.expander("Open Edit Form"):
        edit_country = st.text_input("Edit Country", selected_row.get("Country", ""))
        edit_university = st.text_input("Edit University", selected_row.get("University", ""))
        edit_program = st.text_input("Edit Program Name", selected_row.get("Program", ""))
        edit_level = st.selectbox(
            "Edit Level",
            ["Bachelor", "Master", "PhD"],
            index=["Bachelor", "Master", "PhD"].index(selected_row.get("Level", "Bachelor"))
        )
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
            df.loc[edit_index] = {
                "Country": edit_country, "Field": selected_row["Field"], "Level": edit_level,
                "University": edit_university, "Program": edit_program, "Funding": edit_funding,
                "Deadline": edit_deadline, "Email": edit_email, "Link": edit_link,
                "Notes": edit_notes, "IELTS": edit_ielts, "GPA": edit_gpa,
                "Application Status": edit_status, "Verified": edit_verified
                }
            df.to_csv(DATA_FILE, index=False)
            st.success("Program updated successfully ✅")
            st.experimental_rerun()
else:
    st.sidebar.info("No programs to edit yet.")

# Main: Display Table
st.subheader("📌 Saved Programs")
filtered_df = df.copy()
filtered_df = filtered_df.dropna(how="all", axis=1)  # حذف ستون‌های کاملاً خالی
filtered_df = filtered_df.loc[:, (filtered_df != "").any(axis=0)]  # حذف ستون‌های خالی از نظر محتوا
st.dataframe(filtered_df, use_container_width=True)
                
