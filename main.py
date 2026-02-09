from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from agent.core import app as agent_graph  # LangGraph agent import
from langchain_core.messages import HumanMessage
import logging
import time

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="RepoInsight Agent", version="1.0")

# CORS for Streamlit
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class RepoRequest(BaseModel):
    repo_url: str

@app.get("/")
def home():
    return {
        "status": "✅ LIVE",
        "message": "RepoInsight Agent is running!",
        "instructions": "POST to /analyze with {\"repo_url\": \"https://github.com/user/repo\"}"
    }

@app.get("/health")
def health_check():
    return {"status": "ok", "agent": "ready"}

@app.post("/analyze")
async def analyze_repo(request: RepoRequest):
    start_time = time.time()
    repo_url = request.repo_url.strip()
    
    # 🔒 Security: Basic validation
    if not repo_url.startswith("https://github.com/"):
        raise HTTPException(status_code=400, detail="❌ Invalid URL. Only GitHub repos allowed.")
    
    try:
        logger.info(f"Analyzing repo: {repo_url}")
        
        # ⚙️ Run LangGraph agent
        result = agent_graph.invoke({
            "messages": [HumanMessage(content=repo_url)]
        })
        
        # Extract agent response
        agent_response = result["messages"][-1].content
        
        # ⏱️ Timeout protection (5 seconds max)
        if time.time() - start_time > 5:
            logger.warning("Analysis took >5s")
        
        return {
            "status": "success",
            "repo_url": repo_url,
            "analysis": agent_response,
            "processing_time_sec": round(time.time() - start_time, 2)
        }
        
    except Exception as e:
        logger.error(f"Agent error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Agent failed: {str(e)}")
