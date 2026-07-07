# Skill: Agentic engineering KB builder

> Typ: agent_skill | Doména: it | Citlivost: internal

## Skill: Agentic engineering KB builder

# 🪵 Git Strategy

# 💡 The `main` Idea

The main idea is that there is only one protected `main` branch. This branch contains code that has been thoroughly tested, [code reviewed](#h-code-reviews), and is considered stable and ready for deployment to production at any time. All developers create feature or hotfix branches as needed, and these branches are merged directly into the `main` branch. There are no separate development or staging branches in this approach.

 [image omitted]

## **Single Repository**

We will use a single repository that will contain all code for the project, including frontend, backend, and infrastructure. The structure of the repository is described in the Blueprint document. The main reason for using a single repository is to better sync changes between teams.

# 🪵 Branches

The new Strategy is inspired by [**Trunk Based Development**](https://trunkbaseddevelopment.com/)**.** The Trunk is in our case called `main`.

The only types of branches which are allowed to be created are **Feature and Hotfix branches**. Both work basically the same. We do not use *Release branches*! The deploys are done directly from the Trunk.

The main goal is to have **small and short-lived branches** and thus being able to do **releases fast and often**. We do not have a hard limit set for how long the branch can live, but the goal is to strive for atomic tasks. This is journey begins with creating smaller Issues in the specification phase.

## **Feature branches**

Every
