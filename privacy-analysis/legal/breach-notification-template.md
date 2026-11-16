# Breach-Notification Assessment — <chain name>
*One copy per chain. Fill after you have the measured exposure figure (Weeks 5–8).*
*This is the "exploit → obligation" bridge that makes the project a Data Privacy project.*

## 1. Incident summary
- **Vulnerability:** <e.g. SQL injection on login>
- **Owner:** <member>
- **Data fields exposed:** <ref inventory rows #, e.g. #1 email, #2 password hash>
- **Records / data subjects affected (measured):** <number — from the chain's measurement step>
- **Measurement method:** <how the count was obtained, so it's defensible, not estimated>

## 2. Is this a personal-data breach?
> A breach = accidental/unlawful destruction, loss, alteration, unauthorised disclosure of,
> or access to personal data (GDPR Art.4(12); mirrored in Law 151/2020).
- Confidentiality / integrity / availability breach? **<which>**
- Decision: **<yes / no>** — justification: <...>

## 3. GDPR notification analysis
| Question | Finding |
|---|---|
| **Art.33** — notify supervisory authority within **72h**? | <yes/no> — "unless unlikely to result in a risk to rights and freedoms" |
| **Art.34** — notify affected individuals without undue delay? | <yes/no> — triggered by **high risk** to rights and freedoms |
| Factors raising risk | <e.g. credentials + emails = credential-stuffing; weak hashes; financial data> |
| Mitigation reducing risk | <e.g. strong hashing, data encrypted, access revoked> |

## 4. Egypt Law 151/2020 analysis
| Question | Finding |
|---|---|
| Notifiable personal-data breach under Law 151/2020 + Executive Regulations? | <yes/no> |
| Notification to the Personal Data Protection Center / data subjects? | <who / timeline> |
| Sensitive-data handling (stricter regime)? | <applies? which fields> |
| Context | Executive Regulations in effect 2025; full enforcement 2026 |

## 5. Conclusion
- **Notification required:** Authority <yes/no> · Individuals <yes/no>
- **Timeline / actions:** <...>
- **How remediation (your fix) changes this assessment:** <re-run after patch — exposure now 0>
