# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.

My initial design focused on a simple pet-care scheduling system with three core ideas: managing pet profiles, representing care tasks, and producing a daily plan from those tasks under a set of scheduling constraints.

- What classes did you include, and what responsibilities did you assign to each?

I included the following classes:

- Owner: represents the person managing the pet-care routine and keeps track of the pets they are responsible for.
- Pet: represents an individual animal and holds basic information such as name, species, age, and needs, along with the tasks associated with that pet.
- Task: represents one care activity, such as feeding, walking, or grooming, and stores attributes like duration, priority, and preferred time.
- Constraint: captures scheduling limits such as available daily minutes, preferred time windows, and times to avoid.
- ScheduledTask: represents a task once it has been placed into a daily schedule, including its start time, end time, and completion status.
- DailyPlan: acts as the container for the final plan for a day and tracks the scheduled tasks and total planned duration.
- Scheduler: is responsible for choosing which tasks to include and arranging them into a daily plan based on priority and constraints.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

I reviewed the skeleton in pawpal_system.py and the main feedback was that the first design was too abstract for implementation because it did not clearly show how tasks become an actual schedule. The biggest change was making the scheduling flow more explicit.

I adjusted the design so that the relationships are composition-based rather than inheritance-based: an Owner has Pets, a Pet has Tasks, and a Scheduler uses those tasks plus constraints to build a DailyPlan. I also introduced ScheduledTask as a separate class so the system could distinguish between a general care task and a task that has been placed into a specific time slot. This change made the logic easier to follow and reduced the risk of bottlenecks caused by trying to handle both task definition and scheduling inside one object.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

One tradeoff the scheduler makes is that it currently warns about tasks that share the exact same scheduled time, but it does not attempt a full overlap analysis for tasks that start at different times and run past each other. This keeps the conflict logic lightweight and easy to explain, which is reasonable for a small pet-care planner where the main goal is to catch obvious scheduling clashes rather than model every possible time-window edge case.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
