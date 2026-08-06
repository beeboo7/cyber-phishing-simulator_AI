import random

import ollama
import dotenv
import os
import json
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

dotenv.load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://localhost:5173", "http://localhost:4200"],
    allow_methods=["*"],
    allow_headers=["*"],
)

client = ollama.Client(
    host="https://api.ollama.com",
    headers={"Authorization": f"Bearer {os.getenv('API_KEY')}"}
)

@app.get("/simple-scenario")
def generate_simple_scenario():
    difficulty = random.choice(["Easy", "Medium", "Hard"])
    correct_answer = random.choice(["suspicious", "not suspicious"])
    category = random.choice(["phishing", "smishing", "vishing", "social engineering", "malware", "ransomware", "business email compromise", "spear phishing", "whaling"])
    interactionType = random.choice(["Email", "Text Message", "Phone Call", "Social Media"])

    response = client.chat(model="gemma4", messages=[
        {"role": "user", "content": (
            f"Generate a {difficulty} difficulty phishing email scenario for security awareness training. "
            f"The scenario MUST be an example of a '{correct_answer}' message — "
            f"the correctAnswer field must be exactly '{correct_answer}'. "
            "Make the scenario plausible but clearly educational, ensure all content is fictional and not real. "
            "All names must be entirely fictional. "
            "Invent fictional company and brand names. "
            "If the interactionType is Phone Call, Social Media, or Text Message, the scenario should be adapted accordingly. For example, if the interactionType is Phone Call, the scenario should describe a phone call transcript instead of an email and use phone numbers instead of email addresses. "
            f"Set the difficulty field to exactly '{difficulty}'. "
            f"Set the category field to exactly '{category}'. "
            f"Set the interactionType field to exactly '{interactionType}'. "
            "Answers should be one word: suspicious or not suspicious. "
            "Return ONLY valid JSON in this exact structure:\n"
            "{\n"
            '  "title": "string",\n'
            '  "scenarioDescription": "string",\n'
            '  "category": "string",\n'
            '  "difficulty": "string",\n'
            '  "interactionType": "string",\n'
            '  "sender": "string",\n'
            '  "recipient": "string",\n'
            '  "subject": "string",\n'
            '  "emailBody": "string",\n'
            '  "redFlags": ["string"],\n'
            '  "correctAnswer": "string",\n'
            '  "wrongAnswer": "string"\n'
            "}\n\n"
            "Do not include markdown, code blocks or extra text. "
            "Do not offer follow-up suggestions, ask questions, or prompt for further actions at the end of your response. "
            "Do not provide any additional commentary or analysis beyond the requested email scenario and red flags."
        )}
    ], options={
        "temperature": 1.0,
        "top_p": 0.95,
        "top_k": 50
    })

    raw_content = response.message.content
    print(raw_content)

    cleaned = raw_content.replace("```json", "").replace("```", "").strip()
    return json.loads(cleaned)

@app.get("/detailed-scenario")
def generate_detailed_scenario():
    response = client.chat(model="gemma4", messages=[
        {"role": "user", "content": (
            "Generate a realistic phishing email scenario for security awareness training. "
            "Make the scenario plausible but clearly educational, ensure all content is fictional and not real. "
            "Do not use the names of any real companies, brands, products, services, banks, or organisations "
            "(for example: PayPal, Amazon, Microsoft, Google, Apple, Netflix, etc.). "
            "Invent fictional company and brand names instead. "
            "Return difficulty out of easy, medium, hard."
            "neutralFlags are other options that are not suspicious"
            "Return category such as: phishing, smishing, vishing, social engineering, malware, ransomware, business email compromise, spear phishing, whaling, or other relevant categories."
            "Return ONLY valid JSON in this exact structure:\n"
            "{\n"
            '  "category": "string",\n'
            '  "difficulty": "string",\n'
            '  "sender": "string",\n'
            '  "recipient": "string",\n'
            '  "subject": "string",\n'
            '  "emailBody": "string",\n'
            '  "redFlags": ["string"]\n'
            '  "neutralFlags": ["string"]\n'
            "}\n\n"
            "Do not include markdown, code blocks or extra text."
            "Do not offer follow-up suggestions, ask questions, or prompt for further actions at the end of your response."
            "Do not provide any additional commentary or analysis beyond the requested email scenario and red flags."
        )}
    ])

    raw_content = response.message.content

    print(raw_content)

    cleaned = raw_content.replace("```json", "").replace("```", "").strip()
    return json.loads(cleaned)
