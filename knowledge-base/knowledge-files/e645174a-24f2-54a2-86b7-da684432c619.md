# Runbook: Due diligence — fáze a checklist

> Organizace: **Meridian Pay a.s.** | Doména: **legal** | Typ: runbook | Citlivost: internal

## Přehled

Runbook popisuje operativní postup: **Runbook: Due diligence — fáze a checklist**. Používejte při incidentech, plánovaných oknech i ad-hoc eskalacích v doméně legal.

## Předpoklady

- Přístup do **iManage** a souvisejících systémů
- Role: operátor L2+ nebo on-call engineer
- Aktuální kontakty v PagerDuty / Slack `#oncall-legal`

## Kroky

### 1. Detekce a klasifikace

- Ověřte alert nebo ticket v monitoringu.
- Přiřaďte závažnost P1–P4 dle dopadu na zákazníky Meridian Pay a.s..

### 2. Stabilizace

- Izolujte dotčenou službu nebo datový tok.
- Zdokumentujte čas začátku incidentu (UTC).

### 3. Diagnostika

- Zkontrolujte logy a poslední deploye v integraci iManage.
- Porovnejte s posledním známým dobrým stavem (baseline dataset).

### 4. Náprava

- Aplikujte schválený rollback nebo hotfix dle SOP.
- Po obnově služby spusťte smoke testy.

### 5. Uzavření

- Aktualizujte ticket, přidejte timeline.
- Do 48 hodin post-mortem pro P1/P2.

## Eskalace

| Úroveň | Kontakt | Podmínka |
|--------|---------|----------|
| L1 | Service desk | První reakce |
| L2 | Domain on-call | P3+, neznámá příčina |
| L3 | Architekt / vendor | P1/P2, data loss risk |

## Přílohy

- Odkaz na dashboard v iManage
- Checklist pro handover mezi směnami
