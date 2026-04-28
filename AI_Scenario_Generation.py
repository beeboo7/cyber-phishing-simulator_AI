import ollama
import dotenv 
import os

dotenv.load_dotenv()

client = ollama.Client(
    host="https://api.ollama.com",
    headers={"Authorization": f"Bearer {os.getenv('API_KEY')}"}
)

response = client.chat(model="gemma3:4b", messages=[
    {"role": "user", "content": (
        "Generate a realistic phishing email scenario for security awareness training. "
        "Include the following clearly labeled sections:\n"
        "- Sender: (fake name and spoofed email address)\n"
        "- Recipient: (name and email)\n"
        "- Subject: (urgent or deceptive subject line)\n"
        "- Email Body: (the full phishing message with typical social engineering tactics)\n"
        "- Red Flags: (a bullet list of warning signs present in this email that a user should notice)\n\n"
        "Make the scenario plausible but clearly educational, ensure all content is fictional and not real. "
        "Do not offer follow-up suggestions, ask questions, or prompt for further actions at the end of your response."
        "Do not provide any additional commentary or analysis beyond the requested email scenario and red flags."
    )}
])

print(response.message.content)