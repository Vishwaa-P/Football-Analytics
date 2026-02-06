import pandas as pd
import numpy as np

# ============================================================
# LOAD & CLEAN RAW DATA
# ============================================================
def load_data(path="final_dataset.csv"):
    try:
        df = pd.read_csv(path)
    except FileNotFoundError:
        # Fallback for demo/testing
        df = pd.read_csv("players_data_light-2024_2025.csv")

    required_cols = [
        "Player", "Nation", "Pos", "Squad", "Comp", "Age", "MP", "Min", "90s",
        "Gls", "Ast", "G+A", "xG", "npxG", "xAG", "npxG+xAG",
        "Sh", "SoT", "SoT%", "Sh/90", "SoT/90", "G/Sh", "G/SoT",
        "PrgC", "PrgP", "PrgR",
        "Cmp", "Att", "Cmp%", "KP", "1/3", "PPA", "CrsPA",
        "xA", "Carries",
        "Tkl", "TklW", "Def 3rd", "Mid 3rd", "Att 3rd",
        "Int", "Clr", "Err", "Tkl+Int",
        "GA", "GA90", "SoTA", "Saves", "Save%",
        "PSxG", "PSxG/SoT", "PSxG+/-", "CS", "CS%"
    ]

    # Keep existing columns
    existing_cols = [c for c in required_cols if c in df.columns]
    df = df[existing_cols].copy()
    
    # Fill missing critical columns with 0.0 to prevent crashes
    for col in ["PSxG+/-", "Save%", "CS%", "GA90", "Saves", "GA"]:
        if col not in df.columns:
            df[col] = 0.0

    # Remove duplicates
    df = df.loc[:, ~df.columns.duplicated()]
    
    # Clean Position
    df["Pos"] = df["Pos"].apply(lambda x: x.split(",")[0].strip())

    if "MP" in df.columns:
        df = df.drop(columns=["MP"])
    
    # Filter by Minutes
    df = df[df["Min"] >= 800].reset_index(drop=True)
    return df


# ============================================================
# PER-90 METRICS
# ============================================================
def add_per90(df):
    if df.empty: return df
    
    if "90s" not in df.columns:
        df["90s"] = df["Min"] / 90

    metrics_map = {
        "Gls": "Gls_per90", "Ast": "Ast_per90", "G+A": "G+A_per90",
        "Sh": "Sh_per90", "SoT": "SoT_per90", "xG": "xG_per90", "xAG": "xAG_per90",
        "KP": "KP_per90", "CrsPA": "CrsPA_per90", "Carries": "Carries_per90",
        "PrgC": "PrgC_per90", "PrgP": "PrgP_per90", "PrgR": "PrgR_per90",
        "Tkl": "Tkl_per90", "Int": "Int_per90", "Clr": "Clr_per90", "Tkl+Int": "Tkl+Int_per90",
        "Saves": "Saves_per90", "SoTA": "SoTA_per90", "GA": "GA_per90",
        "PSxG": "PSxG_per90", "PSxG+/-": "PSxG+/-_per90"
    }

    for col, new_col in metrics_map.items():
        if col in df.columns:
            df[new_col] = df[col] / df["90s"]
        else:
            df[new_col] = 0.0

    return df


# ============================================================
# PERCENTILES
# ============================================================
metrics_to_rank = [
    "Gls_per90", "Ast_per90", "G+A_per90", "Sh_per90", "SoT_per90",
    "xG_per90", "xAG_per90", "KP_per90", "CrsPA_per90", "Carries_per90",
    "PrgC_per90", "PrgP_per90", "PrgR_per90",
    "Tkl_per90", "Int_per90", "Clr_per90", "Tkl+Int_per90",
    "Saves_per90", "Save%", "CS%", "PSxG+/-_per90", "Cmp%", 
    "GA90" 
]

def add_percentiles(df):
    if df.empty: return df
    
    for col in metrics_to_rank:
        if col in df.columns:
            if col == "GA90":
                # Lower is better -> Ascending=False gives rank 100 to lowest GA
                df[col + "_pct"] = df[col].rank(pct=True, ascending=False) * 100
            else:
                df[col + "_pct"] = df[col].fillna(0).rank(pct=True) * 100
    return df


# ============================================================
# LEAGUE WEIGHTS & SCORING
# ============================================================
league_weights = {
    "eng Premier League": 1.00, "es La Liga": 0.95, "de Bundesliga": 0.90,
    "it Serie A": 0.90, "fr Ligue 1": 0.85, "nl Eredivisie": 0.75,
    "pt Primeira Liga": 0.75, "eng Championship": 0.70, "be Jupiler Pro League": 0.70,
    "aut Bundesliga": 0.65, "sui Super League": 0.65, "usa MLS": 0.60,
    "tr Süper Lig": 0.60, "other": 0.60
}

def apply_league_weight(df):
    if df.empty: return df
    
    df["league_weight"] = df["Comp"].apply(lambda c: league_weights.get(c, 0.60))
    for col in df.columns:
        if col.endswith("_pct"):
            df[col + "_adj"] = df[col] * df["league_weight"]
    return df

def score_player(df, position):
    if df.empty: return pd.Series(dtype=float)
    
    def safe_mean(cols):
        valid_cols = [c for c in cols if c in df.columns]
        if not valid_cols: return 0
        return df[valid_cols].mean(axis=1)

    if position == "GK":
        stopping = safe_mean(["Saves_per90_pct_adj", "Save%_pct_adj", "GA90_pct_adj"])
        stability = safe_mean(["CS%_pct_adj", "Cmp%_pct_adj"])
        return (0.65 * stopping) + (0.35 * stability)
    else:
        finish = safe_mean(["Gls_per90_pct_adj","G+A_per90_pct_adj","Sh_per90_pct_adj","SoT_per90_pct_adj","xG_per90_pct_adj"])
        create = safe_mean(["KP_per90_pct_adj","Ast_per90_pct_adj","Carries_per90_pct_adj","xAG_per90_pct_adj"])
        prog = safe_mean(["Carries_per90_pct_adj","PrgC_per90_pct_adj","PrgP_per90_pct_adj","PrgR_per90_pct_adj"])
        defend = safe_mean(["Tkl_per90_pct_adj","Int_per90_pct_adj","Clr_per90_pct_adj","Tkl+Int_per90_pct_adj"])

        weights = {
            "FW": (0.70, 0.15, 0.10, 0.05),
            "MF": (0.20, 0.35, 0.30, 0.15),
            "FB": (0.15, 0.30, 0.30, 0.25),
            "CB": (0.05, 0.10, 0.25, 0.60),
        }
        w_fin, w_cre, w_prog, w_def = weights.get(position, (0.25, 0.25, 0.25, 0.25))
        return (w_fin * finish + w_cre * create + w_prog * prog + w_def * defend)

def process_single_df(df, position_code):
    """Helper to process one dataframe completely to avoid copy issues."""
    if df.empty: return df
    
    # 1. Add Per 90
    df = add_per90(df)
    
    # 2. Remove Dupes
    df = df.loc[:, ~df.columns.duplicated()]
    
    # 3. Percentiles & Weights
    df = add_percentiles(df)
    df = apply_league_weight(df)
    
    # 4. Score
    df["score"] = score_player(df, position_code)
    
    return df

def get_processed_data(path="final_dataset.csv"):
    df = load_data(path)

    # Split
    df_fw = df[df["Pos"] == "FW"].copy()
    df_mf = df[df["Pos"] == "MF"].copy()
    df_df = df[df["Pos"] == "DF"].copy()
    df_gk = df[df["Pos"] == "GK"].copy()

    df_fullback = df_df[df_df["CrsPA"] >= 6].copy()
    df_centerback = df_df[df_df["CrsPA"] < 6].copy()

    # Process each one explicitly (No Loop Variable Traps!)
    df_fw = process_single_df(df_fw, "FW")
    df_mf = process_single_df(df_mf, "MF")
    df_fullback = process_single_df(df_fullback, "FB")
    df_centerback = process_single_df(df_centerback, "CB")
    df_gk = process_single_df(df_gk, "GK")

    return df_fw, df_mf, df_fullback, df_centerback, df_gk 
