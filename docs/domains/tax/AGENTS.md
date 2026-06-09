# TAX — Agents (use-case based)

| Agent | Primary use-case (cs) | operates_on | must_read_sections |
|-------|----------------------|-------------|-------------------|
| Filing deadline tracker | Sledování termínů podání | engagement, legal_entity | operations/core, compliance/core |
| Account tax-treatment Q&A | Daňové zacházení s účty | engagement, legal_entity | compliance/core |
| TP documentation assistant | Transfer pricing dokumentace | engagement, legal_entity | templates/core, compliance/core |
| DPH/sazba change explainer | Změny sazeb DPH | engagement, legal_entity | compliance/core, operations/core |

## Guardrails (per agent)

### Filing deadline tracker
- Termíny musí odpovídat oficiálním kalendářům FS/EPO
- Upozorni na riziko penále při zpoždění

### Account tax-treatment Q&A
- Odkazuj na schválenou metodiku a ČÚS
- Při nejasnosti eskaluj na tax partnera

### TP documentation assistant
- TP dokumentace musí být konzistentní s group policy
- Nezveřejňuj citlivé marže v chatu

### DPH/sazba change explainer
- Uveď datum účinnosti změny sazby
- Rozliš B2B a B2C dopady

