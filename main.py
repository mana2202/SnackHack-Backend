from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/generate")
async def generate(request: Request):
    data = await request.json()

    ingredients = data.get("ingredients", "")
    mood = data.get("mood", "any")
    time = data.get("time", "30")
    restrictions = data.get("restrictions", "")

    prompt = f"""
You are a helpful cooking assistant. Generate one {restrictions} {mood} recipe 
with the following ingredients - {ingredients} which I can cook in under {time} minutes.
Include:
- A fun title
- Ingredient list (with possible substitutions in brackets)
- Clear step-by-step instructions (easy to follow)
"""

    messages = [{"role": "user", "content": prompt}]
    text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    model_inputs = tokenizer([text], return_tensors="pt").to(model.device)

    generated_ids = model.generate(
        **model_inputs,
        max_new_tokens=1024,
        do_sample=True,
        temperature=0.9,
        top_p=0.95
    )

    output_ids = generated_ids[0][len(model_inputs.input_ids[0]):].tolist()
    content = tokenizer.decode(output_ids, skip_special_tokens=True)

    return JSONResponse(content={"recipe": content})
