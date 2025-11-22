import json
import random
import os
import sys

# Try to import openai, but don't fail if it's missing
try:
    import openai
except ImportError:
    openai = None

def load_profiles(filepath="synthetic_profiles.json"):
    if not os.path.exists(filepath):
        print(f"Error: {filepath} not found. Please run generate_persona.py first.")
        sys.exit(1)
    
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def generate_system_prompt(profile):
    demo = profile['demographics']
    pol = profile['political_identity']
    dig = profile['digital_behavior']
    geo = profile['geographic_context']

    prompt = f"""You are a synthetic voter profile from Tamil Nadu, India. You must act, speak, and think exactly like this persona. Do not break character.

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
- Respond to questions based ONLY on your demographics, political leanings, and local context.
- Use a tone appropriate for your age and engagement style (e.g., if 'Angry', be critical; if 'Passive', be brief).
- If asked about local issues, refer to your location and inferred context.
- Do not mention that you are an AI. You are a citizen of {demo.get('location')}.
"""
    return prompt

def chat_loop(profile):
    system_prompt = generate_system_prompt(profile)
    
    print("\n" + "="*60)
    print("GENERATED SYSTEM PROMPT")
    print("="*60)
    print(system_prompt)
    print("="*60 + "\n")

    api_key = os.getenv("OPENAI_API_KEY")
    
    if openai and api_key:
        print(">> OpenAI library detected and API key found. Starting real interaction...")
        client = openai.OpenAI(api_key=api_key)
        messages = [{"role": "system", "content": system_prompt}]
        
        print("Type 'quit' to exit.\n")
        while True:
            try:
                user_input = input("You: ")
                if user_input.lower() in ['quit', 'exit']:
                    break
                
                messages.append({"role": "user", "content": user_input})
                
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=messages
                )
                
                reply = response.choices[0].message.content
                print(f"Persona: {reply}")
                messages.append({"role": "assistant", "content": reply})
                
            except KeyboardInterrupt:
                print("\nExiting...")
                break
            except Exception as e:
                print(f"Error during API call: {e}")
                break
    else:
        print(">> NOTE: 'openai' library not found or OPENAI_API_KEY not set.")
        print(">> Running in MOCK mode. The persona will not actually reply, but you can see the prompt above.")
        print(">> To enable real interaction, install openai (`pip install openai`) and set OPENAI_API_KEY environment variable.")
        print("-" * 60)
        print("Type 'quit' to exit.\n")
        
        while True:
            try:
                user_input = input("You: ")
                if user_input.lower() in ['quit', 'exit']:
                    break
                print(f"Persona (Mock): [I would reply acting as a {profile['demographics']['age']} year old {profile['demographics']['gender']}...]")
            except KeyboardInterrupt:
                print("\nExiting...")
                break

if __name__ == "__main__":
    profiles = load_profiles()
    if not profiles:
        print("No profiles found in JSON.")
        sys.exit(1)
    
    # Select a random profile
    selected_profile = random.choice(profiles)
    chat_loop(selected_profile)
