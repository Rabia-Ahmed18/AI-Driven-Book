# HuggingFace Spaces Startup Script
import os
from backend.src.api.main import app

# For HuggingFace Spaces, we need to expose the FastAPI app instance
# HuggingFace will automatically handle the port configuration

# Set the port from the environment variable if available
port = int(os.environ.get("PORT", 8000))

# The app instance is what HuggingFace Spaces will use to run the application
# This follows the convention that HuggingFace Spaces expects
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=port)