import json
import random
import os
import sys
from dotenv import load_dotenv
load_dotenv()

# Try to import openai, but don't fail if it's missing
try:
    from openai import AzureOpenAI
except ImportError:
    openai = None

OPENAI_KEY = os.getenv("OPENAI_KEY")
OPENAI_VERSION = os.getenv("OPENAI_VERSION")
OPENAI_ENDPOINT = os.getenv("OPENAI_ENDPOINT")


# ---------------- LOADING PROFILES ----------------
def load_profiles(filepath="synthetic_profiles.json"):
    if not os.path.exists(filepath):
        print(f"Error: {filepath} not found. Please run generate_persona.py first.")
        sys.exit(1)
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


# ---------------- SYSTEM PROMPT GENERATION ----------------
def generate_system_prompt(profile):
    demo = profile['demographics']
    pol = profile['political_identity']
    dig = profile['digital_behavior']
    geo = profile['geographic_context']

    return f"""
You are a synthetic voter profile from Tamil Nadu, India. You must act, speak, and think exactly like this persona. Do not break character.

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
- Respond only using your demographic, political, and local context.
- Use tone matching engagement style.
- Never say you are AI. You are a citizen of {demo.get('location')}.
"""


# ---------------- STORE Q&A IN TEXT FILE ----------------
def save_to_file(question, answer, filepath="conversation_log.txt"):
    with open(filepath, "a", encoding="utf-8") as log:
        log.write("\n============================\n")
        log.write(f"QUESTION: {question}\n")
        log.write(f"ANSWER: {answer}\n")
        log.write("============================\n")


# ---------------- CHAT LOOP ----------------
def chat_loop(profile, question=None):
    system_prompt = generate_system_prompt(profile)

    print("\n" + "="*60)
    print("GENERATED SYSTEM PROMPT")
    print("="*60)
    print(system_prompt)
    print("="*60 + "\n")

    if AzureOpenAI and OPENAI_KEY:
        print(">> Starting real interaction with persona...")
        client = AzureOpenAI(
            api_key=OPENAI_KEY,
            api_version=OPENAI_VERSION,
            azure_endpoint=OPENAI_ENDPOINT,
        )

        messages = [{"role": "system", "content": system_prompt}]
        print("Type 'quit' to exit.\n")

        while True:
            try:
                user_input = question if question else input("You: ")
                if user_input.lower() in ['quit', 'exit']:
                    break

                messages.append({"role": "user", "content": user_input})

                # --- Send question to model ---
                response = client.chat.completions.create(
                    model="gpt-4.1-mini",
                    messages=messages
                )

                reply = response.choices[0].message.content
                print(f"Persona: {reply}")

                messages.append({"role": "assistant", "content": reply})

                # --- Store the Q&A in text file ---
                save_to_file(user_input, reply)
                return reply

            except KeyboardInterrupt:
                print("\nExiting...")
                break
            except Exception as e:
                print(f"Error: {e}")
                break

    else:
        print(">> MOCK MODE (missing library or API key).")
        print("Type 'quit' to exit.\n")

        while True:
            user_input = input("You: ")
            if user_input.lower() in ['quit', 'exit']:
                break
            
            mock_reply = f"[Mock Persona Reply based on age {profile['demographics']['age']}]"
            print(f"Persona (Mock): {mock_reply}")

            save_to_file(user_input, mock_reply)


# ---------------- MAIN ----------------
if __name__ == "__main__":
    profiles = load_profiles()
    if not profiles:
        print("No profiles found.")
        sys.exit(1)

    selected_profile = random.choice(profiles)
    # chat_loop(selected_profile)
