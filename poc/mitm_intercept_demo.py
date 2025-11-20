#!/usr/bin/env python3
"""
mitm_intercept_demo.py


Simple PoC demonstrating that an HTTPS client which disables TLS verification (verify=False)
will connect to a self-signed server. This script performs two requests against a local mock
GGShield API (https://localhost:8443) — once with verification enabled (expected to fail)
and once with verification disabled (expected to succeed).


This is for **local testing only** against the provided mock_gg_api.py. Do NOT target
GitGuardian infrastructure.
"""


import requests
import os
import sys


API_URL = os.environ.get("GITGUARDIAN_API_URL", "https://localhost:8443")
API_KEY = os.environ.get("GITGUARDIAN_API_KEY", "DUMMY_TOKEN")
HEADERS = {"Authorization": f"Token {API_KEY}", "Content-Type": "application/json"}


ENDPOINT = "/exposed/v1/multiscan?all_secrets=True"


PAYLOAD = '[{"file_path":"/Users/tanish/ggshield-test/test.txt"}]'




def try_request(verify):
full_url = API_URL.rstrip("/") + ENDPOINT
print('\n=== Request to:', full_url)
print('verify=', verify)
try:
r = requests.post(full_url, headers=HEADERS, data=PAYLOAD, verify=verify, timeout=5)
print('HTTP', r.status_code)
print('Response body:')
print(r.text)
except requests.exceptions.SSLError as e:
print('SSL ERROR:', e)
except Exception as e:
print('ERROR:', e)




if __name__ == '__main__':
print('PoC: HTTPS request to mock GGShield API')
print('Using API_URL:', API_URL)
# 1) Verified request (should fail with self-signed cert)
try_request(verify=True)
# 2) Insecure request (verify disabled) — demonstrates bypass
try_request(verify=False)
