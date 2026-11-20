# 🏏 IPL 2025 Match Analysis & Dashboard

A comprehensive data analytics and visualization web application built with **Python**, **Streamlit**, **Pandas**, and **Plotly**. This project provides deep analytical insights into the Indian Premier League (IPL) 2025 season, including team performances, venue trends, toss impact, star players, and official Orange & Purple Cap leaderboards.

---

## 📌 Project Overview
* **Interactive Dashboard**: Filter matches by participating franchise, winning franchise, and venue.
* **Key Metrics**: Real-time KPI cards for total matches, team count, leading franchise, and toss-to-win correlation.
* **Visual Analytics**:
  - Franchise-wise win counts with official team branding colors.
  - Top stadiums and venues hosting matches.
  - Toss dynamics (Bat vs. Field preference and match outcome correlation).
  - Player of the Match distribution.
* **Leaderboards**: Official Orange Cap (Batting) and Purple Cap (Bowling) stats.
* **Data Export**: Direct one-click CSV export of filtered match records.

---

## 📁 Project Structure
```
ipl-2025-dashboard/
│
├── app.py                     # Main Streamlit web application
├── requirements.txt           # Required Python packages
├── README.md                  # Project documentation
├── generate_matches.py        # Utility script to generate realistic match dataset
└── data/
    ├── matches.csv            # Match-by-match records for IPL 2025
    ├── orange_cap.csv         # Top run-scorers
    └── purple_cap.csv         # Top wicket-takers
```

---

## 🚀 How to Run

### 1. Prerequisites
Ensure Python 3.10+ is installed on your system.

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Launch Dashboard
```bash
streamlit run app.py
```
Open your web browser at: `http://localhost:8501`

---

## 📊 Dataset Schema

### `matches.csv`
- `match_id`: Unique match identifier
- `season`: Tournament edition (2025)
- `date`: Date of the fixture
- `team1`, `team2`: Competing franchises
- `toss_winner`: Franchise that won the toss
- `toss_decision`: `field` or `bat`
- `winner`: Winning team
- `win_by`: `runs` or `wickets`
- `result_margin`: Margin of victory
- `player_of_match`: Best performer
- `venue`, `city`: Host stadium and location

### `orange_cap.csv`
- `rank`, `player`, `team`, `matches`, `innings`, `runs`, `highest_score`, `average`, `strike_rate`, `hundreds`, `fifties`, `fours`, `sixes`

### `purple_cap.csv`
- `rank`, `player`, `team`, `matches`, `overs`, `runs_conceded`, `wickets`, `best_bowling`, `average`, `economy`, `strike_rate`, `four_wickets`, `five_wickets`
