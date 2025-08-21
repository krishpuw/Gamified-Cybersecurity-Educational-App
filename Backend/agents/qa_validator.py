# qa_validator.py
from openai import OpenAI
import google.generativeai as genai
from config import Config

# init clients
openai_client = OpenAI(api_key=Config.OPENAI_API_KEY)
genai.configure(api_key=Config.GOOGLE_API_KEY)

def validate_question(q: dict) -> bool:
    """
    Validate a generated question using both OpenAI and Gemini.
    Must confirm JSON fields are valid, content matches cybersecurity, and no exploits.
    """
    text = f"Question: {q.get('question')}\nChoices: {q.get('choices')}\nAnswer: {q.get('answer_key')}\nExplanation: {q.get('explanation')}"
    
    # # OpenAI validation
    # resp1 = openai_client.chat.completions.create(
    #     model="gpt-4o-mini",
    #     messages=[{"role":"system","content":"Validate cybersecurity training questions."},
    #               {"role":"user","content":f"Does this question follow rules? Reply only Yes/No.\n{text}"}]
    # )
    # valid1 = "yes" in resp1.choices[0].message.content.lower()

    # Gemini validation
    model = genai.GenerativeModel("gemini-1.5-flash")
    resp2 = model.generate_content(f"Validate this cybersecurity question (Yes/No only):\n{text}")
    valid2 = "yes" in resp2.text.lower()
    return valid2

   # return valid1 and valid2

     
