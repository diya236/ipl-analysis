"""
IPL Complete Data Analysis — Streamlit Web App
Author: Diya Patel
Dataset: IPL 2008–2020
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import warnings

warnings.filterwarnings("ignore")

# ─────────────────────────────────────────────────────────────────────────────
# PAGE CONFIG  (must be the very first Streamlit command)
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="IPL Analysis Dashboard",
    page_icon="images.jpg",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────────────────────
# GLOBAL STYLE
# ─────────────────────────────────────────────────────────────────────────────
sns.set_theme(style="darkgrid")
plt.rcParams.update({"figure.dpi": 120, "axes.titlesize": 13})

TEAM_NAME_MAP = {
    "Royal Challengers Bengaluru": "Royal Challengers Bangalore",
    "Delhi Daredevils": "Delhi Capitals",
    "Kings XI Punjab": "Punjab Kings",
    "Rising Pune Supergiant": "Rising Pune Supergiants",
}

# ─────────────────────────────────────────────────────────────────────────────
# DATA LOADING  (cached so it only runs once)
# ─────────────────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    matches    = pd.read_csv("matches.csv")
    deliveries = pd.read_csv("deliveries.csv")

    # Clean matches
    matches["winner"]   = matches["winner"].fillna("No Result")
    matches["date"]     = pd.to_datetime(matches["date"])
    matches["year"]     = matches["date"].dt.year
    for col in ["team1", "team2", "winner", "toss_winner"]:
        matches[col] = matches[col].replace(TEAM_NAME_MAP)

    return matches, deliveries


matches, deliveries = load_data()
ALL_TEAMS   = sorted(matches["team1"].unique())
ALL_SEASONS = sorted(matches["year"].unique())

# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.image("images.jpg",
             width=160)
    st.markdown("##  IPL Dashboard")
    st.markdown("---")
    page = st.radio(
        "Navigate to",
        [" Overview",
         " Team Analysis",
         " Batting Analysis",
         " Bowling Analysis",
         " Death Overs",
         " Partnerships",
         " Venue Analysis"],
    )
    st.markdown("---")
    st.markdown("**Filter by Seasons**")
    selected_seasons = st.multiselect("Select Season(s)", ALL_SEASONS, default=ALL_SEASONS)
    if not selected_seasons:
        selected_seasons = ALL_SEASONS

    st.markdown("---")
    st.caption("Dataset: IPL 2008–2020 | Kaggle")


# Filter data by selected seasons
m = matches[matches["year"].isin(selected_seasons)]
d = deliveries[deliveries["match_id"].isin(m["id"])]

# ─────────────────────────────────────────────────────────────────────────────
# HELPER: show a matplotlib figure in Streamlit
# ─────────────────────────────────────────────────────────────────────────────
def show_fig(fig):
    st.pyplot(fig)
    plt.close(fig)


# ═════════════════════════════════════════════════════════════════════════════
# PAGE 1: OVERVIEW
# ═════════════════════════════════════════════════════════════════════════════
if page == " Overview":
    st.title("▶ IPL Complete Data Analysis (2008–2020)")
    st.markdown("*Explore 13 seasons of the Indian Premier League — teams, players, toss impact, venues & more.*")
    st.markdown("---")

    # KPI Cards
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("🏟️ Total Matches",   f"{len(m):,}")
    col2.metric("⚾ Total Balls",      f"{len(d):,}")
    col3.metric("🏆 Seasons",          str(len(selected_seasons)))
    col4.metric("👥 Teams",            str(m["team1"].nunique()))

    st.markdown("---")

    # Season-wise match count
    season_data = m.groupby("year").size().reset_index(name="Matches")
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(season_data["year"], season_data["Matches"],
            marker="o", linewidth=2.5, color="#e84393", markersize=8)
    ax.fill_between(season_data["year"], season_data["Matches"], alpha=0.15, color="#e84393")
    for _, row in season_data.iterrows():
        ax.annotate(str(int(row["Matches"])), xy=(row["year"], row["Matches"]),
                    xytext=(0, 8), textcoords="offset points", ha="center", fontsize=8)
    ax.set_title("📅 Season-wise Match Count", fontweight="bold")
    ax.set_xlabel("Season"); ax.set_ylabel("Matches")
    ax.xaxis.set_major_locator(mticker.MaxNLocator(integer=True))
    plt.tight_layout()
    show_fig(fig)

    # Toss decision pie
    c1, c2 = st.columns(2)
    with c1:
        td = m["toss_decision"].value_counts()
        fig2, ax2 = plt.subplots(figsize=(5, 5))
        ax2.pie(td, labels=td.index, autopct="%1.1f%%", startangle=90,
                colors=["#42A5F5", "#FFA726"], explode=(0.05, 0))
        ax2.set_title("Toss Decision Split", fontweight="bold")
        plt.tight_layout(); show_fig(fig2)
    with c2:
        toss_wins   = (m["toss_winner"] == m["winner"]).sum()
        toss_losses = len(m) - toss_wins
        fig3, ax3 = plt.subplots(figsize=(5, 5))
        ax3.pie([toss_wins, toss_losses],
                labels=[f"Toss winner also won\n({toss_wins})",
                        f"Toss winner lost\n({toss_losses})"],
                autopct="%1.1f%%", colors=["#66BB6A", "#EF5350"],
                explode=(0.05, 0), startangle=140)
        ax3.set_title("Toss Impact on Result", fontweight="bold")
        plt.tight_layout(); show_fig(fig3)


# ═════════════════════════════════════════════════════════════════════════════
# PAGE 2: TEAM ANALYSIS
# ═════════════════════════════════════════════════════════════════════════════
elif page == " Team Analysis":
    st.title("▶ Team Analysis")

    win_counts = (m[m["winner"] != "No Result"]["winner"]
                  .value_counts().reset_index())
    win_counts.columns = ["Team", "Wins"]

    fig, ax = plt.subplots(figsize=(12, 6))
    bars = ax.barh(win_counts["Team"], win_counts["Wins"],
                   color=sns.color_palette("Set2", len(win_counts)))
    ax.bar_label(bars, padding=3, fontsize=9)
    ax.set_title("Most Successful IPL Teams", fontsize=14, fontweight="bold")
    ax.set_xlabel("Total Wins"); ax.invert_yaxis()
    plt.tight_layout(); show_fig(fig)

    st.markdown("---")
    st.subheader("📊 Head-to-Head Comparison")
    c1, c2 = st.columns(2)
    team_a = c1.selectbox("Team A", ALL_TEAMS, index=0)
    team_b = c2.selectbox("Team B", ALL_TEAMS, index=1)

    h2h = m[((m["team1"] == team_a) & (m["team2"] == team_b)) |
            ((m["team1"] == team_b) & (m["team2"] == team_a))]
    if len(h2h):
        a_wins = (h2h["winner"] == team_a).sum()
        b_wins = (h2h["winner"] == team_b).sum()
        nr     = len(h2h) - a_wins - b_wins
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Total Matches", len(h2h))
        m2.metric(f"{team_a} Wins", a_wins)
        m3.metric(f"{team_b} Wins", b_wins)
        m4.metric("No Result", nr)
    else:
        st.info("No matches found between these teams in the selected seasons.")


# ═════════════════════════════════════════════════════════════════════════════
# PAGE 3: BATTING ANALYSIS
# ═════════════════════════════════════════════════════════════════════════════
elif page == " Batting Analysis":
    st.title("▶ Batting Analysis")

    top_n = st.slider("Show Top N Batters", 5, 20, 10)
    top_bat = (d.groupby("batter")["batsman_runs"]
               .sum().sort_values(ascending=False).head(top_n).reset_index())
    top_bat.columns = ["Batter", "Runs"]

    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(data=top_bat, x="Batter", y="Runs", palette="Blues_d", ax=ax)
    ax.bar_label(ax.containers[0], padding=3, fontsize=9)
    ax.set_title(f"Top {top_n} IPL Run Scorers", fontsize=14, fontweight="bold")
    plt.xticks(rotation=40, ha="right"); plt.tight_layout(); show_fig(fig)

    st.markdown("---")
    st.subheader("🔍 Individual Batter Stats")
    batter = st.selectbox("Select Batter", sorted(d["batter"].unique()))
    bd = d[d["batter"] == batter]
    runs   = bd["batsman_runs"].sum()
    balls  = len(bd)
    fours  = (bd["batsman_runs"] == 4).sum()
    sixes  = (bd["batsman_runs"] == 6).sum()
    sr     = round((runs / balls) * 100, 2) if balls else 0

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Total Runs", f"{runs:,}")
    c2.metric("Balls Faced", f"{balls:,}")
    c3.metric("Strike Rate", sr)
    c4.metric("4s", fours)
    c5.metric("6s", sixes)


# ═════════════════════════════════════════════════════════════════════════════
# PAGE 4: BOWLING ANALYSIS
# ═════════════════════════════════════════════════════════════════════════════
elif page == " Bowling Analysis":
    st.title("▶ Bowling Analysis")

    top_n = st.slider("Show Top N Bowlers", 5, 20, 10)
    bowler_wkts = (d[d["dismissal_kind"].notnull() &
                     ~d["dismissal_kind"].isin(["run out", "retired hurt"])]
                   ["bowler"].value_counts().head(top_n).reset_index())
    bowler_wkts.columns = ["Bowler", "Wickets"]

    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(data=bowler_wkts, x="Bowler", y="Wickets", palette="Reds_d", ax=ax)
    ax.bar_label(ax.containers[0], padding=3, fontsize=9)
    ax.set_title(f"Top {top_n} IPL Wicket Takers", fontsize=14, fontweight="bold")
    plt.xticks(rotation=40, ha="right"); plt.tight_layout(); show_fig(fig)

    st.markdown("---")
    st.subheader("🔍 Individual Bowler Stats")
    bowler = st.selectbox("Select Bowler", sorted(d["bowler"].unique()))
    bwd = d[d["bowler"] == bowler]
    wkts  = bwd[bwd["dismissal_kind"].notnull() &
                ~bwd["dismissal_kind"].isin(["run out","retired hurt"])].shape[0]
    runs_given = bwd["total_runs"].sum()
    overs_b    = len(bwd) / 6
    economy    = round(runs_given / overs_b, 2) if overs_b else 0

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Wickets", wkts)
    c2.metric("Runs Given", f"{runs_given:,}")
    c3.metric("Overs", round(overs_b, 1))
    c4.metric("Economy", economy)


# ═════════════════════════════════════════════════════════════════════════════
# PAGE 5: DEATH OVERS
# ═════════════════════════════════════════════════════════════════════════════
elif page == " Death Overs":
    st.title("▶ Death Overs Finishers (Overs 16–20)")

    min_balls = st.slider("Minimum Balls Faced in Death Overs", 50, 300, 100)
    death = d[d["over"] >= 16]
    fin   = (death.groupby("batter")
             .agg(runs=("batsman_runs","sum"), balls=("ball","count"))
             .assign(strike_rate=lambda x: (x["runs"]/x["balls"])*100)
             .query(f"balls > {min_balls}")
             .sort_values("strike_rate", ascending=False)
             .head(10).reset_index())

    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(data=fin, x="batter", y="strike_rate", palette="Oranges_d", ax=ax)
    ax.bar_label(ax.containers[0], fmt="%.1f", padding=3, fontsize=9)
    ax.set_title(f"Top Death-Over Finishers (min {min_balls} balls)", fontsize=14, fontweight="bold")
    ax.set_xlabel("Batter"); ax.set_ylabel("Strike Rate")
    plt.xticks(rotation=40, ha="right"); plt.tight_layout(); show_fig(fig)

    st.dataframe(fin.rename(columns={"batter":"Batter","runs":"Runs",
                                      "balls":"Balls","strike_rate":"SR"})
                 .reset_index(drop=True))


# ═════════════════════════════════════════════════════════════════════════════
# PAGE 6: PARTNERSHIPS
# ═════════════════════════════════════════════════════════════════════════════
elif page == " Partnerships":
    st.title("▶ Best Batting Partnerships")

    pair_runs = (d.groupby(["match_id","batter","non_striker"])["batsman_runs"]
                 .sum().reset_index()
                 .groupby(["batter","non_striker"])["batsman_runs"]
                 .sum().reset_index())
    pair_runs["pair"] = pair_runs.apply(
        lambda r: " & ".join(sorted([r["batter"], r["non_striker"]])), axis=1)
    top_pairs = (pair_runs.groupby("pair")["batsman_runs"]
                 .sum().sort_values(ascending=False).head(10).reset_index())
    top_pairs.columns = ["Partnership","Runs"]

    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(data=top_pairs, x="Runs", y="Partnership", palette="Purples_d", ax=ax)
    ax.bar_label(ax.containers[0], padding=3, fontsize=9)
    ax.set_title("Top 10 IPL Batting Partnerships", fontsize=14, fontweight="bold")
    plt.tight_layout(); show_fig(fig)


# ═════════════════════════════════════════════════════════════════════════════
# PAGE 7: VENUE ANALYSIS
# ═════════════════════════════════════════════════════════════════════════════
elif page == " Venue Analysis":
    st.title("▶ Venue Analysis")

    venue_counts = (m["venue"].value_counts().head(10).reset_index())
    venue_counts.columns = ["Venue","Matches"]

    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(data=venue_counts, x="Matches", y="Venue", palette="coolwarm", ax=ax)
    ax.bar_label(ax.containers[0], padding=3, fontsize=9)
    ax.set_title("Top 10 IPL Venues by Matches Hosted", fontsize=14, fontweight="bold")
    plt.tight_layout(); show_fig(fig)

    st.markdown("---")
    st.subheader("🏠 Home Ground Advantage")
    selected_team = st.selectbox("Select Team", ALL_TEAMS)
    team_matches = m[(m["team1"] == selected_team) | (m["team2"] == selected_team)]
    team_venues  = team_matches["venue"].value_counts().head(5)
    st.bar_chart(team_venues)
