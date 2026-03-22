import os
import json
from dotenv import load_dotenv
from supabase import create_client
import google.genai as genai

# --- 1. SETUP ---
load_dotenv()

supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")
supabase = create_client(supabase_url, supabase_key)

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# ---- 2. THE MASTER RULES -----
category_rules = {
    "Psychology": {
        "director": """
            Act as a master psychologist. Find one highly cited, fascinating experiment or concept in Psychology.
            DO NOT USE ANY OF THESE PAST SUBJECTS: {used_subjects}
            
            Step 1: Randomly select ONE of these 10 Archetypes:
            1. The Invisible Ceiling (Self-Limitation): Studies proving how humans artificially cap their own potential or learn helplessness.
            2. The Rationality Illusion (Decision Making): How humans make wildly illogical choices, especially when assessing risk, value, or sunk costs.
            3. The Social Contagion (Group Dynamics): How crowds, peers, and cultural pressure invisibly overwrite our individual reality and morals.
            4. The Perception Filter (Blind Spots): How our brains literally delete or warp information right in front of us if it doesn't fit expectations.
            5. The Motivation Paradox (Drive & Reward): Counter-intuitive studies on why external rewards actually destroy internal passion and cause procrastination.
            6. The Memory Fiction (Identity): The reality that our memories are not recordings, but fluid stories we constantly rewrite to protect our egos.
            7. The Friction of Change (Habits & Inertia): The cognitive and biological reasons humans will choose familiar misery over unfamiliar improvement.
            8. The Empathy Gap (Emotional Forecasting): How we completely fail to predict our future emotions, leading to terrible long-term planning.
            9. The Authority Trap (Power & Obedience): How the mere appearance of authority or a uniform causes people to abandon their moral compass.
            10. The Happiness Treadmill (Fulfillment): Why achieving our biggest goals rarely makes us happier for long, and how satisfaction baselines reset.

            Step 2: Randomly select ONE of these 10 Contextual Arenas:
            1. Financial & Economic Decisions
            2. The Modern Workplace & Leadership
            3. Romantic & Interpersonal Relationships
            4. High-Stakes Crisis & Survival
            5. Consumer Behavior & Advertising
            6. Social Media & The Digital World
            7. Criminal Justice & Interrogation
            8. Medical & Healthcare Decisions
            9. Political & Tribal Identity
            10. Education & Skill Acquisition

            Step 3: THE EJECT BUTTON. If the Archetype and Arena combination is forced or illogical, immediately discard the Arena and randomly select a different one.
            
            Step 4: Output ONLY a title formatted in two parts separated by a colon: '[The Concept]: [The Friction]'. Maximum 7 words. (e.g., 'Status Quo Bias: The Cost of Comfort'). No period at the end.
        """,
        "translator": """
            Translate this research into a sophisticated, high-impact behavioral breakdown for a curious 11th-grade reader. 
            Concept: {paper_data}
            
            Strict Constraints:
            1. "hook": Provide the exact title given in the Concept field. Do NOT write a sentence. Just output the hybrid title.
            2. "mechanism": Provide a detailed, 3-5 sentence explanation of the core psychology experiment or bias. Use 'The Facts' as the header.
            3. "shift": The 'Real-World Friction'—A 3-5 sentence breakdown of how this manifests in high-stakes scenarios (toxic relationships, stagnant careers). Use gritty, visceral examples. No trivial snack or shopping examples.
            4. Tone: Analytical, provocative, and grounded. 
            5. End with one Socratic question.
            
            Return ONLY a valid JSON object with: "hook", "mechanism", "shift".
        """
    },
    "Human History": {
        "director": """
            Act as a master historian. Find one highly documented, culturally relevant historical event.
            DO NOT USE ANY OF THESE PAST SUBJECTS: {used_subjects}
            
            Step 1: Randomly select ONE of these 10 Archetypes:
            1. The Hidden Hero: An unknown person whose single action changed history.
            2. The Famous Flaw: A surprising failure, doubt, or quirk from a legendary figure.
            3. The Butterfly Effect: A tiny mistake or coincidence that altered the world.
            4. The Beautiful Defeat: A heroic grand failure that became a testament to human endurance.
            5. The Profitable Blunder: A catastrophic mistake that led to a massive leap in progress.
            6. The Pivot of Despair: A moment a famous figure almost gave up, but pushed through just before the finish line.
            7. The Rivalry Catalyst: How a bitter, personal feud drove two people to achieve impossible heights.
            8. The Outsider's Advantage: Someone who solved an impossible problem because they had no formal training in that field.
            9. The Myth Deconstructed: The chaotic, messy, and highly practical reality behind a polished historical legend.
            10. The Price of Ambition: The steep, hidden personal cost paid by a celebrated figure to achieve their legacy.
            
            Step 2: Randomly select ONE of these 10 Eras:
            1. Ancient Empires
            2. The Middle Ages & Feudal Eras
            3. The Renaissance & Age of Discovery
            4. The Industrial Revolution
            5. The Gilded Age
            6. World War I & II
            7. The Cold War & Space Race
            8. Civil Rights & Counterculture
            9. Silicon Valley Boom
            10. The Digital Age
            
            Step 3: THE EJECT BUTTON. If the Archetype and Era combination is historically barren, discard the Era and pick a new one. 
            
            Step 4: Output ONLY a title formatted in two parts separated by a colon: '[The Event/Person]: [The Impact]'. Maximum 7 words. (e.g., 'Allied Rivalry: The Race Across France'). No period at the end.
        """,
        "translator": """
            Translate this historical event into a detailed, highly compelling educational breakdown for a curious 11th-grade reader.
            Event: {paper_data} 
            
            Strict Constraints:
            1. "hook": Provide the exact title given in the Event field. Do NOT write a sentence. Just output the hybrid title.
            2. "mechanism": Provide a detailed, 3-5 sentence explanation of the historical story, focusing on human decisions.
            3. "shift": Provide a 3-5 sentence breakdown connecting the event to modern daily life, leadership, or overcoming failure.
            4. Tone: Epic but grounded.
            5. End with one Socratic question.
            
            Return ONLY a valid JSON object with: "hook", "mechanism", "shift".
        """
    },
    "Physics": {
        "director": """
            Act as a master physicist. Find one highly fascinating, pure-information physics concept.
            DO NOT USE ANY OF THESE PAST SUBJECTS: {used_subjects}

            Step 1: Randomly select ONE of these 10 Branches:
            1. Kinematics & Classical Mechanics
            2. Thermodynamics & Statistical Mechanics
            3. Fluid & Aerodynamics
            4. Wave Mechanics & Acoustics
            5. Optics & Light
            6. Electromagnetism
            7. Materials Science
            8. Astrophysics & Orbital Mechanics
            9. Relativity (Special & General)
            10. Quantum Mechanics

            Step 2: Randomly select ONE of these 10 Analytical Lenses:
            1. The Everyday Illusion: A profound physical law hiding in plain sight.
            2. The Extreme Limit: What happens to this law at the absolute maximum or minimum scale.
            3. The Paradox: A scenario where this rule of physics completely breaks human logic.
            4. The Historical Eureka: The ingenious physical experiment that originally proved this invisible law existed.
            5. The Catastrophic Failure: What happens when this physical law is ignored and forces compound out of control.
            6. The Biological Hack: How evolution perfectly exploited this physical law in an animal or plant.
            7. The Secret Technology: How this obscure physical law is secretly powering a modern piece of technology.
            8. The Micro-Mechanism: Zooming in to the atomic level to explain why a normal macro-level event happens.
            9. The Cosmic Equivalent: Taking a normal physical law and applying it to a massive, galactic scale.
            10. The Unsolved Mystery: Where this specific area of physics breaks down or confuses modern science.

            Step 3: THE EJECT BUTTON. If the Branch and Lens combination is scientifically impossible or creates a dead zone, immediately discard the Lens and randomly select a different one.

            Step 4: Output ONLY a title formatted in two parts separated by a colon: '[The Concept]: [The Paradox/Illusion]'. Maximum 7 words. (e.g., 'Superposition: Reality Undecided'). No period at the end.
        """,
        "translator": """
            Translate this physics concept into a detailed, pure-information breakdown for a curious 11th-grade reader.
            Concept: {paper_data}
            
            Strict Constraints:
            1. "hook": Provide the exact title given in the Concept field. Do NOT write a sentence. Just output the hybrid title.
            2. "mechanism": Provide a detailed, 3-5 sentence explanation of the pure physics facts. NO life metaphors.
            3. "shift": The 'Intuition Shatter'—A 3-5 sentence breakdown of exactly how this law proves that our human senses are lying to us about how reality functions at a fundamental level.
            4. Tone: Factual and awe-inspiring.
            5. End with one open-ended Socratic question.
            
            Return ONLY a valid JSON object with: "hook", "mechanism", "shift".
        """
    },
    "Biology": {
        "director": """
            Act as a master biologist. Find one highly fascinating, pure-information biological concept.
            DO NOT USE ANY OF THESE PAST SUBJECTS: {used_subjects}

            Step 1: Randomly select ONE of these 10 Branches:
            1. Neuroscience & Cognitive Biology
            2. Evolutionary Biology & Adaptation
            3. Genetics & Epigenetics
            4. Human Physiology & Biomechanics
            5. Microbiology & The Microbiome
            6. Endocrinology & Hormones
            7. Immunology
            8. Zoology & Animal Intelligence
            9. Botany & Plant Communication
            10. Chronobiology

            Step 2: Randomly select ONE of these 10 Analytical Lenses:
            1. The Evolutionary Trade-off: What massive physical/mental flaw a species accepted to gain a biological superpower.
            2. The Modern Mismatch: How a survival trait that kept us alive is actively harming us in the industrialized world.
            3. The Microscopic War: A brutal, invisible conflict happening at the cellular or bacterial level.
            4. The Chemical Illusion: How a purely physical chemical completely alters free will, mood, or perception.
            5. The Biomechanical Marvel: Treating the body strictly like an engineering project to explain its movement.
            6. The Symbiotic Pact: A strange alliance between two completely different species where one cannot survive without the other.
            7. The Neurological Glitch: A fascinating physical short-circuit in the brain that causes a bizarre sensory experience.
            8. The Deep Time Survivor: A biological mechanism that has remained perfectly unchanged for millions of years.
            9. The Environmental Switch: How an external factor physically alters an organism's DNA expression in real-time.
            10. The Biological Limit: What happens to an organism's cells when pushed to the absolute extreme edge of survival.

            Step 3: THE EJECT BUTTON. If the Branch and Lens combination is scientifically barren or forced, immediately discard the Lens and select a different one.

            Step 4: Output ONLY a title formatted in two parts separated by a colon: '[The Concept/Organism]: [The Survival Trait]'. Maximum 7 words. (e.g., 'The Microbiome: The Invisible Army'). No period at the end.
        """,
        "translator": """
            Translate this biological concept into a detailed, pure-information breakdown for a curious 11th-grade reader.
            Concept: {paper_data}
            
            Strict Constraints:
            1. "hook": Provide the exact title given in the Concept field. Do NOT write a sentence. Just output the hybrid title.
            2. "mechanism": Provide a detailed, 3-5 sentence explanation of the pure biological, evolutionary, or biomechanical facts. NO lifestyle metaphors.
            3. "shift": The 'Survival Logic'—A 3-5 sentence breakdown explaining how this mechanism, which might seem strange today, was the literal reason our ancestors survived.
            4. Tone: Factual, awe-inspiring, and grounded in pure hard science.
            5. End with one open-ended Socratic question.
            
            Return ONLY a valid JSON object with: "hook", "mechanism", "shift".
        """
    },
    "Technology": {
        "director": """
            Act as a master technologist. Find one highly fascinating, pure-information technology concept focused on advancement.
            DO NOT USE ANY OF THESE PAST SUBJECTS: {used_subjects}

            Step 1: Randomly select ONE of these 20 Branches:
            1. Artificial Intelligence & Foundation Models
            2. Robotics & Physical Automation
            3. Semiconductors & Micro-architecture
            4. Cryptography & Secure Networks
            5. Biotechnology & Gene Editing
            6. Nanotechnology & Metamaterials
            7. Aerospace & Deep Space Propulsion
            8. Quantum Computing & Information
            9. Renewable Energy Generation
            10. Nuclear Technology
            11. Energy Storage & Battery Chemistry
            12. The Internet of Things & Sensor Networks
            13. Telecommunications & Fiber/Radio Infrastructure
            14. Brain-Computer Interfaces & Neurotech
            15. Synthetic Biology & Bio-manufacturing
            16. Virtual/Augmented Reality & Spatial Computing
            17. Autonomous Vehicles & Drone Swarms
            18. Agricultural Tech & Precision Farming
            19. Medical Imaging & Diagnostics
            20. Distributed Ledgers & Blockchain Architecture

            Step 2: Randomly select ONE of these 5 Analytical Lenses of Advancement:
            1. The Paradigm Shift: A specific breakthrough that completely obsoleted the previous standard.
            2. The Convergence: Two completely different tech sectors merging to create something previously impossible.
            3. The Physical Wall: The brutal physical or engineering limit a technology is currently fighting to break through.
            4. The Accidental Leap: A massive technological advancement that happened while trying to solve an unrelated problem.
            5. The Tipping Point: The innovation that took a technology from a lab experiment to a global force through scale.

            Step 3: THE EJECT BUTTON. If the Branch and Lens combination is barren, immediately discard the Lens and select a different one.

            Step 4: Output ONLY a title formatted in two parts separated by a colon: '[The Tech]: [The Breakthrough/Limit]'. Maximum 7 words. (e.g., 'Quantum Qubits: Escaping Binary Physics'). No period at the end.
        """,
        "translator": """
            Translate this technology concept into a detailed, pure-information breakdown for a curious 11th-grade reader.
            Concept: {paper_data}
            
            Strict Constraints:
            1. "hook": Provide the exact title given in the Concept field. Do NOT write a sentence. Just output the hybrid title.
            2. "mechanism": Provide a detailed, 3-5 sentence explanation of the pure engineering or hardware facts. Focus heavily on how it works.
            3. "shift": The 'Invisible Infrastructure'—A 3-5 sentence breakdown explaining how this specific advancement is secretly holding up a part of the modern world.
            4. Tone: Factual, awe-inspiring, and grounded in pure engineering.
            5. End with one open-ended Socratic question.
            
            Return ONLY a valid JSON object with: "hook", "mechanism", "shift".
        """
    }
}

# --- 3. THE UNIVERSAL VAULT CHECK ---
def get_recent_subjects(category):
    try:
        # Changed limit from 100 to 1000
        response = supabase.table("reality_shifts").select("source_citation").eq("category", category).order("created_at", desc=True).limit(1000).execute()
        used = [row['source_citation'].replace("Subject: ", "") for row in response.data]
        return used # Returning the actual list now, not just a string
    except Exception as e:
        print(f"Memory fetch failed: {e}")
        return []

# --- 4. THE AI FUNCTIONS ---
def generate_hunt_target(category):
    if category not in category_rules:
        return category

    used_subjects_list = get_recent_subjects(category)
    used_subjects_string = ", ".join(used_subjects_list) if used_subjects_list else "None yet."
    
    prompt = category_rules[category]["director"].format(used_subjects=used_subjects_string)

    # The Validation Loop: Try up to 3 times to get a unique target
    max_attempts = 3
    for attempt in range(max_attempts):
        try:
            response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
            target = response.text.strip().replace('"', '')
            
            # Check if the AI's answer is already in the vault
            if target in used_subjects_list:
                print(f"Attempt {attempt + 1}: Duplicate found ({target}). Rerolling...")
                continue # Forces the loop to try again
                
            print(f"Unique Target Acquired for {category}: {target}")
            return target
            
        except Exception as e:
            print(f"Director failed on attempt {attempt + 1}: {e}")
            
    print(f"Failed to find a unique target for {category} after {max_attempts} attempts.")
    return None

def generate_reality_shift(target_string, category):
    if category not in category_rules:
        return None
        
    prompt = category_rules[category]["translator"].format(paper_data=target_string)
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

# --- 5. THE MASTER LOOP ---
def run_daily_hunt():
    active_categories = ["Psychology", "Human History", "Physics", "Biology", "Technology"] 
    
    for category in active_categories:
        print(f"\n--- Waking up for: {category} ---")
        
        # 1. AI acts as Director to find the target
        specific_target = generate_hunt_target(category)
        
        # 2. AI acts as Translator to write the Reality Shift
        shift = generate_reality_shift(specific_target, category)
        
        # 3. Save directly to Supabase
        if shift:
            try:
                supabase.table("reality_shifts").insert({
                    "category": category,
                    "hook": shift.get("hook", ""),
                    "mechanism": shift.get("mechanism", ""),
                    "shift": shift.get("shift", ""),
                    "source_citation": f"Subject: {specific_target}",
                    "source_title": specific_target  # <--- You add it right here in hunter.py
                }).execute()
                print(f"Success: {category} locked into the vault.")
            except Exception as e:
                print(f"Database error: {e}")

if __name__ == "__main__":
    run_daily_hunt()
