from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, timedelta
from typing import List


def _parse_time_to_minutes(value: str) -> int:
    """Convert a HH:MM string into minutes since midnight."""
    try:
        hours_text, minute_text = value.split(":")
        hours = int(hours_text)
        minutes = int(minute_text)
        return hours * 60 + minutes
    except ValueError:
        return 8 * 60


@dataclass
class Task:
    """Represents a single pet-care activity and its scheduling details."""

    description: str = "General task"
    duration_minutes: int = 10
    priority: int = 1
    scheduled_time: str = "08:00"
    frequency: str = "daily"
    due_date: date | None = None
    completed: bool = False
    category: str = "general"

    def __post_init__(self) -> None:
        """Ensure each task has a usable description and a due date."""
        if not self.description:
            self.description = "General task"
        if self.due_date is None:
            self.due_date = date.today()

    @property
    def title(self) -> str:
        return self.description

    @title.setter
    def title(self, value: str) -> None:
        self.description = value

    @property
    def preferred_time(self) -> str:
        return self.scheduled_time

    @preferred_time.setter
    def preferred_time(self, value: str) -> None:
        self.scheduled_time = value

    @property
    def is_recurring(self) -> bool:
        return self.frequency.lower() != "once"

    def update_details(self, title: str, duration: int, priority: int) -> None:
        """Update the core scheduling information for a task."""
        self.description = title
        self.duration_minutes = duration
        self.priority = priority

    def mark_completed(self) -> None:
        """Mark the task as complete."""
        self.completed = True

    def get_priority_score(self) -> int:
        """Return the task's priority score."""
        return self.priority

    def is_urgent(self) -> bool:
        """Return True when the task has high priority."""
        return self.priority >= 3


@dataclass
class Pet:
    """Represents a pet and the tasks associated with their care."""

    name: str
    species: str
    age: int = 0
    needs: List[str] = field(default_factory=list)
    tasks: List[Task] = field(default_factory=list)
    constraint: "Constraint | None" = None

    def add_task(self, task: Task) -> None:
        """Attach a task to the pet."""
        self.tasks.append(task)

    def remove_task(self, task: Task) -> None:
        """Remove a task from the pet's list."""
        if task in self.tasks:
            self.tasks.remove(task)

    def get_tasks_for_day(self) -> List[Task]:
        """Return a copy of the pet's current tasks."""
        return list(self.tasks)

    def get_pending_tasks(self) -> List[Task]:
        """Return the tasks that are still incomplete."""
        return [task for task in self.tasks if not task.completed]

    def complete_task(self, task: Task) -> Task | None:
        """Mark a task complete and create a next occurrence for recurring items with a simple date-based cadence."""
        if task not in self.tasks:
            return None

        task.mark_completed()

        if not task.is_recurring:
            return None

        interval_days = 1 if task.frequency.lower() == "daily" else 7
        next_due_date = (task.due_date or date.today()) + timedelta(days=interval_days)
        next_task = Task(
            description=task.description,
            duration_minutes=task.duration_minutes,
            priority=task.priority,
            scheduled_time=task.scheduled_time,
            frequency=task.frequency,
            due_date=next_due_date,
            category=task.category,
        )
        self.tasks.append(next_task)
        return next_task


@dataclass
class Owner:
    """Represents the pet owner and their pets."""

    name: str
    preferences: List[str] = field(default_factory=list)
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Register a pet with the owner."""
        if pet not in self.pets:
            self.pets.append(pet)

    def remove_pet(self, pet: Pet) -> None:
        """Remove a pet from the owner's care."""
        if pet in self.pets:
            self.pets.remove(pet)

    def get_pet_names(self) -> List[str]:
        """Return the names of all pets for this owner."""
        return [pet.name for pet in self.pets]

    def get_all_tasks(self) -> List[Task]:
        """Collect every task assigned to the owner's pets."""
        all_tasks: List[Task] = []
        for pet in self.pets:
            all_tasks.extend(pet.get_tasks_for_day())
        return all_tasks


@dataclass
class Constraint:
    """Describes scheduling boundaries for the day."""

    available_minutes: int = 120
    preferred_window: str = "morning"
    avoid_times: List[str] = field(default_factory=list)
    max_tasks_per_day: int = 5

    def can_fit(self, task: Task) -> bool:
        """Check whether the task fits within the daily limit."""
        return task.duration_minutes <= self.available_minutes

    def is_time_available(self, time: str) -> bool:
        """Check whether a time slot is not blocked."""
        return time not in self.avoid_times

    def matches_owner_preferences(self, owner: Owner) -> bool:
        """Check whether the preferred window matches the owner's preferences."""
        return self.preferred_window.lower() in [preference.lower() for preference in owner.preferences]


@dataclass
class ScheduledTask:
    """Represents a task placed into a daily schedule."""

    task: Task
    start_time: str
    end_time: str
    reason: str = ""
    completed: bool = False

    def mark_completed(self) -> None:
        """Mark this scheduled task as complete."""
        self.completed = True

    def get_duration(self) -> int:
        """Return the scheduled task's duration."""
        return self.task.duration_minutes


@dataclass
class DailyPlan:
    """Represents the final schedule for a day."""

    date: date
    scheduled_tasks: List[ScheduledTask] = field(default_factory=list)
    total_duration: int = 0
    explanation: str = ""

    def add_scheduled_task(self, scheduled_task: ScheduledTask) -> None:
        """Add a scheduled task to the daily plan."""
        self.scheduled_tasks.append(scheduled_task)
        self.total_duration += scheduled_task.get_duration()

    def explain_plan(self) -> str:
        """Return the plan explanation or a fallback message."""
        return self.explanation or "No explanation provided yet."

    def get_summary(self) -> str:
        """Return a short summary of the plan."""
        return f"{len(self.scheduled_tasks)} tasks planned for {self.date}"


class Scheduler:
    """Builds a simple daily task plan from owner and pet data."""

    def __init__(
        self,
        owner: Owner | None = None,
        constraints: Constraint | None = None,
        pet: Pet | None = None,
        tasks: List[Task] | None = None,
    ) -> None:
        self.owner = owner
        self.pet = pet
        self.constraints = constraints or Constraint()
        self.tasks = list(tasks or [])

        if self.owner is not None:
            self.tasks = self.owner.get_all_tasks()
        elif self.pet is not None:
            self.tasks = list(self.pet.get_tasks_for_day())

    def build_plan(self) -> DailyPlan:
        """Create a daily plan from the current tasks and constraints."""
        plan = DailyPlan(date=date.today())
        for scheduled_task in self.generate_schedule():
            plan.add_scheduled_task(scheduled_task)
        plan.explanation = "A priority-based plan was generated from the available pet-care tasks."
        return plan

    def get_conflict_warnings(self) -> List[str]:
        """Return lightweight warnings for tasks that share the same scheduled time without interrupting the plan."""
        warnings: List[str] = []
        tasks = self.get_available_tasks(include_completed=False)

        seen: List[tuple[str, str]] = []
        for task in tasks:
            key = (task.scheduled_time, task.description)
            if key in seen:
                continue
            seen.append(key)

        for index, first_task in enumerate(tasks):
            for second_task in tasks[index + 1 :]:
                if first_task.scheduled_time != second_task.scheduled_time:
                    continue
                message = (
                    f"Warning: '{first_task.description}' and '{second_task.description}' "
                    f"are both scheduled for {first_task.scheduled_time}."
                )
                if message not in warnings:
                    warnings.append(message)

        return warnings

    def get_available_tasks(
        self,
        pet_name: str | None = None,
        include_completed: bool = False,
    ) -> List[Task]:
        """Return the tasks available to the scheduler, optionally filtered by pet and completion status."""
        if self.owner is not None:
            tasks = []
            for pet in self.owner.pets:
                if pet_name and pet.name.lower() != pet_name.lower():
                    continue
                tasks.extend(pet.get_tasks_for_day())
            return [task for task in tasks if include_completed or not task.completed]
        if self.pet is not None:
            tasks = self.pet.get_tasks_for_day()
            return [task for task in tasks if include_completed or not task.completed]
        return [task for task in self.tasks if include_completed or not task.completed]

    def sort_by_time(self, tasks: List[Task] | None = None) -> List[Task]:
        """Return tasks sorted by their scheduled time in HH:MM format."""
        task_list = tasks if tasks is not None else self.get_available_tasks()
        return sorted(task_list, key=lambda task: _parse_time_to_minutes(task.scheduled_time))

    def sort_tasks_by_priority(self, pet_name: str | None = None, include_completed: bool = False) -> List[Task]:
        """Sort tasks so the highest-priority items are scheduled first, using time when available."""
        return sorted(
            self.get_available_tasks(pet_name=pet_name, include_completed=include_completed),
            key=lambda task: (
                _parse_time_to_minutes(task.scheduled_time),
                -task.get_priority_score(),
                task.duration_minutes,
            ),
        )

    def filter_tasks(self, tasks: List[Task], pet_name: str | None = None, include_completed: bool = False) -> List[Task]:
        """Filter tasks by pet name and completion status."""
        filtered_tasks: List[Task] = []
        for task in tasks:
            if pet_name and not self._task_belongs_to_pet(task, pet_name):
                continue
            if not include_completed and task.completed:
                continue
            filtered_tasks.append(task)
        return filtered_tasks

    def _task_belongs_to_pet(self, task: Task, pet_name: str) -> bool:
        """Check whether a task belongs to a pet with the given name."""
        if self.owner is None:
            return True
        for pet in self.owner.pets:
            if pet.name.lower() == pet_name.lower() and task in pet.tasks:
                return True
        return False

    def choose_tasks(self, pet_name: str | None = None, include_completed: bool = False) -> List[Task]:
        """Select the tasks that fit within the daily scheduling limits."""
        selected: List[Task] = []
        remaining_minutes = self.constraints.available_minutes

        for task in self.sort_tasks_by_priority(pet_name=pet_name, include_completed=include_completed):
            if len(selected) >= self.constraints.max_tasks_per_day:
                break
            if task.duration_minutes <= remaining_minutes and self.constraints.can_fit(task):
                selected.append(task)
                remaining_minutes -= task.duration_minutes

        return selected

    def generate_schedule(self, pet_name: str | None = None, include_completed: bool = False) -> List[ScheduledTask]:
        """Turn the selected tasks into a time-based schedule while avoiding overlaps."""
        schedule: List[ScheduledTask] = []
        current_minutes = 8 * 60

        for task in self.choose_tasks(pet_name=pet_name, include_completed=include_completed):
            preferred_start = _parse_time_to_minutes(task.scheduled_time)
            task_start = max(current_minutes, preferred_start)

            if schedule and preferred_start < self._get_schedule_end(schedule[-1]):
                continue

            if self._conflicts_with_schedule(schedule, task_start, task.duration_minutes):
                continue

            start_time = self._format_minutes(task_start)
            end_minutes = task_start + task.duration_minutes
            end_time = self._format_minutes(end_minutes)
            schedule.append(
                ScheduledTask(
                    task=task,
                    start_time=start_time,
                    end_time=end_time,
                    reason="Selected based on priority and available time.",
                )
            )
            current_minutes = max(current_minutes, end_minutes)

        return schedule

    def _format_minutes(self, minutes: int) -> str:
        """Convert minute values into HH:MM strings."""
        hours, mins = divmod(minutes, 60)
        return f"{hours:02d}:{mins:02d}"

    def _get_schedule_end(self, scheduled_task: ScheduledTask) -> int:
        """Return the end time of a scheduled task in minutes."""
        return _parse_time_to_minutes(scheduled_task.end_time)

    def _conflicts_with_schedule(self, schedule: List[ScheduledTask], start_minutes: int, duration_minutes: int) -> bool:
        """Return True when a task overlaps with an already scheduled item."""
        end_minutes = start_minutes + duration_minutes
        for scheduled_task in schedule:
            scheduled_start = _parse_time_to_minutes(scheduled_task.start_time)
            scheduled_end = _parse_time_to_minutes(scheduled_task.end_time)
            if start_minutes < scheduled_end and end_minutes > scheduled_start:
                return True
            if scheduled_start <= start_minutes < scheduled_end:
                return True
        return False
