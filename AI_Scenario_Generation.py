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
    response = client.chat(model="gemma3:4b", messages=[
        {"role": "user", "content": (
            "Generate a simple phishing email scenario for security awareness training. "
            "Make the scenario plausible but clearly educational, ensure all content is fictional and not real. "
            "Do not use the names of any real companies, brands, products, services, banks, or organisations "
            "(for example: PayPal, Amazon, Microsoft, Google, Apple, Netflix, etc.). "
            "Invent fictional company and brand names instead. "
            "Return difficulty out of easy, medium, hard."
            "Return category such as: phishing, smishing, vishing, social engineering, malware, ransomware, business email compromise, spear phishing, whaling, or other relevant categories."
            "Answers should be one word: click vs don't click, suspicious vs not suspicious, or similar."
            "Return ONLY valid JSON in this exact structure:\n"
            "{\n"
            '  "category": "string",\n'
            '  "difficulty": "string",\n'
            '  "sender": "string",\n'
            '  "recipient": "string",\n'
            '  "subject": "string",\n'
            '  "emailBody": "string",\n'
            '  "redFlags": ["string"]\n'
            '  "correctAnswer": "string"\n'
            '  "wrongAnswer": "string"\n'
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

@app.get("/detailed-scenario")
def generate_detailed_scenario():
    response = client.chat(model="gemma3:4b", messages=[
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
