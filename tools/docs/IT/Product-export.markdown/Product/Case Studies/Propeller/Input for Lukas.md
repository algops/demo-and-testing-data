# Input for Lukas

# ==Business Case: Propeller SaaS==

## ==Context==

==Propeller is a production SaaS platform for boat rental businesses, built by Iguana. The goal is to write a **structured case study outline** (section headings + bullet points) for the Iguana website, targeting **potential clients** (business owners / CTOs evaluating Iguana as a development partner). The emphasis is on **product scope**, **business outcomes**, and **technical complexity**.==


---

## ==Output==

==A single structured Markdown file:== `docs/business-case-propeller.md` ==(not committed to the repo — just created locally for copy-paste into the agency site CMS).==


---

## ==Outline Structure==

### ==1. Hero / Summary==

* ==Client challenge in one line==
* ==What Iguana built==
* ==Key impact statement (e.g. "End-to-end SaaS replacing multiple manual tools")==

### ==2. The Challenge==

* ==Boat rental businesses struggle to coordinate fleet availability, multi-channel bookings, sales CRM, and payment reconciliation across fragmented tools==
* ==No off-the-shelf solution handles the full lifecycle: listing → booking → contract → payment → owner payout==
* ==Client needed a scalable, multi-account SaaS (not a custom one-off app)==
* ==Multi-market: EU compliance, VAT, multiple currencies, international payment processors==

### ==3. What We Built — Product Scope==

==Organized around the 4 bounded contexts:==

#### ==Fleet Management==

* **==Boat inventory with specifications, photos, descriptions, locations==** ==Each boat is modelled as a rich entity covering technical specs (capacity, length, number of bathrooms, crew requirements), multilingual descriptions, photo galleries, and precise geolocation via PostGIS. Operators can manage an unlimited number of vessels from a single dashboard, and every detail is surfaced accurately to customers at the point of booking.==
* **==Availability calendar management==** ==A calendar-based scheduling system lets operators block dates, define seasonal windows, and manage real-time availability per vessel. This eliminates double-bookings and gives both the operations team and end-customers an accurate, live view of what is available and when.==
* **==Pricing models: base, seasonal/calendar, promotional codes, add-ons==** ==The pricing engine supports layered rules: a base rate per boat, calendar-driven seasonal adjustments, time-limited promotional codes, and a configurable catalogue of add-on extras (e.g. fuel, skipper, catering). This flexibility lets operators run sophisticated yield-management strategies without any code changes.==
* **==Owner management and commission structures==** ==For businesses that aggregate boats from multiple private owners, Propeller tracks each owner's fleet, calculates their revenue share automatically based on configured commission rates, and feeds the correct amounts into the payout engine. This removes the need for manual owner settlement calculations at the end of each month.==

#### ==Booking & Distribution==

* **==Full booking lifecycle: inquiry → offer → booking → contract → fulfilment==** ==Propeller manages every stage of a booking from first contact to completed trip. Sales teams can create draft offers for customers, convert them to confirmed bookings, attach a legally binding contract, and track fulfilment status — all within a single workflow. This end-to-end visibility reduces handoff errors between sales, operations, and finance.==
* **==Multi-channel distribution: direct, agents, brokers, ambassadors, form leads==** ==The platform supports five distinct distribution channels, each with its own commission logic and attribution tracking. A sailing charter company can simultaneously sell directly to consumers, through travel agencies, via broker networks, and through brand ambassadors — with Propeller automatically attributing the booking to the right channel and calculating the correct fees.==
* **==Skipper / crew assignment==** ==When a booking requires a licensed skipper or additional crew, Propeller manages the assignment within the booking record. This ensures compliance with safety regulations and gives operations teams a clear view of crew allocation across the fleet calendar.==
* **==Contract generation with e-signature workflow==** ==Rental agreements are generated automatically from booking data and sent to customers for digital signature. This eliminates manual document preparation, reduces turnaround time from days to minutes, and produces a legally traceable audit trail for every booking.==
* **==Embeddable booking widget for third-party websites==** ==Operators and their distribution partners can embed a fully functional booking widget on any external website with a single script tag. The widget connects live to Propeller's API, so availability and pricing are always accurate, and completed bookings flow directly into the platform without manual data entry.==

#### ==CRM & Lead Management==

* **==Embeddable lead capture widget==** ==A lightweight, configurable form widget can be embedded on any marketing page or partner site. Submitted leads are instantly created in Propeller with structured data (trip preferences, dates, group size), ready for the sales team to action — replacing email inboxes as the primary lead channel.==
* **==Lead lifecycle (New → Working → Closed Sold/Lost)==** ==Every lead moves through a defined pipeline with status tracking, so sales managers have real-time visibility into what the team is working on and where deals are being won or lost. The structured lifecycle also makes it possible to set SLA targets for response times at each stage.==
* **==Sales agent assignment, internal notes, activity tracking==** ==Leads and customers are assigned to individual sales agents, with a full activity log of every note, status change, and communication. This gives managers accountability data and ensures that when a salesperson is absent, any colleague can pick up the conversation with full context.==
* **==Bidirectional messaging: unified email + SMS thread per customer (SendGrid + Twilio)==** ==Rather than switching between an email client and a messaging tool, sales agents send and receive both email and SMS messages from a single threaded view inside Propeller. Inbound emails (via SendGrid inbound parsing) and inbound SMS replies (via Twilio webhooks) are automatically matched to the correct customer record and appended to the thread.==
* **==Lead conversion statistics and KPI dashboards==** ==The platform aggregates lead volume, conversion rates, response times, and revenue per channel into dashboards and CSV exports. Sales leadership can track team performance and channel ROI without pulling data manually from separate systems.==

#### ==Payments & Finance==

* **==Multiple payment processors: Stripe, Authorize.net, WorldPay, manual/external==** ==Propeller integrates with four payment methods, allowing operators to accept online card payments through their preferred gateway while also recording cash or bank-transfer payments made outside the platform. This flexibility accommodates the diverse payment habits of international charter customers.==
* **==Take-rate calculation (platform cut, owner share, agent commission)==** ==Every payment is automatically split according to configured take-rates: Propeller's platform fee, the boat owner's revenue share, and any agent or broker commission. The calculation happens in real time at payment confirmation, eliminating the spreadsheet reconciliation that previously happened at month-end.==
* **==Payout management and reconciliation==** ==The finance module tracks what is owed to each owner and agent, generates payout records, and provides a reconciliation view showing paid vs. outstanding balances. Finance teams can identify discrepancies immediately rather than discovering them weeks later.==
* **==Balance-based payments, refunds, voids==** ==Customers can hold a credit balance on the platform (e.g. from a cancelled trip), which can be applied to future bookings. The system also handles partial and full refunds, and payment voids, with full audit trails.==
* **==VAT/tax handling for EU markets==** ==Propeller applies country-specific VAT rules to financial reports, ensuring that operators in Spain and other EU markets produce compliant documentation. Tax rates are configurable per market, so the platform can expand to new countries without code changes.==

### ==4. Business Outcomes==

* ==Replaced a patchwork of spreadsheets and manual processes with one unified platform==
* ==Multi-account SaaS model allows the client to onboard new fleet operators without custom work==
* ==Embeddable widgets enable distribution through the client's agent/broker network without rebuilding external websites==
* ==Automated commission and payout calculations eliminate manual financial reconciliation==
* ==Bidirectional messaging (email + SMS) in one thread reduces customer communication overhead for sales teams==
* ==Lead-to-booking funnel is now measurable end-to-end==

### ==5. Technical Highlights (for CTOs)==

* **==Architecture==**==: Domain-Driven Design with 4 bounded contexts; CQRS pattern separating reads and writes==
* **==Backend==**==: .NET 8 / ASP.NET Core, PostgreSQL + PostGIS (geolocation queries)==
* **==Frontend==**==: Next.js 13+ / TypeScript in a Turborepo monorepo (Admin app, Public booking app, embeddable CRM widget)==
* **==Integrations==**==: Stripe, Authorize.net, WorldPay, SendGrid (email + inbound parsing), Twilio (SMS + delivery tracking)==
* **==Background processing==**==: Hangfire for scheduled jobs, payout runs, contract generation==
* **==Scalability==**==: Multi-tenant architecture; generated API clients from OpenAPI spec; event-driven cross-context communication==

### ==6. Iguana's Approach (optional section)==

* ==Domain workshops to map out bounded contexts and ubiquitous language before writing a line of code==
* ==CQRS from day one to keep read-side performance separate from write-side complexity==
* ==Modular monorepo frontend so the team can ship the admin, public, and widget apps independently==
* ==Code review standards documented as living rules (==`be.md`==,== `fe.md`==) embedded in the repo==

### ==7. Call to Action==

* =="Building a SaaS platform? Let's talk."==
* ==Link to contact / discovery call==