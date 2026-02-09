# ds-agent-production
# RepoInsight Agent - Production Ready

A LangGraph-powered agent that analyzes public GitHub repositories and returns insights about stars, language, description, and owner.

## ✅ Production Features

- **Testing**: Pytest coverage for agent tools (`tests/`)
- **Security**: Input validation + CORS protection
- **Resilience**: Timeout handling (5s max) + error logging
- **Deployment**: Ready for Render.com (see `render.yaml`)
- **Monitoring**: Structured logging with processing time metrics

## 🚀 Deployment

1. Deploy backend on Render:
   ```bash
   git push render main
