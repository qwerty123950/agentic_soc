# Agentic SOC with Specialized AI Agents

An enterprise-style Security Operations Center (SOC) platform powered by multiple specialized AI agents, developed using production-quality software engineering practices.

---

## Project Description

Modern Security Operations Centers face an overwhelming volume of security alerts, logs, and potential incidents. Single-chatbot interfaces often lack the context, specialized knowledge, and depth to resolve complex multi-stage cyber threats. 

This project implements a multi-agent framework comprising specialized AI agents (e.g., Log Analyzers, Network Forensics Agents, Threat Intel Refiners, and Incident Commanders) working collaboratively to detect, analyze, and mitigate security threats in real time.

---

## Objectives

- **Specialization**: Deploy dedicated, role-specific AI agents rather than a single general-purpose assistant.
- **Collaborative Forensics**: Orchestrate agents to solve complex alerts via agent-to-agent negotiation and structured messaging.
- **Production Standards**: Implement clean architecture, robust configuration handling, full type safety, and comprehensive logging telemetry.

---

## Current Sprint Status

- **Sprint 1 (Release)**: Complete. Established backend framework foundation, global logging formatting, request-scoped UUID tracing, middleware flow, and centralized exception structures.
- **AI/Database logic**: Out of scope for Sprint 1. (No agents, databases, or cybersecurity business logic are implemented yet).

---

## Technology Stack

- **Runtime**: Python 3.14+
- **Web Framework**: FastAPI (ASGI)
- **Settings & Validation**: Pydantic v2 & Pydantic Settings
- **Server**: Uvicorn (standard event loop & HTTP tools)
- **Environments**: dotenv variables
- **Testing**: Python Standard Library / Pytest-ready scaffolding

---

## Folder Structure

```text
agentic_soc/
├── backend/                  # Application Source Code
│   ├── api/                  # Unified Router Layout
│   │   ├── router.py         # Main API Router
│   │   └── v1/               # Version 1 Namespace
│   │       ├── router.py     # V1 Router Assembly
│   │       └── endpoints/    # Route Handlers
│   │           ├── health.py # System Health Checker
│   │           └── root.py   # API Root Info
│   ├── core/                 # Core Infrastructure
│   │   ├── config.py         # App Settings (Pydantic Settings)
│   │   ├── context.py        # ContextVars definitions (Request ID)
│   │   ├── exceptions.py     # Custom exceptions base class
│   │   └── logging.py        # Unified logging setup
│   ├── database/             # Database connectivity (empty skeleton)
│   ├── middleware/           # HTTP Request Middlewares
│   │   ├── errors.py         # Centralized error mapping
│   │   ├── logging_middleware.py # Request latency logger
│   │   └── request_id.py     # X-Request-ID injector
│   ├── models/               # Database ORM models (empty skeleton)
│   ├── schemas/              # Pydantic Request/Response models
│   │   └── responses.py      # Standard envelopes (Root, Health, Errors)
│   ├── services/             # Core business logic (empty skeleton)
│   └── utils/                # Helper utilities (empty skeleton)
├── docs/                     # Documentation directory
├── tests/                    # Backend automated test suite
│   ├── e2e/                  # End-to-End tests
│   ├── integration/          # Integration tests
│   ├── test_data/            # Mock schemas / payloads
│   └── unit/                 # Unit tests
├── pyproject.toml            # Build tool specification
├── requirements.txt          # Third-party dependencies
├── .env.example              # Environment variables template
└── run.sh                    # Shell script launcher
```

---

## Prerequisites

- **Python**: Version `3.14` or higher.
- **Git**: For version control.

---

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/qwerty123950/agentic_soc.git
   cd agentic_soc
   ```

2. **Virtual Environment Setup**:
   Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies**:
   Install the required packages in editable mode:
   ```bash
   pip install -r requirements.txt
   pip install -e .
   ```

4. **Environment Variables**:
   Copy the example environment file and adjust values:
   ```bash
   cp .env.example .env
   ```

---

## Running the Application

A pre-configured shell launcher is provided to start the backend with all safety checks applied.

```bash
chmod +x run.sh
./run.sh
```

The server will spin up by default at `http://127.0.0.1:8000`.

---

## API Documentation URLs

When the server is running, the following endpoints are accessible:
- **Interactive documentation (Swagger)**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **Alternative documentation (Redoc)**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)
- **OpenAPI Schema Definition**: [http://127.0.0.1:8000/openapi.json](http://127.0.0.1:8000/openapi.json)
- **Health Check**: [http://127.0.0.1:8000/api/v1/health](http://127.0.0.1:8000/api/v1/health)

---

## Project Roadmap

- **Sprint 1 (Done)**: Professional backend foundation setup (FastAPI skeleton, structured logging, UUID tracing, global exception handling).
- **Sprint 2 (Upcoming)**: Datastore setups, security authentication layers, mock threat simulation pipelines.
- **Sprint 3**: Multi-agent framework setup and agent communication protocol.
- **Sprint 4**: Specialization coding (role-specific reasoning loops).
- **Sprint 5**: Incident Response dashboard (UI/UX) integration.

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Future Work

- Integrate real-time security telemetry feeds (e.g. Zeek logs, Syslog, Auditd records).
- Develop semantic vectors search capabilities for local indicator lookup (IOCs).
- Implement human-in-the-loop approvals for critical agent actions.
