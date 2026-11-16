#!/usr/bin/env python3
"""Step 1 (find/confirm): inspect the JWT and reset surface for weak auth config.

Registers its own account, captures its own token, and decodes it WITHOUT verifying
or modifying it, reporting the signing algorithm and claims. Flags weak configuration
worth attacking in step 2 (Weeks 5-8). No token forgery or account takeover here.
"""
import sys
import pathlib
import time

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "common"))
import common  # noqa: E402

CHAIN = "auth"


def decode_segment(seg):
    import base64
    import json
    seg += "=" * (-len(seg) % 4)
    return json.loads(base64.urlsafe_b64decode(seg.encode()))


def main():
    s = common.session()
    if not common.check_target(s):
        sys.exit(1)
    url = common.target_url()

    email = f"auth_probe_{int(time.time())}@test.local"
    pw = "Passw0rd!probe"
    s.post(url + "/api/Users", json={"email": email, "password": pw,
                                     "passwordRepeat": pw, "securityAnswer": "x"}, timeout=8)
    r = s.post(url + "/rest/user/login", json={"email": email, "password": pw}, timeout=8)

    token = None
    try:
        token = r.json().get("authentication", {}).get("token")
    except Exception:
        pass

    if not token:
        print("[!] No token returned (API shape may differ). Inspect /rest/user/login first.")
        sys.exit(1)

    header = decode_segment(token.split(".")[0])
    payload = decode_segment(token.split(".")[1])
    alg = header.get("alg")

    print(f"\n[account] {email}")
    print(f"[jwt] header alg = {alg}")
    print(f"[jwt] payload claims = {sorted(payload.keys())}")

    weak = []
    if str(alg).lower() == "none":
        weak.append("alg:none (signature not required)")
    if str(alg).upper().startswith("RS"):
        weak.append("RS* — check whether server also accepts HS* with the public key (alg-confusion)")
    if "exp" not in payload:
        weak.append("no exp claim (token may not expire)")

    if weak:
        print("\n==> WEAK-AUTH SIGNALS to attack in step 2:")
        for w in weak:
            print(f"    - {w}")
    else:
        print("\n==> No obvious weak-config signal from the header/claims alone.")
    print("    Also review the password-reset flow (security questions) for the reset takeover path.")

    common.save_evidence(CHAIN, "jwt-inspect", {
        "chain": "broken_authentication",
        "owner": "Ebrahim",
        "jwt_alg": alg,
        "jwt_claims": sorted(payload.keys()),
        "weak_signals": weak,
        "reset_flow_to_review": "security-question based password reset",
        "step": "1_find_confirm",
    })


if __name__ == "__main__":
    main()
