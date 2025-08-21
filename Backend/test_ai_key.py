# import os
# from openai import OpenAI
# from dotenv import load_dotenv
# from pathlib import Path
# env_path = Path(__file__).resolve().parent / ".env"
# load_dotenv(env_path)

# # Load from environment
# api_key = os.getenv("OPENAI_API_KEY")

# if not api_key:
#     print("❌ OPENAI_API_KEY not found in environment!")
#     exit(1)

# print(f"✅ Using API key: {api_key[:6]}... (length {len(api_key)})")

# # Initialize client
# client = OpenAI(api_key=api_key)

# try:
#     response = client.chat.completions.create(
#         model="gpt-4o-mini",
#         messages=[
#             {"role": "system", "content": "You are a test assistant."},
#             {"role": "user", "content": "Say hello in one short sentence."},
#         ],
#     )
#     print("✅ Response:", response.choices[0].message.content)

# except Exception as e:
#     print("❌ OpenAI API call failed:", repr(e))


import os
from pathlib import Path
from dotenv import load_dotenv
import google.generativeai as genai

# Load .env that sits next to this file (adjust path if needed)
env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(env_path)

api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    print("❌ GOOGLE_API_KEY not found in environment!")
    raise SystemExit(1)

print(f"✅ Using GOOGLE_API_KEY: {api_key[:6]}... (length {len(api_key)})")

# Configure the SDK
genai.configure(api_key=api_key)

# Choose a model (flash = fast/cheap, pro = higher quality)
model = genai.GenerativeModel("gemini-1.5-flash")

try:
    resp = model.generate_content("Say hello in one short sentence.")
    print("✅ Response:", resp.text.strip())
except Exception as e:
    print("❌ Gemini API call failed:", repr(e))

