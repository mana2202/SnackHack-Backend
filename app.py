from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import google.generativeai as genai
import os
import uvicorn
from datetime import datetime

# Initialize FastAPI app
app = FastAPI()

# Add CORS middleware (same as your Colab code)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure Gemini API (replacing the local model)
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
model = genai.GenerativeModel('gemini-2.5-flash-lite')

@app.get("/")
async def health_check():
    return JSONResponse(content={
        "status": "healthy",
        "service": "SnackHack API",
        "timestamp": datetime.now().isoformat()
    })

@app.post("/generate")
async def generate(request: Request):
    try:
        data = await request.json()

        # Extract data (same structure as your Colab code)
        ingredients = data.get("ingredients", "")
        mood = data.get("mood", "any")
        time = data.get("time", "30")
        restrictions = data.get("restrictions", "")

        # Use your exact prompt structure
        prompt = f"""
You are a helpful cooking assistant. Generate one {restrictions} {mood} recipe with the following ingredients - {ingredients} which I can cook in under {time} minutes.
Include:
- A fun title
- Ingredient list (with possible substitutions in brackets)
- Clear step-by-step instructions (easy to follow)
"""

        # Generate using Gemini instead of local model
        response = model.generate_content(prompt)
        content = response.text

        # Return in same format as your Colab code
        return JSONResponse(content={"recipe": content})
        
    except Exception as e:
        return JSONResponse(
            content={"error": str(e)}, 
            status_code=500
        )

# Health check endpoint
@app.get("/health")
async def health():
    return {"status": "healthy", "service": "SnackHack"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
