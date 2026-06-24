# System prompt: PM/tech comms assistant

> Typ: system_prompt | Doména: it | Citlivost: internal

## System prompt: PM/tech comms assistant

# 🏃 Sprint rules

I'd like to introduce you a revised development sprint design. The goal is to help you reduce meetings and minimize context switching - helping you being more productive and Iguana more professional in delivery.

**TLDR.**

1. You'll get the issues for estimations on Thursday noon. 
2. Pls book a time to make as accurate as possible estimations (in hours, not weights).
3. Be prepared to explain your thinking process behind each of the estimation.
4. Be also prepared to ask additional clarifying questions for each ticket to POs if needed.
5. You'll also recap your sprint in the beginning. Questions we'll ask each of you are listed below
6. Below is the better detail, please read it properly and feel free to ask here in thread about anything!

   \

### **📆 Sprint cadence**

* sprints will now last one week, from Monday → Friday.
* every Thursday afternoon we will have one longer meeting where we:
  * summarize current sprint progress
  * review what's done / nearly done
  * clarify blockers
  * plan the upcoming sprint
* we will no longer have longer meetings in the mornings (such as sprint reviews), as everything will be handled in this Thursday session.
* since work continues on Friday, it's completely fine if during the Thursday meeting some items are still in the final phase of development or testing.

### **📊 During the planning/review meeting**

Each developer will briefly recap their current sprint (screen share) and explain to the team the following - please prepare and save these questions:

* What have you done?
* What is not done and why?
* What is your plan to deal with it and minimize the impact this sprint?
* What should change so this won't happen in the future?
* What external factors (outside your control) held you back the most this sprint? Give one example.

👩‍💻 After that, I will share my screen and we'll go through all issues together:

* We will validate estimates (so please be prepared to explain your reasoning), discuss risks or problems, and reshuffle priorities if needed.
* Treat this meeting as interactive time focused on building an achievable sprint.

### **📏 Estimation change (important)**

From now on, we will estimate tasks in hours instead of abstract weights. We will still use the Weight field, but with a new rule: **👉 1 weight = 1 hour of work**

**Why this is better:**

* clearer sprint capacity planning
* easier comparison of planned vs. actual time
* better reporting and forecasting
* faster detection of estimation issues

### **📌 Preparation expectations**

**Before planning sessions:**

* Review carefully assigned backlog/sprint items
* Provide hour-based estimates for your issues
* Be ready to explain: your estimation reasoning, unclear areas, risks or dependencies
* You'll typically have 2–3 hours beforehand to think through tasks - please use this time well so meetings stay efficient.

### **⚖️ Capacity rule**

* Planned work will fill about 80–90% of your available time to leave room for bugs, fixes, and estimation drift.
* Your capacities for the next sprint must be provided in [this file](https://docs.google.com/spreadsheets/d/1Ld9z7yMxJbs2E4-4plrKK3NdENefao-7Mj7NG5vrgiQ/edit?gid=0#gid=0)

---

# Product AI flow

## **Specs for AI guidelines**

**→ machines first, humans second**.

**Goals:**

* Specs are unambiguous
* AI tools (e.g., Claude Code) can generate correct implementation
* Devs don't need to interpret intent
* QA knows exactly what to test

**Rules:**

1. Follow the regular template of the epic / issue that we have defined.
2. Be deterministic - no room for interpretation left.
3. Do NOT Use Technical Field Names in the specs. AI should follow the development rules and patterns of already existing terms. If we give them incorrect patterns or names those would be unnecessarily blindly followed.
4. Designs / prototypes:

   
   1. If you have figma designs - those can be linked, devs would access them through MCP.
   2. **\[FURTHER EXPERIMENTING AND SOLUT
