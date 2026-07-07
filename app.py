import streamlit as st

from pawpal_system import Constraint, Owner, Pet, Scheduler, Task

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="Jordan")

owner = st.session_state.owner

st.subheader("Manage Pets")
owner_name = st.text_input("Owner name", value=owner.name)
owner.name = owner_name

pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])

if st.button("Add pet"):
    new_pet = Pet(name=pet_name, species=species)
    owner.add_pet(new_pet)
    st.success(f"Added {new_pet.name} to {owner.name}'s care team.")

if owner.pets:
    st.write("Current pets:")
    for pet in owner.pets:
        st.write(f"- {pet.name} ({pet.species})")
else:
    st.info("No pets yet. Add one above.")

st.divider()

st.subheader("Schedule Tasks")
if owner.pets:
    pet_names = [pet.name for pet in owner.pets]
    selected_pet_name = st.selectbox("Select pet", pet_names)
    selected_pet = next(pet for pet in owner.pets if pet.name == selected_pet_name)
else:
    selected_pet = None
    st.info("Add a pet before scheduling tasks.")

col1, col2, col3 = st.columns(3)
with col1:
    task_title = st.text_input("Task title", value="Morning walk", key="task_title")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20, key="task_duration")
with col3:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2, key="task_priority")

if st.button("Add task") and selected_pet is not None:
    priority_value = {"low": 1, "medium": 2, "high": 3}[priority]
    task = Task(description=task_title, duration_minutes=int(duration), priority=priority_value)
    selected_pet.add_task(task)
    st.success(f"Added '{task.description}' to {selected_pet.name}'s plan.")
elif st.button("Add task"):
    st.warning("Please add a pet first.")

if selected_pet is not None and selected_pet.tasks:
    st.write(f"Tasks for {selected_pet.name}:")
    task_rows = [
        {
            "title": task.description,
            "duration_minutes": task.duration_minutes,
            "priority": task.priority,
        }
        for task in selected_pet.tasks
    ]
    st.table(task_rows)
elif selected_pet is not None:
    st.info(f"No tasks yet for {selected_pet.name}. Add one above.")

st.divider()

st.subheader("Build Schedule")
st.caption("Generate a simple daily plan from the current pet-care data.")

if st.button("Generate schedule") and owner.pets:
    constraints = Constraint(available_minutes=90, preferred_window="morning", max_tasks_per_day=4)
    scheduler = Scheduler(owner=owner, constraints=constraints)
    plan = scheduler.build_plan()

    st.write(f"Planned tasks: {len(plan.scheduled_tasks)}")
    for scheduled_task in plan.scheduled_tasks:
        task = scheduled_task.task
        st.write(f"- {scheduled_task.start_time} - {scheduled_task.end_time}: {task.description}")
else:
    st.info("Add a pet and some tasks before generating a schedule.")
