```markdown
# 🧟‍♂️ Zombie VDP – Advanced Bug Bounty Framework

[![Version](https://img.shields.io/badge/version-1.0.2-purple)](https://github.com/pormes-90/ZOMBIE/releases)
[![License](https://img.shields.io/badge/license-MIT-blue)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.9%2B-green)](https://www.python.org/)
[![NASA VDP](https://img.shields.io/badge/VDP-NASA%20Compliant-orange)](https://nasa-bug-bounty.dodsecurity.us/)

**Advanced passive vulnerability scanner designed for responsible disclosure programs.**

Zombie VDP is a self-contained, 100% passive reconnaissance and vulnerability detection framework built specifically for bug bounty hunters targeting NASA's Vulnerability Disclosure Program (VDP) and similar programs. It operates slowly, ethically, and leaves no aggressive footprint.

---

## 🔥 Core Features

### 🔍 Passive Reconnaissance
- **Wayback Machine** – historical URL collection
- **Common Crawl** – web index scanning
- **crt.sh** – certificate transparency log enumeration
- **AlienVault OTX** – threat intelligence (API key required)
- **urlscan.io** – URL and screenshot retrieval (API key required)
- **DNS Enumeration** – subdomain discovery with 200+ common prefixes

### ⚔️ Triple Filter System
| Filter | Description |
|--------|-------------|
| 🥷 **Ninja** | Only findings with concrete evidence (≥95% confidence) |
| ⚔️ **Samurai** | Only HIGH/CRITICAL severity with significant response length |
| 👻 **Ghost** | Only confidence ≥98% or timing/OOB detected vulnerabilities |

### 🎯 High-Impact Hunters
| Hunter | Target Vulnerabilities |
|--------|----------------------|
| **IDOR Hunter** | Insecure Direct Object References (8+ parameter patterns) |
| **SSRF Hunter** | Server-Side Request Forgery (cloud metadata, internal services) |
| **Auth Bypass Hunter** | Broken authentication (15+ sensitive paths, header manipulation) |
| **Logic Flaw Hunter** | Business logic flaws (price/quantity/step manipulation) |
| **Command Injection** | RCE detection via timing analysis |
| **Subdomain Takeover** | CNAME analysis for cloud services |

### 🛡️ Core Scanners
- **XSS Detection** – reflected & DOM-based with HTML encoding verification
- **SQLi Detection** – error-based, boolean-based, and blind (timing) techniques
- **LFI Detection** – multi-depth path traversal testing
- **SSTI Detection** – template injection with math verification
- **Open Redirect** – header and meta refresh analysis
- **CORS Misconfiguration** – origin reflection testing
- **CRLF Injection** – header injection detection
- **Rate Limit Testing** – basic rate limiting verification

### 🔧 Advanced Features
- **Zombie Dork Scanner** – 1000+ sensitive pattern regexes
- **Zombie Secret Scanner** – 30+ API key/token patterns with entropy analysis
- **Zombie Fuzzer** – adaptive payload delivery with response analysis
- **Zombie Deep Scanner** – multi-stage verification (re-request, timing, DBMS detection)
- **Zombie Evidence Locker** – AES-256 encrypted evidence storage with integrity verification
- **Zombie Auto-PoC** – automatic curl/Python proof-of-concept generation
- **Professional HTML Report** – detailed findings with CWE/OWASP/CVSS info

### 🕵️ Stealth & Ethics
- **Configurable rate limiting** with jitter (default: 1 request/2 seconds)
- **Automatic cooling down** when blocked (60-120 second pauses)
- **Ethical User-Agent** with researcher identification
- **Respects robots.txt** (optional)
- **Time-slice scheduling** for off-peak operation
- **100% passive** – no exploitation, no brute force

---

## 🚀 Quick Start

### Prerequisites
- Python 3.9 or higher
- Linux/macOS/Windows (binary available for Linux aarch64)

### Installation
```bash
pip install zombie-vdp
```

Or download the pre-built binary from GitHub Releases:

```bash
./zombie_vdp
```

Configuration

Create a config.yaml file in the same directory:

```yaml
target_domains:
  - "nasa.gov"
  - "*.nasa.gov"

researcher_name: "Your Name"
researcher_email: "your@email.com"

password: "zombie"          # optional

max_workers: 1              # 1 request at a time
rate_limit: 0.5             # 1 request every 2 seconds
crawl_delay: [60.0, 120.0]  # 1-2 minutes between pages
```

Run

```bash
zombie
# or
python zombie_vdp/zombie.py
```

---

📊 Output Structure

```
output/
├── evidence/          ← Encrypted evidence files (.zombie)
├── poc/               ← Auto-generated PoC scripts
├── reports/           ← Professional HTML vulnerability reports
└── zombie.db          ← SQLite findings database
```

---

⚠️ Disclaimer

This tool is for authorized security testing only.

· Only test systems you own or have explicit written permission to test
· Do not exploit discovered vulnerabilities
· Report findings responsibly through official VDP channels
· Follow all program rules and scope limitations

The author assumes no liability for misuse of this tool.

---

📄 License

MIT License – see LICENSE file for details.

---

👤 Author

Dikha Pormes

· Email: pormesdikha90@gmail.com
· GitHub: pormes-90

---

🙏 Acknowledgments

Built with love for the bug bounty community. Special thanks to NASA for their commitment to security through responsible disclosure.

---

"Zombie VDP – because the best hunters move slowly and strike precisely." 🧟‍♂️💖

```
🧟‍♂️💖
