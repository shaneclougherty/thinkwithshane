import os
import requests
import json
import random
from dotenv import load_dotenv
from supabase import create_client
import google.genai as genai

# --- 1. SETUP ---
load_dotenv()

supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")
supabase = create_client(supabase_url, supabase_key)

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

categories = ["Psychology", "Human History", "Physics", "Biology", "Technology"]

# --- 2. THE MASTER RULES DICTIONARY ---
category_rules = {
    "Psychology": {
        "director": """
            Name one highly cited, fascinating experiment or concept in Psychology.
            Focus strictly on practical, everyday cognitive biases. Randomly choose ONE of these 11 archetypes:
            1. The Invisible Ceiling (e.g., learned helplessness)
            2. The Rationality Illusion (e.g., sunk-cost)
            3. The Social Contagion (e.g., bystander effect)
            4. The Perception Filter (e.g., confirmation bias)
            5. The Motivation Paradox (e.g., overjustification effect)
            6. The Memory Fiction (e.g., false memory)
            7. The Friction of Change (e.g., status quo bias)
            8. The Empathy Gap (e.g., hot-cold empathy gap)
            9. The Authority Trap (e.g., Milgram)
            10. The Happiness Treadmill (e.g., hedonic adaptation)
            11. The Wildcard: A mind-bending, practical quirk not listed above.
            Output ONLY the 1-5 word name of the concept. No punctuation.
        """,
        "translator": """
            Translate this research into an 8th-grade level reality shift. Data: {paper_data}
            Strict Constraints:
            1. "mechanism": Explain the experiment simply.
            2. "shift": Act as a practical metaphor for daily life or personal growth.
            3. Tone: Humble, educational, grounded. 
            4. End with one Socratic question.
            Return ONLY a valid JSON object with: "hook", "mechanism", "shift".
        """
    },
    "Human History": {
        "director": """
            Act as a master historian. Find one highly documented, culturally relevant historical event.
            DO NOT USE ANY OF THESE PAST SUBJECTS: {used_subjects}
            
            Step 1: Randomly select ONE of these 10 Archetypes:
            1. The Hidden Hero
            2. The Famous Flaw
            3. The Butterfly Effect
            4. The Beautiful Defeat
            5. The Profitable Blunder
            6. The Pivot of Despair
            7. The Rivalry Catalyst
            8. The Outsider's Advantage
            9. The Myth Deconstructed
            10. The Price of Ambition
            
            Step 2: Randomly select ONE of these 10 Eras:
            1. Ancient Empires (Rome, Greece, Egypt, Han)
            2. The Middle Ages & Feudal Eras
            3. The Renaissance & Age of Discovery
            4. The Industrial Revolution
            5. The Gilded Age & Early American Capitalism
            6. World War I & II
            7. The Cold War & Space Race
            8. Civil Rights & Counterculture (1950s-1970s)
            9. Silicon Valley Boom (1980s-1990s)
            10. The Digital Age (2000s-2020)
            
            Output ONLY the 1-7 word name of the specific historical event or person. No punctuation.
        """,
        "translator": """
            Translate this historical event into an 8th-grade level reality shift using your own knowledge.
            Event: {paper_data} 
            Strict Constraints:
            1. "hook": Punchy 1-sentence intro to the stakes.
            2. "mechanism": Tell the historical story clearly, focusing on human decisions.
            3. "shift": Connect the event to modern daily life, business, or overcoming failure.
            4. Tone: Epic but grounded.
            5. End with one Socratic question.
            Return ONLY a valid JSON object with: "hook", "mechanism", "shift".
        """
    }
    # Future categories (Physics, Biology, Technology) will follow this exact dictionary structure.
}

# --- 3. THE VAULT CHECK (MEMORY SYSTEM) ---
def get_recent_history_subjects():
    """Fetches the last 100 history stories so the AI doesn't repeat itself."""
    try:
        response = supabase.table("reality_shifts").select("source_citation").eq("category", "Human History").order("created_at", desc=True).limit(100).execute()
        used = [row['source_citation'].replace("Historical Event: ", "") for row in response.data]
        return ", ".join(used) if used else "None yet."
    except Exception as e:
        print(f"Memory fetch failed: {e}")
        return "None yet."

# --- 4. THE AI FUNCTIONS ---
def generate_hunt_target(category):
    if category not in category_rules:
        return category # Fallback for categories we haven't built rules for yet

    prompt = category_rules[category]["director"]
    
    # Inject memory specifically for History
    if category == "Human History":
        used_subjects = get_recent_history_subjects()
        prompt = prompt.format(used_subjects=used_subjects)

    try:
        response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
        target = response.text.strip().replace('"', '')
        print(f"Target Acquired for {category}: {target}")
        return target
    except Exception as e:
        print(f"Director failed: {e}")
        return category

def get_openalex_paper(search_term):
    url = f"https://api.openalex.org/works?search={search_term}&filter=has_abstract:true,type:article&sort=cited_by_count:desc&per-page=15"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        results = data.get("results", [])
        if results:
            paper = random.choice(results)
            return {
                "title": paper.get("title", "Unknown Title"),
                "citation": f"{paper.get('title')} by {paper.get('authorships', [{}])[0].get('author', {}).get('display_name', 'Unknown')} ({paper.get('publication_year')})",
                "raw_data": str(paper)
            }
    return None

def generate_reality_shift(paper_data_string, category):
    if category not in category_rules:
        return None # Skip if no rules exist yet
        
    prompt = category_rules[category]["translator"].format(paper_data=paper_data_string)
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config={'response_mime_type': 'application/json'}
        )
        return json.loads(response.text)
    except Exception as e:
        print(f"Translator Error: {e}")
        return None

# --- 5. THE LOOP ---
def run_daily_hunt():
    # Only hunting Psych and History right now since those have complete rules
    active_categories = ["Psychology", "Human History"] 
    
    for category in active_categories:
        print(f"\n--- Waking up for: {category} ---")
        specific_target = generate_hunt_target(category)
        
        # The Bypass
        if category == "Human History":
            paper = {"raw_data": specific_target, "citation": f"Historical Event: {specific_target}"}
        else:
            paper = get_openalex_paper(specific_target)
        
        if paper:
            shift = generate_reality_shift(paper["raw_data"], category)
            if shift:
                try:
                    supabase.table("reality_shifts").insert({
                        "category": category,
                        "hook": shift["hook"],
                        "mechanism": shift["mechanism"],
                        "shift": shift["shift"],
                        "source_citation": paper["citation"]
                    }).execute()
                    print(f"Success: {category} locked into the vault.")
                except Exception as e:
                    print(f"Database error: {e}")

if __name__ == "__main__":
    run_daily_hunt()
