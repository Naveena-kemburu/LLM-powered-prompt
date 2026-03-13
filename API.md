# API Documentation

REST API documentation for the LLM Prompt Router service.

## Base URL

```
http://localhost:5000
```

## Endpoints

### Health Check

Check if the service is running.

**Endpoint**: `GET /health`

**Response**:
```json
{
  "status": "healthy"
}
```

**Example**:
```bash
curl http://localhost:5000/health
```

---

### Classify Message

Process a single user message through the routing pipeline.

**Endpoint**: `POST /classify`

**Request Body**:
```json
{
  "message": "string (required)"
}
```

**Response**:
```json
{
  "intent": "code|data|writing|career|unclear",
  "confidence": 0.0-1.0,
  "response": "string"
}
```

**Example**:
```bash
curl -X POST http://localhost:5000/classify \
  -H "Content-Type: application/json" \
  -d '{
    "message": "how do i sort a list in python?"
  }'
```

**Response**:
```json
{
  "intent": "code",
  "confidence": 0.95,
  "response": "To sort a list in Python, use the sorted() function..."
}
```

**Error Responses**:

- `400 Bad Request`: Missing or empty message field
```json
{
  "error": "Missing 'message' field in request body"
}
```

- `500 Internal Server Error`: Server error during processing
```json
{
  "error": "Internal server error"
}
```

---

### Batch Classify

Process multiple messages in a single request.

**Endpoint**: `POST /batch`

**Request Body**:
```json
{
  "messages": ["string", "string", ...]
}
```

**Response**:
```json
{
  "results": [
    {
      "intent": "string",
      "confidence": 0.0-1.0,
      "response": "string"
    },
    ...
  ]
}
```

**Example**:
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

**Response**:
```json
{
  "results": [
    {
      "intent": "code",
      "confidence": 0.95,
      "response": "To sort a list in Python..."
    },
    {
      "intent": "data",
      "confidence": 0.91,
      "response": "The average of 10, 20, and 30 is..."
    },
    {
      "intent": "writing",
      "confidence": 0.87,
      "response": "I'd be happy to help improve your sentence..."
    }
  ]
}
```

**Error Responses**:

- `400 Bad Request`: Missing or invalid messages field
```json
{
  "error": "Missing 'messages' field in request body"
}
```
or
```json
{
  "error": "'messages' must be a list"
}
```

---

## Intent Types

The classifier can identify the following intents:

| Intent | Description | Example Messages |
|--------|-------------|------------------|
| `code` | Programming questions, debugging, code review | "how do i sort a list?", "fix this bug" |
| `data` | Data analysis, statistics, datasets | "what's the average?", "explain pivot tables" |
| `writing` | Text improvement, grammar, clarity | "make this more professional", "fix my paragraph" |
| `career` | Job search, interviews, career planning | "resume tips", "interview preparation" |
| `unclear` | Ambiguous or out-of-scope requests | "hey", "help me", multiple intents |

## Confidence Scores

Confidence scores range from 0.0 to 1.0:

- **0.9 - 1.0**: Very confident classification
- **0.7 - 0.9**: Confident classification
- **0.5 - 0.7**: Moderate confidence
- **0.0 - 0.5**: Low confidence (often results in "unclear")

## Rate Limiting

The service uses OpenAI's API, which has rate limits based on your plan:

- Free tier: ~3 requests/minute
- Pay-as-you-go: ~60 requests/minute
- Higher tiers: Contact OpenAI for limits

## Logging

All requests are automatically logged to `route_log.jsonl` in JSON Lines format:

```json
{"intent": "code", "confidence": 0.95, "user_message": "...", "final_response": "..."}
```

## Error Handling

The service gracefully handles:

- Malformed JSON from LLM responses
- Invalid intent labels
- Out-of-range confidence scores
- API failures and timeouts
- Empty or missing messages

All errors default to `{"intent": "unclear", "confidence": 0.0}` to prevent crashes.

## Authentication

Currently, the API does not require authentication. In production, consider adding:

- API key authentication
- Rate limiting per client
- Request validation
- HTTPS/TLS encryption

## Testing

Use the provided test script to validate the service:

```bash
python test_router.py
```

Or test individual endpoints:

```bash
# Health check
curl http://localhost:5000/health

# Single message
curl -X POST http://localhost:5000/classify \
  -H "Content-Type: application/json" \
  -d '{"message": "test message"}'

# Batch messages
curl -X POST http://localhost:5000/batch \
  -H "Content-Type: application/json" \
  -d '{"messages": ["msg1", "msg2"]}'
```

## Performance

Typical response times:

- Classification: 200-500ms
- Generation: 500-2000ms
- Total: 700-2500ms per request

Batch requests process messages sequentially, so total time = n × single request time.

## Customization

To customize the service:

1. **Add new intents**: Edit `prompts.py` to add new expert personas
2. **Adjust confidence**: Modify temperature in `router.py`
3. **Change model**: Set `OPENAI_MODEL` environment variable
4. **Add middleware**: Extend `app.py` with Flask middleware

## Support

For issues or questions:

1. Check the logs: `docker-compose logs -f`
2. Review `route_log.jsonl` for request history
3. Run validation: `python validate_requirements.py`
4. See full documentation in `README.md`
