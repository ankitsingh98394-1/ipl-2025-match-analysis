import csv
import random
from pathlib import Path

DATA_DIR = Path(r"C:\Users\ankit singh\.gemini\antigravity\scratch\ipl-2025-dashboard\data")
DATA_DIR.mkdir(parents=True, exist_ok=True)

teams = [
    "Chennai Super Kings",
    "Mumbai Indians",
    "Royal Challengers Bengaluru",
    "Kolkata Knight Riders",
    "Rajasthan Royals",
    "Sunrisers Hyderabad",
    "Delhi Capitals",
    "Lucknow Super Giants",
    "Gujarat Titans",
    "Punjab Kings"
]

venues = [
    ("M. A. Chidambaram Stadium", "Chennai"),
    ("Wankhede Stadium", "Mumbai"),
    ("M. Chinnaswamy Stadium", "Bengaluru"),
    ("Eden Gardens", "Kolkata"),
    ("Sawai Mansingh Stadium", "Jaipur"),
    ("Rajiv Gandhi International Cricket Stadium", "Hyderabad"),
    ("Arun Jaitley Stadium", "Delhi"),
    ("BRSABV Ekana Cricket Stadium", "Lucknow"),
    ("Narendra Modi Stadium", "Ahmedabad"),
    ("Maharaja Yadavindra Singh International Cricket Stadium", "Mullanpur")
]

players_by_team = {
    "Chennai Super Kings": ["Ruturaj Gaikwad", "MS Dhoni", "Ravindra Jadeja", "Shivam Dube", "Matheesha Pathirana", "Tushar Deshpande"],
    "Mumbai Indians": ["Jasprit Bumrah", "Suryakumar Yadav", "Rohit Sharma", "Hardik Pandya", "Tilak Varma", "Ishan Kishan"],
    "Royal Challengers Bengaluru": ["Virat Kohli", "Faf du Plessis", "Dinesh Karthik", "Rajat Patidar", "Will Jacks", "Mohammed Siraj"],
    "Kolkata Knight Riders": ["Sunil Narine", "Andre Russell", "Shreyas Iyer", "Phil Salt", "Varun Chakaravarthy", "Mitchell Starc"],
    "Rajasthan Royals": ["Sanju Samson", "Jos Buttler", "Yashasvi Jaiswal", "Riyan Parag", "Trent Boult", "Yuzvendra Chahal"],
    "Sunrisers Hyderabad": ["Travis Head", "Abhishek Sharma", "Heinrich Klaasen", "Pat Cummins", "T Natarajan", "Bhuvneshwar Kumar"],
    "Delhi Capitals": ["Rishabh Pant", "Kuldeep Yadav", "Jake Fraser-McGurk", "Tristan Stubbs", "Axar Patel", "Khaleel Ahmed"],
    "Lucknow Super Giants": ["KL Rahul", "Nicholas Pooran", "Marcus Stoinis", "Krunal Pandya", "Mayank Yadav", "Ravi Bishnoi"],
    "Gujarat Titans": ["Shubman Gill", "Sai Sudharsan", "Rashid Khan", "David Miller", "Mohit Sharma", "Rahul Tewatia"],
    "Punjab Kings": ["Harshal Patel", "Arshdeep Singh", "Sam Curran", "Shashank Singh", "Ashutosh Sharma", "Jonny Bairstow"]
}

# Fix seed for reproducible, realistic results
random.seed(42)

matches = []
match_id = 1
start_day = 22 # March 22, 2025

# Generate 70 league matches
for i in range(1, 71):
    t1, t2 = random.sample(teams, 2)
    venue, city = random.choice(venues)
    toss_winner = random.choice([t1, t2])
    toss_decision = random.choices(["field", "bat"], weights=[0.65, 0.35])[0]
    
    # 52% advantage to team chasing (standard T20 trend)
    if toss_decision == "field":
        winner = toss_winner if random.random() < 0.54 else (t2 if toss_winner == t1 else t1)
    else:
        winner = toss_winner if random.random() < 0.48 else (t2 if toss_winner == t1 else t1)
    
    win_by = "wickets" if ((toss_decision == "field" and winner == toss_winner) or (toss_decision == "bat" and winner != toss_winner)) else "runs"
    margin = random.randint(3, 8) if win_by == "wickets" else random.randint(5, 65)
    
    pom = random.choice(players_by_team.get(winner, ["Virat Kohli", "Rohit Sharma"]))
    
    day_offset = (i - 1) // 2
    month = 3 if day_offset <= 9 else (4 if day_offset <= 39 else 5)
    day = (start_day + day_offset - 1) % 31 + 1
    date_str = f"2025-{month:02d}-{day:02d}"
    
    matches.append({
        "match_id": match_id,
        "season": 2025,
        "date": date_str,
        "team1": t1,
        "team2": t2,
        "toss_winner": toss_winner,
        "toss_decision": toss_decision,
        "winner": winner,
        "win_by": win_by,
        "result_margin": margin,
        "player_of_match": pom,
        "venue": venue,
        "city": city
    })
    match_id += 1

# Playoff matches
playoffs = [
    ("Qualifier 1", "Kolkata Knight Riders", "Sunrisers Hyderabad", "Narendra Modi Stadium", "Ahmedabad", "2025-05-21"),
    ("Eliminator", "Rajasthan Royals", "Royal Challengers Bengaluru", "Narendra Modi Stadium", "Ahmedabad", "2025-05-22"),
    ("Qualifier 2", "Sunrisers Hyderabad", "Rajasthan Royals", "M. A. Chidambaram Stadium", "Chennai", "2025-05-24"),
    ("Final", "Kolkata Knight Riders", "Sunrisers Hyderabad", "M. A. Chidambaram Stadium", "Chennai", "2025-05-26")
]

for stage, t1, t2, venue, city, date_str in playoffs:
    toss_winner = random.choice([t1, t2])
    toss_decision = "field"
    winner = t1 if stage in ["Qualifier 1", "Final"] else (t2 if stage == "Qualifier 2" else t1)
    pom = random.choice(players_by_team[winner])
    win_by = "runs" if stage == "Final" else "wickets"
    margin = 8 if win_by == "wickets" else 24
    
    matches.append({
        "match_id": match_id,
        "season": 2025,
        "date": date_str,
        "team1": t1,
        "team2": t2,
        "toss_winner": toss_winner,
        "toss_decision": toss_decision,
        "winner": winner,
        "win_by": win_by,
        "result_margin": margin,
        "player_of_match": pom,
        "venue": venue,
        "city": city
    })
    match_id += 1

out_path = DATA_DIR / "matches.csv"
fieldnames = list(matches[0].keys())
with open(out_path, mode="w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(matches)

print(f"Generated {len(matches)} matches in {out_path}")
