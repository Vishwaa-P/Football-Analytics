import streamlit as st
import pandas as pd
from preprocessor import get_processed_data
from helper import get_player, compare_players, plot_comparison_bar, plot_top10, plot_radar, player_card

# =====================================================
# CONFIG & PAGE SETUP
# =====================================================
st.set_page_config(page_title="Virtual Scout | Football Analytics", layout="wide", page_icon="⚽")

# =====================================================
# 🎨 CUSTOM CSS STYLING
# =====================================================
st.markdown("""
    <style>
        .stApp { background-color: #0E1117; color: #FAFAFA; }
        .block-container { padding-top: 2rem; padding-bottom: 2rem; }
        div[data-testid="stMetric"] {
            background-color: #161A25; border: 1px solid #282C36;
            padding: 15px; border-radius: 10px; box-shadow: 2px 2px 10px rgba(0,0,0,0.3);
            transition: transform 0.2s ease-in-out;
        }
        div[data-testid="stMetric"]:hover { transform: scale(1.02); border-color: #00B4D8; }
        div[data-testid="stMetricLabel"] { font-size: 14px; color: #A0A0A0; }
        div[data-testid="stMetricValue"] { font-size: 24px; font-weight: 700; color: #FFFFFF; }
        .stButton>button {
            background: linear-gradient(90deg, #00B4D8 0%, #0096C7 100%);
            color: white; border: none; padding: 10px 24px;
            border-radius: 8px; font-weight: 600; transition: all 0.3s ease;
        }
        .stButton>button:hover {
            background: linear-gradient(90deg, #0096C7 0%, #0077B6 100%);
            box-shadow: 0px 4px 15px rgba(0, 180, 216, 0.4); transform: translateY(-2px);
        }
        section[data-testid="stSidebar"] { background-color: #0E1117; border-right: 1px solid #282C36; }
        h1, h2, h3 { font-family: 'Helvetica Neue', sans-serif; font-weight: 700; letter-spacing: -0.5px; }
        .highlight { color: #00B4D8; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# =====================================================
# LOAD DATA
# =====================================================
@st.cache_data
def load_all():
    return get_processed_data()

df_fw, df_mf, df_fullback, df_centerback, df_gk = load_all()

pos_map = {
    "Forwards": df_fw, "Midfielders": df_mf,
    "Fullbacks": df_fullback, "Centerbacks": df_centerback, "Goalkeepers": df_gk
}

# =====================================================
# SIDEBAR
# =====================================================
st.sidebar.title("⚽ Virtual Scout")
st.sidebar.markdown("---")
mode = st.sidebar.radio("Navigate", ["Home", "Single Player Stats", "Compare Two Players", "Top 10 Rankings"])
st.sidebar.markdown("---")
st.sidebar.info("Data: Fbref | Season 24/25")

# =====================================================
# HOME
# =====================================================
if mode == "Home":
    try: st.image("football_analytics_homepage.png", use_container_width=True)
    except: st.error("Please ensure 'football_analytics_homepage.png' is in the project folder.")

    st.title("Welcome to Virtual Scout 🏆")
    st.markdown("""
    <div style='background-color: #161A25; padding: 20px; border-radius: 10px; border-left: 5px solid #00B4D8;'>
        <h3>The Ultimate Player Analysis Tool</h3>
        <p style='color: #cccccc;'>
            Unlock elite football insights with our advanced scouting dashboard. 
            Compare players, visualize strengths, and find the next superstar.
        </p>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("### 🔎 Deep Dive")
        st.write("Analyze individual player profiles with detailed radar charts and per 90 metrics.")
    with c2:
        st.markdown("### ⚔️ Head-to-Head")
        st.write("Compare any two players side-by-side using percentile ranks to see who comes out on top.")
    with c3:
        st.markdown("### 🏆 Top Rankings")
        st.write("Discover the best performing players in every position using our custom algorithm.")

# =====================================================
# SINGLE PLAYER STATS
# =====================================================
elif mode == "Single Player Stats":
    st.header("🔎 Single Player Analysis")
    c1, c2 = st.columns([1, 2])
    with c1: pos = st.selectbox("Position", list(pos_map.keys()))
    df = pos_map[pos]
    player_list = sorted(df["Player"].unique())
    default_idx = None
    if "Kylian Mbappé" in player_list: default_idx = player_list.index("Kylian Mbappé")
    
    with c2: player_name = st.selectbox("Select Player", player_list, index=default_idx)
    st.write("") 

    if st.button("Analyze Player"):
        row = get_player(df, player_name)
        if row is not None:
            card = player_card(row)
            
            st.markdown("---")
            col_img, col_info = st.columns([1, 4])
            with col_img:
                if player_name == "Kylian Mbappé":
                    try: st.image("Kylian_Mbappe.png", width=150)
                    except: st.write("Image missing")
                else: st.markdown("## 👕") 
            with col_info:
                st.markdown(f"## {card['Player']}")
                st.markdown(f"<span class='highlight'>{card['Club']}</span> | {card['Nation']} | {card['Age']} years old", unsafe_allow_html=True)

            st.markdown("### 📊 Performance Overview")
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Matches Played", int(card['Minutes'] / 90))
            c2.metric("Minutes", card["Minutes"])
            c3.metric("League", card["League"])
            c4.metric("Virtual Score", card["Score"], delta_color="normal")
            
            c1, c2, c3, c4 = st.columns(4)
            if pos == "Goalkeepers":
                # --- GK UPDATES: Goals Conceded (Total), Saves/90 ---
                total_ga = int(row.get("GA", 0))
                ga90 = round(row.get("GA90", 0), 2)
                saves_p90 = round(row.get("Saves_per90", 0), 2)
                
                c1.metric("Goals Conceded", total_ga)
                c2.metric("Goals Conc./90", ga90)
                c3.metric("Saves / 90", saves_p90)
                c4.metric("Role", "Goalkeeper")
            else:
                c1.metric("Goals", card["Goals"])
                c2.metric("Assists", card["Assists"])
                c3.metric("G+A", card["G+A"])
                c4.metric("Role", pos[:-1]) 
            st.markdown("---")

            st.markdown("### ⚡ Detailed Stats (Per 90)")
            d1, d2, d3, d4 = st.columns(4)
            if pos == "Goalkeepers":
                # --- GK DETAILED STATS ---
                d1.metric("Save %", f"{round(row.get('Save%', 0), 1)}%")
                d2.metric("Clean Sheet %", f"{round(row.get('CS%', 0), 1)}%")
                d3.metric("Pass Comp %", f"{round(row.get('Cmp%', 0), 1)}%")
                d4.metric("Total Saves", int(row.get("Saves", 0)))
            else:
                xg_p90 = round(row.get("xG_per90", 0), 2)
                sh_p90 = round(row.get("Sh_per90", 0), 2)
                kp_p90 = round(row.get("KP_per90", 0), 2)
                carries_p90 = round(row.get("Carries_per90", 0), 2)
                d1.metric("xG / 90", xg_p90)
                d2.metric("Shots / 90", sh_p90)
                d3.metric("Key Passes / 90", kp_p90)
                d4.metric("Carries / 90", carries_p90)
                
                d1, d2, d3, d4 = st.columns(4)
                d1.metric("Prog. Carries", round(row.get("PrgC_per90", 0), 2))
                d2.metric("Prog. Passes", round(row.get("PrgP_per90", 0), 2))
                d3.metric("Tackles / 90", round(row.get("Tkl_per90", 0), 2))
                d4.metric("Interceptions", round(row.get("Int_per90", 0), 2))
            
            st.markdown("---")
            st.subheader("📈 Player Style Profile")
            
            if pos == "Forwards":
                radar_metrics = ["Gls_per90_pct_adj", "xG_per90_pct_adj", "Sh_per90_pct_adj", "KP_per90_pct_adj", "Carries_per90_pct_adj"]
            elif pos == "Midfielders":
                radar_metrics = ["KP_per90_pct_adj", "PrgP_per90_pct_adj", "Tkl_per90_pct_adj", "Int_per90_pct_adj", "Carries_per90_pct_adj"]
            elif pos in ["Fullbacks", "Centerbacks"]:
                radar_metrics = ["Tkl_per90_pct_adj", "Int_per90_pct_adj", "Clr_per90_pct_adj", "CrsPA_per90_pct_adj", "PrgC_per90_pct_adj"]
            elif pos == "Goalkeepers":
                # --- UPDATED GK RADAR: Replaced PSxG+/- with Saves ---
                radar_metrics = ["Saves_per90_pct_adj", "Save%_pct_adj", "GA90_pct_adj", "CS%_pct_adj", "Cmp%_pct_adj"]
            else:
                radar_metrics = ["Gls_per90_pct_adj", "Ast_per90_pct_adj", "PrgP_per90_pct_adj"]

            fig = plot_radar(df, [player_name], radar_metrics)
            st.pyplot(fig)

# =====================================================
# COMPARE PLAYERS
# =====================================================
elif mode == "Compare Two Players":
    st.header("⚔️ Head-to-Head Comparison")
    pos = st.selectbox("Position", list(pos_map.keys()))
    df = pos_map[pos]
    player_list = sorted(df["Player"].unique())
    c1, c2 = st.columns(2)
    p1 = c1.selectbox("Player 1", player_list, index=None)
    p2 = c2.selectbox("Player 2", player_list, index=None)
    st.write("")

    if st.button("Compare Players"):
        if p1 and p2:
            st.markdown("### 📊 Statistical Breakdown")
            
            if pos == "Goalkeepers":
                # Show Total GA, Saves/90, etc.
                table_metrics = ["GA", "GA90", "Saves_per90", "Save%", "CS%"]
            else:
                table_metrics = ["Gls", "Ast", "Gls_per90", "Ast_per90", "xG_per90", "KP_per90", "Carries_per90"]
                
            comp_table = compare_players(df, p1, p2, table_metrics)
            st.dataframe(comp_table, use_container_width=True)
            st.markdown("---")

            c1, c2 = st.columns(2)
            with c1:
                st.subheader("📈 Percentile Ranks")
                if pos == "Goalkeepers":
                    bar_metrics = ["GA90", "Save%", "CS%", "Saves_per90", "Cmp%"]
                else:
                    bar_metrics = ["Gls_per90", "Ast_per90", "xG_per90", "KP_per90", "Carries_per90"]
                fig_bar = plot_comparison_bar(df, p1, p2, bar_metrics)
                st.pyplot(fig_bar)
            
            with c2:
                st.subheader("🛑 Skill Radar")
                if pos == "Goalkeepers":
                    radar_metrics = ["Saves_per90_pct_adj", "Save%_pct_adj", "GA90_pct_adj", "CS%_pct_adj", "Cmp%_pct_adj"]
                else:
                    radar_metrics = ["Gls_per90_pct_adj", "G+A_per90_pct_adj", "KP_per90_pct_adj", "Carries_per90_pct_adj", "PrgC_per90_pct_adj"]
                fig_radar = plot_radar(df, [p1, p2], radar_metrics)
                st.pyplot(fig_radar)
        else:
            st.warning("Please select two players.")

# =====================================================
# TOP 10 RANKINGS
# =====================================================
elif mode == "Top 10 Rankings":
    st.header("🏆 Top 10 Rankings")
    c1, c2 = st.columns([1, 2])
    with c1: pos = st.selectbox("Position", list(pos_map.keys()))
    df = pos_map[pos]
    
    if pos == "Goalkeepers":
        # Updated Rankings for GK
        metric_options = {
            "Virtual Score": "score", "Save %": "Save%", "Clean Sheet %": "CS%",
            "Goals Conceded/90 (Inv)": "GA90", "Total Saves": "Saves"
        }
    else:
        metric_options = {
            "Virtual Score": "score", "Total Goals": "Gls", "Total Assists": "Ast",
            "Goals / 90": "Gls_per90", "Assists / 90": "Ast_per90",
            "Key Passes / 90": "KP_per90", "Carries / 90": "Carries_per90"
        }
    
    with c2: selected_name = st.selectbox("Rank By", list(metric_options.keys()))
    selected_col = metric_options[selected_name]

    if st.button("Show Rankings"):
        fig = plot_top10(df, selected_col)
        st.pyplot(fig)