import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import aiohttp
import json
from livekit import api
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Enable CORS for web client
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AgentDispatchRequest(BaseModel):
    room: str
    livekit_url: str
    agent_type: str = "translation"
    languages: list[str] = ["English", "Hindi"]

@app.get("/token")
async def get_token(room: str, identity: str):
    """Generate LiveKit access token for a participant"""
    
    # Get LiveKit credentials from environment
    api_key = os.getenv("LIVEKIT_API_KEY")
    api_secret = os.getenv("LIVEKIT_API_SECRET")
    url = os.getenv("LIVEKIT_URL")
    
    if not all([api_key, api_secret, url]):
        raise HTTPException(status_code=500, detail="LiveKit credentials not configured")
    
    # Create access token
    token = api.AccessToken(api_key, api_secret)
    token.with_identity(identity)
    token.with_name(identity)
    token.with_grants(api.VideoGrants(
        room_join=True,
        room=room,
        can_publish=True,
        can_subscribe=True
    ))
    
    return {
        "token": token.to_jwt(),
        "url": url,
        "room": room,
        "identity": identity
    }

@app.post("/dispatch-agent")
async def dispatch_agent(request: AgentDispatchRequest):
    """Acknowledge agent dispatch request - agents should already be running as workers"""
    
    try:
        # Since LiveKit Agents work with a worker dispatch system,
        # we can't directly dispatch agents via API calls.
        # Instead, agents should be running as workers and will automatically
        # be assigned to rooms when participants join.
        
        print(f"Agent dispatch request received for room: {request.room}")
        print(f"Languages: {request.languages}")
        print(f"Agent type: {request.agent_type}")
        
        # Check if LiveKit credentials are configured
        api_key = os.getenv("LIVEKIT_API_KEY")
        api_secret = os.getenv("LIVEKIT_API_SECRET")
        
        if not all([api_key, api_secret]):
            raise HTTPException(status_code=500, detail="LiveKit credentials not configured")
        
        return {
            "success": True,
            "message": f"Agent dispatch acknowledged for room '{request.room}'. If you have agents running as workers, they should automatically join the room.",
            "room": request.room,
            "languages": request.languages,
            "note": "Make sure your translation agent is running with: python translation_agent_v2.py dev"
        }
        
    except Exception as e:
        print(f"Agent dispatch error: {e}")
        raise HTTPException(
            status_code=500, 
            detail=f"Failed to process agent dispatch: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port) 