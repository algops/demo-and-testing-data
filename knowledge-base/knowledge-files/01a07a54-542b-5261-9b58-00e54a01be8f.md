# Skill: Contract/template finder

> Organizace: **Meridian Pay a.s.** | Doména: **legal** | Typ: agent_skill | Citlivost: internal

## Workflow odpovědi

1. **Porozumění** — identifikuj záměr dotazu a dotčené KB sekce.
2. **Vyhledání** — prohledej:
- Prohledej `knowledgebase/legal/templates/core`
- Prohledej `knowledgebase/legal/compliance/core`
3. **Validace** — ověř proti iManage pokud jde o stav systému/recordů.
4. **Odpověď** — struktura: shrnutí → citace KB cesty → doporučený krok.
5. **Eskalace** — pokud chybí podklad, otevři handoff na supervizora.

## Použití nástrojů

- **OCR redaction LLM** — doplňkové akce dle oprávnění v chat-agent setup (execute_tool).
- Integrační data nikdy nepřepisují schválený text politik v KB.

## Formát citace

```
[KB: knowledgebase/legal/<section>/<sub>/<soubor>.md | verze core]
```

## Guardrails (operativní)

- Vždy upozorni na nutnost právního review před podpisem
- Nepoužívej archivované šablony bez kontroly verze

## Příklady interakcí

**Q:** Kde je šablona NDA?
**A:** (1) Najdi relevantní dokument v KB. (2) Cituj cestu a verzi. (3) Shrň odpověď pro uživatele.

**Q:** Která šablona platí pro IT služby?
**A:** (1) Najdi relevantní dokument v KB. (2) Cituj cestu a verzi. (3) Shrň odpověď pro uživatele.


## Kontrolní seznam kvality

- [ ] Odpověď má alespoň jednu KB citaci
- [ ] Guardrails dodrženy
- [ ] Žádné vymyšlené metriky nebo termíny
- [ ] Eskalace nabídnuta pokud data chybí
