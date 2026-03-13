# LLM-Powered Prompt Router for Intent Classification

A production-ready Python service that intelligently routes user requests to specialized AI personas using a two-step classification and generation process. This implementation demonstrates fundamental prompt engineering patterns for building sophisticated, multi-purpose AI applications.

## Overview

Instead of using a single monolithic prompt, this system uses a collection of specialized prompts, each tuned for different tasks. The router first classifies the user's intent, then delegates to a focused 'expert' persona designed specifically for that task.

### How It Works

```
User Message → Classify Intent → Route to Expert → Generate Response → Log Result
```

1. **Classification**: A lightweight LLM call classifies the user's intent
2. **Routing**: The system selects the appropriate expert persona based on intent
3. **Generation**: A second LLM call generates a specialized response
4. **Logging**: All interactions are logged to `route_log.jsonl`

### Supported Intents

- **code**: Programming questions, debugging, code review, technical implementation
- **data**: Data analysis, statistics, datasets, numerical patterns, visualizations
- **writing**: Text improvement, grammar, clarity, tone, structure feedback
- **career**: Job search, interviews, career planning, professional development
- **unclear**: Ambiguous requests that need clarification

## Architecture

```
├── prompts.py          # System prompts for each expert persona
├── router.py           # Core routing logic (classify_intent, route_and_respond)
├── app.py              # Flask REST API server
├── cli.py              # Interactive command-line interface
├── test_router.py      # Automated test suite
├── route_log.jsonl     # JSON Lines log file
├── requirements.txt    # Python dependencies
├── Dockerfile          # Container configuration
└── docker-compose.yml  # Docker Compose setup
```

## Setup Instructions

### Prerequisites

- Python 3.11+ or Docker
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))

### Option 1: Local Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/Naveena-kemburu/LLM-powered-prompt
   cd llm-prompt-router
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edited .env and my OPENAI_API_KEY
   ```

5. **Load environment variables**
   ```bash
   Get-Content .env | ForEach-Object { $var = $_.Split('='); [Environment]::SetEnvironmentVariable($var[0], $var[1]) }
   ```

### Option 2: Docker Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/Naveena-kemburu/LLM-powered-prompt
   cd llm-prompt-router
   ```

2. **Configure environment variables**
   ```bash
   cp .env.example .env
   ```

3. **Build and run with Docker Compose**
   ```bash
   docker-compose up --build
   ```

## Usage

### 1. Command-Line Interface (Interactive)

Run the CLI in interactive mode for a conversational experience:

```bash
python cli.py
```

Example session:
```
You: how do i sort a list in python?

[Intent: CODE] [Confidence: 0.95]

Here's how to sort a list in Python:

```python
# Sort in place
my_list = [3, 1, 4, 1, 5]
my_list.sort()

# Return new sorted list
sorted_list = sorted(my_list)
```

### 3. REST API Server

Start the Flask server:

```bash
python app.py
```

The API will be available at `http://localhost:5000`

#### API Endpoints

**Health Check**
```bash
curl http://localhost:5000/health
```

**Classify Single Message**
```bash
curl -X POST http://localhost:5000/classify \
  -H "Content-Type: application/json" \
  -d '{"message": "how do i fix this bug in my code?"}'
```

Response:
```json
{
  "intent": "code",
  "confidence": 0.92,
  "response": "To help you fix the bug, I need to see your code..."
}
```

**Batch Classification**
```bash
curl -X POST http://localhost:5000/batch \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      "how do i sort a list in python?",
      "what is the average of 10, 20, 30?",
      "help me improve this sentence"
    ]
  }'
```

### 4. Run Test Suite

Execute the automated test suite with 15 predefined test messages:

```bash
python test_router.py
```

This will:
- Process all test messages through the router
- Display intent classification and confidence scores
- Log all results to `route_log.jsonl`
- Show a summary of intent distribution



## Docker Deployment

### Build the image
```bash
docker build -t llm-prompt-router .
```

### Run with Docker Compose
```bash
docker-compose up -d
```

### View logs
```bash
docker-compose logs -f
```

### Stop the service
```bash
docker-compose down
```


