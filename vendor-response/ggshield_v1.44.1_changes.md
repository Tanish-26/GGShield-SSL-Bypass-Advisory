# GitGuardian GGShield — v1.44.1 Changes (Vendor Response Summary)


The vendor published release notes for v1.44.1 which address the clarity of SSL/TLS configuration. Key points:


- **Added**: `--insecure` CLI option and `insecure` configuration setting as explicit alternatives to `--allow-self-signed` and `allow_self_signed`.
- The new option explicitly communicates that SSL verification is completely disabled, reducing ambiguity.


- **Added**: Prominent runtime warning messages when SSL verification is disabled via either `--insecure` or `--allow-self-signed`.
- Warnings recommend using the system certificate trust store (Python >= 3.10) instead.


- **Changed / Deprecated**:
- `--allow-self-signed` CLI option and `allow_self_signed` configuration setting are **deprecated** in favor of `--insecure` / `insecure` (kept functional for backward compatibility during the deprecation period).


- **Security**:
- The release note clarifies the risk model and improves UX for the insecure options, but the behavior of disabling TLS verification remains — the product still permits turning off verification which can be abused.


- **Other fixes**:
- Minor build/workflow fixes and non-related bugfixes.


**Assessment**:
- The changes improve clarity and user awareness but do not remove the root issue: the CLI still allows disabling SSL verification, and that remains a security risk for users who enable it (accidental or otherwise).
- Recommended continued actions:
- Remove the ability to fully disable verification for hosted instances by enforcing verification at client side when instance URL points to public/production domains.
- If deprecated options remain, ensure default behavior is secure (verification on) and consider fail-safe mechanisms (e.g., block `--insecure` when used with `https://` public instances unless explicit admin config consent is present).
