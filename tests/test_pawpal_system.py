from datetime import date, timedelta

from pawpal_system import Constraint, Owner, Pet, Scheduler, Task


def test_task_tracks_completion_and_frequency():
    task = Task(description="Morning walk", scheduled_time="08:00", frequency="daily")

    assert task.description == "Morning walk"
    assert task.completed is False
    assert task.frequency == "daily"

    task.mark_completed()
    assert task.completed is True


def test_owner_collects_tasks_from_all_pets():
    owner = Owner(name="Jordan")
    pet_one = Pet(name="Mochi", species="dog")
    pet_two = Pet(name="Luna", species="cat")

    pet_one.add_task(Task(description="Walk", duration_minutes=20, priority=3))
    pet_two.add_task(Task(description="Feed", duration_minutes=10, priority=2))

    owner.add_pet(pet_one)
    owner.add_pet(pet_two)

    tasks = owner.get_all_tasks()

    assert len(tasks) == 2
    assert [task.description for task in tasks] == ["Walk", "Feed"]


def test_scheduler_builds_plan_from_owner_data():
    owner = Owner(name="Jordan")
    pet = Pet(name="Mochi", species="dog")
    pet.add_task(Task(description="Morning walk", duration_minutes=20, priority=3))
    pet.add_task(Task(description="Feed breakfast", duration_minutes=10, priority=2))
    pet.add_task(Task(description="Grooming", duration_minutes=30, priority=1))
    owner.add_pet(pet)

    constraints = Constraint(available_minutes=60, max_tasks_per_day=3)
    scheduler = Scheduler(owner=owner, constraints=constraints)
    plan = scheduler.build_plan()

    assert plan is not None
    assert len(plan.scheduled_tasks) > 0
    assert plan.total_duration > 0


def test_scheduler_filters_tasks_by_pet_and_status():
    owner = Owner(name="Jordan")
    mochi = Pet(name="Mochi", species="dog")
    luna = Pet(name="Luna", species="cat")

    completed_task = Task(description="Completed feed", duration_minutes=10, priority=2)
    completed_task.mark_completed()
    recurring_task = Task(description="Daily meds", duration_minutes=15, priority=3, frequency="daily")

    mochi.add_task(completed_task)
    luna.add_task(recurring_task)
    owner.add_pet(mochi)
    owner.add_pet(luna)

    scheduler = Scheduler(owner=owner, constraints=Constraint(available_minutes=120, max_tasks_per_day=5))
    tasks = scheduler.get_available_tasks(pet_name="Luna", include_completed=False)

    assert [task.description for task in tasks] == ["Daily meds"]


def test_scheduler_skips_overlapping_tasks():
    owner = Owner(name="Jordan")
    pet = Pet(name="Mochi", species="dog")
    first_task = Task(description="Feed", duration_minutes=20, priority=3, scheduled_time="08:00")
    second_task = Task(description="Walk", duration_minutes=20, priority=2, scheduled_time="08:10")

    pet.add_task(first_task)
    pet.add_task(second_task)
    owner.add_pet(pet)

    scheduler = Scheduler(owner=owner, constraints=Constraint(available_minutes=120, max_tasks_per_day=5))
    plan = scheduler.build_plan()

    assert len(plan.scheduled_tasks) == 1
    assert plan.scheduled_tasks[0].task.description == "Feed"


def test_recurring_task_creates_next_occurrence_when_completed():
    pet = Pet(name="Mochi", species="dog")
    task = Task(description="Daily meds", duration_minutes=10, priority=3, scheduled_time="08:00", frequency="daily")
    pet.add_task(task)

    next_task = pet.complete_task(task)

    assert task.completed is True
    assert next_task is not None
    assert next_task.completed is False
    assert next_task.frequency == "daily"
    assert next_task.due_date == date.today() + timedelta(days=1)


def test_scheduler_warns_about_tasks_scheduled_at_the_same_time():
    owner = Owner(name="Jordan")
    mochi = Pet(name="Mochi", species="dog")
    luna = Pet(name="Luna", species="cat")

    mochi.add_task(Task(description="Morning walk", duration_minutes=20, priority=3, scheduled_time="09:00"))
    luna.add_task(Task(description="Grooming", duration_minutes=15, priority=1, scheduled_time="09:00"))
    owner.add_pet(mochi)
    owner.add_pet(luna)

    scheduler = Scheduler(owner=owner, constraints=Constraint(available_minutes=120, max_tasks_per_day=5))
    warnings = scheduler.get_conflict_warnings()

    assert len(warnings) == 1
    assert "Morning walk" in warnings[0]
    assert "Grooming" in warnings[0]
    assert "09:00" in warnings[0]
