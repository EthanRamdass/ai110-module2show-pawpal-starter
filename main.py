from pawpal_system import Constraint, Owner, Pet, Scheduler, Task


def main() -> None:
    owner = Owner(name="Jordan", preferences=["morning", "calm"])

    mochi = Pet(name="Mochi", species="dog", age=3)
    luna = Pet(name="Luna", species="cat", age=2)

    mochi.add_task(Task(description="Morning walk", duration_minutes=20, priority=3, scheduled_time="09:00", frequency="daily"))
    mochi.add_task(Task(description="Feed breakfast", duration_minutes=10, priority=2, scheduled_time="08:00", frequency="daily"))
    luna.add_task(Task(description="Grooming", duration_minutes=15, priority=1, scheduled_time="09:00", frequency="weekly"))
    luna.add_task(Task(description="Play session", duration_minutes=25, priority=3, scheduled_time="16:00", frequency="daily"))

    completed_task = Task(description="Completed feed", duration_minutes=5, priority=2, scheduled_time="07:00")
    completed_task.mark_completed()
    mochi.add_task(completed_task)

    owner.add_pet(mochi)
    owner.add_pet(luna)

    constraints = Constraint(available_minutes=90, preferred_window="morning", max_tasks_per_day=4)
    scheduler = Scheduler(owner=owner, constraints=constraints)

    all_tasks = scheduler.get_available_tasks(include_completed=False)
    sorted_tasks = scheduler.sort_by_time(all_tasks)
    filtered_tasks = scheduler.filter_tasks(sorted_tasks, pet_name="Mochi", include_completed=False)

    print("Sorted pending tasks")
    print("====================")
    for task in filtered_tasks:
        print(f"- {task.scheduled_time} | {task.description} ({task.duration_minutes} min)")

    print()
    warnings = scheduler.get_conflict_warnings()
    if warnings:
        print("Conflict warnings")
        print("=================")
        for warning in warnings:
            print(f"- {warning}")
        print()

    plan = scheduler.build_plan()
    print("Today's Schedule")
    print("================")
    for index, scheduled_task in enumerate(plan.scheduled_tasks, start=1):
        task = scheduled_task.task
        print(f"{index}. {scheduled_task.start_time} - {scheduled_task.end_time} | {task.description} ({task.duration_minutes} min, priority {task.priority})")


if __name__ == "__main__":
    main()
