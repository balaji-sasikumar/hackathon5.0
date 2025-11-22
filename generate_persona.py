import csv
import json
import os
import random

def load_csv_data(filepath):
    data = []
    if not os.path.exists(filepath):
        print(f"Warning: File not found: {filepath}")
        return data
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                data.append(row)
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
    return data

def get_safe(row, key, default=""):
    return row.get(key, default) if row.get(key) else default

def main():
    base_dir = "Hack-Data"
    
    # Load Data Sources
    print("Loading data...")
    voters = load_csv_data(os.path.join(base_dir, "oraniyil_tn.csv"))
    party_members = load_csv_data(os.path.join(base_dir, "DMK-party-Membership.csv"))
    election_results = load_csv_data(os.path.join(base_dir, "election_result.csv"))
    volunteers = load_csv_data(os.path.join(base_dir, "volunteer.csv"))
    influencers = load_csv_data(os.path.join(base_dir, "influnencer_data.csv"))
    
    # Create Lookup Maps
    party_member_map = {m.get('MobileNo'): m for m in party_members if m.get('MobileNo')}
    
    # Election result map by AC No (assuming AC No matches ac_no in voter data, might need cleaning)
    # Voter data has 'ac_no' like 'AC112', election result might have '112' or 'AC 112'
    election_map = {}
    for res in election_results:
        ac_num = res.get('AC No.', '').strip()
        election_map[ac_num] = res
        # Also try to map by District if AC not found
        district = res.get('District', '').strip()
        if district:
            if district not in election_map:
                election_map[district] = res

    synthetic_profiles = []

    print(f"Processing {len(voters)} voters...")
    
    for voter in voters:
        # 1. Demographics
        # voter_id,party_member,serial_no,name,relative,relation_ship,door_no,age,gender,street_name,street_no,booth_no,date,modification_date,page_no,page_position,consituency_number,is_modified,ac_no,district,status,house_no,is_deleted.data,family_head,family_head_id,updatedAt,numberVerified,phoneNumber
        
        phone = get_safe(voter, 'phoneNumber')
        ac_no_raw = get_safe(voter, 'ac_no') # e.g., AC112
        district = get_safe(voter, 'district')
        
        # Clean AC No for lookup (remove 'AC' prefix if present)
        ac_lookup_key = ac_no_raw.replace('AC', '').strip()
        
        # 2. Political Identity
        is_party_member = get_safe(voter, 'party_member')
        party_data = party_member_map.get(phone, {})
        
        election_context = election_map.get(ac_lookup_key) or election_map.get(district, {})
        
        # 3. Digital Behavior (Synthetic Assignment)
        # Randomly pick a behavior profile from volunteers or influencers to simulate digital footprint
        digital_persona = {}
        if random.random() > 0.7 and volunteers: # 30% chance to match a volunteer profile
            vol_profile = random.choice(volunteers)
            digital_persona = {
                "content_preferences": f"Interested in {vol_profile.get('campaignName', 'general')} campaigns, hashtags: {vol_profile.get('hashtags', '')}",
                "engagement_patterns": f"Active volunteer. Likes: {vol_profile.get('likes', '0')}, Retweets: {vol_profile.get('retweets', '0')}",
                "emotional_tendencies": "High engagement, likely positive sentiment"
            }
        elif random.random() > 0.8 and influencers: # 20% chance to match influencer interaction style
            inf_profile = random.choice(influencers)
            digital_persona = {
                "content_preferences": f"Engages with {inf_profile.get('party', 'political')} content. Media type pref: {inf_profile.get('media_type', 'mixed')}",
                "engagement_patterns": f"Reacts frequently. Total reactions: {inf_profile.get('total_reactions', '0')}",
                "emotional_tendencies": f"Dominant reaction: {max(['like', 'love', 'angry', 'haha'], key=lambda k: int(inf_profile.get(f'{k}_count', 0)) if inf_profile.get(f'{k}_count', '0').isdigit() else 0)}"
            }
        else:
             digital_persona = {
                "content_preferences": "General news, local updates",
                "engagement_patterns": "Passive observer, low interaction",
                "emotional_tendencies": "Neutral"
            }

        profile = {
            "demographics": {
                "age": get_safe(voter, 'age'),
                "gender": get_safe(voter, 'gender'),
                "location": f"{get_safe(voter, 'street_name')}, {get_safe(voter, 'district')}, {ac_no_raw}",
                "family_status": f"{get_safe(voter, 'relation_ship')} of {get_safe(voter, 'relative')}" if get_safe(voter, 'relative') else "Head of Family",
                "ac_no": ac_no_raw,
                "district": district
            },
            "political_identity": {
                "party_member": f"{is_party_member} (Renewed: {get_safe(voter, 'is_party_member_renewed')})",
                "constituency_history": f"District: {district}. Winner: {election_context.get('Winning Candidate', 'Unknown')} ({election_context.get('Party', 'Unknown')})",
                "engagement_level": "High" if get_safe(voter, 'membership_questionnaire') == 'TRUE' else "Medium" if get_safe(voter, 'family_questionnaire') == 'TRUE' else "Low"
            },
            "digital_behavior": digital_persona,
            "geographic_context": {
                "booth_number": get_safe(voter, 'booth_no'),
                "constituency": f"{ac_no_raw} - {get_safe(voter, 'consituency_number')}",
                "local_issues": f"Inferred from {district} context"
            }
        }
        
        synthetic_profiles.append(profile)

    # Output
    output_file = "synthetic_profiles.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(synthetic_profiles, f, indent=4)
    
    print(f"Successfully generated {len(synthetic_profiles)} synthetic profiles in {output_file}")

if __name__ == "__main__":
    main()
