# Privacy-Driven Threat Modelling, Exploitation & Remediation
**Module 26CSCN26H — Data Privacy — Prof. Ahmad Mostafa**

Target: **OWASP Juice Shop** (intentionally-vulnerable training app, run locally in Docker).
Angle: for every vulnerability, **quantify the personal data exposed** and map it to
**breach-notification obligations under GDPR Art. 33/34 and Egypt's Law 151/2020**, then
**remediate and re-test** to prove the fix holds.

## Team & owned chains
| Member | Chain | Personal data at stake | Folder |
|---|---|---|---|
| Abdelrahman (243700) | SQL injection | user table — emails, password hashes | `chains/sqli-abdelrahman` |
| Sohaila (245365) | Broken access control / IDOR | other users' addresses, order history | `chains/idor-sohaila` |
| Ebrahim (241939) | Broken authentication (JWT / reset) | full profile via account takeover | `chains/auth-ebrahim` |

Each chain follows the same loop:
**find → exploit → measure exposure → fix → re-test (prove it fails) → write runbook section.**
This scaffold delivers **step 1 (find / confirm)** for all three. Exploit + measurement is Weeks 5–8.

## Layout
```
env/                 environment notes
docker-compose.yml   pinned Juice Shop target
common/common.py     shared helpers (base URL, HTTP session, evidence logging)
inventory/           personal-data inventory (the privacy backbone)
chains/<name>/       per-member chain: README + 01_identify.py (step 1)
legal/               GDPR 33/34 + Law 151/2020 breach-notification template
evidence/            raw scan output (nmap, zap) + per-chain evidence
report/              draft + final report
```

## Getting started
```bash
# 0. Install Docker Desktop first (not currently installed on this machine).
# 1. Bring the target up:
docker compose up -d
# 2. Confirm it's live:  open http://localhost:3000
# 3. Pin by digest (see docker-compose.yml comment) so builds are reproducible.
# 4. Create a Python env for the probes:
python -m venv .venv && . .venv/Scripts/activate   # Windows: .venv\Scripts\activate
pip install requests pyjwt
# 5. Run your chain's step-1 identify script, e.g.:
python chains/sqli-abdelrahman/01_identify.py
```

## Scope & ethics
Testing is confined to the local Juice Shop container only. Juice Shop is built to be
attacked for training. Nothing here targets real systems or real personal data.

## Status (per milestone plan)
- [x] Week 3 — environment + repo scaffold, baseline scan folders ready
- [ ] Week 3 — baseline Nmap/ZAP scans captured into `evidence/`
- [ ] Week 4 — personal-data inventory completed (`inventory/`)
- [ ] Weeks 5–8 — each member: exploit → measure → fix → re-test → runbook
