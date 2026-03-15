import os
import requests
import json
import random
from dotenv import load_dotenv
from supabase import create_client

# --- 1. SETUP ---
load_dotenv()

supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")
supabase = create_client(supabase_url, supabase_key)

# Add your AI provider's API key here (e.g., OpenAI or Gemini)
AI_API_KEY = os.getenv("AI_API_KEY")

# Your 5 new exact categories
categories = ["Psychology", "Human History", "Physics", "Biology", "Technology"]

# --- 2. THE OPENALEX FETCHER ---
def get_openalex_paper(category):
    """Searches OpenAlex for a recent, relevant academic paper."""
    # We search the category, ensure it has an abstract, and sort by newest
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
            
            # Format the clean citation for the bottom of your website
            citation = f"{title} by {author} ({year}) - {doi}"
            
            return {"title": title, "citation": citation, "raw_data": str(paper)}
            
    return None

# --- 3. THE AI TRANSLATOR ---
def generate_reality_shift(paper_data):
    """Passes the raw academic paper to your AI to format the story."""
    
    # This is your new, highly-constrained AI prompt
    system_prompt = """
    You are a translator of complex academic research. Your goal is to make empirical, pragmatic, and highly counter-intuitive findings accessible to the general public.
    
    Strict Constraints:
    1. Write at an 8th to 10th-grade reading level. Keep it human, conversational, and clear.
    2. DO NOT use the following words: paradigm, existential, ontological, microscopic, fathom.
    3. Output exactly three sections in JSON format: 
       - "hook": A short, punchy 1-sentence opening that grabs attention.
       - "mechanism": A 2-3 paragraph explanation of 'The Facts' from the study. 
       - "shift": A 1-2 paragraph 'So What?' section explaining how this changes our daily lives or understanding of the world.
    4. The "shift" section MUST end with a single, open-ended Socratic question to spark thought.
    """
    
    # ---------------------------------------------------------
    # TODO: INSERT YOUR SPECIFIC AI GENERATION CODE HERE.
    # Send 'system_prompt' and 'paper_data' to your LLM API.
    # Parse the response into a JSON object.
    # ---------------------------------------------------------
    
    # Mock return block (Replace this with your actual AI response)
    return {
        "hook": "Scientists just found a new way to look at how we behave.",
        "mechanism": "The study shows that standard rules don't always apply...",
        "shift": "This changes how we operate daily. What would you do differently today if you knew this?"
    }

# --- 4. THE DAILY HUNT (THE LOOP) ---
def run_daily_hunt():
    print("Waking up the engine...")
    
    # This loops through all 5 categories so your whole site updates
    for category in categories:
        print(f"Hunting for: {category}...")
        
        paper = get_openalex_paper(category)
        if not paper:
            print(f"Failed to find a paper for {category}. Skipping.")
            continue
            
        shift_data = generate_reality_shift(paper)
        
        try:
            # Inject the data, including the new citation, directly into Supabase
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
