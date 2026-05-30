import streamlit as st
import pandas as pd
import os
from datetime import datetime
st.set_page_config(page_title="Scholarship Tracker", layout="wide")

DATA_FILE = "programs.csv"

st.title("🎓 Scholarship Tracker")
st.write("برنامه شخصی برای ذخیره و مدیریت دانشگاه‌ها و بورسیه‌ها")
st.sidebar.header("⚙️ Personal Settings")

user_name = st.sidebar.text_input("Your Name", "Niusha")

target_country = st.sidebar.selectbox(
    "Target Country",
    ["Germany", "Italy", "Sweden", "Finland", "Netherlands", "France", "Austria"]
)

target_degree = st.sidebar.selectbox(
    "Target Degree",
    ["Bachelor", "Master", "PhD"]
)

target_ielts = st.sidebar.number_input(
    "Target IELTS",
    min_value=0.0,
    max_value=9.0,
    value=6.5,
    step=0.5
)

dream_universities = st.sidebar.text_area(
    "Dream Universities",
    placeholder="Aalto University\nUniversity of Helsinki\nTU Munich"
)

st.info(
    f"👋 Welcome {user_name}! | IELTS: {target_ielts} "
)

with st.expander("⭐ My Dream Universities"):
    if dream_universities.strip():
        for uni in dream_universities.splitlines():
            st.write(f"• {uni}")
    else:
        st.write("No dream universities added yet.")
# ----------------------------
# Funding Classifier
# ----------------------------

def classify_funding(text):
    text = str(text).lower()

    if "fully funded" in text or "stipend" in text:
        return "Full Funded"

    elif "partial" in text:
        return "Partial Funded"

    elif "tuition-free" in text:
        return "Tuition Free"

    return "Unknown"

def deadline_status(deadline):
    try:
        deadline_date = datetime.strptime(str(deadline), "%Y-%m-%d")
        today = datetime.today()
        days_left = (deadline_date - today).days

        if days_left < 0:
            return "Expired"
        elif days_left <= 30:
            return f"⚠️ {days_left} days left"
        else:
            return f"{days_left} days left"
    except:
        return ""
# ----------------------------
# Database
# ----------------------------

columns = [
    "Country",
    "University",
    "Program",
    "Level",
    "Field",
    "Funding",
    "Deadline",
    "IELTS",
    "GPA",
    "Application Status",
    "Verified",
    "Email",
    "Link",
    "Notes",
    "Deadline Status"
]

if os.path.exists(DATA_FILE):
    df = pd.read_csv(DATA_FILE)
else:
    df = pd.DataFrame(columns=columns)

for col in columns:
    if col not in df.columns:
        df[col] = ""

# ----------------------------
# Sidebar
# ----------------------------

st.sidebar.header("➕ Add Program")

country = st.sidebar.text_input("Country")
university = st.sidebar.text_input("University")
program = st.sidebar.text_input("Program Name")

level = st.sidebar.selectbox(
    "Level",
    ["Bachelor", "Master", "PhD"]
)

field = st.sidebar.text_input("Field")

deadline = st.sidebar.text_input("Deadline")

ielts = st.sidebar.text_input("IELTS")

gpa = st.sidebar.text_input("GPA")

status = st.sidebar.selectbox(
    "Application Status",
    [
        "Not Started",
        "Preparing",
        "Applied",
        "Accepted",
        "Rejected"
    ]
)

verified = st.sidebar.selectbox(
    "Verified",
    ["No", "Yes"]
)

email = st.sidebar.text_input("Email")

link = st.sidebar.text_input("Official Link")

notes = st.sidebar.text_area("Notes")

funding = classify_funding(notes)

# ----------------------------
# Save
# ----------------------------

if st.sidebar.button("Save Program"):

    if program.strip() == "":
        st.sidebar.error("Program Name cannot be empty")
    else:

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
            "Verified": verified,
            "Email": email,
            "Link": link,
            "Notes": notes,
            "Deadline Status": deadline_status(deadline)
        }

        df = pd.concat(
            [df, pd.DataFrame([new_row])],
            ignore_index=True
        )

        df.to_csv(DATA_FILE, index=False)
        st.success("Saved successfully ✅")

# ----------------------------
# Filters
# ----------------------------

st.subheader("📌 Saved Programs")
total_programs = len(df)
applied_count = len(df[df["Application Status"] == "Applied"])
accepted_count = len(df[df["Application Status"] == "Accepted"])
rejected_count = len(df[df["Application Status"] == "Rejected"])

m1, m2, m3, m4 = st.columns(4)

m1.metric("Total Programs", total_programs)
m2.metric("Applied", applied_count)
m3.metric("Accepted", accepted_count)
m4.metric("Rejected", rejected_count)

search_text = st.text_input("🔎 Search by University / Program / Country")

if search_text:
    filtered_df = df[
        df["University"].astype(str).str.contains(search_text, case=False, na=False) |
        df["Program"].astype(str).str.contains(search_text, case=False, na=False) |
        df["Country"].astype(str).str.contains(search_text, case=False, na=False)
    ]
else:
    filtered_df = df.copy()

col1, col2, col3, col4 = st.columns(4)

with col1:
    country_filter = st.selectbox(
        "Filter by Country",
        ["All"] + sorted(df["Country"].dropna().astype(str).unique().tolist())
    )

with col2:
    funding_filter = st.selectbox(
        "Filter by Funding",
        ["All"] + sorted(df["Funding"].dropna().astype(str).unique().tolist())
    )

with col3:
    level_filter = st.selectbox(
        "Filter by Level",
        ["All"] + sorted(df["Level"].dropna().astype(str).unique().tolist())
    )

with col4:
    status_filter = st.selectbox(
        "Filter by Status",
        ["All"] + sorted(df["Application Status"].dropna().astype(str).unique().tolist())
    )


if country_filter != "All":
    filtered_df = filtered_df[
        filtered_df["Country"] == country_filter
    ]

if funding_filter != "All":
    filtered_df = filtered_df[
        filtered_df["Funding"] == funding_filter
    ]

if level_filter != "All":
    filtered_df = filtered_df[
        filtered_df["Level"] == level_filter
    ]

if status_filter != "All":
    filtered_df = filtered_df[
        filtered_df["Application Status"] == status_filter
    ]

# ----------------------------
# Delete
# ----------------------------

st.subheader("🗑 Delete Program")

program_list = (
    df["Program"]
    .dropna()
    .astype(str)
    .tolist()
)

if len(program_list) > 0:

    delete_program = st.selectbox(
        "Select Program",
        program_list
    )

    if st.button("Delete Selected Program"):

        df = df[df["Program"] != delete_program]

        df.to_csv(DATA_FILE, index=False)

        st.success(f"{delete_program} deleted!")

        st.rerun()

# ----------------------------
# Edit Program
# ----------------------------

st.subheader("✏️ Edit Program")

df["Edit Label"] = (
    df["University"].fillna("").astype(str)
    + " | "
    + df["Program"].fillna("").astype(str)
    + " | "
    + df["Country"].fillna("").astype(str)
)

edit_list = df["Edit Label"].tolist()

selected_edit_program = st.selectbox(
    "Select Program To Edit",
    edit_list
)

edit_index = df[df["Edit Label"] == selected_edit_program].index[0]
selected_row = df.loc[edit_index]

    with st.expander("Open Edit Form"):
        edit_country = st.text_input("Edit Country", selected_row.get("Country", ""))
        edit_university = st.text_input("Edit University", selected_row.get("University", ""))
        edit_program = st.text_input("Edit Program Name", selected_row.get("Program", ""))

        edit_level = st.selectbox(
            "Edit Level",
            ["Bachelor", "Master", "PhD"],
            index=["Bachelor", "Master", "PhD"].index(selected_row.get("Level", "Bachelor"))
            if selected_row.get("Level", "Bachelor") in ["Bachelor", "Master", "PhD"] else 0
        )

        edit_field = st.text_input("Edit Field", selected_row.get("Field", ""))
        edit_deadline = st.text_input("Edit Deadline", selected_row.get("Deadline", ""))
        edit_ielts = st.text_input("Edit IELTS", selected_row.get("IELTS", ""))
        edit_gpa = st.text_input("Edit GPA", selected_row.get("GPA", ""))

        edit_status = st.selectbox(
            "Edit Application Status",
            ["Not Started", "Preparing", "Applied", "Accepted", "Rejected"],
            index=["Not Started", "Preparing", "Applied", "Accepted", "Rejected"].index(
                selected_row.get("Application Status", "Not Started")
            )
            if selected_row.get("Application Status", "Not Started") in ["Not Started", "Preparing", "Applied", "Accepted", "Rejected"] else 0
        )

        edit_verified = st.selectbox(
            "Edit Verified",
            ["No", "Yes"],
            index=["No", "Yes"].index(selected_row.get("Verified", "No"))
            if selected_row.get("Verified", "No") in ["No", "Yes"] else 0
        )

        edit_email = st.text_input("Edit Email", selected_row.get("Email", ""))
        edit_link = st.text_input("Edit Link", selected_row.get("Link", ""))
        edit_notes = st.text_area("Edit Notes", selected_row.get("Notes", ""))

        if st.button("Save Changes"):
            if edit_program.strip() == "":
                st.error("Program Name cannot be empty")
            else:
                df.loc[edit_index, "Country"] = edit_country
                df.loc[edit_index, "University"] = edit_university
                df.loc[edit_index, "Program"] = edit_program
                df.loc[edit_index, "Level"] = edit_level
                df.loc[edit_index, "Field"] = edit_field
                df.loc[edit_index, "Funding"] = classify_funding(edit_notes)
                df.loc[edit_index, "Deadline"] = edit_deadline
                df.loc[edit_index, "IELTS"] = edit_ielts
                df.loc[edit_index, "GPA"] = edit_gpa
                df.loc[edit_index, "Application Status"] = edit_status
                df.loc[edit_index, "Verified"] = edit_verified
                df.loc[edit_index, "Email"] = edit_email
                df.loc[edit_index, "Link"] = edit_link
                df.loc[edit_index, "Notes"] = edit_notes

                df.to_csv(DATA_FILE, index=False)

                st.success("Program updated successfully ✅")
                st.rerun()
else:
    st.info("No programs to edit yet.")
# ----------------------------
# Display Table
# ----------------------------

display_df = filtered_df.copy()

display_df = display_df.dropna(
    axis=1,
    how="all"
)

display_df = display_df.loc[
    :,
    (display_df != "").any(axis=0)

]

if "Deadline" in filtered_df.columns:
    filtered_df["Deadline Status"] = filtered_df["Deadline"].apply(deadline_status)

sort_deadline = st.checkbox("Sort by nearest deadline")

if sort_deadline:
    filtered_df["Deadline Date"] = pd.to_datetime(filtered_df["Deadline"], errors="coerce")
    filtered_df = filtered_df.sort_values("Deadline Date")
    filtered_df = filtered_df.drop(columns=["Deadline Date"])


    st.dataframe(display_df, width="stretch")

# ----------------------------
# Download CSV
# ----------------------------

csv = filtered_df.to_csv(
    index=False
).encode("utf-8")

st.download_button(
    label="⬇ Download CSV",
    data=csv,
    file_name="scholarship_programs.csv",
    mime="text/csv"
)
from io import BytesIO

excel_file = BytesIO()

with pd.ExcelWriter(excel_file, engine="openpyxl") as writer:
    filtered_df.to_excel(
        writer,
        index=False,
        sheet_name="Scholarships"
    )

st.download_button(
    label="📊 Download Excel",
    data=excel_file.getvalue(),
    file_name="scholarship_programs.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)
