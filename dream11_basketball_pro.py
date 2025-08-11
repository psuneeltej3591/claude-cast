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
    page_title="Dream11 Basketball Pro - First Rank Guide",
    page_icon="🏀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
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
        border-left: 5px solid #1f77b4;
        margin: 0.5rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .team-suggestion {
        background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        border: 2px solid #ff6b6b;
    }
</style>
""", unsafe_allow_html=True)

# Sample data for demonstration (in real app, this would come from API/database)
def load_sample_data():
    """Load sample basketball player data for demonstration"""
    
    # Player data with realistic Dream11 metrics
    players_data = {
        'Player Name': [
            'LeBron James', 'Stephen Curry', 'Kevin Durant', 'Giannis Antetokounmpo',
            'Nikola Jokic', 'Luka Doncic', 'Joel Embiid', 'Damian Lillard',
            'Jayson Tatum', 'Jimmy Butler', 'Anthony Davis', 'Devin Booker',
            'Zion Williamson', 'Trae Young', 'Ja Morant', 'Donovan Mitchell',
            'Bam Adebayo', 'Rudy Gobert', 'Karl-Anthony Towns', 'Bradley Beal'
        ],
        'Position': [
            'SF', 'PG', 'SF', 'PF', 'C', 'PG', 'C', 'PG', 'SF', 'SF',
            'PF', 'SG', 'PF', 'PG', 'PG', 'SG', 'C', 'C', 'C', 'SG'
        ],
        'Team': [
            'LAL', 'GSW', 'PHX', 'MIL', 'DEN', 'DAL', 'PHI', 'MIL',
            'BOS', 'MIA', 'LAL', 'PHX', 'NOP', 'ATL', 'MEM', 'CLE',
            'MIA', 'MIN', 'MIN', 'PHX'
        ],
        'Points': [
            25.4, 29.4, 29.7, 31.1, 24.5, 32.4, 33.1, 25.1,
            30.1, 22.9, 24.7, 27.8, 25.8, 26.2, 25.1, 26.1,
            20.4, 13.4, 20.8, 23.2
        ],
        'Rebounds': [
            7.5, 6.1, 6.7, 11.8, 11.8, 8.6, 10.2, 4.1,
            8.8, 5.9, 12.1, 4.5, 7.0, 3.0, 5.6, 4.1,
            9.2, 11.6, 10.8, 3.9
        ],
        'Assists': [
            7.3, 6.3, 5.3, 5.7, 9.8, 8.0, 4.2, 6.8,
            4.6, 5.3, 3.9, 5.5, 4.6, 10.2, 8.1, 4.3,
            3.2, 1.2, 3.6, 5.4
        ],
        'Steals': [
            1.1, 1.0, 0.7, 1.0, 1.3, 1.4, 1.0, 0.9,
            1.1, 1.8, 1.2, 0.8, 1.1, 1.1, 1.0, 1.4,
            1.0, 0.8, 0.8, 1.0
        ],
        'Blocks': [
            0.6, 0.4, 1.4, 0.8, 0.8, 0.5, 1.7, 0.3,
            1.1, 0.3, 2.4, 0.3, 0.6, 0.1, 0.3, 0.4,
            0.8, 2.1, 1.2, 0.3
        ],
        'Field Goal %': [
            50.6, 42.7, 56.0, 55.3, 63.2, 49.6, 54.8, 42.4,
            46.6, 53.9, 56.3, 49.4, 60.8, 42.9, 46.0, 45.4,
            54.0, 65.9, 52.6, 50.6
        ],
        '3-Point %': [
            32.1, 42.7, 40.4, 27.5, 38.3, 34.2, 33.0, 37.1,
            35.0, 35.0, 25.7, 36.8, 36.0, 33.5, 30.7, 34.8,
            8.3, 0.0, 36.6, 36.5
        ],
        'Free Throw %': [
            76.2, 91.5, 91.9, 72.2, 82.0, 74.2, 85.7, 91.4,
            85.4, 85.0, 78.4, 86.6, 71.5, 88.6, 75.9, 86.7,
            81.4, 64.6, 84.1, 84.2
        ],
        'Games Played': [
            55, 56, 47, 63, 69, 66, 66, 58, 74, 64,
            56, 53, 29, 73, 61, 68, 75, 70, 29, 50
        ],
        'Minutes': [
            35.5, 34.7, 35.6, 32.1, 33.7, 36.2, 34.6, 36.3,
            36.9, 33.4, 34.0, 35.4, 33.0, 34.8, 31.9, 35.7,
            34.6, 26.9, 32.7, 33.5
        ]
    }
    
    df = pd.DataFrame(players_data)
    
    # Calculate Dream11 fantasy points
    df['Fantasy Points'] = (
        df['Points'] * 1.0 +
        df['Rebounds'] * 1.5 +
        df['Assists'] * 2.0 +
        df['Steals'] * 3.0 +
        df['Blocks'] * 3.0 +
        (df['Field Goal %'] - 40) * 0.1 +
        (df['3-Point %'] - 30) * 0.1 +
        (df['Free Throw %'] - 70) * 0.1
    ).round(2)
    
    # Calculate consistency score
    df['Consistency'] = (
        df['Games Played'] / 82 * 100 +
        df['Minutes'] / 40 * 100
    ).round(2)
    
    # Calculate value for money (fantasy points per game)
    df['Value Score'] = (df['Fantasy Points'] * df['Consistency'] / 100).round(2)
    
    return df

def calculate_team_score(selected_players, df):
    """Calculate total team fantasy points"""
    team_df = df[df['Player Name'].isin(selected_players)]
    return team_df['Fantasy Points'].sum()

def get_team_composition(selected_players, df):
    """Get team composition analysis"""
    team_df = df[df['Player Name'].isin(selected_players)]
    
    composition = {
        'PG': len(team_df[team_df['Position'] == 'PG']),
        'SG': len(team_df[team_df['Position'] == 'SG']),
        'SF': len(team_df[team_df['Position'] == 'SF']),
        'PF': len(team_df[team_df['Position'] == 'PF']),
        'C': len(team_df[team_df['Position'] == 'C'])
    }
    
    return composition

def create_optimal_team(df, budget=100, max_players=8):
    """Create optimal team based on value score and budget"""
    # Sort by value score (descending)
    sorted_df = df.sort_values('Value Score', ascending=False)
    
    selected_players = []
    total_budget = 0
    
    for _, player in sorted_df.iterrows():
        if len(selected_players) >= max_players:
            break
            
        # Simple budget allocation (in real app, this would be more sophisticated)
        player_cost = max(8, min(15, 20 - player['Value Score'] / 10))
        
        if total_budget + player_cost <= budget:
            selected_players.append(player['Player Name'])
            total_budget += player_cost
    
    return selected_players, total_budget

def main():
    # Header
    st.markdown('<h1 class="main-header">🏀 Dream11 Basketball Pro</h1>', unsafe_allow_html=True)
    st.markdown('<h2 style="text-align: center; color: #ff6b6b;">First Rank Strategy Guide</h2>', unsafe_allow_html=True)
    
    # Load data
    df = load_sample_data()
    
    # Sidebar
    st.sidebar.title("🎯 Team Builder")
    st.sidebar.markdown("---")
    
    # Filters
    st.sidebar.subheader("📊 Filters")
    position_filter = st.sidebar.multiselect(
        "Position",
        options=['PG', 'SG', 'SF', 'PF', 'C'],
        default=['PG', 'SG', 'SF', 'PF', 'C']
    )
    
    min_fantasy_points = st.sidebar.slider(
        "Minimum Fantasy Points",
        min_value=float(df['Fantasy Points'].min()),
        max_value=float(df['Fantasy Points'].max()),
        value=float(df['Fantasy Points'].quantile(0.25))
    )
    
    # Filter data
    filtered_df = df[
        (df['Position'].isin(position_filter)) &
        (df['Fantasy Points'] >= min_fantasy_points)
    ]
    
    # Main content
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📈 Player Performance Analysis")
        
        # Top performers
        top_players = filtered_df.nlargest(10, 'Fantasy Points')
        
        fig = px.bar(
            top_players,
            x='Player Name',
            y='Fantasy Points',
            color='Position',
            title="Top 10 Players by Fantasy Points",
            color_discrete_map={
                'PG': '#1f77b4', 'SG': '#ff7f0e', 'SF': '#2ca02c',
                'PF': '#d62728', 'C': '#9467bd'
            }
        )
        fig.update_layout(height=500, showlegend=True)
        st.plotly_chart(fig, use_container_width=True)
        
        # Player statistics table
        st.subheader("🏆 Player Statistics")
        display_df = filtered_df[['Player Name', 'Position', 'Team', 'Fantasy Points', 
                                'Value Score', 'Consistency', 'Points', 'Rebounds', 'Assists']]
        st.dataframe(display_df.sort_values('Fantasy Points', ascending=False), use_container_width=True)
    
    with col2:
        st.subheader("💰 Team Builder")
        
        # Auto-generate optimal team
        if st.button("🎯 Generate Optimal Team", type="primary"):
            optimal_players, total_cost = create_optimal_team(filtered_df)
            
            st.markdown('<div class="team-suggestion">', unsafe_allow_html=True)
            st.markdown("### 🏆 Optimal Team Suggestion")
            st.markdown(f"**Total Cost:** ${total_cost}")
            st.markdown(f"**Players:** {len(optimal_players)}")
            st.markdown("---")
            
            for i, player in enumerate(optimal_players, 1):
                player_data = df[df['Player Name'] == player].iloc[0]
                st.markdown(f"**{i}.** {player} ({player_data['Position']})")
                st.markdown(f"   Fantasy Points: {player_data['Fantasy Points']}")
            
            st.markdown("</div>", unsafe_allow_html=True)
        
        # Manual team selection
        st.markdown("---")
        st.markdown("### ✏️ Manual Team Selection")
        
        selected_players = st.multiselect(
            "Select Players (Max 8)",
            options=filtered_df['Player Name'].tolist(),
            max_selections=8
        )
        
        if selected_players:
            team_score = calculate_team_score(selected_players, df)
            composition = get_team_composition(selected_players, df)
            
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Total Fantasy Points", f"{team_score:.2f}")
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Team composition chart
            fig = go.Figure(data=[
                go.Bar(
                    x=list(composition.keys()),
                    y=list(composition.values()),
                    marker_color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
                )
            ])
            fig.update_layout(
                title="Team Composition",
                height=300,
                showlegend=False
            )
            st.plotly_chart(fig, use_container_width=True)
    
    # Strategy section
    st.markdown("---")
    st.markdown("## 🎯 First Rank Strategy Guide")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown("### 📊 Key Metrics to Focus On")
        st.markdown("""
        - **Fantasy Points**: Primary scoring metric
        - **Value Score**: Efficiency per game
        - **Consistency**: Reliability factor
        - **Position Balance**: Proper team composition
        """)
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown("### 🏀 Position Strategy")
        st.markdown("""
        - **PG/SG**: High assist potential
        - **SF**: Balanced scoring
        - **PF/C**: Rebound and block specialists
        - **Balance**: 2-3 players per position
        """)
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown("### 💡 Pro Tips")
        st.markdown("""
        - Monitor injury reports
        - Check recent form trends
        - Consider home/away games
        - Analyze head-to-head matchups
        """)
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Advanced analytics
    st.markdown("---")
    st.markdown("## 📊 Advanced Analytics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Scatter plot: Fantasy Points vs Value Score
        fig = px.scatter(
            filtered_df,
            x='Fantasy Points',
            y='Value Score',
            color='Position',
            size='Consistency',
            hover_data=['Player Name', 'Team'],
            title="Fantasy Points vs Value Score"
        )
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Position-wise fantasy points distribution
        fig = px.box(
            filtered_df,
            x='Position',
            y='Fantasy Points',
            title="Fantasy Points Distribution by Position"
        )
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)
    
    # Recent form analysis (simulated)
    st.markdown("---")
    st.markdown("## 📈 Recent Form Analysis")
    
    # Simulate recent form data
    np.random.seed(42)
    recent_form = filtered_df.copy()
    recent_form['Last 5 Games Avg'] = recent_form['Fantasy Points'] * np.random.uniform(0.8, 1.2, len(recent_form))
    recent_form['Form Trend'] = np.random.choice(['📈', '📉', '➡️'], len(recent_form))
    
    form_display = recent_form[['Player Name', 'Position', 'Fantasy Points', 'Last 5 Games Avg', 'Form Trend']]
    form_display = form_display.sort_values('Last 5 Games Avg', ascending=False)
    
    st.dataframe(form_display, use_container_width=True)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 2rem;">
        <p>🏀 <strong>Dream11 Basketball Pro</strong> - Your ultimate guide to first rank!</p>
        <p>⚠️ This is a demonstration app. Always verify data before making real decisions.</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()