# OpenDocGen - Open-source Autonomous Document Generation Agent

[![License: Apache](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Docker](https://img.shields.io/badge/docker-ready-blue.svg)](https://www.docker.com/)

OpenDocGen is an open-source autonomous document generation agent that leverages multiple specialized AI agents to research, analyze, write, and review documents automatically.

## 🚀 Features

- **Multi-Agent Architecture**: Specialized agents for research, analysis, writing, code generation, and review
- **Web Integration**: Built-in web search, content scraping, and file downloading capabilities
- **Document Templates**: Pre-built templates for business reports, research papers, technical docs, and proposals
- **Workflow Orchestration**: Automated workflows that coordinate multiple agents
- **REST API**: FastAPI-based API for easy integration
- **Docker Support**: Complete containerized deployment
- **Vector Storage**: ChromaDB integration for document storage and retrieval
- **LLM Support**: Ollama integration for local LLM execution

## 🏗️ Architecture

```
├── 📁 agents/                    # AI Agent definitions
│   ├── research_agent.py         # Web research specialist
│   ├── analysis_agent.py         # Data analysis specialist
│   ├── writer_agent.py           # Document composition
│   ├── code_agent.py             # Code generation/execution
│   └── reviewer_agent.py         # Quality assurance
│
├── 📁 tools/                     # Agent tools
│   ├── web_tools/                # Search, scraping, download
│   ├── document_tools/           # Parsing, templates
│   ├── analysis_tools/           # Code execution, visualization
│   └── utility_tools/            # File management, text processing
│
├── 📁 core/                      # Core system logic
│   ├── orchestrator.py           # Crew orchestration
│   ├── task_manager.py           # Task lifecycle
│   └── state_manager.py          # State persistence
│
├── 📁 api/                       # REST API layer
│   ├── routes/                   # API endpoints
│   └── middleware/              # Auth, logging, rate limiting
│
└── 📁 workflows/                 # Predefined workflows
    └── research_workflow.py      # Research → Analysis → Write
```

## 🚀 Quick Start

### Prerequisites

- Python 3.9 or higher
- Docker and Docker Compose (optional)
- Ollama (for local LLM execution)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/opendocgen/opendocgen.git
   cd opendocgen
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

4. **Start Ollama** (if using local LLM)
   ```bash
   ollama serve
   ollama pull llama2
   ```

5. **Run the application**
   ```bash
   opendocgen serve
   ```

### Docker Installation

1. **Using Docker Compose**
   ```bash
   cd docker
   docker-compose up -d
   ```

## 📖 Usage

### CLI Usage

Start the server:
```bash
opendocgen serve
```

Generate a document:
```bash
opendocgen generate "Impact of AI on Healthcare" --output report.md
```

Setup environment:
```bash
opendocgen setup
```

Show configuration:
```bash
opendocgen config --show
```

### API Usage

The API will be available at `http://localhost:8000` when you run `opendocgen serve`.

#### Generate a Document

```bash
curl -X POST "http://localhost:8000/api/v1/documents/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "Impact of AI on Healthcare",
    "document_type": "research_report",
    "requirements": ["Include statistics", "Add citations", "Executive summary"]
  }'
```

#### Create a Research Task

```bash
curl -X POST "http://localhost:8000/api/v1/tasks" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "research",
    "agent": "research",
    "data": {
      "query": "latest developments in quantum computing",
      "num_results": 10
    }
  }'
```

### Python SDK

```python
from src.main import OpenDocGen

# Initialize the system
odg = OpenDocGen()

# Generate a document
document = await odg.generate_document(
    topic="Climate Change Impact on Agriculture",
    document_type="research_report",
    requirements=["Include data visualization", "Add policy recommendations"]
)

print(document)
```

## 🛠️ Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `OLLAMA_BASE_URL` | `http://localhost:11434` | Ollama server URL |
| `SEARXNG_URL` | `http://localhost:8080` | SearXNG search URL |
| `BROWSERLESS_URL` | `http://localhost:3000` | Browserless URL |
| `DEFAULT_MODEL` | `llama2` | Default LLM model |
| `DEBUG` | `false` | Enable debug mode |
| `API_PORT` | `8000` | API server port |

### Custom Agents

Create custom agents by extending the `BaseAgent` class:

```python
from src.agents.base_agent import BaseAgent

class CustomAgent(BaseAgent):
    def __init__(self, **kwargs):
        super().__init__(
            name="Custom Agent",
            role="Your custom role",
            goal="Your custom goal",
            backstory="Your agent backstory",
            **kwargs
        )
    
    async def execute_task(self, task):
        # Implement your custom logic
        return {"result": "Custom task completed"}
```

### Custom Workflows

Create custom workflows by defining agent coordination:

```python
from src.workflows.research_workflow import ResearchWorkflow

class CustomWorkflow:
    def __init__(self, agents):
        self.agents = agents
    
    async def execute(self, task):
        # Define your workflow steps
        research = await self.agents["research"].execute_task(...)
        analysis = await self.agents["analysis"].execute_task(...)
        writing = await self.agents["writer"].execute_task(...)
        
        return {"research": research, "analysis": analysis, "writing": writing}
```

## 🐳 Docker Services

The Docker setup includes:

- **opendocgen**: Main application
- **ollama**: LLM server
- **searxng**: Privacy-respecting search engine
- **browserless**: Headless browser for scraping
- **chromadb**: Vector database
- **redis**: Caching layer

## 📊 Monitoring

### Health Checks

- `GET /health` - Basic health check
- `GET /health/detailed` - Detailed system status

### Metrics

The system provides metrics at `/metrics` (when enabled)

## 🧪 Development

### Running Tests

```bash
pytest tests/
```

### Code Quality

```bash
black src/
isort src/
flake8 src/
mypy src/
```

### Development Server

```bash
opendocgen serve --reload --port 8000
```

## 📚 Documentation

- [API Documentation](docs/API.md)
- [Architecture Guide](docs/ARCHITECTURE.md)
- [Deployment Guide](docs/DEPLOYMENT.md)
- [Development Guide](docs/DEVELOPMENT.md)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [CrewAI](https://github.com/joaomdmoura/crewAI) for the multi-agent framework
- [Ollama](https://ollama.ai/) for local LLM execution
- [SearXNG](https://github.com/searxng/searxng) for privacy-respecting search
- [ChromaDB](https://www.trychroma.com/) for vector storage

## 📞 Support

- 📧 Email: team@opendocgen.com
- 💬 Discord: [Join our community](https://discord.gg/opendocgen)
- 🐛 Issues: [GitHub Issues](https://github.com/opendocgen/opendocgen/issues)

---

**Built with ❤️ by the OpenDocGen team**
