The Chaos Healer
An AIOps Self-Healing Infrastructure for Mushroom Systems

The Chaos Healer is a proactive, AI-driven monitoring and remediation system. Instead of waiting for a human to fix a server crash, our AI Doctor detects the failure, consults a custom Knowledge Base (RAG), and executes a terminal-level fix automatically.

🛠️ The Tech Stack
Backend: Node.js & Express

Database: MongoDB (Containerized)

Infrastructure: Docker & Docker Compose

AI Brain: Llama 3.3-70B (via Groq LPU for sub-second inference)

AI Strategy: Retrieval-Augmented Generation (RAG) using Markdown Playbooks

👥 The Team & Roles
Aashi (Architect): AI Architecture & Groq Integration.

Aarohi (SRE): Knowledge Base Engineering & RAG Documentation.

Anagha (Automation): Remediation Logic & System Execution (child_process).

Aditi (Chaos): Chaos Engineering & Failure Injection Testing.

🩺 How It Works (The Healing Loop)
The Crash: A service (like MongoDB) fails or is stopped manually.

The Detection: The Node.js start() function catches the connection error.

The Retrieval: The system reads knowledge/remediation_guide.md to find the specific cure.

The Diagnosis: Groq processes the error + manual and generates a fix command.

The Cure: The system executes the command (e.g., docker start database) automatically.

🚀 Getting Started
1. Prerequisites
Docker Desktop installed.

A Groq API Key.

2. Setup
Clone the repo:

Bash
git clone https://github.com/aashi596/PBL-PROJECT.git
cd PBL-PROJECT
Configure Secrets:
Create a .env file in the root directory:

Plaintext
GROQ_API_KEY=your_groq_key_here
Launch Infrastructure:

Bash
docker-compose up -d
Start the Healer:

Bash
npm install
node server.js
🌋 Testing Chaos
To see the healer in action, manually stop the database while the server is running:

Bash
docker stop database
Watch the terminal as the AI Doctor detects the disappearance and brings the database back online.

## Chaos Engineering 

This project includes chaos engineering experiments to test the resilience of the system.

### Start the system

Start MongoDB container:

docker compose up -d

Start the backend server:

node server.js

Open the application:

http://localhost:3000

---

### Inject chaos (simulate database crash)

Stop the MongoDB container:

docker stop pbl-project-database-1

Expected behavior:

- MongoDB stops
- Node.js detects database failure
- Chaos Healer AI analyzes the error
- Remediation command is suggested

---

### Restore the database

docker start pbl-project-database-1
