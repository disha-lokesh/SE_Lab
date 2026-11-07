# Deviation Log — CRM-RACRL

Every change from the original plan (SRS, SAD, Test Plan, sprint plan), with the reason and its impact.

| # | Date | Area | Planned | Actual | Reason | Impact |
|---|------|------|---------|--------|--------|--------|
| D1 | 27 Oct | Process | Track work in GitHub Projects (course handout) | Tracked in Jira (Scrum board, story points, burndown) | Team lead's instruction | None on scope; burndown in Jira |
| D2 | 29 Oct | Process | Jira linked to GitHub, cards move automatically | Jira not linked; cards moved by hand, Done only after the PR is merged | Keep setup simple | Burndown depends on manual updates, checked at each standup |
| D3 | 29 Oct | Schedule | Sprint 1: 27–31 Oct | Sprint 1 started 29 Oct. A sprint was started by mistake during setup and closed with 0 points ("Setup - started by mistake") | Setup delay; wrong sprint started after import | Sprint 1 had 3 working days; extra closed sprint visible in reports |
| D4 | 30 Oct | Tech | Docker Compose for the local database | Docker is the default; members may use a locally installed PostgreSQL 16 instead (README Option B) | Port clash with an existing local PostgreSQL | Local setup only; CI and deployment unchanged |
| D5 | 31 Oct | Scope | CRM-13 (convert lead) done in Sprint 1 | Code finished in Sprint 1; PR merged 1 Nov and counted in Sprint 2 | Its PR depended on CRM-11 being merged first | Sprint 1 velocity lower by CRM-13's points |
| D6 | 31 Oct | Scope | Separate Contacts and Accounts screens (CRM-11) | Contacts and Accounts API delivered; customers are browsed through the Customers and Customer 360 pages | Avoid two screens showing the same records | No missing function; API covers CRUD and search |
| D7 | 3 Nov | Design | Loyalty tier rule not fixed in SRS | Tier = highest tier reached by lifetime earned points; redeeming never lowers a tier | Customers should not lose a tier by using their points | Defines CRM-F-051; tested by TC-LOY-02 |
| D8 | 3 Nov | Design | Points rule | 1 point per full Rs 100; orders under Rs 100 write no ledger row | Matches acceptance "Rs 2,550 → +25"; avoids zero-value ledger rows | Tested by TC-LOY-01 |
| D9 | 5 Nov | Design | Reward stock not specified | Each redemption takes one unit of stock; stock 0 or an inactive reward returns 409 | Prevent giving away rewards that are not available | Tested alongside TC-LOY-03 and TC-OPS-04 |
| D10 | 29 Oct–5 Nov | Design | Role access per SRS 2.3 | Support reads but cannot change contacts; only Admin/Sales Manager delete accounts or assign leads; only Admin/Support record orders and redeem rewards; an admin cannot deactivate themselves | Prevent data loss and admin lock-out | Covered by role tests |
