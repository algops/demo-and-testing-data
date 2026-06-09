# LEGAL — Agents (use-case based)

| Agent | Primary use-case (cs) | operates_on | must_read_sections |
|-------|----------------------|-------------|-------------------|
| In-house know-how copilot | Interní právní know-how | matter, contract | compliance/core, operations/core |
| Contract/template finder | Vyhledávání smluv a šablon | contract, matter | templates/core, compliance/core |
| DD progress assistant | Sledování due diligence | matter, contract | operations/core |
| Conflict-check helper | Kontrola střetu zájmů | matter, contract | operations/core, compliance/core |
| Legislative update summarizer | Shrnutí legislativních změn | matter, contract | compliance/core, compliance/drafts |

## Guardrails (per agent)

### In-house know-how copilot
- Neposkytuj závazné právní stanovisko bez attorney review
- Cituj pouze schválené interní dokumenty

### Contract/template finder
- Vždy upozorni na nutnost právního review před podpisem
- Nepoužívej archivované šablony bez kontroly verze

### DD progress assistant
- Nezveřejňuj DD materiály mimo oprávněné spisy
- Eskaluj chybějící fáze DD na matter lead

### Conflict-check helper
- Při podezření na conflict okamžitě eskaluj
- Nikdy nepotvrzuj absenci střetu bez úplných dat

### Legislative update summarizer
- Rozliš návrh zákona od účinné verze
- Vždy uveď datum účinnosti a zdroj

