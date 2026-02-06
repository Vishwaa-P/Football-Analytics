import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

METRIC_ALIASES = {
    # Raw Totals
    "Gls": "Total Goals",
    "Ast": "Total Assists",
    "G+A": "Total G+A",
    "GA": "Goals Conceded",          # <--- NEW
    "Saves": "Total Saves",          # <--- NEW

    # Per 90 Stats
    "Gls_per90": "Goals / 90",
    "Ast_per90": "Assists / 90",
    "G+A_per90": "G+A / 90",
    "Sh_per90": "Shots / 90",
    "xG_per90": "xG / 90",
    "KP_per90": "Key Passes / 90",
    "Carries_per90": "Carries / 90",
    "PrgC_per90": "Prog. Carries / 90",
    "PrgP_per90": "Prog. Passes / 90",
    
    # GK Stats
    "Saves_per90": "Saves / 90",
    "GA90": "Goals Conceded / 90",
    "Saves_per90_pct_adj": "Saves (Pct)",
    "Save%_pct_adj": "Save % (Pct)",
    "CS%_pct_adj": "Clean Sheet % (Pct)",
    "Cmp%_pct_adj": "Pass Completion (Pct)",
    "GA90_pct_adj": "Goals Conceded (Inv Pct)", 

    # Percentiles
    "Gls_per90_pct_adj": "Goals",
    "Ast_per90_pct_adj": "Assists",
    "G+A_per90_pct_adj": "G+A",
    "xG_per90_pct_adj": "xG",
    "Sh_per90_pct_adj": "Shots",
    "KP_per90_pct_adj": "Key Passes",
    "Carries_per90_pct_adj": "Carries",
    "PrgC_per90_pct_adj": "Prog. Carries",
    "PrgP_per90_pct_adj": "Prog. Passes",
    "Tkl_per90_pct_adj": "Tackles",
    "Int_per90_pct_adj": "Interceptions",
    "Clr_per90_pct_adj": "Clearances",
    "CrsPA_per90_pct_adj": "Crosses",
}

def get_alias(metric):
    return METRIC_ALIASES.get(metric, metric)

def get_player(df, name):
    row = df[df["Player"] == name]
    if row.empty: return None
    return row.iloc[0]

def compare_players(df, player1, player2, metrics):
    p1 = get_player(df, player1)
    p2 = get_player(df, player2)
    if p1 is None or p2 is None: return None
    
    readable_metrics = [get_alias(m) for m in metrics]
    data = {"Metric": readable_metrics, player1: [p1[m] for m in metrics], player2: [p2[m] for m in metrics]}
    return pd.DataFrame(data)

def plot_comparison_bar(df, player1, player2, metrics):
    pct_metrics = [m + "_pct_adj" for m in metrics if m + "_pct_adj" in df.columns]
    if not pct_metrics: pct_metrics = metrics

    comp = compare_players(df, player1, player2, pct_metrics)
    if comp is None or comp.empty: return None

    fig, ax = plt.subplots(figsize=(8, 5))
    fig.patch.set_facecolor('none')
    ax.set_facecolor('none')

    x = np.arange(len(pct_metrics))
    width = 0.35
    
    ax.bar(x - width/2, comp[player1], width, label=player1, color="#00B4D8", edgecolor='white', linewidth=0.5)
    ax.bar(x + width/2, comp[player2], width, label=player2, color="#FF006E", edgecolor='white', linewidth=0.5)

    readable_labels = [get_alias(m) for m in pct_metrics]
    ax.set_xticks(x)
    ax.set_xticklabels(readable_labels, rotation=45, ha="right", color="white", fontsize=10)
    ax.set_ylabel("Percentile Rank (0-100)", color="white", fontsize=10)
    ax.tick_params(axis='y', colors='white')
    
    legend = ax.legend(facecolor='#0E1117', edgecolor='white')
    plt.setp(legend.get_texts(), color='white')

    ax.grid(axis='y', linestyle='--', alpha=0.3, color='white')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_color('white')
    ax.spines['left'].set_color('white')

    plt.tight_layout()
    return fig

def plot_radar(df, players, metrics):
    readable_labels = [get_alias(m) for m in metrics]
    num_vars = len(metrics)
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    fig.patch.set_facecolor('none')
    ax.set_facecolor('#0E1117')
    
    colors = ["#00B4D8", "#FF006E"]
    
    for idx, p in enumerate(players):
        row = get_player(df, p)
        if row is None: continue
        values = []
        for m in metrics:
            val = row.get(m, 0) 
            values.append(val)
        values += values[:1]
        ax.plot(angles, values, linewidth=2, linestyle='solid', label=p, color=colors[idx % len(colors)])
        ax.fill(angles, values, alpha=0.25, color=colors[idx % len(colors)])

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(readable_labels, color='white', size=11, weight='bold')
    ax.tick_params(axis='x', pad=15) 
    
    ax.set_rlabel_position(0)
    plt.yticks([20, 40, 60, 80], ["20", "40", "60", "80"], color="#aaaaaa", size=8)
    plt.ylim(0, 100)
    
    ax.spines['polar'].set_color('#444444')
    ax.grid(color='#555555', linestyle='--', alpha=0.5)

    legend = ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))
    frame = legend.get_frame()
    frame.set_facecolor('#0E1117')
    frame.set_edgecolor('white')
    plt.setp(legend.get_texts(), color='white')

    return fig

def plot_top10(df, metric="score"):
    top = df.sort_values(metric, ascending=False).head(10)
    fig, ax = plt.subplots(figsize=(8, 5))
    fig.patch.set_facecolor('none')
    ax.set_facecolor('none')

    ax.barh(top["Player"], top[metric], color="#00CC96")
    ax.invert_yaxis()
    
    readable_metric = get_alias(metric)
    ax.set_xlabel(readable_metric, color="white", fontsize=10)
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_color('white')
    ax.spines['left'].set_color('white')
    return fig

def player_card(player_row):
    if player_row is None: return {}
    return {
        "Player": player_row["Player"],
        "Age": int(player_row["Age"]),
        "Nation": player_row["Nation"],
        "Club": player_row["Squad"],
        "League": player_row["Comp"],
        "Minutes": int(player_row["Min"]),
        "Goals": int(player_row["Gls"]),
        "Assists": int(player_row["Ast"]),
        "G+A": int(player_row["G+A"]),
        "Score": round(player_row["score"], 2)
    }