import os
import json

from dotenv import load_dotenv
from groq import Groq


load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

client = Groq(api_key=api_key)


def review_code(code, language):

    prompt = f"""
You are an expert software code reviewer.

Review the following {language} code.

Return a JSON object with exactly these fields:

{{
    "score": 90,
    "bugs": 0,
    "suggestions": 2,
    "review": "Explain the problems and improvements.",
    "corrected_code": "Corrected source code"
}}

Rules:

- Keep the original language.
- Find syntax errors.
- Find logical errors.
- Find bugs.
- Give suggestions.
- If the code is correct, return the same code.
- corrected_code must contain only code.
- Preserve indentation.
- Preserve line breaks.
- Do not convert the code to another language.
- For HTML, keep proper HTML indentation.
- Do not use markdown code fences.

Language:
{language}

Source Code:
{code}
"""

    try:

        response = client.chat.completions.create(

            model="llama-3.3-70b-versatile",

            messages=[
                {
                    "role": "system",
                    "content": "You are a code reviewer. Always return valid JSON."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],

            temperature=0.1,

            response_format={
                "type": "json_object"
            }
        )


        text = response.choices[0].message.content

        print("GROQ RESPONSE:")
        print(text)


        result = json.loads(text)


        corrected_code = result.get(
            "corrected_code",
            code
        )


        if not corrected_code:
            corrected_code = code


        return {

            "score": result.get(
                "score",
                0
            ),

            "bugs": result.get(
                "bugs",
                0
            ),

            "suggestions": result.get(
                "suggestions",
                0
            ),

            "review": result.get(
                "review",
                "No review generated"
            ),

            "corrected_code": corrected_code

        }


    except Exception as e:

        print("GROQ ERROR:", repr(e))

        return {

            "score": 0,

            "bugs": 0,

            "suggestions": 0,

            "review": "AI Review Failed",

            "corrected_code": code

        }