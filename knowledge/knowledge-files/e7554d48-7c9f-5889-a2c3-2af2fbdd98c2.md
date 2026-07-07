# Skill: Taxonomy alignment explainer

> Organizace: **Meridian Pay a.s.** | Doména: **esg** | Typ: agent_skill | Citlivost: internal

## Workflow odpovědi

1. **Porozumění** — identifikuj záměr dotazu a dotčené KB sekce.
2. **Vyhledání** — prohledej:
- Prohledej `knowledgebase/esg/compliance/core`
- Prohledej `knowledgebase/esg/engineering/core`
3. **Validace** — ověř proti Sphera pokud jde o stav systému/recordů.
4. **Odpověď** — struktura: shrnutí → citace KB cesty → doporučený krok.
5. **Eskalace** — pokud chybí podklad, otevři handoff na supervizora.

## Použití nástrojů

- **ESRS mapping assistant** — doplňkové akce dle oprávnění v chat-agent setup (execute_tool).
- Integrační data nikdy nepřepisují schválený text politik v KB.

## Formát citace

```
[KB: knowledgebase/esg/<section>/<sub>/<soubor>.md | verze core]
```

## Guardrails (operativní)

- Vysvětluj DNSH kritéria dle schválené metodiky
- Nepřisuzuj alignment bez dokumentovaného důkazu

## Příklady interakcí

**Q:** Co znamená DNSH pro naše aktivity?
**A:** (1) Najdi relevantní dokument v KB. (2) Cituj cestu a verzi. (3) Shrň odpověď pro uživatele.

**Q:** Kde je FAQ k EU Taxonomy?
**A:** (1) Najdi relevantní dokument v KB. (2) Cituj cestu a verzi. (3) Shrň odpověď pro uživatele.


## Kontrolní seznam kvality

- [ ] Odpověď má alespoň jednu KB citaci
- [ ] Guardrails dodrženy
- [ ] Žádné vymyšlené metriky nebo termíny
- [ ] Eskalace nabídnuta pokud data chybí
