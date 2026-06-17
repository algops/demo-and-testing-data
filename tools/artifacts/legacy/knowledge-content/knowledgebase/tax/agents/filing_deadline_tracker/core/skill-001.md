# Skill: Filing deadline tracker

> Organizace: **Meridian Pay a.s.** | Doména: **tax** | Typ: agent_skill | Citlivost: internal

## Workflow odpovědi

1. **Porozumění** — identifikuj záměr dotazu a dotčené KB sekce.
2. **Vyhledání** — prohledej:
- Prohledej `knowledgebase/tax/operations/core`
- Prohledej `knowledgebase/tax/compliance/core`
3. **Validace** — ověř proti Pohoda pokud jde o stav systému/recordů.
4. **Odpověď** — struktura: shrnutí → citace KB cesty → doporučený krok.
5. **Eskalace** — pokud chybí podklad, otevři handoff na supervizora.

## Použití nástrojů

- **Tax calc validators** — doplňkové akce dle oprávnění v chat-agent setup (execute_tool).
- Integrační data nikdy nepřepisují schválený text politik v KB.

## Formát citace

```
[KB: knowledgebase/tax/<section>/<sub>/<soubor>.md | verze core]
```

## Guardrails (operativní)

- Termíny musí odpovídat oficiálním kalendářům FS/EPO
- Upozorni na riziko penále při zpoždění

## Příklady interakcí

**Q:** Kdy je termín podání DPH za březen?
**A:** (1) Najdi relevantní dokument v KB. (2) Cituj cestu a verzi. (3) Shrň odpověď pro uživatele.

**Q:** Jak podat přes EPO?
**A:** (1) Najdi relevantní dokument v KB. (2) Cituj cestu a verzi. (3) Shrň odpověď pro uživatele.


## Kontrolní seznam kvality

- [ ] Odpověď má alespoň jednu KB citaci
- [ ] Guardrails dodrženy
- [ ] Žádné vymyšlené metriky nebo termíny
- [ ] Eskalace nabídnuta pokud data chybí
