# Product Analytics

## PROJECT: Product Analytics Implementation for Propeller (Widget Funnel + End-User Behavior)

**Objective:**\nSet up PostHog tracking to capture, analyze, and visualize end-user (potential customers) interactions starting from the Propeller booking widget — to understand user behavior, optimize conversion, and support data-driven product decisions.


---

### **1. Project Scope**

* Track end-user journey starting from **widget interaction** up to **booking submission**.
* Include key events such as: widget load, date selection, boat selection, price view, CTA clicks, booking submission, and any drop-offs.
* Enable data flow to PostHog for real-time insights and funnel analysis.
* Deliver dashboards and event naming conventions for future scalability.


---

### **2. Team & Roles**

| Role | Person | Responsibilities |
|------|--------|------------------|
| **Project Lead** | Aga    | Project coordination, events definition, specs for dev, PostHog dashboards |
| **Project Support** | Kasia  | Tasks assigned by PL during each phase |
| **Project Support**   | Vale   | Tasks assigned by PL during each phase |
| **Developer** | TBD    | Implement event tracking in the widget, push to PostHog |
| **QA** | TBD    | Verify events fire correctly in staging/production |


---

### **3. Project Plan**

#### **Phase 1: Discovery & Definition (October)**

**Goal:** Define what we want to learn from user behavior

**Tasks:**

* Map user flow (Widget entry → Booking form → Payment)
* Identify core questions we want to answer
* Define success metrics
* Define event list (event names, properties, triggers)

**Deliverable:** Draft events document


---

#### **Phase 2: Implementation Planning (November)**

**Goals:** Prepare for tracking implementation

**Tasks:**

* Finalize events document
* Set naming conventions, property structure, and user/session identifiers
* Prepare specs for development

**Deliverable:** Specs for dev incl. final events document


---

#### **Phase 3: Implementation & QA (December)**

**Goals:** Tracking implementation

**Tasks:**

* Developer implements all events and tracking
* QA checks event firing via PostHog live events feed
* Validate key properties

**Deliverable:** Working event tracking in production


---

#### **Phase 4: Dashboard & Insights Setup (January)**

**Goal:** Create dashboards and funnels for continuous analysis

**Tasks:**

* Define and build PostHog dashboards
* Document/Train how to read dashboards
* Share dashboards with stakeholders

**Deliverable:** PostHog dashboards & funnels


---

#### **Phase 5: Review & Next Steps (March)**

**Goal:** Gather feedback and plan improvements

**Tasks:**

* Hold review session with Vale and Kasia
* Identify insights or gaps
* Prepare backlog of next steps


\