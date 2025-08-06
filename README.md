# 📚 StudyBuddy API Documentation

**Base URL:**  

https://studybuddy-api.onrender.com
---

## 🔄 Common Request Format

Each route expects:

- A **form-data** or **JSON** object containing:
  - `message`: `string` — User prompt
  - `history`: `array` — Conversation history (initially an empty array `[]`)
  - A media file (`image`, `pdf`, `audio`) if applicable

Each response returns:
```
{
  "reply": "LLM generated output",
  "history": [
    { "role": "human", "content": "Explain what is AI?" },
    { "role": "ai", "content": "LLM response" }
  ]
}
```
📝 The history field is a list of objects with role and content. This format remains consistent across all routes.

🖼️ Image Processing
Endpoint: /studybuddy/process-image

Method: POST

Content-Type: form-data

Form Fields:

```
req: JSON string of the format:

{
  "message": "Your question",
  "history": []
}
image: Image file to be processed
```

📄 PDF Processing
Endpoint: /studybuddy/process-pdf

Method: POST

Content-Type: form-data

Form Fields:

```
req: JSON string

pdf: PDF file to be processed
```

🎧 Audio Processing
Endpoint: /studybuddy/process-audio

Method: POST

Content-Type: form-data

Form Fields:

```
req: JSON string

audio: Audio file to be processed
```

🗺️ Roadmap Generation
Endpoint: /studybuddy/roadmap

Method: POST

Content-Type: application/json

Request Body:

```
{
  "message": "Your input",
  "history": []
}
```

📺 YouTube Video Processing
Endpoint: /studybuddy/roadmap

Method: POST

Content-Type: application/json

Request Body:
```
{
  "message": "YouTube link or query related to it",
  "history": []
}
```
