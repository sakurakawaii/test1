# EventBridge Migration Status Tracker

**Maintained by:** Sofia Andrade (Platform Engineering)  
**Last updated:** 2026-07-01  
**Note:** This tracker is updated periodically. For the most current status on any integration, contact #platform-eng.

---

| Service | Owner Team | PiSync Topics | Auth Type | Migration Status | Target Date | Notes |
|---|---|---|---|---|---|---|
| CS Tooling | Customer Success Eng | account.updated, account.status_changed | OAuth2 | Complete | — | Migrated June 2026 |
| Billing Sync | Finance Eng | billing.invoice_issued, billing.payment_received | OAuth2 | In Progress | Sep 2026 | OAuth2 in place, endpoint migration in progress |
| Analytics Dashboard | Data Eng | account.updated, billing.invoice_issued | API Key | In Progress | Q4 2026 | Auth migration blocked on IAM provisioning |
| Payment Gateway Webhooks | Payments Eng | billing.payment_received, account.status_changed | OAuth2 | In Progress | Aug 2026 | — |
| Risk Alerts Service | Risk Eng | risk.alert_raised | OAuth2 | In Progress | Q4 2026 | Validation changes in review |
| Partner Notification Feed | Partner Eng | partner.event | API Key | Maintenance | — | Under review for deprecation |
| LogArchive Service | Infra Eng | account.created, account.updated | API Key | In Progress | Dec 2026 | Dependency on storage backend migration |
| Fraud Detection | Risk Eng | risk.alert_raised, account.status_changed | OAuth2 | Complete | — | Migrated July 2026 |

---

**Status definitions:**  
- **Complete** — Migration verified by Platform Engineering  
- **In Progress** — Migration underway  
- **Blocked** — Migration cannot proceed pending a dependency  
- **Maintenance** — Existing PiSync subscription active; no new PiSync integrations  

