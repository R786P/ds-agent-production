# agent/core.py
import os
import requests
from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage, AIMessage
from typing import TypedDict, Annotated, Sequence
from langchain_core.messages import BaseMessage
import operator

# ========================
# Agent State Definition
# ========================
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]

# ========================
# Tool: Fetch GitHub Repo Info (Public Only)
# ========================
def fetch_github_repo_info(repo_url: str) -> str:
    """
    Fetch basic metadata for a PUBLIC GitHub repository.
    Works without token (rate-limited but sufficient for demo).
    """
    if not repo_url.startswith("https://github.com/"):
        return "❌ Invalid URL. Please provide a GitHub repo URL."
    
    try:
        # Convert to GitHub API URL
        api_url = repo_url.replace("https://github.com/", "https://api.github.com/repos/")
        headers = {}
        
        # Optional: Use GitHub token if available (for higher rate limit)
        token = os.getenv("GITHUB_TOKEN")
        if token:
            headers["Authorization"] = f"token {token}"
        
        response = requests.get(api_url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            return (
                f"✅ **{data['name']}**\n"
                f"👨‍💻 Owner: {data['owner']['login']}\n"
                f"📄 Description: {data['description'] or 'No description'}\n"
                f"⭐ Stars: {data['stargazers_count']}\n"
                f"📦 Primary Language: {data['language'] or 'Not specified'}\n"
                f"🔗 URL: {data['html_url']}"
            )
        elif response.status_code == 403:
            return "⚠️ GitHub API rate limit reached. Try again in a minute."
        else:
            return "❌ Repo not found or is private."
            
    except Exception as e:
        return f"❌ Error fetching repo: {str(e)}"

# ========================
# Agent Node
# ========================
def agent_node(state: AgentState):
    last_message = state["messages"][-1].content.strip()
    
    # Assume the input is a GitHub URL
    result = fetch_github_repo_info(last_message)
    
    return {
        "messages": [AIMessage(content=result)]
    }

# ========================
# Build LangGraph Workflow
# ========================
workflow = StateGraph(AgentState)
workflow.add_node("agent", agent_node)
workflow.set_entry_point("agent")
workflow.add_edge("agent", END)

# Compile the graph
app = workflow.compile()
