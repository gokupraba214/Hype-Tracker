import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import json
import numpy as np

# Page configuration
st.set_page_config(
    page_title="🔥 Twitch Hype Tracker",
    page_icon="🔥",
    layout="wide"
)

# Custom CSS
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
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Title
st.markdown('<h1 class="main-header">🔥 Twitch Hype Tracker</h1>', unsafe_allow_html=True)

# Sidebar for configuration
st.sidebar.header("⚙️ Configuration")

# File upload for demo data
st.sidebar.markdown("### 📁 Load Chat Data")
uploaded_file = st.sidebar.file_uploader("Upload chat data JSON", type=['json'])

# Sample data generator
if st.sidebar.button("🎲 Generate Sample Data"):
    sample_data = []
    sentiments = ['positive', 'neutral', 'negative']
    messages = [
        "This stream is amazing! 🔥",
        "Love the content!",
        "Not feeling this stream",
        "Great gameplay!",
        "Boring content...",
        "Best stream ever!",
        "Meh, could be better",
        "Awesome! 😊",
        "This is lit!",
        "Not my cup of tea"
    ]
    
    for i in range(50):
        sample_data.append({
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'username': f'user{i}',
            'message': messages[i % len(messages)],
            'sentiment_score': round(np.random.uniform(-1, 1), 2),
            'sentiment_label': sentiments[np.random.randint(0, 3)],
            'channel': 'demo'
        })
    
    st.session_state.sample_data = sample_data
    st.success("📊 Sample data generated!")

# Main content
if 'sample_data' in st.session_state or uploaded_file is not None:
    # Load data
    if uploaded_file is not None:
        try:
            data = json.loads(uploaded_file.read().decode('utf-8'))
            df = pd.DataFrame(data)
        except Exception as e:
            st.error(f"Error loading file: {e}")
            df = pd.DataFrame()
    else:
        df = pd.DataFrame(st.session_state.sample_data)
    
    if not df.empty:
        # Calculate metrics
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        recent_df = df.tail(50)
        
        # Metrics
        avg_sentiment = recent_df['sentiment_score'].mean()
        message_count = len(recent_df)
        sentiment_counts = recent_df['sentiment_label'].value_counts()
        
        # Display metrics
        st.markdown("### 📊 Real-Time Metrics")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            hype_color = "#4CAF50" if avg_sentiment > 0.1 else "#F44336" if avg_sentiment < -0.1 else "#FF9800"
            st.markdown(f"""
            <div class="metric-card">
                <h3>Hype Score</h3>
                <h2 style="color: {hype_color}">{avg_sentiment:.3f}</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <h3>Messages</h3>
                <h2>{message_count}</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            positive_count = sentiment_counts.get('positive', 0)
            st.markdown(f"""
            <div class="metric-card">
                <h3>😊 Positive</h3>
                <h2>{positive_count}</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            negative_count = sentiment_counts.get('negative', 0)
            st.markdown(f"""
            <div class="metric-card">
                <h3>😠 Negative</h3>
                <h2>{negative_count}</h2>
            </div>
            """, unsafe_allow_html=True)
        
        # Charts
        st.markdown("### 📈 Analytics")
        
        chart_col1, chart_col2 = st.columns(2)
        
        with chart_col1:
            st.markdown("#### 🎯 Sentiment Distribution")
            fig_pie = px.pie(
                values=sentiment_counts.values,
                names=sentiment_counts.index,
                color_discrete_map={'positive': '#4CAF50', 'negative': '#F44336', 'neutral': '#FF9800'},
                title="Message Sentiment Breakdown"
            )
            st.plotly_chart(fig_pie, use_container_width=True)
        
        with chart_col2:
            st.markdown("#### 📊 Sentiment Timeline")
            recent_df['time'] = recent_df['timestamp'].dt.strftime('%H:%M:%S')
            fig_timeline = px.line(
                recent_df,
                x='time',
                y='sentiment_score',
                color='sentiment_label',
                color_discrete_map={'positive': '#4CAF50', 'negative': '#F44336', 'neutral': '#FF9800'},
                title="Sentiment Score Over Time",
                markers=True
            )
            st.plotly_chart(fig_timeline, use_container_width=True)
        
        # Recent messages
        st.markdown("### 💬 Recent Messages")
        recent_messages = recent_df.tail(10).copy()
        recent_messages['sentiment_emoji'] = recent_messages['sentiment_label'].map({
            'positive': '😊', 'negative': '😠', 'neutral': '😐'
        })
        recent_messages['sentiment_display'] = recent_messages.apply(
            lambda row: f"{row['sentiment_emoji']} {row['sentiment_score']:.2f}", axis=1
        )
        
        display_df = recent_messages[['timestamp', 'username', 'message', 'sentiment_display']].copy()
        display_df.columns = ['Time', 'User', 'Message', 'Sentiment']
        display_df['Time'] = display_df['Time'].dt.strftime('%H:%M:%S')
        
        st.dataframe(display_df, use_container_width=True)
        
else:
    st.info("📡 No data available. Use the sidebar to generate sample data or upload a chat data file.")
    
    # Instructions
    st.markdown("""
    ### 🚀 How to Use This Dashboard
    
    1. **Generate Sample Data**: Click the "Generate Sample Data" button to see demo functionality
    2. **Upload Real Data**: Upload a JSON file with chat data in this format:
    ```json
    [
        {
            "timestamp": "2024-01-01 12:00:00",
            "username": "user123",
            "message": "Great stream!",
            "sentiment_score": 0.8,
            "sentiment_label": "positive",
            "channel": "ninja"
        }
    ]
    ```
    3. **View Analytics**: Explore the real-time metrics and visualizations
    """)

# Footer
st.markdown("---")
st.markdown("🔥 **Twitch Hype Tracker** - Real-time sentiment analysis for Twitch chat")
st.markdown("*Built with Python, VADER, Pandas, and Streamlit*")
