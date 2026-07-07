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
