# Skill: Benefits eligibility guide

> Organizace: **Meridian Pay a.s.** | Doména: **hr** | Typ: agent_skill | Citlivost: internal

## Workflow odpovědi

1. **Porozumění** — identifikuj záměr dotazu a dotčené KB sekce.
2. **Vyhledání** — prohledej:
- Prohledej `knowledgebase/hr/operations/core`
- Prohledej `knowledgebase/hr/compliance/core`
3. **Validace** — ověř proti SAP SuccessFactors pokud jde o stav systému/recordů.
4. **Odpověď** — struktura: shrnutí → citace KB cesty → doporučený krok.
5. **Eskalace** — pokud chybí podklad, otevři handoff na supervizora.

## Použití nástrojů

- **LLM HR assistant** — doplňkové akce dle oprávnění v chat-agent setup (execute_tool).
- Integrační data nikdy nepřepisují schválený text politik v KB.

## Formát citace

```
[KB: knowledgebase/hr/<section>/<sub>/<soubor>.md | verze core]
```

## Guardrails (operativní)

- Nárok na benefity vždy ověř dle politiky a seniority
- Nezveřejňuj mzdové údaje jiných zaměstnanců

## Příklady interakcí

**Q:** Mám nárok na sick days?
**A:** (1) Najdi relevantní dokument v KB. (2) Cituj cestu a verzi. (3) Shrň odpověď pro uživatele.

**Q:** Kdy začíná nárok na stravenkový paušál?
**A:** (1) Najdi relevantní dokument v KB. (2) Cituj cestu a verzi. (3) Shrň odpověď pro uživatele.


## Kontrolní seznam kvality

- [ ] Odpověď má alespoň jednu KB citaci
- [ ] Guardrails dodrženy
- [ ] Žádné vymyšlené metriky nebo termíny
- [ ] Eskalace nabídnuta pokud data chybí
