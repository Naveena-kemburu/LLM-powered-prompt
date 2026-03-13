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
   git clone <repository-url>
   cd llm-prompt-router
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env and add your OPENAI_API_KEY
   ```

5. **Load environment variables**
   ```bash
   # On Linux/Mac:
   export $(cat .env | xargs)
   
   # On Windows (PowerShell):
   Get-Content .env | ForEach-Object { $var = $_.Split('='); [Environment]::SetEnvironmentVariable($var[0], $var[1]) }
   ```

### Option 2: Docker Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd llm-prompt-router
   ```

2. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env and add your OPENAI_API_KEY
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

You: quit
```

### 2. Command-Line Interface (Single Message)

Process a single message and exit:

```bash
python cli.py "explain what a pivot table is"
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

## Design Decisions

### Two-Step Process

The system uses two separate LLM calls:

1. **Classifier Call** (Fast & Cheap)
   - Uses a focused prompt optimized for classification
   - Lower temperature (0.3) for consistent results
   - Minimal token usage (~100 tokens)
   - Returns structured JSON output

2. **Generation Call** (Specialized & High-Quality)
   - Uses expert system prompts tailored to each domain
   - Higher temperature (0.7) for creative responses
   - More tokens for detailed answers (~1000 tokens)

### Error Handling

The system gracefully handles:
- Malformed JSON responses from the LLM
- Invalid intent labels
- Out-of-range confidence scores
- Missing or empty messages
- API failures

All errors default to `{"intent": "unclear", "confidence": 0.0}` to prevent crashes.

### Logging

Every interaction is logged to `route_log.jsonl` in JSON Lines format:

```json
{"intent": "code", "confidence": 0.92, "user_message": "how do i...", "final_response": "..."}
{"intent": "data", "confidence": 0.88, "user_message": "what's the average...", "final_response": "..."}
```

This format is:
- Easy to parse line-by-line
- Append-only (no file locking issues)
- Compatible with log analysis tools

### Expert Personas

Each system prompt is carefully crafted to:
- Establish a clear role and expertise
- Define output format and constraints
- Set appropriate tone and style
- Avoid scope creep into other domains

## Core Requirements Checklist

✅ **Requirement 1**: Four distinct expert system prompts stored in `prompts.py`
- code, data, writing, career, unclear

✅ **Requirement 2**: `classify_intent()` function returns structured JSON
- Returns `{"intent": "string", "confidence": float}`

✅ **Requirement 3**: `route_and_respond()` maps intent to system prompt
- Selects correct prompt from `SYSTEM_PROMPTS` dictionary
- Makes second LLM call with specialized persona

✅ **Requirement 4**: Unclear intents generate clarifying questions
- Never guesses or uses default expert
- Asks user to specify their need

✅ **Requirement 5**: All interactions logged to `route_log.jsonl`
- JSON Lines format with intent, confidence, user_message, final_response

✅ **Requirement 6**: Graceful handling of malformed LLM responses
- Try-except blocks around JSON parsing
- Defaults to unclear intent on parse errors
- No unhandled exceptions

## Testing

The `test_router.py` script includes all 15 required test messages:

1. "how do i sort a list of objects in python?" → code
2. "explain this sql query for me" → code
3. "This paragraph sounds awkward, can you help me fix it?" → writing
4. "I'm preparing for a job interview, any tips?" → career
5. "what's the average of these numbers: 12, 45, 23, 67, 34" → data
6. "Help me make this better." → unclear
7. "I need to write a function... but also i need help with my resume." → unclear
8. "hey" → unclear
9. "Can you write me a poem about clouds?" → unclear
10. "Rewrite this sentence to be more professional." → writing
11. "I'm not sure what to do with my career." → career
12. "what is a pivot table" → data
13. "fxi thsi bug pls: for i in range(10) print(i)" → code
14. "How do I structure a cover letter?" → career
15. "My boss says my writing is too verbose." → writing

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

## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `OPENAI_API_KEY` | Yes | - | Your OpenAI API key |
| `OPENAI_MODEL` | No | `gpt-3.5-turbo` | Model to use for LLM calls |
| `PORT` | No | `5000` | Port for Flask server |

## Troubleshooting

**Issue**: "OPENAI_API_KEY environment variable is not set"
- **Solution**: Ensure you've created a `.env` file and loaded it, or set the variable directly

**Issue**: API rate limit errors
- **Solution**: Add delays between requests or upgrade your OpenAI plan

**Issue**: Docker container fails to start
- **Solution**: Check logs with `docker-compose logs` and verify your `.env` file

**Issue**: JSON parsing errors in logs
- **Solution**: The system handles these gracefully and defaults to "unclear" intent

## Future Enhancements

- Confidence threshold filtering (reject low-confidence classifications)
- Manual intent override with `@code`, `@data` prefixes
- Web UI with real-time intent visualization
- Support for additional LLM providers (Anthropic, Cohere)
- Intent-specific confidence thresholds
- Multi-intent detection and routing
- Conversation history and context management

## License

MIT License - See LICENSE file for details

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.
