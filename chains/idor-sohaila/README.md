# Chain: Broken Access Control / IDOR — Sohaila (245365)
**Personal data at stake:** other users' delivery addresses (#3) and order/basket history (#4).

## The loop (this folder = step 1 only)
1. **find / confirm** ← `01_identify.py` (delivered now)
2. exploit — access another user's object by changing its ID *(Weeks 5–8)*
3. measure exposure — how many other users' records are reachable *(Weeks 5–8)*
4. fix — enforce ownership checks server-side on each object request *(Weeks 5–8)*
5. re-test — re-run `01_identify.py`, confirm access is now denied (401/403) *(Weeks 5–8)*
6. runbook — write this chain's report section *(Weeks 5–8)*

## Step 1 — what `01_identify.py` does
Registers a throwaway account, logs in, and checks whether an **object endpoint that uses a
direct reference (an ID)** enforces ownership. It requests your own object (expected OK) and a
**neighbouring ID you don't own** (expected 401/403 if access control works). If the neighbour
returns data, the endpoint is a confirmed IDOR candidate. Writes evidence to `evidence/idor/`.

Enumerating *all* other users' records is step 2 — this only confirms the control is missing.

## Run
```bash
python 01_identify.py
```
