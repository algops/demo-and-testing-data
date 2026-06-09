# Skill: Conflict-check helper

> Organizace: **Meridian Pay a.s.** | Doména: **legal** | Typ: agent_skill | Citlivost: internal

## Workflow odpovědi

1. **Porozumění** — identifikuj záměr dotazu a dotčené KB sekce.
2. **Vyhledání** — prohledej:
- Prohledej `knowledgebase/legal/operations/core`
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

- Při podezření na conflict okamžitě eskaluj
- Nikdy nepotvrzuj absenci střetu bez úplných dat

## Příklady interakcí

**Q:** Jak provést conflict check před novým mandatem?
**A:** (1) Najdi relevantní dokument v KB. (2) Cituj cestu a verzi. (3) Shrň odpověď pro uživatele.

**Q:** Kdy eskalovat na ethics committee?
**A:** (1) Najdi relevantní dokument v KB. (2) Cituj cestu a verzi. (3) Shrň odpověď pro uživatele.


## Kontrolní seznam kvality

- [ ] Odpověď má alespoň jednu KB citaci
- [ ] Guardrails dodrženy
- [ ] Žádné vymyšlené metriky nebo termíny
- [ ] Eskalace nabídnuta pokud data chybí
