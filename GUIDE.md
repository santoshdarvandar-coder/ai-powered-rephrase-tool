# AWS API Gateway Setup

## 1. Create REST API

Go to AWS API Gateway Console.

Choose:
- REST API
- Build

---

## 2. Configure REST API

| Field | Value |
|---|---|
| API Name | RephraseAPI |
| Endpoint Type | Regional |

Click:
- Create API

---

## 3. Create Resource

Navigate to:
- Resources
- Actions → Create Resource

Fill:

| Field | Value       |
|---|-------------|
| Resource Name | rephrase    |
| Resource Path | /rephrase |

Click:
- Create Resource

---

## 4. Create POST Method

Select:
- `/rephrase`

Then:
- Actions → Create Method
- Choose `POST`
- Click ✔

---

## 5. Connect Lambda Function

Configure:

| Field | Value           |
|---|-----------------|
| Integration Type | Lambda Function |
| Lambda Proxy Integration | Enabled         |
| Lambda Function | rephrase-api    |
| Enable CORS | enable          |

Save configuration and allow API Gateway permissions.

---

## 6. Enable CORS (this step is Optional if you already enabled CORS)

Select:
- POST

Then:
- Actions → Enable CORS

Keep defaults:

| Setting | Value |
|---|---|
| Access-Control-Allow-Origin | * |
| Access-Control-Allow-Headers | Content-Type |

Click:
- Enable CORS and replace existing headers

---

## 7. Deploy API

Navigate:
- Actions → Deploy API

Create stage:

```text
Dev
```

Click:
- Deploy

---

## 8. Copy Invoke URL

Example:

```text
https://abc123.execute-api.ap-southeast-2.amazonaws.com/prod
```

Final endpoint:

```text
https://abc123.execute-api.ap-southeast-2.amazonaws.com/prod/paraphrase
```

---

# Streamlit Configuration

Update API URL:

```python
API_URL = "https://abc123.execute-api.ap-southeast-2.amazonaws.com/prod/paraphrase"
```

---

# API Request Example

```json
{
  "language": "English",
  "tone": "Formal",
  "variants": 2,
  "text": "Artificial intelligence is evolving rapidly."
}
```

---

# API Response Example

```json
{
  "results": [
    "1. Artificial intelligence is advancing at a rapid pace.",
    "2. AI technology continues to evolve quickly."
  ]
}
```

---

# Lambda Response Format

```python
return {
    "statusCode": 200,
    "headers": {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*"
    },
    "body": json.dumps({
        "results": results
    })
}
```

Important:
REST API Gateway with Lambda Proxy Integration requires:
- `statusCode`
- `headers`
- `body` as stringified JSON

---
# AWS Lambda + Groq API Setup

## 1.Go to AWS CloudShell Folder

```bash
mkdir clean-lambda
cd clean-lambda
```

---

## 2.Install `requests` (Python Classes)

```bash
pip install requests -t .
```

This isolates dependencies inside the deployment package.

---

## 3.Create `lambda_function.py`

```bash
nano lambda_function.py
```

Paste the following code:

```python
import json
import os
import requests
import re

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

def lambda_handler(event, context):

    try:

        body = json.loads(event["body"])

        language = body.get("language", "English")
        tone = body.get("tone", "Formal")
        variants = int(body.get("variants", 1))
        input_text = body.get("text", "")

        prompt = f"""
Generate exactly {variants} paraphrases.

Language: {language}
Tone: {tone}

Return only numbered paraphrases.

Text:
{input_text}
"""

        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "llama-3.3-70b-versatile",
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "temperature": 0.7
            }
        )

        data = response.json()

        output = data["choices"][0]["message"]["content"]

        matches = re.findall(r"\d+\.\s*(.*)", output)

        if not matches:
            matches = [output]

        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({
                "results": matches
            })
        }

    except Exception as e:

        return {
            "statusCode": 500,
            "headers": {
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({
                "error": str(e)
            })
        }
```

Save the file:

* `CTRL + O`
* Press `Enter`
* `CTRL + X`

---

## 4.ZIP Properly

```bash
zip -r deployment.zip .
```

---

## 5.Upload ZIP to Lambda

In AWS Lambda:

* Upload from ZIP
* Save
* Deploy

---

## 6.Add Environment Variable

Go to:

`Lambda → Configuration → Environment Variables`

Add:

| Key            | Value    |
| -------------- | -------- |
| `GROQ_API_KEY` | your key |

---

## 7.Test Lambda First

Use this test event:

```json
{
  "body": "{\"language\":\"English\",\"tone\":\"Formal\",\"variants\":2,\"text\":\"AI is changing the world.\"}"
}
```

---

## Expected Response

```json
{
  "results": [
    "Artificial intelligence is transforming the world.",
    "AI is reshaping industries and society globally."
  ]
}
```
