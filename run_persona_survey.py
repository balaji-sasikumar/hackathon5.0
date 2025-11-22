import pandas as pd
import json
import os
from openai import AzureOpenAI

client = AzureOpenAI(
    api_key=os.getenv("OPENAI_KEY"),
    api_version=os.getenv("OPENAI_VERSION"),
    azure_endpoint=os.getenv("OPENAI_ENDPOINT"),
)


def generate_system_prompt(profile):
    demo = profile['demographics']
    pol = profile['political_identity']
    dig = profile['digital_behavior']
    geo = profile['geographic_context']

    return f"""
You are a synthetic voter profile from Tamil Nadu, India. 
You must act, speak, and think exactly like this persona. 
Do not break character.

--- PERSONA DETAILS ---

1. DEMOGRAPHICS:
   - Age: {demo.get('age')}
   - Gender: {demo.get('gender')}
   - Location: {demo.get('location')}
   - Family Status: {demo.get('family_status')}

2. POLITICAL IDENTITY:
   - Party Membership: {pol.get('party_member')}
   - Engagement Level: {pol.get('engagement_level')}
   - Constituency Context: {pol.get('constituency_history')}

3. DIGITAL BEHAVIOR:
   - Interests: {dig.get('content_preferences')}
   - Engagement Style: {dig.get('engagement_patterns')}
   - Emotional Tendency: {dig.get('emotional_tendencies')}

4. GEOGRAPHIC CONTEXT:
   - Constituency: {geo.get('constituency')}
   - Local Issues: {geo.get('local_issues')}

--- INSTRUCTIONS ---
- For each question, select ONLY one option: A, B, C, or D.
- Provide the answer as: "A", "B", "C", or "D".
- Stay fully in-character.
"""


def load_questions(file_path="Persona Questions.xlsx"):
    df = pd.read_excel(file_path)

    required = ["Question", "Option A", "Option B", "Option C", "Option D"]
    if not all(col in df.columns for col in required):
        raise ValueError(f"XLSX must contain columns: {required}")

    questions = []
    for idx, row in df.iterrows():
        questions.append({
            "id": f"Q{idx + 1}",
            "question": row["Question"],
            "options": {
                "A": row["Option A"],
                "B": row["Option B"],
                "C": row["Option C"],
                "D": row["Option D"]
            }
        })

    return questions


def ask_model(system_prompt, question_item):
    q_text = f"""
Question: {question_item['question']}

Options:
A. {question_item['options']['A']}
B. {question_item['options']['B']}
C. {question_item['options']['C']}
D. {question_item['options']['D']}

Respond with ONLY the letter (A/B/C/D).
"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": q_text}
        ]
    )

    ans = response.choices[0].message.content.strip()

    # extract only valid A/B/C/D
    ans = ans.replace(".", "").upper()
    if ans not in ["A", "B", "C", "D"]:
        ans = "A"   # fallback

    return ans


def run_persona_survey_json(profile):
    system_prompt = generate_system_prompt(profile)
    questions = load_questions()

    results = {}

    for q in questions:
        ans = ask_model(system_prompt, q)
        results[q["id"]] = ans

    return results
