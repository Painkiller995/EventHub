# 📅 EventHub – Local Development Setup

Welcome to the **EventHub** project! This guide will walk you through setting up and running the application locally using Docker and Python.

---

## 🚀 Prerequisites

Make sure you have the following tools installed on your machine:

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)
- [Python 3.10+](https://www.python.org/downloads/)
- [pip](https://pip.pypa.io/en/stable/installation/)

---

## 🐳 Why We Use Docker in This Project

- The project depends on services like:
  - **MySQL** – for data storage
  - **Adminer** – for managing the database
  - **Mailhog** – for capturing and testing outgoing emails  
- With Docker, these services are up and running with **one command** (`docker compose up -d`), no need to install them manually.

---

## 🧱 Project Structure Overview

```
.
├── app/                     # Flask application package
├── run                     # Entry point for the app
├── requirements.txt        # Python dependencies
├── docker-compose.yml      # Docker services
├── .env.local              # Local environment variables (not committed)
└── adminer.css             # Custom styling for Adminer (optional)
```

---

## 📥 Clone the Repository

Start by cloning the project from GitHub:

```bash
git clone https://github.com/Painkiller995/EventHub.git
cd EventHub
code .
```

> 💡 The `code .` command opens the project in Visual Studio Code.
Make sure you have the `code` command available in your terminal (enabled during VS Code installation).

---

## ⚙️ Step-by-Step Setup

### 0. 🛠️ Create Your `.env.local` File

Before running the app or starting Docker services, you need a `.env.local` file with environment variables.

Copy the example file provided in the project:

```bash
cp .env.example .env.local
```

This will create a local `.env.local` file with the necessary default values for development.
You can leave the values as they are for local testing, or adjust them if needed.

---

### 1. 📦 Install Python dependencies

Create and activate a virtual environment (optional but recommended):

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

Install the required packages:

```bash
pip install -r requirements.txt
```

---

### 2. 🐳 Start Docker Services

Use `docker-compose` to spin up the necessary services (MySQL, Adminer, Mailhog):

```bash
docker compose up -d
```

This will launch the following containers:

| Service   | Description               | Port       |
|-----------|---------------------------|------------|
| MySQL     | Database server           | `3306`     |
| Adminer   | DB Management UI          | `http://localhost:8080` |
| Mailhog   | Email testing tool        | `http://localhost:8025` (UI), `1025` (SMTP) |

> 💡 Ensure you have a `.env.local` file in the root directory with database and app credentials.


---

### 3. 🛠️ Initialize the Database

Before using the app, you need to create the necessary tables in the MySQL database.

I’ve included a script called **`initial_db.py`** in the root of the project to handle this for you.

### ▶️ How to Run It

Once your Docker containers are up and running, run this command:

```bash
python initial_db.py
```

Alternatively, you can run the Python file directly in VSCode by clicking the "Run Python File" button at the top right of the editor. This will also work fine.

This script will:

- Connect to the MySQL database using the credentials from your environment file
- Create all required tables defined in your Flask application's models

### 💡 When Should You Run It?

- The **first time** you set up the project
- After making changes to your model structure
- When resetting or reinitializing your development database

---


### 4. 🔥 Run the Flask App

Run the Flask application with the entry point script:

```bash
python run
```

Alternatively, you can run the Python file directly in VSCode

By default, it runs on: `http://127.0.0.1:5000`

---

## 🧪 Testing Your Setup

- Access the database via **Adminer** at `http://localhost:8080`
- Check email sending through **Mailhog** at `http://localhost:8025`
- Interact with the web app at `http://127.0.0.1:5000`

---

## 🧹 Stopping the Environment

To stop all Docker containers:

```bash
docker compose down
```

---

## 📫 Questions?

Feel free to open an issue or contact the maintainer.