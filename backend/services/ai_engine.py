from groq import Groq
import os

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def get_ai_fix(error):
    response = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are an AIOps system."},
            {"role": "user", "content": error}
        ],
        model="llama-3.3-70b-versatile"
    )

    return response.choices[0].message.content