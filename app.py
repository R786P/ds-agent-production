import streamlit as st
import requests
import os

st.set_page_config(page_title="RepoInsight Agent", layout="centered")
st.title("🔍 RepoInsight Agent")
st.markdown("Enter a **public GitHub repo URL** to get instant insights!")

# Direct Render URL use karo (Streamlit Cloud se bhi kaam karega)
API_URL = "https://ds-agent-production.onrender.com/analyze"  # Space hata diya!

repo_url = st.text_input("GitHub Repo URL", placeholder="https://github.com/langchain-ai/langgraph")

if st.button("Analyze Repo") and repo_url:
    with st.spinner("🤖 Agent analyzing repo..."):
        try:
            response = requests.post(API_URL, json={"repo_url": repo_url}, timeout=15)
            if response.status_code == 200:
                data = response.json()
                if "error" in data or data.get("status") == "error":
                    st.error(f"❌ {data.get('detail', data.get('error', 'Analysis failed'))}")
                else:
                    st.success("✅ Analysis Complete!")
                    st.markdown("### Analysis Result")
                    st.text_area("Agent Response", data["analysis"], height=300)
                    st.caption(f"⏱️ Processing time: {data.get('processing_time_sec', 'N/A')}s")
            else:
                st.error(f"❌ API error {response.status_code}: {response.text}")
        except requests.exceptions.ConnectionError:
            st.error(f"❌ Cannot connect to backend. Is FastAPI running at {API_URL}?")
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")

st.markdown("---")
st.caption("💡 Works only with public GitHub repos. No login required.")
