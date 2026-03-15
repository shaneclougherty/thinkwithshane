import os
import requests
import json
import random
import google.genai as genai
from dotenv import load_dotenv
from supabase import create_client

# --- 1. SETUP ---
load_dotenv()

supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")
supabase = create_client(supabase_url, supabase_key)

# Initialize NEW Gemini Client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

categories = ["Psychology", "Human History", "Physics", "Biology", "Technology"]

# --- 2. THE OPENALEX FETCHER ---
def get_openalex_paper(category):
    url = f"https://api.openalex.org/works?search={category}&filter=has_abstract:true,type:article&sort=publication_date:desc&per-page=15"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        results = data.get("results", [])
        if results:
            paper = random.choice(results)
            title = paper.get("title", "Unknown Title")
            author = paper.get("authorships", [{}])[0].get("author", {}).get("display_name", "Unknown Author")
            doi = paper.get("doi", "No DOI")
            year = paper.get("publication_year", "Unknown")
            return {"title": title, "citation": f"{title} by {author} ({year}) - {doi}", "raw_data": str(paper)}
    return None

# --- 3. THE AI TRANSLATOR (UPDATED FOR 2026 SDK) ---
def generate_reality_shift(paper_data):
    prompt = f"""
    Translate this research into an 8th-grade level reality shift.
    Data: {paper_data['raw_data']}
    
    Return ONLY a JSON object with:
    "hook": 1 punchy sentence.
    "mechanism": 2 paragraphs of facts.
    "shift": 1 paragraph + 1 Socratic question.
    """
    
    try:
        # Using Gemini 2.5 Flash
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config={'response_mime_type': 'application/json'}
        )
        return json.loads(response.text)
    except Exception as e:
        print(f"AI Error: {e}")
        return None

# --- 4. THE LOOP ---
def run_daily_hunt():
    for category in categories:
        print(f"Hunting for: {category}...")
        paper = get_openalex_paper(category)
        if paper:
            shift = generate_reality_shift(paper)
            if shift:
                supabase.table("reality_shifts").insert({
                    "category": category,
                    "hook": shift["hook"],
                    "mechanism": shift["mechanism"],
                    "shift": shift["shift"],
                    "source_citation": paper["citation"]
                }).execute()
                print(f"Success: {category}")

if __name__ == "__main__":
    run_daily_hunt()
