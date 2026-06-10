# 🏏 IPL Complete Data Analysis (2008–2020)

> An end-to-end Exploratory Data Analysis (EDA) and interactive Streamlit dashboard built on 13 seasons of Indian Premier League data.

![Python](https://img.shields.io/badge/Python-3.10-blue?logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.35-red?logo=streamlit)
![Pandas](https://img.shields.io/badge/Pandas-2.1-green?logo=pandas)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## 📌 Project Overview

This project performs a comprehensive analysis of IPL cricket data spanning **2008 to 2020** using Python. It includes:

-  Team win analysis across all seasons
-  Toss impact on match outcomes
-  Top batsmen by total runs and strike rate
-  Top bowlers by wickets (excluding run-outs)
-  Best death-over finishers (Overs 16–20)
-  Best batting partnerships
-  Venue-wise match distribution

The project is also deployed as an **interactive Streamlit web app** with season filters, player search, and head-to-head comparisons.

---

##  Live Demo

👉 **[Click here to open the Streamlit App](https://ipl-analysis-ifjtkta3ef8rjyappmjrxn.streamlit.app/)** 

---

## 📁 Project Structure

```
ipl-analysis/
│
├── app.py                        # Streamlit web application
├── IPL_Analysis_Complete.ipynb   # Jupyter Notebook (full EDA)
├── requirements.txt              # Python dependencies
├── README.md                     # This file
│
├── data/
│   ├── matches.csv               # Match-level data
│   └── deliveries.csv            # Ball-by-ball data
│
└── screenshots/
    ├── overview.png
    ├── team_analysis.png
    └── batting_analysis.png
```

---

## 📊 Dataset

| File | Rows | Description |
|------|------|-------------|
| `matches.csv` | ~816 | One row per IPL match |
| `deliveries.csv` | ~179,078 | One row per ball bowled |

**Source:** [IPL Complete Dataset 2008–2020 on Kaggle](https://www.kaggle.com/datasets/patrickb1912/ipl-complete-dataset-20082020)

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| Python 3.10 | Core programming language |
| Pandas | Data loading, cleaning, analysis |
| NumPy | Numerical operations |
| Matplotlib & Seaborn | Data visualization |
| Streamlit | Interactive web app |
| Jupyter Notebook | Exploratory analysis |

---

## ⚙️ How to Run Locally

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/ipl-analysis.git
cd ipl-analysis
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Add dataset files
Download `matches.csv` and `deliveries.csv` from [Kaggle](https://www.kaggle.com/datasets/patrickb1912/ipl-complete-dataset-20082020) and place them in the project root folder.

### 4. Run the Streamlit app
```bash
streamlit run app.py
```

Open your browser at `http://localhost:8501`

---

## 💡 Key Insights

1. **Mumbai Indians** are the most successful IPL franchise by total wins
2. Winning the toss gives only a ~50% advantage — skill matters more than luck
3. **Virat Kohli** is the all-time leading IPL run scorer
4. **Lasith Malinga** leads the wicket-taking charts
5. Most captains prefer to **field first** after winning the toss
6. **Wankhede Stadium** hosts the most IPL games

---

## 👨‍💻 Author

**Your Name**
- 📧 diyabhavesh2306@gmail.com
- 💼 [LinkedIn](https://www.linkedin.com/in/diya-patel-4b0375335/)
- 🐙 [GitHub](https://github.com/diya236)

---

*If you found this project helpful, please ⭐ star the repository!*
