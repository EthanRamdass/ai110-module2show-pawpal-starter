from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from typing import List


@dataclass
class Task:
    """Represents a single pet-care activity and its scheduling details."""

    description: str = "General task"
    duration_minutes: int = 10
    priority: int = 1
    scheduled_time: str = "08:00"
    frequency: str = "daily"
    completed: bool = False
    category: str = "general"

    def __post_init__(self) -> None:
        """Ensure each task has a usable description."""
        if not self.description:
            self.description = "General task"

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

    def get_available_tasks(self) -> List[Task]:
        """Return the tasks available to the scheduler."""
        if self.owner is not None:
            return self.owner.get_all_tasks()
        if self.pet is not None:
            return self.pet.get_tasks_for_day()
        return list(self.tasks)

    def sort_tasks_by_priority(self) -> List[Task]:
        """Sort tasks so the highest-priority items are scheduled first."""
        return sorted(
            self.get_available_tasks(),
            key=lambda task: (-task.get_priority_score(), task.duration_minutes, task.scheduled_time),
        )

    def choose_tasks(self) -> List[Task]:
        """Select the tasks that fit within the daily scheduling limits."""
        selected: List[Task] = []
        remaining_minutes = self.constraints.available_minutes

        for task in self.sort_tasks_by_priority():
            if len(selected) >= self.constraints.max_tasks_per_day:
                break
            if task.duration_minutes <= remaining_minutes and self.constraints.can_fit(task):
                selected.append(task)
                remaining_minutes -= task.duration_minutes

        return selected

    def generate_schedule(self) -> List[ScheduledTask]:
        """Turn the selected tasks into a time-based schedule."""
        schedule: List[ScheduledTask] = []
        current_minutes = 8 * 60

        for task in self.choose_tasks():
            start_time = self._format_minutes(current_minutes)
            end_minutes = current_minutes + task.duration_minutes
            end_time = self._format_minutes(end_minutes)
            schedule.append(
                ScheduledTask(
                    task=task,
                    start_time=start_time,
                    end_time=end_time,
                    reason="Selected based on priority and available time.",
                )
            )
            current_minutes = end_minutes

        return schedule

    def _format_minutes(self, minutes: int) -> str:
        """Convert minute values into HH:MM strings."""
        hours, mins = divmod(minutes, 60)
        return f"{hours:02d}:{mins:02d}"
