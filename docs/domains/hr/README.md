# HR domain module

**`domain_id`:** `hr`  
**Anchor tenant:** [ANCHOR_TENANT.md](../../ANCHOR_TENANT.md)  
**Propozice (authoring):** [05_HR_SOP.md](../../05_HR_SOP.md) — §1 VTM is an example only

## Module scope

Meridian Pay people operations: policies, SOPs, employees, training, benefits. HR owns authoritative `employee` schema; `person` records live in org-layer (`shared`).

## Reframe from propozice

- No manufacturing sites — Praha HQ + Brno engineering hub only
- ~180–240 employees (not 310+)
- Single pracovní řád with Brno/Praha addenda (not VTM Olomouc clash)

## Volume targets (MVP)

30–45 policies, 35–55 processes, 180–240 employees, 8–12 departments.

## Org-bridge links

- `employee` → `person` (shared)
- `department` → Process, Role
- SuccessFactors `system` → HR integrations
