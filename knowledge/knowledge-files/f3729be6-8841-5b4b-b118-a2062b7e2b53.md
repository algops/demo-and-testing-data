# System prompt: Agentic engineering KB builder

> Typ: system_prompt | Doména: it | Citlivost: internal

## System prompt: Agentic engineering KB builder

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

Every new feature should be developed as separate issue in it's own branch

* Branch name is always in format `feat/{issue-id}-{issue-name}`
  * Example: `feat/1786-availability-calendar`
  * GitLab -> Settings -> Repository -> Branch default -> Set Branch name template to feat/%{id}-%{title}

At the end of development every branch has to pass code review from BE or FE or from both.

## **Hotfix branches**

The process is the same as with the Feature branches. 

* Resolving Hotfixes has higher priority than the Feature branches
* Branch name is always in format `fix/{issue-id}-{issue-name}`
* Fix has to be covered by new test!
* Issue Assignee should deploy the fix to the Production

# ↩️ Merge Requests

Because everything should be **Code Reviewed** and tested before deploying to the production, every Feature branch should be merged to `main` via Merge Request (MR).

## Merge Request Roles

1. **Issue Assignee**

   Developer of the Issue, is responsible to implement the issue and resolve all the feedback from the *Reviewer*. 
   * There might be multiple developers assigned to the issue. For example one from BE and one from FE.
   * If there is multiple developers it's important to assign every merge request comment/feedback to one of them.
2. **MR Assignee**\nMerge Request Assignee is responsible for the entire feature. The assignee performs the last final tests and merges the branch to the `main`. 

   [image omitted]
   * Assignee of the MR is not necessarily always the same person as the Assignee of Issue
     * For example the Issue might be developed by a junior developer and the *MR Assignee* should be a more experienced developer.
   * *MR Assignee* is responsible for running all the tests (and possibly blames the *Reviewer*)
   * He should mark the Issue with label `State: 4. On Main` when he merges the MR to `main`.
3. **Reviewer**\nChecks if the code is well structured and the implementation follows specification.

##  [image omitted]How to create a Merge Request (MR)

Merge request can be created either **from Issue** detail (using *Create merge request* button). The button automatically creates Branch and redirects you to Merge Request form.

Or you can create everything **manually**:

1. Create the branch using git
2. Create the MR in GitLab
3. Link the MR to Issue

### Merge Request requirements

1. The **Branch** must be **named correctly (see above****).**
2. The Merge Request **status** must be tracked with **Label** `CR State` to reflect in
