# IT — Agents (use-case based)

| Agent | Primary use-case (cs) | operates_on | must_read_sections |
|-------|----------------------|-------------|-------------------|
| Agentic engineering KB builder | Budování znalostní báze z GitLab a Confluence | service, adr | engineering/core, operations/core |
| Automated code review copilot | Automatizované code review a Snyk nálezy | service, incident | compliance/core, operations/core |
| Incident/runbook assistant | Asistence při incidentech a runboocích | incident, service | operations/core |
| Architecture & ADR Q&A | Dotazy na ADR a architekturu | adr, service | engineering/core |
| PM/tech comms assistant | Shrnutí technických rozhodnutí do Slacku | service, team | engineering/core, operations/core |

## Guardrails (per agent)

### Agentic engineering KB builder
- Nepublikuj neověřený obsah z GitLabu bez review
- Respektuj klasifikaci citlivosti dokumentů

### Automated code review copilot
- Nikdy neobcházej security gate ani merge pravidla
- Nezveřejňuj secrets ani tokeny z diffů

### Incident/runbook assistant
- Při P1/P2 vždy eskaluj na on-call lead
- Neposkytuj rollback bez schváleného runbooku

### Architecture & ADR Q&A
- Odkazuj pouze na přijaté ADR v KB
- Nenavrhuje architekturu mimo schválené patterny

### PM/tech comms assistant
- Shrnutí musí obsahovat odkaz na zdrojový ADR nebo ticket
- Nešíř interní security detaily na veřejné kanály

