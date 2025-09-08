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
You are a helpful and creative cooking assistant.
Generate ONE recipe that matches the following criteria:
Dietary restrictions: {restrictions} (e.g., vegetarian, vegan, gluten-free)
Mood: {mood} (e.g., cozy, bold, refreshing, quick comfort)
Ingredients: {ingredients}
Time: Must be ready in under {time} minutes
Recipe Format:
Title: Fun, mood-matching, and catchy
Nutrition Snapshot (estimate per serving): Calories, Protein, Carbs, Fat
Ingredient List: List each item with possible substitutions in brackets
Instructions: Numbered steps, conversational and friendly in tone (suitable for beginners)
(Optional) Chef’s Tip: A short tip or variation to enhance the experience
Constraints:
Recipe must be doable in a home kitchen
No rare tools or ingredients outside the list
Avoid meat unless explicitly listed
Prioritize creativity, clarity, and comfort
Keep the tone fun but informative
Output only one recipe
Use short sentences. Be concise. Do not exceed the character limit.
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
