from fastapi import FastAPI, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional
import os
import json
from .config import Config
from .utils.auth import generate_token, get_current_user
from .services.recommender import recommend_products
from .services.calculator import calculate_loan_details
from .services.llm_client import call_llm

app = FastAPI(title="AI Loan Advisor")


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(BASE_DIR, "..", "frontend")

if not os.path.exists(FRONTEND_DIR):
    raise RuntimeError(f"Frontend directory not found at {FRONTEND_DIR}")


app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")

@app.get("/")
async def index():
    index_path = os.path.join(FRONTEND_DIR, "index.html")
    if not os.path.exists(index_path):
        raise HTTPException(status_code=404, detail="index.html not found")
    return FileResponse(index_path)

# In-memory storage per user (for demo)
user_profiles = {}
user_chat_histories = {}  # user_id -> list of {"role": "user"|"assistant", "content": str}

# Request/Response models
class LoginRequest(BaseModel):
    user_id: str

class ProfileRequest(BaseModel):
    amount: float
    purpose: str
    monthly_income: float
    existing_emi: Optional[float] = 0
    tenure: int
    employment_type: str
    business_income: Optional[float] = 0

class AdviseRequest(BaseModel):
    query: str

@app.post("/api/login")
async def login(req: LoginRequest):
    token = generate_token(req.user_id)
    return {"token": token}

@app.post("/api/profile", dependencies=[Depends(get_current_user)])
async def set_profile(profile: ProfileRequest, user_id: str = Depends(get_current_user)):
    user_profiles[user_id] = profile.dict()
    return {"status": "profile saved"}

@app.post("/api/advise", dependencies=[Depends(get_current_user)])
async def advise(req: AdviseRequest, user_id: str = Depends(get_current_user)):
    profile = user_profiles.get(user_id)
    if not profile:
        raise HTTPException(status_code=400, detail="Please provide your profile first via /api/profile")

    # Get recommendations
    recommendations = recommend_products(profile)
    if not recommendations:
        return {
            "advice": "Based on your inputs, no product matches your criteria. Please consider adjusting the loan amount, tenure, or purpose.",
            "recommendations": []
        }

    # Prepare recommendation text for grounding
    rec_text = ""
    for idx, rec in enumerate(recommendations, 1):
        p = rec["product"]
        d = rec["details"]
        rec_text += f"{idx}. {p['name']}: EMI ₹{d['emi']:,.2f}, Total Interest ₹{d['total_interest']:,.2f}, Total Payment ₹{d['total_payment']:,.2f} at {p['interest_rate']}% p.a., tenure {profile['tenure']} months.\n"

    # Build conversation history (last 3 exchanges)
    history = user_chat_histories.get(user_id, [])
    # Keep only last 3 messages 
    recent_history = history[-3:] if len(history) > 3 else history
    history_str = ""
    for msg in recent_history:
        role = "User" if msg["role"] == "user" else "Assistant"
        history_str += f"{role}: {msg['content']}\n"

    # Construct the full prompt with grounding + history
    prompt = f"""You are a responsible loan advisor. You have the following data about the user:
- Amount needed: ₹{profile['amount']:,.0f}
- Monthly income: ₹{profile['monthly_income']:,.0f}
- Existing EMI: ₹{profile['existing_emi']:,.0f}
- Purpose: {profile['purpose']}
- Preferred tenure: {profile['tenure']} months

Based on our calculations, the most suitable products are:
{rec_text}

Previous conversation (for context):
{history_str}

The user's new query is: {req.query}

Always base your answers on the data above. 
Always show the user's profile summary.
Do not invent new products, rates, or numbers.  
If asked something outside this data, politely say you don't have that information and suggest they contact a human advisor.  
Include the following disclaimer in every final response: *"Disclaimer: Final loan approval is subject to underwriting and verification by the lending partner."*
Keep your answers clear, concise, and helpful.
"""

    # Call LLM
    llm_response = call_llm(prompt)
    if not llm_response:
        llm_response = f"Based on your profile, we recommend the following:\n{rec_text}\nDisclaimer: Final loan approval is subject to underwriting and verification by the lending partner."
    else:
        if "Disclaimer" not in llm_response:
            llm_response += "\n\n Disclaimer:Final loan approval is subject to underwriting and verification by the lending partner."

    # Store chat history
    if user_id not in user_chat_histories:
        user_chat_histories[user_id] = []
    user_chat_histories[user_id].append({"role": "user", "content": req.query})
    user_chat_histories[user_id].append({"role": "assistant", "content": llm_response})
    # Keep only last 10 messages to bound memory
    if len(user_chat_histories[user_id]) > 10:
        user_chat_histories[user_id] = user_chat_histories[user_id][-10:]

    return {
        "recommendations": recommendations,
        "advice": llm_response
    }