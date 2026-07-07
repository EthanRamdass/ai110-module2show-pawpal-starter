from datetime import date, timedelta

from pawpal_system import Constraint, Owner, Pet, Scheduler, Task


def test_task_mark_complete_updates_status():
    task = Task(description="Morning walk", duration_minutes=20, priority=3)

    task.mark_completed()

    assert task.completed is True


def test_adding_task_increases_pet_task_count():
    pet = Pet(name="Mochi", species="dog")
    task = Task(description="Feed breakfast", duration_minutes=10, priority=2)

    pet.add_task(task)

    assert len(pet.tasks) == 1
    assert pet.tasks[0].description == "Feed breakfast"


def test_sort_by_time_orders_tasks_chronologically():
    pet = Pet(name="Mochi", species="dog")
    later_task = Task(description="Grooming", duration_minutes=15, priority=1, scheduled_time="10:00")
    earlier_task = Task(description="Walk", duration_minutes=20, priority=3, scheduled_time="08:00")
    middle_task = Task(description="Feed", duration_minutes=10, priority=2, scheduled_time="09:00")

    pet.add_task(later_task)
    pet.add_task(earlier_task)
    pet.add_task(middle_task)

    scheduler = Scheduler(pet=pet, constraints=Constraint(available_minutes=120, max_tasks_per_day=5))
    ordered_tasks = scheduler.sort_by_time(pet.get_tasks_for_day())

    assert [task.description for task in ordered_tasks] == ["Walk", "Feed", "Grooming"]


def test_recurring_daily_task_creates_next_day_task_when_completed():
    pet = Pet(name="Mochi", species="dog")
    task = Task(description="Daily meds", duration_minutes=10, priority=3, scheduled_time="08:00", frequency="daily")
    pet.add_task(task)

    next_task = pet.complete_task(task)

    assert task.completed is True
    assert next_task is not None
    assert next_task.completed is False
    assert next_task.frequency == "daily"
    assert next_task.due_date == date.today() + timedelta(days=1)


def test_scheduler_flags_duplicate_scheduled_times():
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


def test_pet_with_no_tasks_has_no_pending_items():
    pet = Pet(name="Mochi", species="dog")

    assert pet.get_pending_tasks() == []
