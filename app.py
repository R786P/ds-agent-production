import streamlit as st
import requests

st.set_page_config(page_title="RepoInsight Agent", layout="centered")
st.title("🔍 RepoInsight Agent")
st.markdown("Enter a **public GitHub repo URL** to get instant insights!")

API_URL = "https://ds-agent-1nup.onrender.com/analyze"

repo_url = st.text_input("GitHub Repo URL", placeholder="https://github.com/langchain-ai/langgraph")

if st.button("Analyze Repo") and repo_url:
    with st.spinner("Fetching data from GitHub..."):
        try:
            response = requests.post(API_URL, json={"repo_url": repo_url}, timeout=15)
            if response.status_code == 200:
                data = response.json()
                # ✅ Fixed: proper 'if' condition
                if "error" in data:
                    st.error(f"❌ {data['error']}")
                else:
                    st.success("✅ Analysis Complete!")
                    st.markdown(f"### **{data.get('name', 'Unknown')}**")
                    st.markdown(f"**Owner:** {data.get('owner', 'N/A')}")
                    st.markdown(f"**Description:** {data.get('description', 'No description')}")
                    st.markdown(f"**⭐ Stars:** {data.get('stars', 'N/A')}")
                    st.markdown(f"**📦 Language:** {data.get('language', 'N/A')}")
            else:
                st.error(f"❌ API returned status {response.status_code}")
        except Exception as e:
            st.error(f"❌ Request failed: {str(e)}")

st.markdown("---")
st.caption("💡 Works only with public GitHub repos. No login required.")
