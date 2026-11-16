# Chain: Broken Authentication (JWT / reset) — Ebrahim (241939)
**Personal data at stake:** full profile via account takeover (#9 token, #6 security answer).

## The loop (this folder = step 1 only)
1. **find / confirm** ← `01_identify.py` (delivered now)
2. exploit — forge/abuse the token or reset flow to take over an account *(Weeks 5–8)*
3. measure exposure — what a taken-over account exposes per victim *(Weeks 5–8)*
4. fix — strong JWT config (reject weak `alg`, verify signature) / harden reset *(Weeks 5–8)*
5. re-test — re-run `01_identify.py`, confirm weak-config flags are gone *(Weeks 5–8)*
6. runbook — write this chain's report section *(Weeks 5–8)*

## Step 1 — what `01_identify.py` does
Registers a throwaway account, logs in, captures the **JWT**, and inspects it **without
attacking anything**:
- decodes the header and payload (no verification) and reports the algorithm and claims,
- flags weak signals (e.g. `alg: none`, or an algorithm that invites tampering),
- notes the password-reset mechanism to review (security questions).
Writes evidence to `evidence/auth/`. Forging tokens / taking over accounts is step 2.

## Run
```bash
pip install pyjwt
python 01_identify.py
```
