# Role: Incident/runbook assistant

> Typ: agent_role | Doména: it | Citlivost: internal

## Role: Incident/runbook assistant

# 🚚 Releases

To facilitate swift and structured development, along with efficient product delivery, it's essential to automate and thoroughly document the release portion of the life cycle. 

This document delineates the procedures for executing new version releases.

# 🏷️ Issue Naming and Labeling

For each Release, an automated version of the Release log is compiled to aid in the creation of the final version, which is typically shared with the broader team using the product (client).

The automated version of the Release log is **assembled** **based on the titles of GitLab Issues**, which are tagged with a **Label** `State: On Main`. All these issues are considered part of this Release, as we are releasing what is currently on the `main` branch.

Therefore, the naming of the issues is crucial for creating an understandable Release log.

## Naming Conventions

The naming conventions for Issue titles should mirror those of Git commit messages and must adhere to the rules of Conventional Commits. Please refer to the ✉️ Commit Messages section in the Git Strategy document.

:::tip
Pay particular attention to the `<description>` part of the commit message. We do not want to include the `<scope>` in the Issue titles.

Additionally, Issue titles should always begin with a capital letter.

:::

<https://docs.gitlab.com/ee/development/changelog.html#writing-good-changelog-entries>

# 🚩 Create a Tag

The whole process of Release (including automatic Build, Test, Deploy, etc) is automated and **triggered by creating a Tag on the** `main` **branch**.

## Semantic Versioning

Adhere to the typical Semantic versioning convention: `v{MAJOR}.{MINOR}.{PATCH}` where:

* On **Regular** release, the `MINOR` number is raised
* On **Hotfix** release, only the `PATCH` version is raised

Major version is bumped only on special occasions. 

:::info
Please note that the name of the tag will become also the name of the Release on the Release log.

:::

# 🤖 The Automated Part

## Deployment

The application is automatically built, tests are executed, and the code is **deployed to both Production and Staging** environments.

## Issues Status

Upon successful completion of the Deployment, all Issues that bear the Label `State: On Main` will be automatically updated to feature the **Label** `State: On Production`.

## Automated Release Log

At this stage, a new Release is created in GitLab with the automatically compiled Release log, as outlined in the [Issue Naming and Labeling sec
