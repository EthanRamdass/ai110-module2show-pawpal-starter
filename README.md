# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

The following terminal output was produced by running the sample script in main.py:

```text
Today's Schedule
================
1. 08:00 - 08:20 | Morning walk (20 min, priority 3)
2. 08:20 - 08:45 | Play session (25 min, priority 3)
3. 08:45 - 08:55 | Feed breakfast (10 min, priority 2)
4. 08:55 - 09:10 | Grooming (15 min, priority 1)
```

## 🧪 Testing PawPal+

```bash
# Run the full test suite:
pytest

# Run with coverage:
pytest --cov
```

Sample test output:

```
# Paste your pytest output here
```

## 📐 Smarter Scheduling

PawPal+ now includes a lightweight scheduling layer that helps the app choose, order, and review pet-care tasks without overcomplicating the logic.

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Sorting behavior | `Scheduler.sort_by_time()` | Orders pending tasks by their preferred clock time so the plan reads naturally from morning to evening. |
| Filtering behavior | `Scheduler.filter_tasks()` and `Scheduler.get_available_tasks()` | Lets the scheduler focus on a specific pet or exclude completed tasks before planning. |
| Conflict detection logic | `Scheduler.get_conflict_warnings()` | Detects tasks that share the same scheduled time and reports a warning instead of crashing. |
| Recurring task logic | `Pet.complete_task()` | Marks a recurring task complete and creates the next occurrence for daily or weekly care items. |

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
