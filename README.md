# cyber-phishing-simulator_AI

AI-powered phishing simulation tool for cybersecurity awareness training. Uses Ollama to generate realistic phishing scenarios and evaluate learner responses with constructive feedback.

## Setup

1. Install dependencies:
   ```
   pip install ollama python-dotenv fastapi uvicorn pydantic
   ```

2. Create a `.env` file in the project root:
   ```
   API_KEY= {YOUR_API_KEY}
   ```

## Usage

### Generate a phishing scenario
```
python AI_Scenario_Generation.py
```
Prints a generated phishing email scenario with red flags to the console.

### Run the feedback API
```
uvicorn AI_Feedback_Generation:app --reload
```
Starts a FastAPI server exposing a `/feedback` endpoint.

## API

### `POST /feedback`
Evaluates a learner's response to a phishing scenario.

**Request body:**
```json
{
  "scenario_content": "string",
  "scenarioChoices": [
    { "id": 1, "text": "string", "isCorrect": true, "scenarioId": 1 }
  ],
  "selectedChoiceId": 1
}
```

**Response:**
```json
{ "feedback": "string" }
```

Feedback includes a score (0-100), explanation, tips, and red flags missed.
