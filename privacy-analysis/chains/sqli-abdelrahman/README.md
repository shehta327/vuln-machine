# Chain: SQL Injection — Abdelrahman (243700)
**Personal data at stake:** Users table — email addresses (#1), password hashes (#2).

## The loop (this folder = step 1 only)
1. **find / confirm** ← `01_identify.py` (delivered now)
2. exploit — auth bypass + data extraction *(Weeks 5–8)*
3. measure exposure — count rows & fields reachable → feeds the legal template *(Weeks 5–8)*
4. fix — parameterised queries in source (WAF fallback: ModSecurity + OWASP CRS) *(Weeks 5–8)*
5. re-test — re-run `01_identify.py`, confirm it NO LONGER flags injectable *(Weeks 5–8)*
6. runbook — write this chain's report section *(Weeks 5–8)*

## Step 1 — what `01_identify.py` does
Non-destructively **confirms whether the login endpoint is injectable**:
- sends a normal invalid login (baseline),
- sends an input containing a single quote that, on an injectable query, changes the
  server's behaviour (SQL error / different status),
- reports the finding and writes an evidence record to `evidence/sqli/`.

It does **not** extract data or bypass auth — that's step 2. This is the "find" step that
proves the vulnerability exists and gives you a regression check for after the fix.

## Run
```bash
python 01_identify.py
```
