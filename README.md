# LiveKit Token Server

A FastAPI-based token server for LiveKit that provides authentication tokens and agent dispatch functionality for real-time translation services.

## Features

- **Token Generation**: Generate LiveKit access tokens for room participants
- **Agent Dispatch**: Acknowledge agent dispatch requests for translation services
- **CORS Support**: Configured for web client access
- **Environment Configuration**: Secure credential management via environment variables

## Local Development

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set up environment variables (copy from `env.example`):
   ```bash
   cp env.example .env
   ```
   
   Edit `.env` and add your LiveKit credentials:
   ```
   LIVEKIT_API_KEY=your_actual_api_key
   LIVEKIT_API_SECRET=your_actual_api_secret
   LIVEKIT_URL=wss://your-livekit-server.livekit.cloud
   ```

3. Run the server:
   ```bash
   python token_server.py
   ```

The server will start on `http://localhost:8000`. Visit `http://localhost:8000/docs` to see the API documentation.

## Railway Deployment

### Prerequisites
- Railway account ([railway.app](https://railway.app))
- LiveKit server credentials

### Deploy Steps

1. **Connect Repository**:
   - Go to [Railway Dashboard](https://railway.app/dashboard)
   - Click "New Project" → "Deploy from GitHub repo"
   - Select this repository

2. **Configure Environment Variables**:
   In your Railway project dashboard, go to Variables tab and add:
   ```
   LIVEKIT_API_KEY=your_actual_api_key
   LIVEKIT_API_SECRET=your_actual_api_secret
   LIVEKIT_URL=wss://your-livekit-server.livekit.cloud
   ```

3. **Deploy**:
   - Railway will automatically detect the Python project
   - The `railway.json` configuration will handle the build and start commands
   - Your app will be available at the generated Railway URL

### Configuration Files

- `requirements.txt`: Python dependencies
- `railway.json`: Railway-specific build and deployment configuration
- `env.example`: Template for required environment variables

## API Endpoints

### GET `/token`
Generate a LiveKit access token for a participant.

**Parameters**:
- `room` (string): Room name
- `identity` (string): Participant identity

**Response**:
```json
{
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "url": "wss://your-livekit-server.livekit.cloud",
  "room": "room-name",
  "identity": "participant-id"
}
```

### POST `/dispatch-agent`
Acknowledge agent dispatch request for translation services.

**Body**:
```json
{
  "room": "room-name",
  "livekit_url": "wss://your-livekit-server.livekit.cloud",
  "agent_type": "translation",
  "languages": ["English", "Hindi"]
}
```

**Response**:
```json
{
  "success": true,
  "message": "Agent dispatch acknowledged for room 'room-name'...",
  "room": "room-name",
  "languages": ["English", "Hindi"],
  "note": "Make sure your translation agent is running with: python translation_agent_v2.py dev"
}
```

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `LIVEKIT_API_KEY` | LiveKit API key | Yes |
| `LIVEKIT_API_SECRET` | LiveKit API secret | Yes |
| `LIVEKIT_URL` | LiveKit server WebSocket URL | Yes |
| `PORT` | Server port (auto-set by Railway) | No |

## Notes

- The agent dispatch endpoint acknowledges requests but doesn't directly spawn agents
- Translation agents should be running separately as LiveKit workers
- The server includes comprehensive CORS configuration for web client compatibility
