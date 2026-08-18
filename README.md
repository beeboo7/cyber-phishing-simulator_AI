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

### Run the scenario API
```
python -m uvicorn AI_Scenario_Generation:app --reload
```
Starts a FastAPI server exposing `/simple-scenario` and `/detailed-scenario` endpoints.

### Run the feedback API
```
python -m uvicorn AI_Feedback_Generation:app --reload
```
Starts a FastAPI server exposing a `/feedback` endpoint.

## API

### `GET /simple-scenario`
Generates a phishing email scenario for security awareness training wit h a single correct/incorrect classification.

**Response:**
```json
{
  "title": "string",
  "scenarioDescription": "string",
  "category": "string",
  "difficulty": "string",
  "interactionType": "string",
  "sender": "string",
  "recipient": "string",
  "subject": "string",
  "emailBody": "string",
  "redFlags": ["string"],
  "correctAnswer": "string",
  "wrongAnswer": "string"
}
```

The learner's task is to classify the scenario as suspicious or not suspicious, matching correctAnswer.

### `GET /detailed-scenario`
Generates a more detailed phishing scenario for security awareness training, where the learner must identify specific suspicious elements within the content rather than making a single overall classification.

**Response:**
```json
{
  "title": "string",
  "scenarioDescription": "string",
  "category": "string",
  "difficulty": "string",
  "interactionType": "string",
  "sender": "string",
  "recipient": "string",
  "subject": "string",
  "emailBody": "string",
  "redFlags": ["string"],
  "neutralFlags": ["string"]
}
```

The learner's task is to correctly identify which specific elements of the scenario are genuine indicators of suspicious activity (redFlags), while correctly disregarding elements that look suspicious at first glance but are actually legitimate (neutralFlags, used as distractors).

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
{
  "score": 0,
  "explanation": "string",
  "tips": ["string"],
  "redFlagsMissed": ["string"]
}
```

Feedback includes a score (0-100), explanation, tips, and red flags missed.
