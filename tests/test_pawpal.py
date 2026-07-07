from pawpal_system import Pet, Task


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
