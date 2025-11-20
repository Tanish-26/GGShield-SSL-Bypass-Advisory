# Advisory — GGShield SSL/TLS Verification Bypass (Feature: disable TLS verification)


**Title**: GGShield SSL/TLS Verification Bypass (Insecure CLI option)


**Status**: Public advisory (CVE submission cancelled / not used)


**Product**: GGShield (gitguardian/ggshield)
**Versions affected**: All versions up to v1.44.1 (behavior confirmed prior to/including v1.44.1)
**Severity**: High (demonstrable ability to disable TLS verification)


## Executive Summary


GGShield's CLI historically provided an option (`--allow-self-signed` / configuration `allow_self_signed`) that effectively disables SSL/TLS certificate verification for backend API connections. This allows a local or network attacker to perform a man-in-the-middle (MITM) attack when users run the CLI with the option enabled, exposing secrets, tokens, and scan results.


GitGuardian released v1.44.1 which renames the option to `--insecure` and adds warning messages; the option remains usable and verification can still be disabled.


## Impact


- An attacker positioned on the network (or a malicious local proxy) can intercept and modify communications between ggshield and its API when the client disables certificate verification.
- Possible outcomes: exfiltration of scanned secrets, token harvesting, tampering of scan responses, and supply-chain manipulation.


## Technical Details


### Root cause


The client sets the underlying HTTP client's `verify` attribute to `False` when certain CLI flags or configuration settings are present. This completely turns off certificate validation and bypasses trust-chain checks.


### Example (simplified)


```python
# illustrative snippet (not from the repo)
session = requests.Session()
if allow_self_signed:
urllib3.disable_warnings()
session.verify = False
```

Demonstration (local, safe)

A safe reproduction using the provided local mock server (included in PoC) demonstrates the behaviour:

Start the mock server (mock_gg_api.py) with a self-signed certificate.

Run ggshield in secure mode (no --allow-self-signed) — TLS verification fails and the client refuses to connect.

Run ggshield with --allow-self-signed (or --insecure) — the client connects to the mock, performs API calls (GET /exposed/v1/metadata, POST /exposed/v1/multiscan) and accepts the self-signed certificate.

Evidence artifacts included: mock server logs, ggshield debug output, curl reproduction, and the small Python PoC.

Proof-of-Concept (summary)

Commands:

# Set local instance
ggshield config set instance https://localhost:8443
export GITGUARDIAN_API_URL="https://localhost:8443"
export GITGUARDIAN_API_KEY="DUMMY_TOKEN"


# Secure run: expected TLS verification error
GGSHIELD_DEBUG=1 ggshield secret scan path ~/ggshield-test --recursive


# Insecure run: connects to local mock and posts scan
GGSHIELD_DEBUG=1 ggshield secret scan path ~/ggshield-test --allow-self-signed --recursive --verbose


# curl reproduction (shows response body)
curl -k -s -D - \
  -H "Authorization: Token DUMMY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '[{"file_path":"/Users/tanish/ggshield-test/test.txt"}]' \
  "https://localhost:8443/exposed/v1/multiscan?all_secrets=True"

Full reproduction artifacts are in the poc/ folder and logs from the mock. Do not use these PoCs against production or GitGuardian servers.

Vendor timeline & response

See timeline/disclosure_timeline.md and vendor-response/ggshield_v1.44.1_changes.md for vendor communications and release notes summary.

Recommended Mitigations (for users)

Never use --allow-self-signed, --insecure, or any option that disables TLS verification in production. Treat such options as emergency-only local testing flags.

Use system trust stores: prefer configuring and using the OS or Python system certificate store rather than disabling verification.

