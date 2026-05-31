import streamlit as st
from supabase import create_client, Client
import pandas as pd

# --- Supabase Connection ---
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

st.title("Scholarship Tracker with Supabase 🚀")

# --- Session Management ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_email" not in st.session_state:
    st.session_state.user_email = ""
if "user_id" not in st.session_state:
    st.session_state.user_id = None

# --- Authentication ---
def login(email, password):
    res = supabase.auth.sign_in_with_password({
        "email": email,
        "password": password
    })
    if res.user:
        st.session_state.logged_in = True
        st.session_state.user_email = email
        st.session_state.user_id = res.user.id
        st.success("Logged in ✅")
        st.experimental_rerun()
    else:
        st.error("Login failed")

def register(email, password):
    res = supabase.auth.sign_up({"email": email, "password": password})
    if res.user:
        st.success("Registered! Check your email for confirmation.")
    else:
        st.error(res.error.message)

def logout():
    supabase.auth.sign_out()
    st.session_state.logged_in = False
    st.session_state.user_email = ""
    st.session_state.user_id = None
    st.experimental_rerun()

# --- Login/Register Form ---
if not st.session_state.logged_in:
    st.subheader("Login / Register")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Register"):
            register(email, password)
    with col2:
        if st.button("Login"):
            login(email, password)
    st.stop()
else:
    st.sidebar.button("Logout", on_click=logout)

# --- Fetch Programs for Logged-in User ---
programs = supabase.table("programs").select("*").eq("user_id", st.session_state.user_id).execute().data
df = pd.DataFrame(programs)

# --- Sidebar Inputs ---
st.sidebar.header("Add New Program")
country = st.sidebar.text_input("country")
university = st.sidebar.text_input("university")
program = st.sidebar.text_input("program")
level = st.sidebar.text_input("level")
field = st.sidebar.text_input("field")
funding = st.sidebar.text_input("funding")
deadline = st.sidebar.text_input("deadline")
ielts = st.sidebar.text_input("ielts")
gpa = st.sidebar.text_input("gpa")
status = st.sidebar.selectbox("Application Status", ["Applied", "Accepted", "Rejected", "Preparing"])
email_field = st.sidebar.text_input("email")
link = st.sidebar.text_input("link")
notes = st.sidebar.text_area("notes")
verified = st.sidebar.checkbox("verified")

if st.sidebar.button("Save Program"):
    new_row = {
        "user_id": st.session_state.user_id,
        "country": country,
        "university": university,
        "program": program,
        "level": level,
        "field": field,
        "funding": funding,
        "deadline": deadline,
        "ielts": ielts,
        "gpa": gpa,
        "application_status": status,
        "email": email_field,
        "link": link,
        "notes": notes,
        "verified": verified
    }
    supabase.table("programs").insert(new_row).execute()
    st.success("Program saved successfully ✅")
    st.experimental_rerun()

# --- Filters ---
st.sidebar.header("Filters")
selected_country = st.sidebar.multiselect("Filter by country", df["country"].dropna().unique())
selected_status = st.sidebar.multiselect("Filter by Status", df["application_status"].dropna().unique())
filtered_df = df.copy()
if selected_country:
    filtered_df = filtered_df[filtered_df["country"].isin(selected_country)]
if selected_status:
    filtered_df = filtered_df[filtered_df["application_status"].isin(selected_status)]

# --- Main Table ---
st.subheader("📋 Saved Programs")
main_columns = ["country","university","program","level","field","funding","deadline","ielts","gpa","application_status"]
st.dataframe(filtered_df[main_columns], width="stretch")

# --- Details Table ---
st.subheader("📝 Program Details")
detail_columns = ["email","link","notes","verified"]
with st.expander("Show Details"):
    st.dataframe(filtered_df[detail_columns], width="stretch")

# --- Edit / Delete Program ---
st.subheader("✏️ Edit / Delete Program")
edit_list = df["program"].dropna().astype(str).tolist()
if edit_list:
    selected_edit_program = st.selectbox("Select Program To Edit", edit_list)
    selected_row = df[df["program"]==selected_edit_program].iloc[0]

    with st.expander("Open Edit Form"):
        edit_country = st.text_input("Edit Country", selected_row.get("country",""))
        edit_university = st.text_input("Edit University", selected_row.get("university",""))
        edit_program = st.text_input("Edit Program Name", selected_row.get("program",""))
        edit_level = st.text_input("Edit Level", selected_row.get("level",""))
        edit_field = st.text_input("Edit Field", selected_row.get("field",""))
        edit_funding = st.text_input("Edit Funding", selected_row.get("funding",""))
        edit_deadline = st.text_input("Edit Deadline", selected_row.get("deadline",""))
        edit_ielts = st.text_input("Edit IELTS", selected_row.get("ielts",""))
        edit_gpa = st.text_input("Edit GPA", selected_row.get("gpa",""))
        edit_status = st.selectbox("Edit Application Status", ["Applied","Accepted","Rejected","Preparing"], index=["Applied","Accepted","Rejected","Preparing"].index(selected_row.get("application_status","Applied")))
        edit_email = st.text_input("Edit Email", selected_row.get("email",""))
        edit_link = st.text_input("Edit Link", selected_row.get("link",""))
        edit_notes = st.text_area("Edit Notes", selected_row.get("notes",""))
        edit_verified = st.checkbox("Edit Verified", selected_row.get("verified",False))

        col1,col2 = st.columns(2)
        with col1:
            if st.button("Save Changes"):
                supabase.table("programs").update({
                    "country": edit_country,
                    "university": edit_university,
                    "program": edit_program,
                    "level": edit_level,
                    "field": edit_field,
                    "funding": edit_funding,
                    "deadline": edit_deadline,
                    "ielts": edit_ielts,
                    "gpa": edit_gpa,
                    "application_status": edit_status,
                    "email": edit_email,
                    "link": edit_link,
                    "notes": edit_notes,
                    "verified": edit_verified
                }).eq("id", selected_row["id"]).execute()
                st.success("Changes saved ✅")
                st.experimental_rerun()
        with col2:
            if st.button("Delete Program"):
                supabase.table("programs").delete().eq("id", selected_row["id"]).execute()
                st.success("Deleted ✅")
                st.experimental_rerun()
