---
title: "Project AETHER: Agent Framework Workshop"
description: "A challenge-based workshop to learn the Microsoft Agent Framework by rebuilding Neo-Tokyo's city AI system"
ms.date: 2026-02-22
ms.topic: tutorial
---

## The Story

The year is 2029. Neo-Tokyo's city-wide automation system, AETHER, has suffered a catastrophic "logic-cascade failure." Every district is dark. Communications are down. Automated defenses are offline.

You are a Neural Architect, one of the few engineers authorized to interface directly with AETHER's core. Your mission: rebuild the system from scratch using the Microsoft Agent Framework, one subsystem at a time.

## What You Will Build

A multi-agent swarm capable of managing city resources, securing the perimeter, remembering operator context, and evaluating its own performance. Each challenge adds a new capability to your growing AETHER system.

## Prerequisites

* Python 3.11 or later
* An Azure AI Foundry project endpoint (with a deployed model such as `gpt-5.2`)
* Azure CLI installed and authenticated (`az login`)
* [`uv`](https://docs.astral.sh/uv/getting-started/installation/) for package management
* A terminal and code editor (VS Code recommended)

## Quick Start

```bash
# Clone the repository
git clone <repo-url>
cd agent-framework-workshop

# Install dependencies (creates .venv automatically)
uv sync
```

### Activate the Virtual Environment

After `uv sync` creates the `.venv` directory, activate it for your platform:

**Linux / macOS:**

```bash
source .venv/bin/activate
```

**Windows (PowerShell):**

```powershell
.venv\Scripts\Activate.ps1
```

**Windows (Command Prompt):**

```cmd
.venv\Scripts\activate.bat
```

> **Tip:** If you use `uv run python ...` you do not need to activate the venv manually — `uv run`
> handles it automatically. Activation is only needed when you want to use `python` directly.

### Configure and Run

```bash
# Configure your environment
cp .env.sample .env
# Edit .env with your Azure AI Foundry endpoint and model deployment

# Start with Challenge 01
cd challenges/challenge-01-basic-agent
uv run python starter.py
```

## Challenge Map

### Phase 1: Foundations

| #  | Challenge | What You Build | Outcome |
|----|-----------|----------------|--------|
| 01 | [**The Sentry Agent**](challenges/challenge-01-basic-agent/README.md) | A single reconnaissance agent connected to an Azure OpenAI model. The Sentry is AETHER's first heartbeat: it reads the state of the city and delivers a military-style status report. | A runnable script that creates a chat client, instantiates an agent with a persona, and prints a city status report. |
| 02 | [**Deployment**](challenges/challenge-02-deployment/README.md) | The Sentry Agent served as a live HTTP endpoint. Toggle between a DevUI browser chat interface for development and a FastAPI production API using the `DEPLOY_MODE` environment variable. | A web-accessible agent at `localhost:8080` responding through a browser chat UI or a FastAPI endpoint. |

### Phase 2: Orchestration

| #  | Challenge | What You Build | Outcome |
|----|-----------|----------------|--------|
| 03 | [**Function Tools**](challenges/challenge-03-function-tools/README.md) | The Sentry Agent enhanced with function tools that query AETHER's data feeds: `query_power_grid` and sensor-query functions pulling live district data from the city utilities module. | An agent that invokes real data tools when asked about a district, returning actual grid status and sensor readings. |
| 04 | [**Sequential Workflows**](challenges/challenge-04-sequential-workflow/README.md) | A two-agent pipeline using `SequentialBuilder`: the Sentry Agent detects grid faults, then hands off to a Technician Agent that generates step-by-step repair scripts referencing the same Grid ID. | A chained workflow where fault detection flows into repair planning, with streaming output showing both agents' contributions. |

### Phase 3: Multi-Agent

| #  | Challenge | What You Build | Outcome |
|----|-----------|----------------|--------|
| 05 | [**Concurrent Workflows**](challenges/challenge-05-concurrent-workflow/README.md) | Two parallel Technician Agents (North and South district) running simultaneously via `ConcurrentBuilder`, with a custom aggregator function that merges both district repair reports into a unified operations briefing. | A concurrent workflow dispatching parallel district repairs and producing a single merged report. |
| 06 | [**Agent Orchestration**](challenges/challenge-06-agent-orchestration/README.md) | Two tasks. **Task 1 (GroupChat):** A Leadership Council of City Manager, Resource Agent, and Security Agent coordinated through `GroupChatBuilder` with an orchestrator routing turns. **Task 2 (Agent-as-Tool):** The same council restructured so the City Manager invokes the Resource and Security agents on demand via `Agent.as_tool()`. | Task 1: a self-terminating multi-agent conversation producing a comprehensive city status report. Task 2: a coordinator agent calling specialist agents as tools and comparing both orchestration patterns. |

### Advanced Challenges

| #  | Challenge | What You Build | Outcome |
|----|-----------|----------------|--------|
| A1 | [**Adding Memory**](challenges/advanced-challenges/advanced-01-memory/README.md) | A custom `BaseContextProvider` that extracts operator security clearance via LLM structured extraction, stores it in session state, and gates tool access by clearance level. Stacked with `Mem0ContextProvider` for cross-session long-term memory. | An agent that remembers clearance across turns, restricts tool access accordingly, and recalls your identity across restarts via Mem0. |
| A2 | [**Security Guardrails**](challenges/advanced-challenges/advanced-02-guardrails/README.md) | A custom `AgentMiddleware` with an input guard that blocks prompt injection patterns before they reach the agent, and an output guard that catches accidental credential leaks in responses. | A hardened agent where injection attempts are blocked, password requests are intercepted, and leaked secrets are stripped from responses. |
| A3 | [**Agent Evaluation**](challenges/advanced-challenges/advanced-03-evaluation/README.md) | An evaluation harness that reads test cases from a JSONL suite, runs each through the guarded Sentry Agent, performs assertion-based checks against expected outputs, and prints a pass/fail summary with a percentage score. | A diagnostic runner that validates agent behavior across normal tool-call tests and guardrail tests, producing a scored report. |

## Workshop Phases

### Phase 1: The Foundations (45 min)

The core terminal is offline. Initialize a Sentry Agent and deploy it as a live HTTP service. Challenges 01 and 02 establish the building blocks: creating agents, connecting them to LLMs, and deploying the agent.

### Phase 2: Orchestrating the Flow (45 min)

Power is back, but it is chaotic. Give the agent function tools and chain agents into sequential workflows to coordinate district repairs without blowing a fuse. Challenges 03 and 04 introduce function tools and orchestration patterns.

### Phase 3: Multi-Agent and Orchestration (45 min)

The system needs coordination. Run concurrent workflows and assemble a Leadership Council of specialized agents with GroupChat orchestration. Challenges 05 and 06 add concurrent workflows and multi-agent orchestration.

### Advanced Challenges

For advanced participants: cure AETHER's "Digital Amnesia" with persistent memory, harden the agent with security guardrails, and run a formal evaluation suite.

## Project Structure

```text
agent-framework-workshop/
├── .env.sample                              # Environment variable template
├── pyproject.toml                           # Python project & dependencies (uv)
├── shared/
│   ├── __init__.py
│   └── city_utils.py                        # Mock city data shared by all challenges
└── challenges/
    ├── challenge-01-basic-agent/            # Phase 1
    │   ├── README.md
    │   └── starter.py
    ├── challenge-02-deployment/             # Phase 1
    │   ├── README.md
    │   └── starter.py
    ├── challenge-03-function-tools/         # Phase 2
    │   ├── README.md
    │   └── starter.py
    ├── challenge-04-sequential-workflow/    # Phase 2
    │   ├── README.md
    │   └── starter.py
    ├── challenge-05-concurrent-workflow/    # Phase 3
    │   ├── README.md
    │   └── starter.py
    ├── challenge-06-agent-orchestration/            # Phase 3
    │   ├── README.md
    │   ├── task1_starter.py
    │   └── task2_starter.py
    └── advanced-challenges/
        ├── advanced-01-memory/                 # Advanced
        │   ├── README.md
        │   └── starter.py
        ├── advanced-02-guardrails/             # Advanced
        │   ├── README.md
        │   └── starter.py
        └── advanced-03-evaluation/             # Advanced
            ├── README.md
            ├── starter.py
            └── test_suite.jsonl
```

Each challenge directory contains:

* `README.md` with narrative context, learning objectives, and step-by-step instructions
* `starter.py` (or `task1_starter.py` / `task2_starter.py` for multi-task challenges) with TODO markers guiding your implementation

## Troubleshooting

### "Module not found" errors

Verify you installed dependencies: `uv sync`

### Authentication errors

Confirm you are logged in via Azure CLI (`az login`) and your `.env` file has a valid `AZURE_AI_PROJECT_ENDPOINT` and `AZURE_AI_MODEL_DEPLOYMENT_NAME`.

### Import errors for `shared.city_utils`

Each challenge script adds the workspace root to `sys.path`. Run scripts from within their challenge directory.

### Generating a Mem0 API key (Advanced 01)

Advanced Challenge 01 requires a `MEM0_API_KEY` for persistent long-term memory.

1. Go to <https://app.mem0.ai/> and sign up or log in.
2. In the dashboard, navigate to **API Keys** in the left sidebar.
3. Click **Create API Key**, give it a name (e.g. `aether-workshop`), and copy the generated key.
4. Paste the key into your `.env` file:

   ```dotenv
   MEM0_API_KEY=your-copied-key-here
   ```
