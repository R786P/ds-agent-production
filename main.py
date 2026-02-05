from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from langchain_core.messages import HumanMessage
from agent.core import app as agent_app  # Your LangGraph agent
from agent.security import validate_csv_input, safe_load_csv
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Data Science Helper Agent", version="1.0")

@app.post("/analyze")
async def analyze_csv(file: UploadFile):
    # 1. Validate file type
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Only .csv files allowed")
    
    # 2. Read content
    content = await file.read()
    csv_text = content.decode('utf-8')
    
    # 3. Security check
    if not validate_csv_input(csv_text):
        raise HTTPException(status_code=400, detail="Invalid or unsafe CSV data")
    
    # 4. Run agent
    try:
        user_input = "Analyze this dataset."
        result = agent_app.invoke({
            "messages": [HumanMessage(content=f"{user_input}\n\nCSV:\n{csv_text}")],
            "csv_data": csv_text,
            "needs_insights": True
        })
        
        # Extract final AI message
        ai_response = result["messages"][-1].content
        
        logger.info(f"Analysis completed for {file.filename}")
        return JSONResponse({"insights": ai_response})
    
    except Exception as e:
        logger.error(f"Agent failed: {str(e)}")
        raise HTTPException(status_code=500, detail="Analysis failed. Try a simpler dataset.")

# Health check
@app.get("/health")
def health():
    return {"status": "ok"}
