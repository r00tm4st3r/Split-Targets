# 🏴 Split-Targets

> Effortlessly split, clean, and deduplicate huge URL/IP target lists for your next scanning or pentesting project!

---
```bash
BANNER = rf"""{CYAN}

 __       _ _ _  _____                     _
/ _\_ __ | (_) |/__   \__ _ _ __ __ _  ___| |_ ___
\ \| '_ \| | | __|/ /\/ _  |  __/ _  |/ _ \ __/ __|
_\ \ |_) | | | |_/ / | (_| | | | (_| |  __/ |_\__ \
\__/ .__/|_|_|\__\/   \__,_|_|  \__, |\___|\__|___/
   |_|                          |___/

```

## 🏴 What is Split-Targets?

Split-Targets is a **lightweight and flexible Python CLI tool** designed for security researchers, pentesters, and automation engineers who need to:

- Split large target files into smaller, manageable chunks  
- Remove duplicates across all chunks to avoid redundant scans  
- Automatically exclude specified IP prefixes and private IP ranges  
- Interactively decide whether to keep files in place, move, or copy them  
- Support very large chunk sizes for scalability  
- Run dry-runs to preview file splits without writing any output  

It’s simple to use yet packed with smart features to streamline your target preparation workflow.

---

## 🏴 Key Features

| Feature                              | Description                                         |
|------------------------------------|-----------------------------------------------------|
| Deduplication across chunks         | Avoid duplicate targets anywhere in the split files |
| IP prefix and private IP exclusion  | Filter out unwanted IP ranges automatically         |
| Custom chunk size and start index   | Control how many lines per chunk and file numbering |
| Interactive file storage            | Choose to keep files locally, move, or copy them    |
| Dry-run mode                       | Preview actions without creating or modifying files |
| Robust URL, IP, and domain parsing  | Supports varied input formats flexibly               |
| Dependency-free and cross-platform  | Runs anywhere Python 3.6+ is installed               |

---

## 🏴 Installation

No dependencies required beyond Python 3.6 or higher.

Clone this repository or download the script directly:

```bash
git clone https://github.com/yourusername/Split-Targets.git
cd Split-Targets
```

---

## 🏴 Usage
Run the script from the command line with your input file and options:

```bash
python3 Split-Targets.py -i <targets.txt> -s 2 -n 10000 -x 23,104,173
Parameters
-i <filepath> (required) — Path to your input target list file (one URL/IP per line)

-s <start_index> — Starting index for output files (default: 2)

-n <lines_per_file> — Number of lines per chunk file (default: 10,000)

-x <prefixes> — Comma-separated IP prefixes to exclude (default: 23,104,173)

--dry-run — Show how the input would be split without writing any files
```
