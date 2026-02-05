import streamlit as st
import requests

st.set_page_config(page_title="RepoInsight Agent", layout="centered")
st.title("🔍 RepoInsight Agent")
st.markdown("Enter a **public GitHub repo URL** to get instant insights!")

# Your Render API URL
API_URL = "https://ds-agent-1nup.onrender.com/analyze"

repo_url = st.text_input("GitHub Repo URL", placeholder="https://github.com/langchain-ai/langgraph")

if st.button("Analyze Repo") and repo_url:
    with st.spinner("Fetching data from GitHub..."):
        try:
            response = requests.post(API_URL, json={"repo_url": repo_url}, timeout=15)
            if response.status_code == 200:
                data = response.json()
                if "error" in 
                    st.error(f"❌ {data['error']}")
                else:
                    st.success("✅ Analysis Complete!")
                    st.markdown(f"### **{data['name']}**")
                    st.markdown(f"**Owner:** {data['owner']}")
                    st.markdown(f"**Description:** {data['description']}")
                    st.markdown(f"**⭐ Stars:** {data['stars']}")
                    st.markdown(f"**📦 Language:** {data['language']}")
            else:
                st.error("❌ Failed to connect to agent. Try again.")
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")

st.markdown("---")
st.caption("💡 Works only with **public** GitHub repos. No login required.")
