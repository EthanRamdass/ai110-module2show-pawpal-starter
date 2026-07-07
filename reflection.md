# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.

Pet tracker, Constraints, Daily Plan

- What classes did you include, and what responsibilities did you assign to each?

Pet Class (name, age, meds), Owner (pet registered), Tasks(walks, feeding, scheduling priority. grooming frequency), Daily Plan Class (Inherits from Tasks to genrate a time/task/duration/priority)

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

A strong critique of the initial design is that it named the right domain ideas, but it was still too abstract to guide implementation. The biggest issue is that the Daily Plan should not inherit from Task; a plan is a container for scheduled activities, not a type of task. The design also needs explicit support for scheduling behavior, such as time constraints, priorities, and task ordering. In practice, I would improve the model by introducing a Scheduler class, a Constraint class, and a ScheduledTask class so the system can represent both the task list and the generated plan clearly.

The main design change I would make is to shift from a simple inheritance-based model to a composition-based one. An Owner has Pets, a Pet has Tasks, a Scheduler creates a DailyPlan from those pieces, and the DailyPlan contains ScheduledTask objects that reference the original tasks.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

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
