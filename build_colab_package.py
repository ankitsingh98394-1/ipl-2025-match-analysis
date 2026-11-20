import json
import zipfile
from pathlib import Path

BASE = Path(r"C:\Users\ankit singh\.gemini\antigravity\scratch\ipl-2025-dashboard")

# 1. Read files
app_code = (BASE / "app.py").read_text(encoding="utf-8")
matches_csv = (BASE / "data" / "matches.csv").read_text(encoding="utf-8")
orange_csv = (BASE / "data" / "orange_cap.csv").read_text(encoding="utf-8")
purple_csv = (BASE / "data" / "purple_cap.csv").read_text(encoding="utf-8")

# 2. Build Colab Notebook (.ipynb)
# Cells:
# Cell 1: Markdown title & guide
# Cell 2: Install dependencies
# Cell 3: Create directory and data files
# Cell 4: Create app.py
# Cell 5: Run with localtunnel

nb = {
    "nbformat": 4,
    "nbformat_minor": 0,
    "metadata": {
        "colab": {
            "name": "IPL_2025_Dashboard.ipynb",
            "provenance": []
        },
        "kernelspec": {
            "name": "python3",
            "display_name": "Python 3"
        },
        "language_info": {
            "name": "python"
        }
    },
    "cells": [
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "# 🏏 IPL 2025 Match Analysis Dashboard\n",
                "### Complete Interactive Streamlit App in Google Colab\n",
                "\n",
                "Follow these 3 quick steps to run this notebook:\n",
                "1. Click **Runtime** -> **Run all** (or press `Ctrl + F9`).\n",
                "2. In the last cell, copy the **Endpoint IP password** printed on the screen.\n",
                "3. Click the `your url is: https://...loca.lt` link, paste the IP into **Tunnel Password**, and view your live dashboard!"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Step 1: Install required packages\n",
                "!pip install -q streamlit plotly pandas"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Step 2: Setup project data directory and CSV files\n",
                "import os\n",
                "os.makedirs('data', exist_ok=True)\n",
                "\n",
                "# Create matches.csv\n",
                "with open('data/matches.csv', 'w', encoding='utf-8') as f:\n",
                f"    f.write({repr(matches_csv)})\n",
                "\n",
                "# Create orange_cap.csv\n",
                "with open('data/orange_cap.csv', 'w', encoding='utf-8') as f:\n",
                f"    f.write({repr(orange_csv)})\n",
                "\n",
                "# Create purple_cap.csv\n",
                "with open('data/purple_cap.csv', 'w', encoding='utf-8') as f:\n",
                f"    f.write({repr(purple_csv)})\n",
                "\n",
                "print('✅ Data files successfully created in data/ folder!')"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Step 3: Write the Streamlit application code\n",
                "with open('app.py', 'w', encoding='utf-8') as f:\n",
                f"    f.write({repr(app_code)})\n",
                "\n",
                "print('✅ app.py successfully created!')"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Step 4: Run Streamlit and expose via LocalTunnel\n",
                "import urllib.request\n",
                "\n",
                "# Print public IP required by LocalTunnel password prompt\n",
                "public_ip = urllib.request.urlopen('https://ipv4.icanhazip.com').read().decode('utf8').strip()\n",
                "print('=' * 60)\n",
                "print(f'🔑 YOUR LOCALTUNNEL PASSWORD / ENDPOINT IP: {public_ip}')\n",
                "print('(Copy this IP to paste into the tunnel page when prompted)')\n",
                "print('=' * 60)\n",
                "\n",
                "# Launch Streamlit and tunnel\n",
                "!streamlit run app.py & npx localtunnel --port 8501"
            ]
        }
    ]
}

out_nb = BASE / "ipl_2025_colab.ipynb"
with open(out_nb, "w", encoding="utf-8") as f:
    json.dump(nb, f, indent=2)

print(f"Generated Colab Notebook at: {out_nb}")

# 3. Create zip file
zip_path = BASE / "ipl_2025_dashboard.zip"
with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
    zf.write(BASE / "app.py", arcname="app.py")
    zf.write(BASE / "requirements.txt", arcname="requirements.txt")
    zf.write(BASE / "README.md", arcname="README.md")
    zf.write(BASE / "data" / "matches.csv", arcname="data/matches.csv")
    zf.write(BASE / "data" / "orange_cap.csv", arcname="data/orange_cap.csv")
    zf.write(BASE / "data" / "purple_cap.csv", arcname="data/purple_cap.csv")

print(f"Generated Zip archive at: {zip_path}")
