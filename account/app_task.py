import streamlit as st
from api_service_task import *
from datetime import datetime

def task_app() : 

    # =========================
    # SESSION STATE INIT
    # =========================
    if "add_title" not in st.session_state:
        st.session_state.add_title = ""

    if "add_desc" not in st.session_state:
        st.session_state.add_desc = ""

    if "add_priority" not in st.session_state:
        st.session_state.add_priority = "low"

    if "add_due_date" not in st.session_state:
        st.session_state.add_due_date = datetime.today()

    if "add_due_time" not in st.session_state:
        st.session_state.add_due_time = datetime.now().time()

    if "reset_form" not in st.session_state:
        st.session_state.reset_form = False


    # =========================
    # RESET FORM
    # =========================
    if st.session_state.reset_form:
        st.session_state.add_title = ""
        st.session_state.add_desc = ""
        st.session_state.add_priority = "low"
        st.session_state.add_due_date = datetime.today()
        st.session_state.add_due_time = datetime.now().time()
        st.session_state.reset_form = False


    # =========================
    # HEADER
    # =========================
    st.title("My Task Manager")

    # =========================
    # ADD TASK FORM
    # =========================
    st.subheader("Add Task")

    with st.form("add_task_form"):

        col1, col2 = st.columns(2)

        with col1:
            title = st.text_input("Title", key="add_title")

        with col2:
            description = st.text_input("Description", key="add_desc")

        priority = st.selectbox(
            "Priority",
            ["low", "medium", "high"],
            key="add_priority"
        )

        col1, col2 = st.columns(2)

        with col1 :
            due_date = st.date_input("Due Date", key="add_due_date")
        
        with col2 :
            due_time = st.time_input("Due Time", key="add_due_time", step=60) 

        submitted = st.form_submit_button("Add Task")

        if submitted:
            if title.strip():
                add_task(st.session_state.user_id, title, description, priority, str(due_date), due_time.strftime("%H:%M:%S"))
                st.session_state.reset_form = True
                st.success("Task Added")
                st.rerun()
            else:
                st.error("Title is required!")

    st.divider()

    # =========================
    # SEARCH
    # =========================
    search_query = st.text_input(
        "Search Tasks",
        placeholder="Type to search...",
        key="search_input"
    )

    if search_query:
        tasks = search_task(st.session_state.user_id, search_query)
    else:
        tasks = get_tasks(st.session_state.user_id)

    st.divider()

    # =========================
    # SHOW TASKS
    # =========================
    st.subheader("Your Tasks")

    if not tasks:
        st.info("No tasks found")

    PRIORITY_LABELS = {
        "high": "High",
        "medium": "Medium",
        "low": "Low"
    }

    for task in tasks:
        with st.container():
            col1, col2, col3, col4 = st.columns([5, 2, 2, 1])

            with col1:
                st.markdown(f"**{task['title']}**")
                st.caption(task["des"])

            with col2:
                st.write(task["due_date"])
                try:
                    time_obj = datetime.strptime(str(task["due_time"]), "%H:%M:%S")
                    st.write(time_obj.strftime("%I:%M %p"))
                except:
                    st.write(task["due_time"])

            with col3:
                st.markdown(
                    f"**{PRIORITY_LABELS.get(task['priority'], task['priority'])}**"
                )

            with col4:

                if st.button("Edit", key=f"edit_{task['id']}"):
                    st.session_state.edit_task = task

                if st.button("Delete", key=f"del_{task['id']}"):
                    delete_task(task["id"])
                    st.success("Task Deleted")
                    st.rerun()

    st.divider()


    # =========================
    # EDIT TASK
    # =========================
    if "edit_task" in st.session_state:

        task = st.session_state.edit_task
        st.subheader("Edit Task")

        with st.form("edit_task_form"):

            new_title = st.text_input("Title", value=task["title"])
            new_desc = st.text_input("Description", value=task["des"])

            new_priority = st.selectbox(
                "Priority",
                ["low", "medium", "high"],
                index=["low", "medium", "high"].index(task["priority"])
            )
            col1, col2 = st.columns(2)
            with col1 : 
                new_date = st.date_input(
                    "Due Date",
                    value=datetime.strptime(task["due_date"], "%Y-%m-%d")
                )
            with col2 : 
                new_time = st.time_input(
                    "Due Time",
                    value=datetime.strptime(task["due_time"], "%H:%M:%S").time()
                )

            col1, col2 = st.columns(2)

            with col1:
                save = st.form_submit_button("Save Changes")

            with col2:
                cancel = st.form_submit_button("Cancel")

            if save:
                update_task(
                    task["id"],
                    new_title,
                    new_desc,
                    new_priority,
                    str(new_date),
                    new_time.strftime("%H:%M:%S"),
                    task["completed"]
                )

                del st.session_state.edit_task
                st.success("Task Updated")
                st.rerun()

            if cancel:
                del st.session_state.edit_task
                st.rerun()  

    back = st.button("BACK TO LOGIN")

    if back:
        if "user_id" in st.session_state:
            del st.session_state.user_id   # 🔥 logout

        st.session_state.page = "login"
        st.rerun()