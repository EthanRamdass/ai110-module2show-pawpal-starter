from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from typing import List


@dataclass
class Owner:
    """Represents the pet owner and their pets."""

    name: str
    preferences: List[str] = field(default_factory=list)
    pets: List["Pet"] = field(default_factory=list)

    def add_pet(self, pet: "Pet") -> None:
        self.pets.append(pet)

    def remove_pet(self, pet: "Pet") -> None:
        if pet in self.pets:
            self.pets.remove(pet)

    def get_pet_names(self) -> List[str]:
        return [pet.name for pet in self.pets]


@dataclass
class Pet:
    """Represents a pet and the tasks associated with their care."""

    name: str
    species: str
    age: int = 0
    needs: List[str] = field(default_factory=list)
    tasks: List["Task"] = field(default_factory=list)
    constraint: "Constraint | None" = None

    def add_task(self, task: "Task") -> None:
        self.tasks.append(task)

    def remove_task(self, task: "Task") -> None:
        if task in self.tasks:
            self.tasks.remove(task)

    def get_tasks_for_day(self) -> List["Task"]:
        return list(self.tasks)


@dataclass
class Task:
    """Represents a single pet-care task."""

    title: str
    category: str = "general"
    duration_minutes: int = 10
    priority: int = 1
    preferred_time: str = "morning"
    is_recurring: bool = False

    def update_details(self, title: str, duration: int, priority: int) -> None:
        self.title = title
        self.duration_minutes = duration
        self.priority = priority

    def get_priority_score(self) -> int:
        return self.priority

    def is_urgent(self) -> bool:
        return self.priority >= 3


@dataclass
class Constraint:
    """Describes scheduling boundaries for the day."""

    available_minutes: int = 120
    preferred_window: str = "morning"
    avoid_times: List[str] = field(default_factory=list)
    max_tasks_per_day: int = 5

    def can_fit(self, task: Task) -> bool:
        return task.duration_minutes <= self.available_minutes

    def is_time_available(self, time: str) -> bool:
        return time not in self.avoid_times

    def matches_owner_preferences(self, owner: Owner) -> bool:
        return self.preferred_window.lower() in [p.lower() for p in owner.preferences]


@dataclass
class ScheduledTask:
    """Represents a task placed into a daily schedule."""

    task: Task
    start_time: str
    end_time: str
    reason: str = ""
    completed: bool = False

    def mark_completed(self) -> None:
        self.completed = True

    def get_duration(self) -> int:
        return self.task.duration_minutes


@dataclass
class DailyPlan:
    """Represents the final schedule for a day."""

    date: date
    scheduled_tasks: List[ScheduledTask] = field(default_factory=list)
    total_duration: int = 0
    explanation: str = ""

    def add_scheduled_task(self, scheduled_task: ScheduledTask) -> None:
        self.scheduled_tasks.append(scheduled_task)
        self.total_duration += scheduled_task.get_duration()

    def explain_plan(self) -> str:
        return self.explanation or "No explanation provided yet."

    def get_summary(self) -> str:
        return f"{len(self.scheduled_tasks)} tasks planned for {self.date}"


class Scheduler:
    """Builds a simple daily task plan from a pet, tasks, and constraints."""

    def __init__(self, pet: Pet, tasks: List[Task], constraints: Constraint):
        self.pet = pet
        self.tasks = tasks
        self.constraints = constraints

    def build_plan(self) -> DailyPlan:
        plan = DailyPlan(date=date.today())
        for scheduled_task in self.generate_schedule():
            plan.add_scheduled_task(scheduled_task)
        plan.explanation = "A simple priority-based plan was generated."
        return plan

    def sort_tasks_by_priority(self) -> List[Task]:
        return sorted(self.tasks, key=lambda task: (-task.get_priority_score(), task.duration_minutes))

    def choose_tasks(self) -> List[Task]:
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
        hours, mins = divmod(minutes, 60)
        return f"{hours:02d}:{mins:02d}"
