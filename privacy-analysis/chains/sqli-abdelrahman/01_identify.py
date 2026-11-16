#!/usr/bin/env python3
"""Step 1 (find/confirm): is the Juice Shop login endpoint SQL-injectable?

Non-destructive. Compares the server's response to a benign invalid login against
its response to an input containing a single quote. On a vulnerable, unparameterised
query the quote breaks SQL syntax and the behaviour changes (error / different status),
which confirms the injection point. Extraction & auth-bypass are step 2 (Weeks 5-8).
"""
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "common"))
import common  # noqa: E402

LOGIN = "/rest/user/login"
CHAIN = "sqli"


def probe(s, url, email, password):
    r = s.post(url + LOGIN, json={"email": email, "password": password}, timeout=8)
    body = r.text[:300]
    return r.status_code, body


def main():
    s = common.session()
    if not common.check_target(s):
        sys.exit(1)
    url = common.target_url()

    # Baseline: an invalid but syntactically harmless login.
    base_status, base_body = probe(s, url, "nobody@example.com", "wrongpassword")

    # Probe: a single quote that breaks an unparameterised SQL string.
    test_status, test_body = probe(s, url, "test'", "x")

    sql_error_markers = ["SQLITE_ERROR", "syntax error", "SQL", "near \"", "Error:"]
    changed = (test_status != base_status) or any(m in test_body for m in sql_error_markers)

    print(f"\n[baseline] invalid login      -> HTTP {base_status}")
    print(f"[probe]    quote in email     -> HTTP {test_status}")
    if changed:
        print("\n==> LIKELY INJECTABLE: the quote changed server behaviour / raised a SQL error.")
        print("    Next (step 2): craft auth-bypass payload, then measure rows & fields exposed.")
    else:
        print("\n==> No injection signal from this probe.")
        print("    If this is the POST-FIX run, that's the result you want (regression passes).")

    common.save_evidence(CHAIN, "login-injection-confirm", {
        "chain": "sql_injection",
        "owner": "Abdelrahman",
        "endpoint": LOGIN,
        "baseline": {"status": base_status, "body_snippet": base_body},
        "probe": {"input_email": "test'", "status": test_status, "body_snippet": test_body},
        "verdict": "likely_injectable" if changed else "no_signal",
        "step": "1_find_confirm",
    })


if __name__ == "__main__":
    main()
