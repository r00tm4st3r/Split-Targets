# 🏴 Split-Targets

> Effortlessly split, clean, and deduplicate huge URL/IP target lists for your next scanning or pentesting project!

---

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
