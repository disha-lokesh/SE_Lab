# CRM-RACRL v1.0.0 — Release Notes

Customer Relationship Management covering Reach → Acquire → Convert → Retain → Loyalty.

**Team:** Balla Santhosh, Dhriti Kamani, Disha Lokesh, Diya Agarwal
**Stack:** React + Vite + TypeScript, Node/Express + TypeScript, PostgreSQL + Prisma, GitHub Actions CI/CD

## What's included

| Module | Features |
|--------|----------|
| Auth | Login with JWT and hashed passwords, role-based access, user admin (create, deactivate, change role) |
| Reach | Customer segments with live audience count, campaigns, sending and results |
| Acquire | Lead capture and public enquiry form, CSV lead import, manual and round-robin lead assignment |
| Convert | Contacts and accounts, convert lead in one transaction, deal pipeline board, activities and reminders |
| Retain | Support tickets with SLA, churn-risk flag, Customer 360 timeline |
| Loyalty | Orders and points ledger (1 point per Rs 100), loyalty tiers, reward catalogue and redemption |
| Analytics | Dashboard KPIs, global search, funnel report, CSV export, audit log |

## Quality

- 370+ automated API tests (Jest + Supertest on PostgreSQL) and 93+ web tests (Vitest), plus Playwright end-to-end tests
- CI on every pull request: lint, type-check, API tests, web tests, Jira key in the PR title
- Every story merged through a reviewed pull request

## Changes from the plan

See `docs/deviation-log.md`.

## Run it

See `README.md` section 1.
