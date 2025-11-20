# Security Advisory: GGShield SSL Verification Bypass

**Type:** Security Design Issue  
**Severity:** High  
**Identifier:** Third-party advisory (no CVE)  
**Affected:** GGShield ≤ v1.43.0  
**Mitigated in:** v1.44.1  

## Summary

The `--allow-self-signed` flag in GGShield disabled all SSL/TLS certificate validation, allowing potential interception of scanned data and credentials.

## Details

Setting `session.verify = False` disables all verification layers, making GGShield traffic vulnerable to MITM.

## Impact

- Credential exposure  
- Secret exfiltration  
- Source code interception  
- Tampered scan results  

## Mitigation

Upgrade to **v1.44.1** or later.

Avoid using `--allow-self-signed` or `--insecure`.

Use proper certificate trust configuration.

## Credits

Reported by **Tanish Saxena**

