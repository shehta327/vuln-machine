# Personal-Data Inventory — OWASP Juice Shop
*The privacy backbone. Every exposure figure in every chain maps back to a row here.*
*Fill during Week 4. One row per data field the application stores or processes.*

## Classification key
- **Category:** `personal` (identifies/relates to a person) · `special` (GDPR Art.9 sensitive:
  health, biometric, etc.) · `credential` (password hash, token, secret) · `financial`
  (card / payment) · `non-personal`.
- **Subjects:** who the data is about (customers, employees).
- **Where:** table / endpoint / storage location in the app.
- **Notify if exposed?** Does loss of this field, at scale, plausibly trigger GDPR Art.33
  (authority) and/or Art.34 (data subjects) + Egypt Law 151/2020? (yes / no / depends)

## Inventory table
| # | Data field | Category | Subjects | Where (table / endpoint) | Notify if exposed? | Notes |
|---|---|---|---|---|---|---|
| 1 | Email address | personal | customers | Users table / `/rest/user/*` | yes | primary identifier |
| 2 | Password hash | credential | customers | Users table | yes | hash strength matters (Art.34 risk) |
| 3 | Delivery address | personal | customers | Addresses / `/api/Addresss` | yes | IDOR target (Sohaila) |
| 4 | Order / basket history | personal | customers | Orders, Baskets / `/rest/basket/*` | depends | reveals behaviour |
| 5 | Payment card data | financial | customers | Cards / `/api/Cards` | yes | high-risk, Art.34 likely |
| 6 | Security-question answer | credential | customers | SecurityAnswers | yes | reset-flow weakness (Ebrahim) |
| 7 | Full name | personal | customers | Users table | depends | |
| 8 | Feedback / reviews | personal | customers | Feedbacks | depends | may contain free-text PII |
| 9 | Session / JWT token | credential | customers | client / `Authorization` header | yes | account takeover (Ebrahim) |
|   | *(add rows as you enumerate the app)* | | | | | |

## How to complete this (Week 4)
1. Bring up Juice Shop (`docker compose up -d`).
2. Register a throwaway account; browse the REST API surface (the app documents many
   `/rest/*` and `/api/*` endpoints) and the data each returns.
3. For each field you find, add a row and classify it.
4. Confirm the **"Notify if exposed?"** column with the legal template in `legal/`.
5. This table is cited in the final report as the project's data-protection scope.
