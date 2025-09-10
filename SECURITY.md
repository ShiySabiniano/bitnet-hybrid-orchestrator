# Security Policy

Thank you for helping keep **BitNet Hybrid Orchestrator** and its users safe.  
This document explains how to report vulnerabilities and what to expect.

---

## 📣 Reporting a Vulnerability

**Please do not create public issues for security problems.**

Use one of the private channels below:

1. **GitHub Security Advisory (preferred)**  
   Go to the repo → **Security** tab → **Report a vulnerability**.  
   This creates a private discussion visible only to maintainers.

2. **Email (optional fallback)**  
   If you cannot use GitHub, email the maintainers at **\<your-security-email@domain\>** with the subject `SECURITY: <short description>`.  
   *(Replace the placeholder with your preferred address before publishing.)*

If you need to encrypt your message, include your **PGP public key** here once available.

---

## 🔒 What to Include

Please provide as much of the following as possible:

- Affected version/commit (`git rev-parse HEAD`) and environment (OS, Python, runtime)
- Vulnerability type (RCE, privilege escalation, info disclosure, logic bug, etc.)
- Minimal reproducible steps / PoC (commands, payloads, configs)
- Expected vs. actual behavior
- Impact assessment (who/what can be affected)
- Any temporary mitigations or workarounds

> **Never include secrets, live PII, or access tokens** in your report. If demonstrating PII exposure, use synthetic data.

---

## 🔄 Coordinated Disclosure

We follow a responsible disclosure process:

- **Acknowledgement:** within **72 hours**
- **Triage / initial assessment:** within **7 days**
- **Fix window (targets, best-effort):**
  - Critical: aim for **30 days**
  - High: **60–90 days**
  - Medium: **90–180 days**
  - Low/Informational: scheduled as appropriate

We may request additional time for complex fixes or dependency chains. Once a fix is available, we will publish release notes and (if applicable) a GitHub Security Advisory with credit to the reporter (opt-in).

---

## 🧭 Scope & Out-of-Scope

**In scope**
- Vulnerabilities in this repository’s source code, configurations, and published artifacts
- Supply-chain issues specific to how this project consumes dependencies
- Leaks or bypasses related to the **TinyBERT Guard** (PII, jailbreak, policy evasion)
- Orchestrator DAG execution / sandbox escape / unsafe tool invocation

**Out of scope**
- Third-party libraries **not** maintained in this repo (report those upstream)
- Social engineering, physical attacks, stolen devices
- Denial-of-Service (volumetric, fuzzing at scale), spam, or rate-limit abuses
- Best-practice suggestions without a demonstrable security impact
- Vulnerabilities that require root/admin on the target host to exploit

---

## 🧪 Testing Guidelines (Safe Harbor)

We encourage good-faith research following these rules:

- Do not access, modify, or exfiltrate data that does not belong to you.
- Do not degrade service for others (no volumetric DoS, no automated scanning of hosted demos).
- Only test against instances you control. If you discover a vulnerability in someone else’s deployment, inform them and us privately.
- Respect rate limits and applicable laws (CFAA, local regulations).
- If you encounter sensitive data inadvertently, **stop**, **do not** store it, and report immediately.

We will not pursue legal action against researchers who abide by this policy and act in good faith.

---

## 🔐 AGPL §13 (Network Use) Note

If you host a modified version of this software over a network, **AGPLv3** requires providing users with access to the **Corresponding Source** for your running version. See `COMPLIANCE.md` for:
- a `/source` endpoint example,
- the `X-AGPL-Source` header, and
- Docker labels to advertise the exact commit.

---

## 🧱 Supported Versions

We generally patch:
- **`main`** branch, and
- the **latest tagged release**.

Older releases may receive fixes at our discretion if the patch is low-risk or widely impactful.

---

## 🧮 Severity & Scoring

We classify issues using **CVSS v3.1** (Base score) and practical impact in typical deployments (edge devices, SBCs, lean VPS). If appropriate, we will request a **GHSA** and/or **CVE** during advisory publication.

---

## 🔗 Dependency Security

We use Dependabot (or equivalent) to surface upstream issues. If your report concerns a third-party package, please include links to upstream advisories or commits when possible.

---

## 🙏 Recognition

With your consent, we’ll credit you in the advisory and release notes (name, handle, or “anonymous”). We do not currently run a bounty program.

---

## 📬 Contact Summary

- **Report via GitHub (preferred):** Security → *Report a vulnerability*  
- **Email (fallback):** [Troubleshooting@sabiniano.me](mailto:Troubleshooting@sabiniano.me)

## 🔐 PGP

**Maintainer:** Shiy Sabiniano  
**Email:** Troubleshooting@sabiniano.me  
**Key ID (long):** 0x330C258F91939D41  
**Fingerprint:** C445 E530 2004 1B8A 7784 286A 330C 258F 9193 9D41  
**Algo:** Ed25519 (sign) + Curve25519 (encrypt)  
**Created:** 2025-09-10 • **Expires:** 2027-09-10  
**Public key (.asc):** [/security/pgp/ShiySabiniano.asc](./security/pgp/ShiySabiniano.asc)

Thank you for helping to keep **BitNet Hybrid Orchestrator** safe for everyone.
