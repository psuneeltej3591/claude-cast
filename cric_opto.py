import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="Cric Opto - Dream11 Cricket Optimization",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #228B22;
        text-align: center;
        margin-bottom: 2rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    .metric-card {
        background: linear-gradient(135deg, #228B22 0%, #32CD32 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .player-card {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #228B22;
        margin: 0.5rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .team-suggestion {
        background: linear-gradient(135deg, #90EE90 0%, #98FB98 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        border: 2px solid #228B22;
    }
    .position-batsman { border-left-color: #FF6B6B !important; }
    .position-bowler { border-left-color: #4ECDC4 !important; }
    .position-allrounder { border-left-color: #45B7D1 !important; }
    .position-wicketkeeper { border-left-color: #96CEB4 !important; }
</style>
""", unsafe_allow_html=True)

# Sample cricket data for demonstration
def load_sample_data():
    """Load sample cricket player data for demonstration"""
    
    # Player data with realistic Dream11 cricket metrics
    players_data = {
        'Player Name': [
            'Virat Kohli', 'Rohit Sharma', 'KL Rahul', 'Jasprit Bumrah',
            'Ravindra Jadeja', 'Hardik Pandya', 'Rishabh Pant', 'Mohammed Shami',
            'Yuzvendra Chahal', 'Bhuvneshwar Kumar', 'Shreyas Iyer', 'Axar Patel',
            'Suryakumar Yadav', 'Arshdeep Singh', 'Harshal Patel', 'Deepak Chahar',
            'Washington Sundar', 'Shardul Thakur', 'Ishan Kishan', 'Sanju Samson'
        ],
        'Position': [
            'Batsman', 'Batsman', 'Batsman', 'Bowler',
            'All-Rounder', 'All-Rounder', 'Wicket-Keeper', 'Bowler',
            'Bowler', 'Bowler', 'Batsman', 'All-Rounder',
            'Batsman', 'Bowler', 'Bowler', 'Bowler',
            'All-Rounder', 'All-Rounder', 'Wicket-Keeper', 'Wicket-Keeper'
        ],
        'Team': [
            'RCB', 'MI', 'LSG', 'MI',
            'CSK', 'GT', 'DC', 'GT',
            'RR', 'SRH', 'KKR', 'DC',
            'MI', 'PBKS', 'RCB', 'CSK',
            'SRH', 'KKR', 'MI', 'RR'
        ],
        'Batting Average': [
            52.7, 48.9, 45.2, 8.9,
            23.4, 28.7, 34.2, 9.8,
            12.3, 11.2, 42.1, 18.9,
            38.4, 7.8, 9.2, 8.9,
            25.6, 19.8, 31.4, 29.8
        ],
        'Strike Rate': [
            137.2, 139.8, 136.9, 89.2,
            127.8, 145.6, 144.8, 92.1,
            98.7, 95.4, 134.2, 125.6,
            141.2, 87.6, 89.4, 88.9,
            128.9, 135.2, 138.7, 136.8
        ],
        'Bowling Average': [
            999.0, 999.0, 999.0, 22.8,
            28.9, 32.4, 999.0, 25.6,
            27.8, 29.1, 999.0, 31.2,
            999.0, 24.7, 26.8, 28.9,
            35.6, 30.2, 999.0, 999.0
        ],
        'Economy Rate': [
            999.0, 999.0, 999.0, 7.2,
            7.8, 8.4, 999.0, 8.1,
            7.9, 8.2, 999.0, 7.6,
            999.0, 8.3, 7.9, 8.1,
            8.7, 8.5, 999.0, 999.0
        ],
        'Wickets': [
            0, 0, 0, 145,
            97, 89, 0, 156,
            134, 141, 0, 78,
            0, 89, 92, 85,
            67, 74, 0, 0
        ],
        'Catches/Stumpings': [
            108, 95, 87, 23,
            156, 89, 187, 34,
            45, 38, 67, 89,
            78, 12, 15, 18,
            67, 45, 156, 134
        ],
        'Recent Form': [
            85, 78, 92, 88,
            76, 82, 79, 85,
            81, 77, 89, 74,
            91, 83, 79, 81,
            75, 78, 84, 76
        ]
    }
    
    df = pd.DataFrame(players_data)
    
    # Calculate fantasy points based on Dream11 cricket scoring
    df['Fantasy Points'] = calculate_cricket_fantasy_points(df)
    
    # Calculate value score (fantasy points per credit)
    df['Value Score'] = df['Fantasy Points'] / 10  # Assuming 10 credits per player
    
    # Calculate consistency factor
    df['Consistency'] = df['Recent Form'] / 100
    
    return df

def calculate_cricket_fantasy_points(df):
    """Calculate fantasy points for cricket players based on Dream11 rules"""
    points = []
    
    for _, row in df.iterrows():
        fp = 0
        
        # Batting points
        if row['Position'] in ['Batsman', 'All-Rounder', 'Wicket-Keeper']:
            # Runs points (1 point per run)
            fp += row['Batting Average'] * 0.8  # Estimated runs per match
            
            # Strike rate bonus
            if row['Strike Rate'] > 140:
                fp += 10
            elif row['Strike Rate'] > 130:
                fp += 5
            elif row['Strike Rate'] < 100:
                fp -= 5
        
        # Bowling points
        if row['Position'] in ['Bowler', 'All-Rounder']:
            # Wickets points (10 points per wicket)
            fp += row['Wickets'] * 0.8  # Estimated wickets per match
            
            # Economy rate points
            if row['Economy Rate'] < 7:
                fp += 15
            elif row['Economy Rate'] < 8:
                fp += 10
            elif row['Economy Rate'] > 9:
                fp -= 5
        
        # Fielding points
        if row['Position'] == 'Wicket-Keeper':
            fp += row['Catches/Stumpings'] * 0.3  # Stumpings worth more
        else:
            fp += row['Catches/Stumpings'] * 0.2
        
        # Recent form bonus
        fp += row['Recent Form'] * 0.3
        
        points.append(round(fp, 2))
    
    return points

def calculate_team_score(selected_players, df):
    """Calculate total fantasy points for selected team"""
    if not selected_players:
        return 0
    
    selected_df = df[df['Player Name'].isin(selected_players)]
    return selected_df['Fantasy Points'].sum()

def get_team_composition(selected_players, df):
    """Get team composition analysis"""
    if not selected_players:
        return {}
    
    selected_df = df[df['Player Name'].isin(selected_players)]
    composition = selected_df['Position'].value_counts().to_dict()
    
    # Ensure all positions are represented
    all_positions = ['Batsman', 'Bowler', 'All-Rounder', 'Wicket-Keeper']
    for pos in all_positions:
        if pos not in composition:
            composition[pos] = 0
    
    return composition

def create_optimal_team(df, budget=100, max_players=11):
    """Create optimal team using greedy algorithm"""
    # Sort players by value score (fantasy points per credit)
    df_sorted = df.sort_values('Value Score', ascending=False)
    
    selected_players = []
    remaining_budget = budget
    current_players = 0
    
    # Ensure we have at least one player from each position
    required_positions = ['Batsman', 'Bowler', 'All-Rounder', 'Wicket-Keeper']
    position_counts = {pos: 0 for pos in required_positions}
    
    # First, select one player from each required position
    for pos in required_positions:
        pos_players = df_sorted[df_sorted['Position'] == pos]
        if not pos_players.empty:
            best_player = pos_players.iloc[0]['Player Name']
            selected_players.append(best_player)
            position_counts[pos] += 1
            current_players += 1
            remaining_budget -= 10  # Assuming 10 credits per player
    
    # Fill remaining slots with best value players
    for _, player in df_sorted.iterrows():
        if current_players >= max_players:
            break
        
        if player['Player Name'] not in selected_players and remaining_budget >= 10:
            selected_players.append(player['Player Name'])
            current_players += 1
            remaining_budget -= 10
    
    return selected_players

def main():
    # Header
    st.markdown('<h1 class="main-header">🏏 Cric Opto - Dream11 Cricket Optimization</h1>', unsafe_allow_html=True)
    
    # Load data
    df = load_sample_data()
    
    # Sidebar
    st.sidebar.title("🎯 Team Builder")
    
    # Filter options
    min_fantasy_points = st.sidebar.slider("Minimum Fantasy Points", 0, 100, 30)
    position_filter = st.sidebar.multiselect(
        "Position Filter",
        ['Batsman', 'Bowler', 'All-Rounder', 'Wicket-Keeper'],
        default=['Batsman', 'Bowler', 'All-Rounder', 'Wicket-Keeper']
    )
    
    # Filter data
    filtered_df = df[
        (df['Fantasy Points'] >= min_fantasy_points) &
        (df['Position'].isin(position_filter))
    ]
    
    # Main content
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📊 Player Analysis")
        
        # Top performers
        st.write("**Top Performers by Fantasy Points:**")
        top_players = filtered_df.nlargest(10, 'Fantasy Points')[['Player Name', 'Position', 'Team', 'Fantasy Points', 'Value Score']]
        st.dataframe(top_players, use_container_width=True)
        
        # Position-wise analysis
        st.write("**Position-wise Performance:**")
        pos_analysis = filtered_df.groupby('Position').agg({
            'Fantasy Points': ['mean', 'max'],
            'Value Score': 'mean'
        }).round(2)
        st.dataframe(pos_analysis, use_container_width=True)
    
    with col2:
        st.subheader("🎮 Team Building")
        
        # Auto-generate team
        if st.button("🚀 Generate Optimal Team"):
            optimal_team = create_optimal_team(filtered_df)
            st.session_state.optimal_team = optimal_team
            st.success("Optimal team generated!")
        
        # Manual team selection
        st.write("**Manual Team Selection:**")
        selected_players = st.multiselect(
            "Select Players (Max 11):",
            filtered_df['Player Name'].tolist(),
            max_selections=11
        )
        
        if selected_players:
            # Team composition
            composition = get_team_composition(selected_players, df)
            st.write("**Team Composition:**")
            for pos, count in composition.items():
                if count > 0:
                    st.write(f"• {pos}: {count}")
            
            # Total score
            total_score = calculate_team_score(selected_players, df)
            st.metric("Total Fantasy Points", f"{total_score:.2f}")
            
            # Team analysis
            if len(selected_players) == 11:
                st.success("✅ Complete team selected!")
                
                # Balance check
                balanced = all(1 <= count <= 4 for count in composition.values())
                if balanced:
                    st.success("✅ Well-balanced team!")
                else:
                    st.warning("⚠️ Team might be unbalanced")
    
    # Strategy Guide
    st.markdown("---")
    st.subheader("🏆 First Rank Strategy Guide")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **🎯 Key Principles:**
        1. **Balance**: 3-4 batsmen, 3-4 bowlers, 2-3 all-rounders, 1 wicket-keeper
        2. **Consistency**: Choose reliable performers with good recent form
        3. **Value**: Focus on high-value players (fantasy points per credit)
        4. **Form**: Consider recent performance trends
        
        **📊 Position Strategy:**
        - **Batsmen**: High strike rate and average
        - **Bowlers**: Low economy rate, high wicket-taking ability
        - **All-Rounders**: Balanced batting and bowling performance
        - **Wicket-Keeper**: Good batting + wicket-keeping skills
        """)
    
    with col2:
        st.markdown("""
        **💡 Pro Tips:**
        - Monitor pitch conditions and weather
        - Check recent form trends (last 5 matches)
        - Consider home/away game factors
        - Analyze head-to-head matchups
        - Don't chase last match's performance
        - Ensure captain and vice-captain are from different teams
        
        **⚠️ Important Notes:**
        - Verify player availability and injury status
        - Check team news and playing XI
        - Consider match timing and venue
        """)
    
    # Advanced Analytics
    st.markdown("---")
    st.subheader("📈 Advanced Analytics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Fantasy Points vs Value Score scatter plot
        fig_scatter = px.scatter(
            filtered_df,
            x='Value Score',
            y='Fantasy Points',
            color='Position',
            hover_data=['Player Name', 'Team'],
            title='Fantasy Points vs Value Score by Position'
        )
        st.plotly_chart(fig_scatter, use_container_width=True)
    
    with col2:
        # Position distribution pie chart
        pos_counts = filtered_df['Position'].value_counts()
        fig_pie = px.pie(
            values=pos_counts.values,
            names=pos_counts.index,
            title='Player Distribution by Position'
        )
        st.plotly_chart(fig_pie, use_container_width=True)
    
    # Recent Form Analysis
    st.write("**Recent Form Analysis:**")
    form_df = filtered_df.nlargest(15, 'Recent Form')[['Player Name', 'Position', 'Team', 'Recent Form', 'Fantasy Points']]
    st.dataframe(form_df, use_container_width=True)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666;'>
        🏏 Cric Opto - Your Dream11 Cricket Companion<br>
        Use this tool as a guide for better team selection decisions
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()