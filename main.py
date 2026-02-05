from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI(title="RepoInsight Agent", version="1.0")

@app.get("/")
def home():
    return {
        "status": "✅ LIVE",
        "message": "RepoInsight Agent is running!",
        "instructions": "Send a POST request to /analyze with {\"repo_url\": \"https://github.com/user/repo\"}"
    }

@app.get("/health")
def health_check():
    return {"status": "ok"}

# Optional: Simple mock analysis endpoint
@app.post("/analyze")
async def analyze_repo(request: dict):
    repo_url = request.get("repo_url", "").strip()
    if not repo_url or "github.com" not in repo_url:
        return {"error": "Please provide a valid GitHub repo URL"}
    
    # Mock response (replace later with real logic)
    return {
        "repo_url": repo_url,
        "summary": "✅ Public repo detected. Ready for deep analysis.",
        "note": "Full agent logic will be added after core module is ready."
    }
