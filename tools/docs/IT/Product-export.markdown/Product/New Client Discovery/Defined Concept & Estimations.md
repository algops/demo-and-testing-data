# Defined Concept & Estimations

The most wanted information by a client is how much is it gonna cost him and how long it's gonna take, to develop a new system/adjust the one they already have.

It takes effort and a lot of discovery to come up with a realistic estimation. In this document you can find some guidelines on how to achieve that.

At the end of this phase you need to produce the following


1. Discover the product needs
2. Deep-dive into each User-flow
3. Define the MVP (high-level + draft specs)
4. Estimate effort & Draw a Roadmap (timeline for implementation)
5. Name a price
6. AI Prototypes



---

## 1. Discover the Business needs


To be able to define the MVP you need to understand the clients needs and focus a lot on the users (who are they and what do they need).

> 🤝To do so, a one-time longer sessions with the client (ideally in person) shall be conducted. Follow this help-tool to remember to ask the right questions.

### User Journeys

* \[PURCHASE\] Describe the full flow, from point of view of the customers, to make a purchase
* \[PURCHASE\] Describe the full flow, from point of view of your internal users (back-office), to manage the purchase which the customer wants to make
* Describe the full flow, from point of view of the customers, when browsing your web/application. Why are they there in the first place?
* What is a conversion for your customers?
* Describe the full flow, from point of view of your back-office users: what they are trying to achieve/manage? Why are they there?
* How many user types do you have? what are their names? what are their roles & responsibilities?

### User Stories

* Describe the smallest action a customer wants to do
* Describe who your customer is? Do you have personas? E.g. John, 27yo, wants to go on a roadtrip with his girlfriend and a dog across Europe.
* What are the most common tasks that your internal users (back-office staff) need to perform daily?
* How does their day look like?
* Give as many user stories for each type of back-office users.

### Pain Points

* Think of the steps which require the biggest amount of manual work: do not solution, just list them in as much details as possible

### Features

* Is there something the customer is lacking?
* Is there something your internal users are currently unable to do? some specific action or analysis?

### Data, users

* What type of data do you currently manage (e.g., customer data, vehicle data, rental history, pictures)?
* Do different types of users have or need to have different permissions or access levels (e.g., admins, managers, customer support)?

### Traffic

* What is the amount of inquiries/purchases you receive daily/weekly/monthly/yearly?
* Do you have high / low / mid seasons? If yes, when?
* Do you have conversion goals? if yes, specify.
* Do you expect traffic to grow significantly? How fast is your company scaling?

### Mobile

* Do you require mobile or offline capabilities for the back-office system? Or will the back-office system be primarily used on desktop?

> **✅ outcome:** You know all the user stories, flows and understand what each user is supposed to do, and what they struggle with.

### Outcome: User Flows definition

You should now have:


1. a List all users types
2. a List of user stories for all users
3. a List of user journeys for all users
4. user flow diagrams



---

## 2. Deep-dive into each User-flow


### Business Requirements


1. For each user flow, gather as much information as possible from the client

> ❗ Each user flows needs deep diving with the client. It's best to have 1 session = 1 user flow to be as focused as possible and gather as many information as possible



---

## 3. Define the MVP


### Map each flow to a solution (can be a specific interface, or a feature)


1. Draw architectural concept 
2. For each user flow, define the solution (conceptually)

> 🧠 these 2 steps, consist of a series of internal PRDs where each user flow is solutioned across multiple departments

Now you have a list of user flows and a list of solutions to each. **NOTE: solutions can overlap**. Example: adding new cars to the system, and checking which cars have been sold the most, can be handled in 1 interface


3. List the interfaces that solve all the user needs
4. Map each user need (or user flow) to the relevant interface



---

## 4. Estimate effort & Draw the Roadmap



1. Take all the interfaces that you have listed in the above step, and order them by priority
2. Estimate effort for each of the interfaces
3. Add effort for the project setup (infra, db, etc.)
4. Keep into account dependencies, resources (how many developers, backend, frontend, designer, PO etc) and write them for each interface
5. Now puzzle up the tasks with the resources, based on priority, effort and dependencies
6. You will obtain a roadmap, which means a list of tasks, distributed in time, with total amount of effort, and overlapping periods.



---

## 5. Name a price


* Sum up all the effort you have estimated in the step above, and you have a price.

> ⏰ Remember: Timeline and price are 2 different things. There may be overlaps between tasks, for example, while developers are working on feature 1, Product Owner and Designer should be working already on feature 2, etc.



---


\

\