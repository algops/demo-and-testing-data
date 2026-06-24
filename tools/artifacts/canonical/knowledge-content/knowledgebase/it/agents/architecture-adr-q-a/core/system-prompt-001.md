# System prompt: Architecture & ADR Q&A

> Typ: system_prompt | Doména: it | Citlivost: internal

## System prompt: Architecture & ADR Q&A

# Domain-Driven Design

## Table Of Contents

* Pros and Cons
* Fundamentals
  * Bounded Context
  * [Ubiquitous Language](/doc/ddd-kP6Cdim6em)
  * Domain
  * Events
  * Shared Kernel
  * Domain Types
  * Aggregates
  * DDD Structure
* Relevant Concepts
* Learning Material

## Pros and Cons

### Why DDD

* Separating logic into smaller managable parts, suited for complex lasting projects
* Performance & Scalability
* Clear communication and discussion

### Challenges

* Data synchronization
* Slower project kick-offs
* Requires educated/experienced team

## Fundamentals

DDD stays for Domain-Driven **Design**, it is not just a tech development approach, it specifies more than just programming concepts and principles. It defines processes in which whole team cooparates, including product department, design department, stakeholders, and whoever else is involved in the project.

The DDD premise, is that the whole development is driven by business, it separates business processes into contexts (like accounting, analytics, marketplace, etc.) which are independent and implement their own shared language (ubiquitous language).

This model is then reflected in the product via design and code, using the ubiquitous language and contexts separation.

### Bounded Context

The purpose of bounded contexts is to separate complex business into smaller managable parts. Each part is fully independent, which helps the team to focus on specific problems. Additionally, teams can define their own processes/tech-stack/development as they are fully independent from others.

:::info
This is a dramatic change from how usually monolith projects work and changing way of thinking takes more than just a day, sometimes helps trying to think of the bounded context as a project of it's own. And visualize them as separate boxes.

:::

So how to decide, what bounded contexts the business has and where to draw the line? Let's use [this analogy by Nick Tune](https://medium.com/nick-tune-tech-strategy-blog/domains-subdomain-problem-solution-space-in-ddd-clearly-defined-e0b49c7b586c). We have several areas our business deals with (e.g. payments, invoices, listing product, etc.) how do we decide how to categorize them into contexts?

 [image omitted]

 [image omitted]

There will always be some overlap and therefore the context boundaries might be a bit fuzzy. Remember, the business is driving the bounded contexts, and more departments can be interested in same area (like invoicing, for accounting and customer service) but both context have different way of interacting, they work with the resources in their own context, independently. Therefore, one system feature can be implemented in multiple bounded contexts but they are split by the business processes. For example, customer service can resend the invoice to customer, while accounting can invalidate the invoice. We must identify these use cases and split them into bounded contexts accordingly.

### Ubiquitous Language

Ubiquitous language is a set of terms that are used to describe the common language of the business **within the context**. Whole team must agree on it so it is consistent and understandable across all team roles. For example, accounting team must all understand that collecting money from a customer is called `Payment` as oppose to `Charge`, so product, design, development, and any other department involved in the process implement the correct term (nothing worse, than having different terms in frontend application, backend application, design, and specifications).

### Domain

We mentioned an "area" already few times. In DDD the bounded contexts consist of domains (*area of interest*), domain is a specific problematic that someone in the business deals with, domain are mainly used in tech development to organize the code into logical spaces. Good examples are invoices (in accounting bounded context), pricing (in marketplace bounded context), orders (ordering bounded context), customers (ordering b
