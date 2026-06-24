# 🧬 Development Blueprint

# [🪵 Git Strategy](./Development%20Blueprint/Git%20Strategy.md)

We are currently using **Git flow** with *feature branches*, *develop* as a default branch, *staging* and *master* branches with similar server environments.

## Current limitations

We are sometimes developing **large features/epics** which takes **long time to develop** (we need to synchronize both backend and frontend), then after CRs are done, we are merging to develop, then to staging, testing as a whole on staging typically and then, when everything on staging is greenlit, we can proceed to **production deploy**.

For us to be not blocked by merging features to develop > staging > master at the right time, doing QA on the whole branch and being able to do a deploy, takes **a lot of planning** and sometimes still puts to a state, where some unfinished **features blocks releasing other features**, that are done and has QA passed.

The need of doing **hotfixes** also has a downside of merging the hotfix back to staging and develop as well. This solution is also prone to human mistakes, when a hotfix is not merged back to a develop and staging and can be lost on future production deploy.

We know, that we want to get to a Pods system (in Campiri), where **separate teams** will have separate agendas and current system will be even more complicated and will cause a lot more management overhead to maintain.

**Code Reviews** also tend to get accumulated and then takes as a long time to sort out and again block the whole pipeline and ability to deliver features and fixes fast. This is not necessarily dictated by the Git Strategy, but should be changed as well.

## Goals

* **Fast release pace**
  * We need to be able to release developed code fast, if needed, even couple times a day
  * Minimize or get rid of blocking times (as described in [Current limitations](https://praguelabs.getoutline.com/doc/the-iguana-dev-blueprint-FryatPvoSQ#h-current-limitations))
* **Quality**
  * We don't want to sacrifice quality in favor of quantity
  * Platform stability of running systems needs to stay on the same level or improve compared to the current state
  * Manual QA, UAT as well as larger involvement of [automated testing](https://praguelabs.getoutline.com/doc/the-iguana-dev-blueprint-FryatPvoSQ#h-🚦-tests) should be taken into consideration
  * Code Reviews system
* **Parallel development and delivery**
  * The new model needs to work for larger projects as well, where we want to have multiple Pods (teams separated by domains) with different agendas and sprints
* **Responsibility**
  * Developers needs to take responsibility for delivering quality product to production
* **Automation**
  * The whole methodic that is to be specified needs to take full automation into account using CI/CD
* **Standard and Conventional**
  * We don't want to invent the wheel. We want to take inspiration from existing strategies and implement something Conventional, that will allow us to onboard any new team members quickly and will not create a new burden of maintaining custom framework or methodic

## Tasks

- [x] Document complete Git strategy
  - [x] Branching strategy
    - [x] Developing smaller/short-lived and longer features
    - [x] Naming conventions
  - [x] Making Releases
  - [x] Making Hotfixes
  - [ ] Role of manual testing
  - [ ] Role of automated tests
  - [x] Code Reviews strategy
  - [x] Commit messages / squashing strategy + rebase strategy
  - [x] CI/CD strategy

## Remarks

Based on the research done until now, we know the best solution appears to be Trunk Based Development. This is a standard and proven solution. There are multiple sub-versions of TBD so we should take that into consideration while choosing the best solution.

Also Filip has shared with us his Git strategy, which is mostly aligned to TBD and I can share it on request for inspiration/validation.

# [🚚 Releases](./Development%20Blueprint/Releases.md)

Strategy for managing, doing and documenting releases/deploys.

## Goals

* **Versioning**
  * Publish to Sentry
    * We know on which build the exception happened
    * Sentry can show us the speed of adoption (frontend)
    * Sentry can suggest on which commit was the regression introduced
  * Have conventional release log
  * Tagging in git - can look up every release snapshot
* **Automation**
  * [Conventional Commits](https://www.conventionalcommits.org/) can help us automate most of the work with creating release notes
  * There are tools that can generate the release log documents. For example [release-it](https://github.com/release-it/release-it). It can work with GitLab API as well to create releases there.
  * Release log would probably need to be edited manually by a user before publishing to Slack, etc.
  * Publishing to Slack can be easily automated as well.
* **Testing**
  * Specify strict rules which needs to pass before any release

## **Questions?**

* **Planning**
  * Do we want to be still planning releases that are aligned to sprints or larger features or in the spirit of TBD, the trunk will be always releasable and there will be releases on almost daily basis?
* **Repository coordination**
  * Automating and versioning will be complicated on so many different repositories. [Single Repository](https://praguelabs.getoutline.com/doc/the-iguana-dev-blueprint-FryatPvoSQ/edit#h-✊-single-repository) might be the answer.

## Tasks

- [x] Version naming convention
- [x] Document exact flow of release process (technical and business as well)
- [x] Document best practices for release logs

# ✊ Single Repository

We want to consider using a single repository model for our projects. That means that all application, test and infrastructure code lives in one repository and is organized in folder structure.

## Structure

Folder structure is TBS, but the general idea is following (using Lightverse as an example):

* \[RepositoryName\]/
  * dotnet/
    * RestApi - default namespace \[RepositoryName\].RestApi
    * Runner - default namespace \[RepositoryName\].Runner
    * Core - default namespace \[RepositoryName\].Core
    * EmailTemplates
    * RestApi.Tests -  default namespace \[RepositoryName\].RestApi.Tests
    * Core.Tests -  default namespace \[RepositoryName\].Core.Tests
    * .sln
  * js/
    * admin/
    * public-web/
    * e2e-tests/
  * infrastructure/
    * app/
    * data-ops/
    * outline/
  * doc/
  * gitlab-ci.yml
  * README.md
  * CHANGELOG.md

## Motivations

* Ability to easier coordinate releases and versions (less overhead)
* Easier tasks management
* Ability to have unified executable specifications and tests reports throughout the whole project
* Ability to implement [monorepo](https://monorepo.tools/#what-is-a-monorepo) in the future

## Known complications

* From our previous experience we know that single repository combined with Git flow can cause complications with large merges, because you can stumble on conflicts that are not in your area of expertise. But we will mitigate this problem by design by implementing a new [Git strategy](https://praguelabs.getoutline.com/doc/the-iguana-dev-blueprint-FryatPvoSQ#h-🪵-git-strategy).

# [✍️ Specifications](./Development%20Blueprint/Specifications.md)

*WIP*

* short stories
* example mappings
* testing scenarios
* acceptance criteria
* BE to FE handover

# [🚦 Tests](./Development%20Blueprint/Tests.md)

*WIP*

* TDD - test should test code behavior, not how it is implemented
* Executable specifications
* Unified test reports

# Code style

* Backend
  * Currently blocked due to performance issues in *dotnet format* <https://github.com/dotnet/format/issues/757>
* Frontend

# DORA Metrics

* Metrics are indicators, not goal values

# Security

* Secrets
  * [Backend](https://iguana.wiki/doc/environment-variables-D1tq1h3v0f)
  * Frontend

# Static Analysis (SAST)

* help code review process