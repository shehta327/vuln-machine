# vuln-machine — Data Privacy project (26CSCN26H)

This repo is the **OWASP Juice Shop source** (v17.1.1), which we **edit directly** to
remediate our assigned vulnerabilities, plus `privacy-analysis/` holding the Data
Privacy deliverable (data inventory, legal mapping, exploit/measurement scripts).

Juice Shop is MIT-licensed (OWASP / Björn Kimminich) — see `LICENSE`. We are modifying
it for coursework; credit stays with the original authors.

## Baseline vs fixed
- `main` = the **unmodified** Juice Shop = our **vulnerable baseline**.
- Each member fixes their vulnerability on their **own branch**, then opens a PR.
- The git diff between main and a fix branch **is** the before/after evidence.

## Who edits what (remediation targets)
| Member | Vulnerability | File to edit | Fix |
|---|---|---|---|
| Abdelrahman | SQL injection | `routes/login.ts` | parameterised query (no string-built SQL) |
| Sohaila | Broken access control / IDOR | `routes/basket.ts` | ownership check: basket must belong to the logged-in user |
| Ebrahim | Broken auth (JWT/reset) | `lib/insecurity.ts`, `routes/resetPassword.ts` | verify JWT signature / stronger secret; harden reset |

Different files = we work in parallel with minimal merge conflicts.

## Run it (edit → rebuild → test)
```bash
docker compose up --build -d     # builds YOUR current source, serves http://localhost:3000
docker compose down
```

## Branch workflow
```bash
git checkout main && git pull
git checkout -b sqli-abdelrahman      # idor-sohaila / auth-ebrahim
# edit your file, test with docker compose up --build
git push -u origin sqli-abdelrahman   # then open a Pull Request
```
Keep `main` protected (require PR review) so nothing lands unreviewed.

## Privacy analysis
See `privacy-analysis/` — the data inventory, GDPR Art.33/34 + Egypt Law 151/2020
breach-notification template, and each chain's exploit/measurement scripts.
