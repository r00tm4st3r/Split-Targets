# 🚀 Split-Targets

> **Effortlessly split, clean, and deduplicate huge URL/IP target lists for your next scanning or pentesting project!**

---

## 🛠️ What is Split-Targets?

Split-Targets is a **powerful yet simple Python CLI tool** that helps security researchers, pentesters, and automation engineers:

- **Split massive target files** into manageable chunks  
- **Remove duplicates** across chunk files, preventing repeated scans  
- **Filter out unwanted IP prefixes and private ranges** automatically  
- **Interactively manage** output files by copying or moving them  
- Support very large chunk sizes
- Run dry-runs to preview file splits without touching disk  

With customizable options and smart deduplication, Split-Targets optimizes your workflow and saves you time.

---

## ⚡ Features

| Feature                                  | Description                                             |
|------------------------------------------|---------------------------------------------------------|
| **Deduplication across chunks**          | Ensures no duplicate targets between files              |
| **Exclude IP prefixes & private IPs**    | Skip unwanted IP blocks effortlessly                     |
| **Custom chunk sizes & start indices**   | Flexible chunk sizing & file numbering                   |
| **Interactive file storage options**     | Choose to keep, move, or copy output files               |
| **Dry-run mode**                         | Preview file splitting without writing anything          |
| **Robust input parsing**                  | Supports IPs, URLs, and domain names                      |
| **Cross-platform & dependency-free**     | Runs anywhere Python3 is installed                        |

---

## 📥 Installation

No dependencies — just Python 3.6 or higher.

Clone the repo or download the script directly:

```bash
git clone https://github.com/yourusername/Split-Targets.git
cd Split-Targets
