# 🧟‍♂️ Zombie VDP — Ultimate Bug Bounty Framework

[![PyPI version](https://img.shields.io/pypi/v/zombie-vdp?color=informational&label=PyPI)](https://pypi.org/project/zombie-vdp/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-blue)](https://www.python.org/)

**Zombie VDP** adalah kerangka kerja bug bounty pribadi yang menggabungkan seluruh pipeline pengujian keamanan dalam satu nafas.  
Dirancang khusus untuk program **Vulnerability Disclosure Program (VDP)** seperti NASA, alat ini bekerja secara **100% pasif**, tidak meninggalkan jejak bot, dan hanya melaporkan temuan dengan confidence **90–100%**.

> **Identitas Zombie**: Semua fitur menggunakan nama `zombie_*` — bukan meniru, melainkan menciptakan ciri khas sendiri.

---

## 🔥 Fitur Utama

### 🔍 Zombie Recon (Pengintaian Pasif)
- **Wayback Machine** — arsip historis URL
- **Common Crawl** — indeks web publik
- **crt.sh** — certificate transparency log
- **AlienVault OTX** — database ancaman (perlu API key)
- **urlscan.io** — tangkapan layar & URL lama (perlu API key)
- **DNS Enumeration** — subdomain umum & zone transfer

### 🕸️ Zombie Crawler
- Perayapan halaman target dengan kedalaman terbatas
- Delay antar permintaan yang dapat dikonfigurasi (default 5–10 detik)
- Menghindari file binary & protokol non-HTTP

### 🧲 Zombie Dorking (Internal)
- Menyaring URL dari hasil recon & crawl menggunakan pola regex
- Tanpa search engine → **100% pasif, tidak terdeteksi**

### 🛡️ Zombie Scanner
| Kerentanan | Metode |
|-----------|--------|
| **XSS** (Reflected) | Payload injection + verifikasi Selenium (opsional) |
| **SQL Injection** | Error-based detection |
| **LFI** (Local File Inclusion) | Path traversal `/etc/passwd` |
| **Open Redirect** | Header `Location` injection |
| **SSTI** (Server-Side Template Injection) | `{{7*7}}` payload |
| **Missing Security Headers** | Pengecekan header HSTS, CSP, dll. |

### ⚡ Zombie Fuzzer (Adaptif)
- Analisis perbedaan respons (panjang, hash, kemiripan teks, waktu, error keyword)
- Hanya anomali dengan skor ≥ 0.9 yang dilaporkan

### 🔑 Zombie Secrets Scanner (TruffleHog Style)
- Pola regex:
  - AWS Access Key
  - GitHub Token
  - Slack Webhook
  - Generic JWT
- Deteksi di halaman web target, bukan hanya repositori

### ⚔️ Triple Filter (Ninja · Samurai · Ghost)
| Filter | Aturan |
|--------|--------|
| 🥷 **Ninja** | Hanya temuan dengan bukti (`evidence`) tidak kosong |
| ⚔️ **Samurai** | Hanya `HIGH`/`CRITICAL` & `response_length > 0` |
| 👻 **Ghost** | Hanya confidence ≥ 98% atau metode `timing`/`oob` |

### 🧪 Zombie Deep Scan
- Validasi lanjutan setelah filter: **timing attack** untuk konfirmasi SQLi

### 🔒 Zombie Evidence Locker
- Setiap temuan lolos filter disimpan sebagai **file terenkripsi** (format `.zombie`)
- Hanya bisa dibuka dengan kunci di folder `./output/evidence/`

### ⏳ Zombie Time Slice
- Zombie hanya beroperasi pada jam yang diizinkan (default nonaktif)
- Contoh: hanya pukul 02:00–05:00 UTC

### ⚡ Zombie Auto-PoC Generator
- Setiap temuan langsung dilengkapi skrip `curl` dan Python
- Tim triase tinggal menjalankan `bash reproduce.sh`

### 🧠 Zombie Memory
- State pemindaian disimpan di `zombie_memory.json`
- Pemindaian terhenti? Zombie bisa melanjutkan dari titik terakhir

### 📊 Zombie Report
- **HTML** — laporan profesional siap kirim ke VDP
- **CSV** — ekspor ke spreadsheet
- **JSON** — integrasi dengan alat lain

---

## 🧬 Arsitektur & Alur Kerja
⚙️ Konfigurasi (config.yaml)

Zombie membaca config.yaml dari folder kerja saat ini. Jika tidak ditemukan, ia membuat default.

```yaml
target_domains:
  - "nasa.gov"
  - "*.nasa.gov"

password: "rahasia"          # kosongkan jika tidak ingin password

output_dir: "./output"
db_name: "zombie.db"

workflow_steps:
  - "zombie_recon"
  - "zombie_crawl"
  - "zombie_dork"
  - "zombie_scan"
  - "zombie_filter"
  - "zombie_deep_scan"
  - "zombie_evidence"
  - "zombie_poc"
  - "zombie_report"

max_workers: 3               # kurangi agar tidak agresif
rate_limit: 1.0              # 1 permintaan/detik
timeout: 30

crawl_delay: [5.0, 10.0]     # jeda 5-10 detik
crawl_depth: 2
max_pages_crawl: 100

enable_wayback: true
enable_commoncrawl: true
enable_crtsh: true
enable_otx: true             # isi otx_api_key
enable_urlscan: true         # isi urlscan_api_key

otx_api_key: "xxx"
urlscan_api_key: "xxx"

confidence_threshold: 90
active_filters:
  - "ninja"
  - "samurai"
  - "ghost"

enable_fuzzer: true
enable_secrets_scan: true
enable_evidence_locker: true
enable_auto_poc: true
enable_memory: true
enable_time_slice: false     # nonaktifkan dulu
```

---

📂 Struktur Output

```
output/
├── evidence/          ← Bukti terenkripsi (.zombie)
├── poc/               ← Skrip curl & Python siap reproduksi
├── reports/           ← Laporan HTML, CSV, JSON
└── zombie_memory.json ← State pemindaian (untuk melanjutkan)
```

---

🎨 Contoh Output di Terminal

```
🔐 Password:           ← (input tersembunyi)

███████╗ ██████╗ ███╗   ███╗██████╗ ██╗███████╗
╚══███╔╝██╔═══██╗████╗ ████║██╔══██╗██║██╔════╝
  ███╔╝ ██║   ██║██╔████╔██║██████╔╝██║█████╗
 ███╔╝  ██║   ██║██║╚██╔╝██║██╔══██╗██║██╔══╝
███████╗╚██████╔╝██║ ╚═╝ ██║██████╔╝██║███████╗
╚══════╝ ╚═════╝ ╚═╝     ╚═╝╚═════╝ ╚═╝╚══════╝

        ☣  Z O M B I E   S Y S T E M  ☣

     [■■■■■■■■■■■■■■■■■■■■] 100%

============================================================
[ZOMBIE_RECON]
============================================================
  ZOMBIE_RECON [■■■■■■■■■■■■■■■■■■■■] 100%

============================================================
[ZOMBIE_CRAWL]
============================================================
  ZOMBIE_CRAWL [■■■■■■■■■■■■■■■■■■■■] 100%

... 

FILTERING WITH TRIPLE WARRIORS...
🥷 Ninja Filter: hanya bukti nyata...
     [■■■■■■■■■■■■■■■■■■■■] 100%
⚔️ Samurai Filter: HIGH/CRITICAL + respons signifikan...
     [■■■■■■■■■■■■■■■■■■■■] 100%
👻 Ghost Filter: confidence ≥98% atau timing/OOB...
     [■■■■■■■■■■■■■■■■■■■■] 100%

✔ 3 high/critical findings after triple filter.
```

---

🎖️ Identitas & Kualitas

· 700+ baris kode bersih, terstruktur, tanpa ketergantungan binary luar
· Async I/O — cepat dan hemat resource
· Rate limiting dan auto‑pause saat terdeteksi block
· Dibangun dengan cinta oleh Dikha Pormes, seorang peneliti bug bounty, untuk peneliti bug bounty

---

📜 Lisensi

MIT License — lihat file LICENSE untuk detail.

---

🙏 Ucapan Terima Kasih

Terima kasih kepada seluruh komunitas bug bounty yang menginspirasi pembuatan alat ini.
Zombie VDP bukan sekadar alat. Ia adalah rekan setia yang hidup di malam hari, mengumpulkan bukti, dan hanya berbicara melalui temuan kelas atas.

---

Made with 🧠 & 🖤 by Dikha Pormes
```
---

⚠️ Ethical Use Only · [Nama Proyek]

Peringatan keras: Kode ini dibuat untuk tujuan edukasi, riset keamanan yang sah, dan pengujian sistem milik sendiri atau dengan izin tertulis.
Setiap penyalahgunaan untuk tindakan ilegal, peretasan tanpa izin, pencurian data, atau kejahatan siber lainnya bukanlah tanggung jawab penulis.

---

📜 Lisensi & Kebijakan Penggunaan

Proyek ini dilisensikan di bawah [MIT / GPL / CC BY-NC-ND] dengan syarat tambahan:

· ❌ Dilarang menggunakan untuk:
  · Akses ilegal ke sistem orang lain.
  · Mencuri, merusak, atau memanipulasi data tanpa izin.
  · Spam, phishing, DDoS, atau bentuk serangan siber lainnya.
  · Melanggar hukum nasional maupun internasional.
· ✅ Diizinkan untuk:
  · Belajar mekanisme keamanan dan kerentanan.
  · Mengaudit atau melindungi sistem yang menjadi tanggung jawab Anda.
  · Menggunakan dalam CTF (Capture The Flag) resmi, laboratorium kampus, atau pelatihan etis.

Dengan mengunduh atau menggunakan kode ini, Anda menyetujui bahwa penulis tidak bertanggung jawab atas segala konsekuensi penyalahgunaan.

---

🛡️ Prinsip “Do No Harm”

Kami menerapkan standar etika berdasarkan Coordinated Vulnerability Disclosure dan HackerOne Code of Conduct.
Jika Anda menemukan kerentanan di dunia nyata, laporkan secara bertanggung jawab – jangan eksploitasi.

---

📞 Kontak & Pelaporan Penyalahgunaan

Jika Anda mengetahui pihak yang menyalahgunakan kode ini untuk tindakan kriminal, harap laporkan ke:
📧 d7xraps90@gmail.com
Atau buka issue di repositori ini.

---

🧪 Contoh Penggunaan Etis

```bash
# Hanya gunakan di lingkungan yang Anda kuasai / miliki izin
#root# - python3 zombie.py
```

[!CAUTION]
Jalankan sekali pun dengan niat iseng pada sistem orang lain = ILEGAL.
Pelajari UU ITE pasal 30–35 (Indonesia) atau undang-undang siber negara Anda.

---

🤝 Kontribusi

Pull request diterima selama menambah nilai edukasi atau pertahanan siber, bukan alat baru untuk menyerang.

---

Ingat: Dengan kekuatan kode datang tanggung jawab besar.
Jadilah ethical hacker yang melindungi, bukan kriminal yang merusak.

---

© [T\2026] – [Dikha Pormes] | Untuk dunia maya yang lebih aman.
