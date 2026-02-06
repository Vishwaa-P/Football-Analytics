# ⚽ Virtual Scout | Football Analytics

**Virtual Scout** is an football analytics dashboard built with Python and Streamlit. It analyzes player performance from Europe's top leagues (Season 24/25), providing data-driven insights, head-to-head comparisons, and a custom "Virtual Score" algorithm to rank players.

Demo: [https://football-analytics-vkdptnbu6p2uiejpoylbfq.streamlit.app/](https://football-analytics-vkdptnbu6p2uiejpoylbfq.streamlit.app/)

[![Python](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/) [![License: MIT](https://img.shields.io/badge/license-MIT-green)](LICENSE) [![Notebooks](https://img.shields.io/badge/notebooks-Jupyter-orange)](#notebooks)

A modular toolkit and interactive dashboard for football (soccer) analytics — suitable for research, scouting, coaching insights, and demos.

## 🚀 Features

- 🏆 "Virtual Score" Algorithm: A custom ranking system scoring players (0-100) using weighted metrics by position (FW, MF, FB, CB, GK).
- 🌍 League Strength Adjustment: Normalize stats by league strength to enable fair cross-league comparisons.
- 🔎 Single Player Analysis: Player cards with Per 90 metrics, percentile ranks, and radar-style profiling.
- ⚔️ Head-to-Head Comparison: Compare any two players side-by-side (bar charts, overlapping radar plots).
- 📊 Top 10 Rankings: Position-based leaderboards (Goals, Assists, Key Passes, Virtual Score).
- 🥅 Goalkeeper Analytics: GK-specific metrics like Save %, Clean Sheet %, and PSxG.

## 🛠️ Tech Stack

- Frontend: Streamlit
- Data processing: pandas, numpy
- Visualization: matplotlib (and Streamlit charts)
- Data source: Fbref (2024–2025 season, sample dataset included)

## 📂 Project Structure

Example layout — update to match your repo if needed:

```text
├── Football-Statistics/
│   ├── app.py               # Main Streamlit app entrypoint
│   ├── preprocessor.py      # Data cleaning, league weighting, scoring logic
│   ├── helper.py            # Visualization helpers (radar, bar plots, pitch)
│   ├── players_data_light-2024_2025.csv  # Sample dataset for demo
│   └── requirements.txt     # Python dependencies
├── 01_exploration.ipynb     # Notebook used for initial data exploration
├── README.md                # Project documentation (this file)
└── LICENSE                  # MIT license
```

## 📥 Quick Start (Run locally)

1. Clone the repo:
```bash
git clone https://github.com/Vishwaa-P/Football-Analytics.git
cd Football-Analytics/Football-Statistics
```

2. Create and activate a virtual environment, then install dependencies:
```bash
python -m venv .venv
source .venv/bin/activate     # macOS / Linux
.venv\Scripts\activate        # Windows
pip install -r requirements.txt
```

3. Run the Streamlit app:
```bash
streamlit run app.py
```



## 📁 Data

- A lightweight sample dataset is included: `players_data_light-2024_2025.csv`. Use this for quick demos.
- For full analysis, place your full datasets under `Football-Statistics/` (or update `preprocessor.py` with actual paths).
- Keep large raw datasets out of GitHub (use cloud storage, private releases, or a dataset downloader script). Add a `.env.example` to document any credentials required.


## Usage examples

Run the app locally:
```bash
streamlit run app.py
```




## Contributing

Contributions welcome. Suggested workflow:
1. Fork the repository
2. Create a branch: `git checkout -b feat/awesome`
3. Add tests and update docs
4. Open a Pull Request describing the changes


## 📝 Contact & Credits

Maintainer: Vishwaa-P  
Repo: [https://github.com/Vishwaa-P/Football-Analytics](https://github.com/Vishwaa-P/Football-Analytics)  
Demo: [https://football-analytics-vkdptnbu6p2uiejpoylbfq.streamlit.app/](https://football-analytics-vkdptnbu6p2uiejpoylbfq.streamlit.app/)  
Email: vishwajeetpadole@gmail.com

## 📜 License

This project is provided under the MIT License. See the `LICENSE` file for details.


---

