# Refactor Label

# Refactor Label

## Purpose

The `Refactor` label is used to track refactoring and technical-debt work in GitLab.

Its purpose is to make refactoring effort visible over time, so we can better understand how much capacity we spend on internal code improvements.

## When to Use the Label

Create a new issue with the `Refactor` label whenever the main goal of the work is refactoring. This includes changes that improve code structure, readability, maintainability, or internal design without intentionally changing business behavior.

Use this label for work whose primary purpose is to reduce technical debt or improve the internal quality of the codebase in a measurable way.

## Small Refactors During Normal Development

Small refactors are still a normal part of development and should continue to happen continuously in the code you touch.

If something can be improved quickly and safely within the original scope, do it without extra process.

As a rule of thumb, create a separate `Refactor` issue when the work is no longer time-insignificant, takes roughly `30 minutes+`, or has broader consequences that should be prioritized explicitly.

The `30 minutes+` threshold is guidance, not a strict rule.

## When Refactoring Appears Inside Another Issue

If a larger refactor comes up during work on another issue, for example during implementation or code review, and it was not part of the original plan:


1. Inform your Product Owner about the extra scope and why it is needed.
2. Create a separate GitLab issue labeled `Refactor` so the work can be tracked.

This separate issue is required for tracking even if the refactor was discovered only during implementation or during CR.

## Merge Request Handling

A separate `Refactor` issue does not automatically require a separate Merge Request.

If it makes sense to keep the refactoring work in the original MR, do that. The main goal is to capture the data about refactoring effort, not to force unnecessary MR splits.

If the refactor is blocked by, or closely tied to, the original issue, keep the issue separate for tracking but allow the implementation to ship together when that is the cleaner solution.

In short: separate issue for tracking, separate MR only when it is actually useful.

## Summary

* Use `Refactor` for issues whose main purpose is refactoring or technical-debt reduction.
* Keep doing small incidental refactors as part of normal development.
* If a larger refactor appears inside another issue, inform the PO and create a separate `Refactor` issue.
* The work may still stay in the original MR if splitting the MR would be artificial.