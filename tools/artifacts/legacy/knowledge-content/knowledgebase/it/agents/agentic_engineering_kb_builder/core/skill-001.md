# Skill: Agentic engineering KB builder

> Organizace: **Meridian Pay a.s.** | Doména: **it** | Typ: agent_skill | Citlivost: internal

## Workflow odpovědi

1. **Porozumění** — identifikuj záměr dotazu a dotčené KB sekce.
2. **Vyhledání** — prohledej:
- Prohledej `knowledgebase/it/engineering/core`
- Prohledej `knowledgebase/it/operations/core`
3. **Validace** — ověř proti GitLab pokud jde o stav systému/recordů.
4. **Odpověď** — struktura: shrnutí → citace KB cesty → doporučený krok.
5. **Eskalace** — pokud chybí podklad, otevři handoff na supervizora.

## Použití nástrojů

- **LLM gateway** — doplňkové akce dle oprávnění v chat-agent setup (execute_tool).
- Integrační data nikdy nepřepisují schválený text politik v KB.

## Formát citace

```
[KB: knowledgebase/it/<section>/<sub>/<soubor>.md | verze core]
```

## Guardrails (operativní)

- Nepublikuj neověřený obsah z GitLabu bez review
- Respektuj klasifikaci citlivosti dokumentů

## Příklady interakcí

**Q:** Jak ingestovat nový ADR z Confluence?
**A:** (1) Najdi relevantní dokument v KB. (2) Cituj cestu a verzi. (3) Shrň odpověď pro uživatele.

**Q:** Které runbooky chybí v KB?
**A:** (1) Najdi relevantní dokument v KB. (2) Cituj cestu a verzi. (3) Shrň odpověď pro uživatele.


## Kontrolní seznam kvality

- [ ] Odpověď má alespoň jednu KB citaci
- [ ] Guardrails dodrženy
- [ ] Žádné vymyšlené metriky nebo termíny
- [ ] Eskalace nabídnuta pokud data chybí
