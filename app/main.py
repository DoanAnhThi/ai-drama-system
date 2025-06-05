from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
from typing import Dict, List

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="AI Drama Automation System",
    description="Automated system for creating and managing AI-generated drama series",
    version="1.0.0"
)

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Root endpoint - System status check"""
    return {
        "status": "operational",
        "system": "AI Drama Automation System",
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        # Add system health checks here
        return {
            "status": "healthy",
            "components": {
                "api": "operational",
                "database": "operational",
                "queue": "operational"
            }
        }
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        raise HTTPException(status_code=500, detail="System health check failed")

@app.get("/api/v1/system/status")
async def system_status():
    """Detailed system status endpoint"""
    try:
        # Add detailed system status checks here
        return {
            "status": "operational",
            "metrics": {
                "episodes_created_today": 0,
                "episodes_in_progress": 0,
                "episodes_failed": 0,
                "average_processing_time": 0,
                "api_usage": {
                    "openai": 0,
                    "elevenlabs": 0,
                    "heygen": 0
                }
            }
        }
    except Exception as e:
        logger.error(f"Status check failed: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to get system status")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 