import pytest
from agent.core import fetch_github_repo_info

def test_valid_repo():
    result = fetch_github_repo_info("https://github.com/langchain-ai/langgraph")
    assert "✅" in result or "langgraph" in result.lower()

def test_invalid_url():
    result = fetch_github_repo_info("https://google.com")
    assert "❌" in result

def test_empty_input():
    result = fetch_github_repo_info("")
    assert "❌" in result
