from fastapi import FastAPI, UploadFile, File, HTTPException, Response, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
import os
import pandas as pd
from pathlib import Path
import json
import numpy as np
from typing import Optional

from app.models import ReportResponse
from app.services.data_service import DataService
from app.services.ai_service import AIService

# Custom encoder for NumPy types
class NumpyEncoder(json.JSONEncoder):
    """Custom encoder for NumPy types"""
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, np.bool_):
            return bool(obj)
        return super(NumpyEncoder, self).default(obj)

app = FastAPI(title="ERP Report Generator API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
ai_service = AIService()

@app.get("/")
async def root():
    return {"message": "ERP Report Generator API"}

@app.get("/download-template")
async def download_template():
    """Download the sample CSV template"""
    template_path = Path(__file__).parent / "templates" / "sample_data.csv"
    
    if not template_path.exists():
        raise HTTPException(status_code=404, detail="Template file not found")
    
    return FileResponse(
        path=template_path,
        filename="erp_data_template.csv",
        media_type="text/csv"
    )

@app.post("/generate-report")
async def generate_report(
    file: UploadFile = File(...),
    start_date: Optional[str] = Form(None),
    end_date: Optional[str] = Form(None)
):
    """Upload CSV and generate a report with optional date filtering"""
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Only CSV files are accepted")
    
    try:
        # Read the file content
        contents = await file.read()
        
        # Process the data
        df = DataService.process_csv_data(contents)
        
        # Apply date filtering if provided
        if start_date:
            df = df[df['date'] >= start_date]
        if end_date:
            df = df[df['date'] <= end_date]
            
        if df.empty:
            raise ValueError("No data found for the selected date range")
        
        # Analyze the data
        metrics = DataService.analyze_data(df)
        
        # Generate the report using AI
        report_text = ai_service.generate_report(metrics)
        
        # Create the response data
        response_data = {
            "report_text": report_text,
            "metrics": metrics
        }
        
        # Use custom JSON encoder to handle NumPy types
        return JSONResponse(
            content=json.loads(json.dumps(response_data, cls=NumpyEncoder))
        )
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)