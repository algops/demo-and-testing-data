# Skill: Architecture & ADR Q&A

> Typ: agent_skill | Doména: it | Citlivost: internal

## Skill: Architecture & ADR Q&A

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

The purpose of bounded contexts is to separate complex business into smaller managable parts. Each part is fully independent, which helps the team to focus on specific problems. Additionally, teams can define their own 
