# Local Library Management System (CLI)

A modular, command-line interface (CLI) Library Management System built with Python. This application leverages Object-Oriented Programming (OOP) methodologies—including inheritance and data encapsulation—paired with a clean, functional transaction layer and automated JSON data persistence.

---

## Key Features

* **Role-Based Access Control:** 
* **Object-Oriented Integrity:** 
* **Automated Data Persistence:** 
* **Comprehensive Transaction Logging:** 

---

## Project Architecture

The codebase maintains strict boundaries across architectural domains to ensure modular scalability and clear version control handling:

* **Database Operations Layer:** Intercepts disk-to-memory I/O, writing back state updates cleanly to prevent runtime race conditions or file corruption.
* **Data Models Layer:** Manages domain-specific logic blueprints (`User`, `Admin`, `Member`, `Book`, `BorrowRecord`) and parses primitive dictionaries into interactive class objects using factories.
* **Functional Transaction Layer:** Orchestrates multi-model state changes, tracking down validation targets and coordinating disk saves.

---

## Quick Start & Installation Guide

Follow these steps exactly to set up your local development space and initialize the application environment.

### 1. Clone the Repository

Open a terminal shell and target your local workspace directory:

```bash
git clone https://github.com/arnoldmwenda/Library_Management_System.git
cd Library_Management_System

```

### 2. Configure Your Virtual Environment

Create a localized Python sandbox environment to isolate package tracking rules cleanly.

* **Create the Environment:**
```bash
python3 -m venv venv

```

* **Activate the Environment:**
* **Linux / macOS / WSL:**
```bash
source venv/bin/activate

```

* **Windows (Command Prompt):**
```cmd
venv\Scripts\activate.bat

```

* **Windows (PowerShell):**
```powershell
venv\Scripts\Activate.ps1

```




*(Once activated, an explicit `(venv)` prefix will match your terminal prompt line.)*

### 3. Handle Dependency Management

Install the official external tooling parameters mapped to the configuration rules file:

```bash
pip install -r requirements.txt

```

---

## Operations Interface Matrix

To boot up the universal execution switchboard loop and enter the command runtime engine, fire up your primary initialization file:

```bash
python3 main.py

```

### Technical Workflow Loop

* **Borrowing Protocol:** Accepts 13-digit literal ISBN keys. Intercepts stock limits, pulls member permission arrays, logs state variables, and saves a timestamped transaction history.
* **Return Protocol:** Matches open checkouts against active tracking parameters. Flips return flags, generates automated timestamp records, and increments stock levels.
* **Admin Purging:** Implements verification checks on user properties before removing targeted collection sets from database storage.

---

## Tracking Configuration Bounds

This workspace contains an optimized `.gitignore` configuration rulebook. The configuration excludes environment artifacts (`venv/`), system speed logs (`__pycache__/`), and system cache variables natively.

Never push raw environment folders or volatile local dependency arrays to remote servers. If you introduce outside structural libraries during testing, follow the update tracking loop exactly before finalizing branches:

```bash
pip freeze > requirements.txt
git add requirements.txt
git commit -m "Update system configuration profile dependencies"
git push origin <your-feature-branch>

```

