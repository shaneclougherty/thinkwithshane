import os
import requests
import json
import random
from dotenv import load_dotenv
from supabase import create_client
import google.generativeai as genai

# --- 1. SETUP ---
load_dotenv()

# Initialize Supabase
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")
supabase = create_client(supabase_url, supabase_key)

# Initialize Gemini API
gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    print("CRITICAL ERROR: Missing GEMINI_API_KEY.")
    exit()

genai.configure(api_key=gemini_api_key)
# Using flash model for speed and efficiency
model = genai.GenerativeModel('gemini-1.5-flash')

# Your 5 exact categories
categories = ["Psychology", "Human History", "Physics", "Biology", "Technology"]

# --- 2. THE OPENALEX FETCHER ---
def get_openalex_paper(category):
    """Searches OpenAlex for a recent, relevant academic paper."""
    url = f"https://api.openalex.org/works?search={category}&filter=has_abstract:true,type:article&sort=publication_date:desc&per-page=15"
    
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        results = data.get("results", [])
        
        if results:
            # Pick a random paper from the recent top 15 so it's fresh every day
            paper = random.choice(results)
            
            title = paper.get("title", "Unknown Title")
            author = paper.get("authorships", [{}])[0].get("author", {}).get("display_name", "Unknown Author")
            doi = paper.get("doi", "No DOI link available")
            year = paper.get("publication_year", "Unknown Year")
            
            citation = f"{title} by {author} ({year}) - {doi}"
            
            return {"title": title, "citation": citation, "raw_data": str(paper)}
            
    return None

# --- 3. THE AI TRANSLATOR ---
def generate_reality_shift(paper_data):
    """Passes the raw academic paper to Gemini to format the story."""
    
    system_prompt = f"""
    You are a translator of complex academic research. Your goal is to make empirical, pragmatic, and highly counter-intuitive findings accessible to the general public.
    
    Raw Academic Data:
    Title: {paper_data['title']}
    Data: {paper_data['raw_data']}
    
    Strict Constraints:
    1. Write at an 8th to 10th-grade reading level. Keep it human, conversational, and clear.
    2. DO NOT use the following words: paradigm, existential, ontological, microscopic, fathom.
    3. Output exactly a valid JSON object with these three keys: 
       - "hook": A short, punchy 1-sentence opening that grabs attention.
       - "mechanism": A 2-3 paragraph explanation of 'The Facts' from the study. 
       - "shift": A 1-2 paragraph 'So What?' section explaining how this changes our daily lives or understanding of the world.
    4. The "shift" section MUST end with a single, open-ended Socratic question to spark thought.
    """
    
    try:
        # Force Gemini to return clean JSON
        response = model.generate_content(
            system_prompt,
            generation_config=genai.GenerationConfig(response_mime_type="application/json")
        )
        
        result = json.loads(response.text)
        return result
    except Exception as e:
        print(f"AI Translation error: {e}")
        return None

# --- 4. THE DAILY HUNT (THE LOOP) ---
def run_daily_hunt():
    print("Waking up the engine...")
    
    for category in categories:
        print(f"Hunting for: {category}...")
        
        paper = get_openalex_paper(category)
        if not paper:
            print(f"Failed to find a paper for {category}. Skipping.")
            continue
            
        shift_data = generate_reality_shift(paper)
        if not shift_data:
            print(f"Failed to translate {category}. Skipping.")
            continue
        
        try:
            # Inject the data into Supabase
            supabase.table("reality_shifts").insert({
                "category": category,
                "hook": shift_data["hook"],
                "mechanism": shift_data["mechanism"],
                "shift": shift_data["shift"],
                "source_citation": paper["citation"]
            }).execute()
            print(f"Successfully locked {category} into the vault.")
            
        except Exception as e:
            print(f"Database error for {category}: {e}")
            
    print("Daily hunt complete. All 5 categories updated. Going back to sleep.")

if __name__ == "__main__":
    run_daily_hunt()
