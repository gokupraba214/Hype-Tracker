import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import time
import threading
import asyncio
from simple_bot import SimpleTwitchBot

# Page configuration
st.set_page_config(
    page_title="🔥 Twitch Hype Tracker",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        text-align: center;
        color: #FF6B6B;
        margin-bottom: 1rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    .hype-positive { color: #4CAF50; }
    .hype-negative { color: #F44336; }
    .hype-neutral { color: #FF9800; }
</style>
""", unsafe_allow_html=True)

# Title
st.markdown('<h1 class="main-header">🔥 Twitch Hype Tracker</h1>', unsafe_allow_html=True)

# Sidebar for configuration
st.sidebar.header("⚙️ Configuration")
channel = st.sidebar.text_input("Twitch Channel", value="ninja")
update_interval = st.sidebar.slider("Update Interval (seconds)", 1, 10, 2)

# Initialize session state
if 'bot' not in st.session_state:
    st.session_state.bot = None
if 'bot_thread' not in st.session_state:
    st.session_state.bot_thread = None
if 'running' not in st.session_state:
    st.session_state.running = False

# Bot control buttons
col1, col2 = st.sidebar.columns(2)

with col1:
    if st.button("▶️ Start Bot", type="primary"):
        if not st.session_state.running:
            st.session_state.bot = SimpleTwitchBot(channel)
            st.session_state.running = True
            st.session_state.bot_thread = threading.Thread(
                target=lambda: asyncio.run(st.session_state.bot.start())
            )
            st.session_state.bot_thread.daemon = True
            st.session_state.bot_thread.start()
            st.success(f"🤖 Bot started for #{channel}")

with col2:
    if st.button("⏹️ Stop Bot"):
        if st.session_state.running and st.session_state.bot:
            st.session_state.bot.running = False
            st.session_state.running = False
            st.warning("⏹️ Bot stopped")

# Status indicator
status_color = "🟢" if st.session_state.running else "🔴"
st.sidebar.markdown(f"### Status: {status_color} {'Running' if st.session_state.running else 'Stopped'}")

# Main dashboard area
if st.session_state.bot and hasattr(st.session_state.bot, 'messages_df'):
    df = st.session_state.bot.messages_df
    
    if not df.empty:
        # Metrics row
        st.markdown("### 📊 Real-Time Metrics")
        
        # Get current metrics
        metrics = st.session_state.bot.get_hype_metrics()
        
        # Create metric columns
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            hype_score = metrics['hype_score']
            hype_color = "hype-positive" if hype_score > 0.1 else "hype-negative" if hype_score < -0.1 else "hype-neutral"
            st.markdown(f"""
            <div class="metric-card">
                <h3>Hype Score</h3>
                <h2 class="{hype_color}">{hype_score:.3f}</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <h3>Messages</h3>
                <h2>{metrics['message_count']}</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            positive_count = metrics['sentiment_breakdown'].get('positive', 0)
            st.markdown(f"""
            <div class="metric-card">
                <h3>😊 Positive</h3>
                <h2>{positive_count}</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            negative_count = metrics['sentiment_breakdown'].get('negative', 0)
            st.markdown(f"""
            <div class="metric-card">
                <h3>😠 Negative</h3>
                <h2>{negative_count}</h2>
            </div>
            """, unsafe_allow_html=True)
        
        # Charts section
        st.markdown("### 📈 Analytics")
        
        # Create two columns for charts
        chart_col1, chart_col2 = st.columns(2)
        
        with chart_col1:
            st.markdown("#### 🎯 Sentiment Distribution")
            sentiment_counts = df['sentiment_label'].value_counts()
            fig_pie = px.pie(
                values=sentiment_counts.values,
                names=sentiment_counts.index,
                color_discrete_map={'positive': '#4CAF50', 'negative': '#F44336', 'neutral': '#FF9800'},
                title="Message Sentiment Breakdown"
            )
            fig_pie.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig_pie, use_container_width=True)
        
        with chart_col2:
            st.markdown("#### 📊 Sentiment Timeline")
            if len(df) > 0:
                df['time'] = pd.to_datetime(df['timestamp']).dt.strftime('%H:%M:%S')
                fig_timeline = px.line(
                    df.tail(50),  # Last 50 messages
                    x='time',
                    y='sentiment_score',
                    color='sentiment_label',
                    color_discrete_map={'positive': '#4CAF50', 'negative': '#F44336', 'neutral': '#FF9800'},
                    title="Sentiment Score Over Time",
                    markers=True
                )
                fig_timeline.update_layout(showlegend=True)
                st.plotly_chart(fig_timeline, use_container_width=True)
        
        # Recent messages table
        st.markdown("### 💬 Recent Messages")
        recent_df = df.tail(10).copy()
        recent_df['sentiment_emoji'] = recent_df['sentiment_label'].map({
            'positive': '😊', 'negative': '😠', 'neutral': '😐'
        })
        recent_df['sentiment_display'] = recent_df.apply(
            lambda row: f"{row['sentiment_emoji']} {row['sentiment_score']:.2f}", axis=1
        )
        
        display_df = recent_df[['timestamp', 'username', 'message', 'sentiment_display']].copy()
        display_df.columns = ['Time', 'User', 'Message', 'Sentiment']
        display_df['Time'] = pd.to_datetime(display_df['Time']).dt.strftime('%H:%M:%S')
        
        st.dataframe(display_df, use_container_width=True)
        
        # Auto-refresh
        time.sleep(update_interval)
        st.rerun()
    else:
        st.info("📡 Waiting for chat messages... Start the bot to begin collecting data!")
else:
    st.info("🤖 Bot not initialized. Click 'Start Bot' to begin tracking hype!")

# Footer
st.markdown("---")
st.markdown("🔥 **Twitch Hype Tracker** - Real-time sentiment analysis for Twitch chat")
st.markdown("*Built with Python, VADER, Pandas, and Streamlit*")
