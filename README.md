# 🕵️‍♂️ Advance Log Detector

![Build Status](https://img.shields.io/badge/build-passing-success)
![Python](https://img.shields.io/badge/python-3.9%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

> An intelligent, high-performance log analysis tool built to parse, monitor, and flag anomalies in server logs in real time. 

---

## 📋 Table of Contents
- [About the Project](#-about-the-project)
- [System Architecture](#-system-architecture)
- [Tech Stack](#-tech-stack)
- [Getting Started](#-getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#-usage)
- [How It Works Under the Hood](#-how-it-works-under-the-hood)
- [Project Structure](#-project-structure)
- [Future Roadmap](#-future-roadmap)
- [License](#-license)

---

## 📖 About the Project
When web servers scale or security breaches happen, answers are buried inside millions of log entries. Reading these files manually is impossible. 

**Advance Log Detector** is an automated monitoring tool designed to ingest raw log files, apply efficient pattern matching, and detect anomalies (like brute-force attacks or 5xx server failures) before they lead to severe downtime.

I built this project to demonstrate low-level log parsing, memory-efficient data streaming, and clean command-line interfaces suitable for modern backend and DevOps environments.

---

## 🏗️ System Architecture

*The diagram below outlines how the detector parses incoming stream data into actionable alerts:*

```mermaid
graph TD;
    A[Raw Log Files / Streams] --> B(Log Ingestion Engine);
    B --> C{Pattern Matching & Regex};
    C -- Normal Logs --> D[Database / Output Log];
    C -- Suspicious / Errors --> E[Alerting System];
    E --> F((Admin CLI / Summary Dashboard));
    D --> F;
---

## 🛠️ Tech Stack
* **Language:** Python 3.9+
* **Data Processing:** Regular Expressions (`re` module)
* **Testing & Quality:** `pytest`

---

## 🚀 Getting Started

### Prerequisites
Make sure Python 3.9 or higher is installed on your machine:
```bash
# Verify Python version
python3 --version
```

### Installation

```bash
# 1. Clone the repository
git clone git@github.com:Danishwani1999/Advance_Log_Detector.git

# 2. Navigate into the project directory
cd Advance_Log_Detector

# 3. Create a virtual environment
python3 -m venv venv

# 4. Activate the environment
# On Linux/macOS:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# 5. Install required dependencies
pip install -r requirements.txt
```

---

## 💻 Usage

### Option 1: Python Module
```python
from log_detector import Detector

# Initialize the detector with your log file path
detector = Detector(file_path="/var/log/nginx/access.log")

# Run the scanner with strict anomaly detection enabled
detector.start_scan(strict_mode=True)
```

### Option 2: Command Line Interface
```bash
# Run the detection engine on a log file from the terminal
python main.py --log /path/to/logfile.log --level critical
```

---

## 🧠 How It Works Under the Hood
1. **Stream-based Processing:** Loading massive log files entirely into RAM causes memory exhaustion. This project leverages Python generators (`yield`) to evaluate entries line-by-line.
2. **Pre-compiled Regex Patterns:** Regular expressions are compiled once at initialization to maximize execution speed per line.
3. **Sliding Time Windows:** Detection logic tracks repeating failures from identical IP addresses over configurable time frames (e.g., 10 failed logins within 60 seconds).

---

## 📁 Project Structure
```text
Advance_Log_Detector/
├── data/                  # Sample log files for testing
├── src/
│   ├── __init__.py
│   ├── detector.py        # Core anomaly detection logic
│   ├── parser.py          # Regex parser and line splitters
│   └── utils.py           # Helper functions & formatting
├── tests/                 # Unit tests with PyTest
├── .gitignore
├── main.py                # Command-line entry point
├── requirements.txt       # Project dependencies
└── README.md
```

---

## 🔮 Future Roadmap
- [ ] Add integrations for Slack/Discord webhook alerts.
- [ ] Create an interactive terminal dashboard using `rich` or `blessed`.
- [ ] Export parsing metrics into Prometheus format.

---

## 📄 License
Distributed under the MIT License. See `LICENSE` for more information.

---

*Developed by [Danish Wani](https://github.com/Danishwani1999)*
