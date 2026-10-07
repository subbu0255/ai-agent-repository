# Mac Real Device IT Support Agent POC

This version is designed specifically for a Mac.

Unlike the first mock version, the diagnostic tools read REAL information from the Mac running the application.

## What is real?

The agent can read:

- macOS version
- hostname
- CPU core count
- real CPU utilization
- real RAM utilization
- RAM used/available
- real disk utilization
- disk free space
- battery status when available

## What is intentionally simulated?

Ticket creation is SAFE and local.

The program writes:

```text
created_ticket.json
```

It does NOT send anything to Jira, ServiceNow, or another external system.

This is intentional for classroom use.

---

# 1. Architecture

```text
                    Employee
                       |
                       v
                LangGraph Agent
                       |
          +------------+-------------+
          |            |             |
          v            v             v
     CPU tool      Memory tool    Device tool
          |            |             |
          +------------+-------------+
                       |
                 REAL Mac metrics
                       |
                       v
                  Agent decides
                       |
             Problem detected?
                  /         \
                No           Yes
                |             |
                v             v
             Explain       Ask for
             status       confirmation
                              |
                              v
                       Local ticket tool
                              |
                              v
                    created_ticket.json
```

---

# 2. Prerequisites

Use Python 3.10 or newer if possible.

Check:

```bash
python3 --version
```

Install Git if needed:

```bash
git --version
```

You also need a Groq API key.

---

# 3. Setup on your Mac

Open Terminal and go into this project:

```bash
cd mac_it_support_agent_poc
```

Create a virtual environment:

```bash
python3 -m venv .venv
```

Activate it:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create your environment file:

```bash
cp .env.example .env
```

Edit it:

```bash
nano .env
```

Put your key:

```text
GROQ_API_KEY=your_actual_groq_api_key
```

Save the file.

---

# 4. Run

```bash
python main.py
```

---

# 5. First test: real device status

Enter:

```text
Check my Mac status.
```

The agent should call:

```text
check_device_status()
```

The returned values come from your actual Mac.

You may see information similar to:

```text
macos_version: 15.x
machine: arm64
cpu_logical_cores: 10
memory_total_gb: 16.0
memory_used_percent: 54.2
disk_used_percent: 62.1
```

Your values will be different.

---

# 6. Second test: real CPU

Enter:

```text
What is my current CPU usage?
```

The tool executes:

```python
psutil.cpu_percent(interval=2)
```

That is a real two-second CPU measurement.

---

# 7. Third test: real memory

Enter:

```text
Check my RAM usage.
```

The agent uses:

```text
get_memory_usage()
```

and reads the actual RAM statistics.

---

# 8. Main agent demonstration

Now enter:

```text
My Mac is slow. Diagnose the problem and create a ticket if necessary.
```

The agent can inspect:

```text
Device
  ↓
CPU
  ↓
Memory
  ↓
Disk
```

Then it evaluates the returned information.

For this POC:

```text
CPU >= 90%       -> high
Memory >= 90%    -> high
Disk >= 90%      -> high
```

If the actual machine is healthy, the agent should not blindly create a ticket.

This is important: your real Mac may NOT have high CPU or memory at the moment you test it.

---

# 9. How to demonstrate a ticket

Use an explicit request:

```text
Check my CPU and memory. If there is a serious issue, create a ticket.
```

If the metrics are abnormal, the agent can call the ticket tool.

The local ticket will be written to:

```text
created_ticket.json
```

Example:

```json
{
  "ticket_id": "MAC-INC-20261006194500",
  "status": "Created - Local POC",
  "priority": "High"
}
```

---

# 10. Why the ticket is local

Do NOT connect a classroom demonstration directly to a production ServiceNow/Jira account initially.

The safer progression is:

```text
Stage 1
Real Mac metrics
+
Local ticket simulation

        ↓

Stage 2
Real Mac metrics
+
Jira test project

        ↓

Stage 3
Real Mac metrics
+
ServiceNow/Jira
+
Authentication
+
RBAC
+
Audit logging
+
Human approval
```

---

# 11. The important agent concept

Students should see this:

```text
Employee:
"My Mac is slow."

             ↓

          Agent

             ↓

"Which tool should I use?"

             ↓

get_cpu_usage()

             ↓

REAL RESULT
CPU = 93%

             ↓

Agent reasons again

             ↓

get_memory_usage()

             ↓

REAL RESULT
Memory = 94%

             ↓

Agent reasons again

             ↓

Problem detected

             ↓

Ticket action
```

The agent is not receiving fake:

```text
CPU = 95%
Memory = 91%
```

It is receiving measurements from the actual machine.

---

# 12. Files

```text
mac_it_support_agent_poc/
│
├── main.py
├── agent.py
├── tools.py
├── requirements.txt
├── .env.example
├── README.md
└── sample_prompts.txt
```

---

# 13. Important limitation

`psutil` gives system-level metrics, but "my Mac is slow" is not fully diagnosable from CPU and RAM alone.

A real enterprise diagnostic agent could additionally inspect:

```text
CPU-heavy processes
Memory-heavy processes
Disk I/O
Network connectivity
Battery health
Thermal state
Free disk space
Running applications
System uptime
Crash logs
OS updates
```

For a teaching POC, start with CPU, memory, disk, device status, and battery.

---

# 14. Next production step

The next useful upgrade is to add a REAL ITSM integration.

For example:

```text
Real Mac
   ↓
Agent
   ↓
CPU / RAM / Disk
   ↓
Agent decision
   ↓
Human approval
   ↓
Jira Service Management API
   ↓
Real ticket
```

That would turn this from a local POC into a realistic enterprise agent architecture.
