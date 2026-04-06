import streamlit as st
from api_services import *
from app_task import task_app

# config 
st.set_page_config(page_title="Task Manager Pro", layout="wide")

# session state 
if "add_name" not in st.session_state : 
    st.session_state.add_name = ""

if "add_pass" not in st.session_state : 
    st.session_state.add_pass = ""

if "add_phoneNum" not in st.session_state : 
    st.session_state.add_phoneNum = ""

if "reset_form" not in st.session_state:
    st.session_state.reset_form = False

# page state : 
if "page" not in st.session_state : 
    st.session_state.page = "signup"

# reset_form 
if st.session_state.reset_form : 
    st.session_state.add_name = ""
    st.session_state.add_pass = ""
    st.session_state.add_phoneNum = ""

# Header
st.title("TASK MANAGER")



# create account 
if st.session_state.page == "signup" : 
    st.subheader("Create Account")

    with st.form("create_account_form") : 
        name = st.text_input("Name", key = "add_name")
        password = st.text_input("Password", key = "add_pass")
        phoneNum = st.text_input("Phone Number", key = "add_phoneNum")

        submitted = st.form_submit_button("Create Account")

        if submitted : 
            if name.strip() : 
                res = create_acc(name, password, phoneNum)
                if res and res["message"] == "Account created successfully...!!":
                    st.success("Account Created Successfully !")
                    st.session_state.page = "login"
                    st.rerun()
                else : 
                    st.error("Some error occured !")
    st.write("Or already hava account !?")
    login = st.button("Login")
    if login : 
        st.session_state.page = "login"
        st.rerun()

# login page
elif st.session_state.page == "login" : 
    st.subheader("Login Account")

    with st.form("login_account_form") : 
        name = st.text_input("Name")
        password = st.text_input("Passsword")

        col1, col2 = st.columns(2)

        with col1 :
            submitted = st.form_submit_button("Login")
        with col2 : 
            back = st.form_submit_button("Back")

        if submitted : 
            if name.strip() : 
                res = login_acc(name, password)
                if res and res.get("message") == "Login Successfully...!!":
                    st.session_state.user_id = res["user_id"]
                    st.success(res["message"])
                    st.session_state.page = "task_app"
                    st.session_state.reset_form = True
                    st.rerun()
                else : 
                    st.error("Some error occured !")
            else : 
                st.error("Credentials not filled !")
        if back : 
            st.session_state.page = "signup"

elif st.session_state.page == "task_app" : 
    task_app()
