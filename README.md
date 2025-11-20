# GGShield SSL/TLS Verification Bypass
### Independent Security Advisory (No CVE)

**Researcher:** Tanish Saxena  
**Product:** GitGuardian GGShield  
**Affected Versions:** ≤ v1.43.0  
**Mitigated In:** v1.44.1  
**Category:** CWE-295 Improper Certificate Validation  
**Disclosure Date:** 17 November 2025  
**Status:** Public Disclosure  

---

## Overview

A design issue in GGShield allowed full SSL/TLS certificate verification bypass when the `--allow-self-signed` option was used.  
The name suggested limited trust relaxation, but internally it disabled *all* certificate validation.

This behavior exposed users to Man-in-the-Middle (MITM) attacks and potential compromise of secrets, repositories, credentials, and scan integrity.

GitGuardian implemented mitigations in **v1.44.1**, including clearer naming and stronger warnings.

---

## Technical Details

Example code path:

```python
def create_session(allow_self_signed: bool = False):
    session = Session()
    if allow_self_signed:
        urllib3.disable_warnings()
        session.verify = False  # Full certificate validation bypass
    return session
```

When used, this disables:

- Domain validation  
- Certificate chain validation  
- CA trust checking  
- Expiration checks  

Any attacker with network positioning could intercept or modify GGShield traffic.

---

## Impact

- Secrets sent for scanning can be intercepted  
- Source code being scanned may leak  
- API Key or GitGuardian tokens exposed  
- Scan results can be manipulated  
- Pipeline security weakened  
- Internal threat actors can exploit it  

---

## Mitigations Introduced in v1.44.1

GitGuardian shipped the following:

- Added explicit `--insecure` flag  
- Added clear warnings describing MITM risk  
- Deprecated the misleading `--allow-self-signed` flag  
- Added documentation on secure alternatives  
- Encouraged use of system trust store  

These changes reduce unintentional misuse of insecure configurations.

---

## Disclosure Timeline

| Date | Action |
|------|--------|
| 20 Sep 2025 | Initial report submitted |
| 13 Oct 2025 | Vendor responds – considers design intentional |
| 20 Oct 2025 | Vendor declines changes |
| 13 Nov 2025 | CERT/CC advises public disclosure |
| 16 Nov 2025 | GitGuardian releases v1.44.1 with mitigations |
| 17 Nov 2025 | Public advisory released |

---

## Author

**Tanish Saxena**  
Independent Security Researcher

