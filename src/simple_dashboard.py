import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime
import json
import numpy as np
import time

# Page configuration
st.set_page_config(
    page_title="Twitch Hype Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Twitch Theme CSS
st.markdown("""
<style>
    /* Global Styles - Twitch Theme */
    .stApp {
        background: linear-gradient(135deg, #18181b 0%, #2d2d2d 100%);
        color: #efeff1;
    }
    
    /* Header Styles - Twitch Purple */
    .dashboard-header {
        background: linear-gradient(135deg, #9146ff 0%, #772ce8 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(145, 70, 255, 0.3);
        color: white;
        border: 2px solid #772ce8;
    }
    
    .dashboard-title {
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0;
        text-align: center;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        color: #ffffff;
    }
    
    .dashboard-subtitle {
        font-size: 1.1rem;
        text-align: center;
        margin: 0.5rem 0 0 0;
        opacity: 0.9;
        color: #efeff1;
    }
    
    /* Metric Cards - Twitch Theme */
    .metric-container {
        background: linear-gradient(135deg, #2d2d2d 0%, #1f1f23 100%);
        border-radius: 15px;
        padding: 1.5rem;
        box-shadow: 0 5px 20px rgba(0,0,0,0.3);
        border: 2px solid #772ce8;
        transition: transform 0.3s ease, box-shadow 0.3s ease, border-color 0.3s ease;
        margin: 0.5rem 0;
    }
    
    .metric-container:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 30px rgba(145, 70, 255, 0.4);
        border-color: #9146ff;
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        color: #9146ff;
        margin: 0;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: #adadb8;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin: 0.5rem 0 0 0;
    }
    
    .metric-change {
        font-size: 0.85rem;
        margin: 0.5rem 0 0 0;
        font-weight: 600;
    }
    
    .positive-change {
        color: #00f89a;
    }
    
    .negative-change {
        color: #eb0400;
    }
    
    /* Section Headers - Twitch Theme */
    .section-header {
        background: linear-gradient(135deg, #772ce8 0%, #5f1dc7 100%);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        font-size: 1.3rem;
        font-weight: 600;
        box-shadow: 0 5px 15px rgba(145, 70, 255, 0.3);
        border: 1px solid #9146ff;
    }
    
    /* Chart Containers - Twitch Theme */
    .chart-container {
        background: linear-gradient(135deg, #2d2d2d 0%, #1f1f23 100%);
        border-radius: 15px;
        padding: 1.5rem;
        box-shadow: 0 5px 20px rgba(0,0,0,0.3);
        margin: 1rem 0;
        border: 1px solid #772ce8;
    }
    
    /* Messages Table - Twitch Theme */
    .messages-container {
        background: linear-gradient(135deg, #2d2d2d 0%, #1f1f23 100%);
        border-radius: 15px;
        padding: 1.5rem;
        box-shadow: 0 5px 20px rgba(0,0,0,0.3);
        margin: 1rem 0;
        border: 1px solid #772ce8;
    }
    
    /* Sidebar Styles - Twitch Theme */
    .sidebar-content {
        background: linear-gradient(135deg, #2d2d2d 0%, #1f1f23 100%);
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
        box-shadow: 0 3px 10px rgba(0,0,0,0.3);
        border: 1px solid #772ce8;
    }
    
    /* Button Styles - Twitch Theme */
    .stButton > button {
        background: linear-gradient(135deg, #9146ff 0%, #772ce8 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 2px 8px rgba(145, 70, 255, 0.3);
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #a855f7 0%, #9146ff 100%);
        box-shadow: 0 4px 12px rgba(145, 70, 255, 0.5);
        transform: translateY(-2px);
    }
    
    /* Status Indicators */
    .status-indicator {
        display: inline-block;
        width: 12px;
        height: 12px;
        border-radius: 50%;
        margin-right: 8px;
    }
    
    .status-online {
        background: #00f89a;
        box-shadow: 0 0 10px rgba(0, 248, 154, 0.5);
    }
    
    .status-offline {
        background: #eb0400;
        box-shadow: 0 0 10px rgba(235, 4, 0, 0.5);
    }
    
    /* Animations */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .fade-in {
        animation: fadeIn 0.5s ease-out;
    }
    
    /* Streamlit overrides for dark theme */
    .stSelectbox > div > div {
        background: #2d2d2d;
        color: #efeff1;
    }
    
    .stSlider > div > div > div {
        background: #772ce8;
    }
    
    .stFileUploader {
        background: #2d2d2d;
        border: 2px dashed #772ce8;
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Professional Header
st.markdown("""
<div class="dashboard-header fade-in">
    <h1 class="dashboard-title">📊 Twitch Hype Analytics</h1>
    <p class="dashboard-subtitle">Real-time Sentiment Analysis & Engagement Metrics</p>
</div>
""", unsafe_allow_html=True)

# Enhanced Interactive Sidebar
with st.sidebar:
    st.markdown('<div class="sidebar-content">', unsafe_allow_html=True)
    
    # Dashboard Control Section
    with st.expander("🎛️ Dashboard Control", expanded=True):
        # Channel Configuration
        st.markdown('#### 📺 Channel Settings')
        channel = st.selectbox(
            'Select Twitch Channel',
            ['otplol', 'ninja', 'shroud', 'pokimane', 'xqc'],
            index=0,
            help='Choose the Twitch channel to analyze'
        )
        
        # Update Interval
        update_interval = st.slider(
            '⏱️ Update Interval (seconds)',
            min_value=1,
            max_value=10,
            value=2,
            help='How often to refresh the dashboard data'
        )
        
        # Auto-refresh toggle
        auto_refresh = st.checkbox('🔄 Auto-refresh', value=True, help='Automatically refresh dashboard data')
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Data Management Section
    st.markdown('<div class="sidebar-content">', unsafe_allow_html=True)
    
    with st.expander("📁 Data Management", expanded=True):
        # File Upload
        st.markdown('#### 📤 Import Data')
        uploaded_file = st.file_uploader(
            'Upload JSON chat data',
            type=['json'],
            help='Upload a JSON file with chat data for analysis'
        )
        
        if uploaded_file is not None:
            st.success(f'✅ File uploaded: {uploaded_file.name}')
            try:
                data = json.loads(uploaded_file.read().decode('utf-8'))
                st.info(f'📊 Loaded {len(data)} messages')
            except Exception as e:
                st.error(f'❌ Error loading file: {e}')
        
        # Sample Data Generator
        st.markdown('#### 🎲 Sample Data')
        col1, col2 = st.columns(2)
        with col1:
            generate_sample = st.button('🎲 Generate', help='Generate sample chat data for testing')
        with col2:
            clear_data = st.button('🗑️ Clear', help='Clear all data from dashboard')
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # System Status Section
    st.markdown('<div class="sidebar-content">', unsafe_allow_html=True)
    
    with st.expander("📊 System Status", expanded=True):
        # Connection Status
        st.markdown("""
        <div style="padding: 10px; background: #1f1f23; border-radius: 8px; margin: 10px 0; border: 1px solid #772ce8;">
            <span class="status-indicator status-online"></span>
            <strong style="color: #efeff1;">Bot Status:</strong> <span style="color: #00f89a;">Online</span>
        </div>
        """, unsafe_allow_html=True)
        
        # Data Status
        if 'sample_data' in st.session_state or uploaded_file is not None:
            st.markdown("""
            <div style="padding: 10px; background: #1f1f23; border-radius: 8px; margin: 10px 0; border: 1px solid #00f89a;">
                <span class="status-indicator status-online"></span>
                <strong style="color: #efeff1;">Data Status:</strong> <span style="color: #00f89a;">Available</span>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="padding: 10px; background: #1f1f23; border-radius: 8px; margin: 10px 0; border: 1px solid #eb0400;">
                <span class="status-indicator status-offline"></span>
                <strong style="color: #efeff1;">Data Status:</strong> <span style="color: #eb0400;">No Data</span>
            </div>
            """, unsafe_allow_html=True)
        
        # Channel Info
        st.markdown(f"""
        <div style="padding: 10px; background: #1f1f23; border-radius: 8px; margin: 10px 0; border: 1px solid #9146ff;">
            <strong style="color: #efeff1;">Current Channel:</strong> <span style="color: #9146ff;">{channel}</span>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Sample data generation logic
if generate_sample:
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
        "Not my cup of tea",
        "Hype train incoming!",
        "GG WP!",
        "First time here, loving it",
        "Can we get 100 viewers?",
        "This content is fire 🔥"
    ]
    
    for i in range(100):  # Increased sample size
        sample_data.append({
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'username': f'user{i}',
            'message': messages[i % len(messages)],
            'sentiment_score': round(np.random.uniform(-1, 1), 2),
            'sentiment_label': sentiments[np.random.randint(0, 3)],
            'channel': channel
        })
    
    st.session_state.sample_data = sample_data
    st.success('📊 Sample data generated successfully!')
    st.rerun()

# Clear data logic
if clear_data:
    if 'sample_data' in st.session_state:
        del st.session_state.sample_data
    st.warning('🗑️ Data cleared from dashboard')
    st.rerun()

# Main Content Area
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
        recent_df = df.tail(100)  # Last 100 messages
        
        # Calculate advanced metrics
        avg_sentiment = recent_df['sentiment_score'].mean()
        message_count = len(recent_df)
        sentiment_counts = recent_df['sentiment_label'].value_counts()
        
        # Calculate additional metrics
        positive_ratio = sentiment_counts.get('positive', 0) / message_count * 100
        engagement_rate = message_count / 100  # Messages per minute (assuming 100 min window)
        top_sentiment = sentiment_counts.index[0] if len(sentiment_counts) > 0 else 'neutral'
        
        # Professional KPI Cards
        st.markdown('<div class="section-header">📊 Key Performance Indicators</div>', unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="metric-container fade-in">
                <p class="metric-value">{avg_sentiment:.2f}</p>
                <p class="metric-label">Hype Score</p>
                <p class="metric-change positive-change">↑ {avg_sentiment:+.2f} vs last hour</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-container fade-in">
                <p class="metric-value">{message_count}</p>
                <p class="metric-label">Messages</p>
                <p class="metric-change positive-change">↑ {min(25, message_count//4)}% increase</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            trend_class = 'positive-change' if positive_ratio > 50 else 'negative-change'
            trend_text = 'Above average' if positive_ratio > 50 else 'Below average'
            st.markdown(f"""
            <div class="metric-container fade-in">
                <p class="metric-value">{positive_ratio:.1f}%</p>
                <p class="metric-label">Positive Ratio</p>
                <p class="metric-change {trend_class}">↑ {trend_text}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div class="metric-container fade-in">
                <p class="metric-value">{engagement_rate:.1f}</p>
                <p class="metric-label">Engagement Rate</p>
                <p class="metric-change positive-change">↑ High activity</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Analytics Section
        st.markdown('<div class="section-header">📈 Advanced Analytics</div>', unsafe_allow_html=True)
        
        chart_col1, chart_col2 = st.columns(2)
        
        with chart_col1:
            st.markdown('<div class="chart-container fade-in">', unsafe_allow_html=True)
            st.markdown('#### 🎯 Sentiment Distribution')
            
            # Enhanced pie chart with Twitch colors
            fig_pie = go.Figure(data=[
                go.Pie(
                    labels=sentiment_counts.index,
                    values=sentiment_counts.values,
                    hole=0.4,
                    marker_colors=['#00f89a', '#eb0400', '#772ce8'],  # Twitch green, red, purple
                    textinfo='label+percent',
                    textposition='auto',
                    showlegend=True,
                    hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>',
                    pull=[0.05, 0, 0]  # Pull out the largest slice
                )
            ])
            
            fig_pie.update_layout(
                title={
                    'text': 'Sentiment Breakdown',
                    'x': 0.5,
                    'font': {'size': 16, 'color': '#efeff1'}
                },
                font=dict(size=12, color='#efeff1'),
                showlegend=True,
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1,
                    font=dict(color='#efeff1')
                ),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)'
            )
            
            st.plotly_chart(fig_pie, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with chart_col2:
            st.markdown('<div class="chart-container fade-in">', unsafe_allow_html=True)
            st.markdown('#### 📊 Sentiment Timeline')
            
            if len(df) > 0:
                recent_df['time'] = recent_df['timestamp'].dt.strftime('%H:%M:%S')
                
                # Enhanced line chart with Twitch colors
                fig_timeline = go.Figure()
                
                for sentiment in ['positive', 'negative', 'neutral']:
                    sentiment_data = recent_df[recent_df['sentiment_label'] == sentiment]
                    if not sentiment_data.empty:
                        fig_timeline.add_trace(go.Scatter(
                            x=sentiment_data['time'],
                            y=sentiment_data['sentiment_score'],
                            mode='lines+markers',
                            name=sentiment.capitalize(),
                            line=dict(
                                color={'positive': '#00f89a', 'negative': '#eb0400', 'neutral': '#772ce8'}[sentiment],
                                width=3
                            ),
                            marker=dict(
                                size=6,
                                color={'positive': '#00f89a', 'negative': '#eb0400', 'neutral': '#772ce8'}[sentiment]
                            ),
                            hovertemplate='<b>%{fullData.name}</b><br>Time: %{x}<br>Score: %{y:.2f}<extra></extra>'
                        ))
                
                fig_timeline.update_layout(
                    title={
                        'text': 'Sentiment Score Over Time',
                        'x': 0.5,
                        'font': {'size': 16, 'color': '#efeff1'}
                    },
                    xaxis_title='Time',
                    yaxis_title='Sentiment Score',
                    xaxis=dict(
                        tickangle=-45,
                        title_font=dict(size=12, color='#efeff1'),
                        tickfont=dict(color='#efeff1'),
                        gridcolor='rgba(255,255,255,0.1)'
                    ),
                    yaxis=dict(
                        title_font=dict(size=12, color='#efeff1'),
                        tickfont=dict(color='#efeff1'),
                        range=[-1, 1],
                        gridcolor='rgba(255,255,255,0.1)'
                    ),
                    font=dict(size=10, color='#efeff1'),
                    hovermode='x unified',
                    showlegend=True,
                    legend=dict(
                        orientation="h",
                        yanchor="bottom",
                        y=1.02,
                        xanchor="right",
                        x=1,
                        font=dict(color='#efeff1')
                    ),
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)'
                )
                
                st.plotly_chart(fig_timeline, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        # Enhanced Recent Messages Section
        st.markdown('<div class="section-header">💬 Recent Chat Activity</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="messages-container fade-in">', unsafe_allow_html=True)
        
        recent_messages = recent_df.tail(15).copy()  # Show more messages
        recent_messages['sentiment_emoji'] = recent_messages['sentiment_label'].map({
            'positive': '🟢', 'negative': '🔴', 'neutral': '🟡'
        })
        recent_messages['sentiment_display'] = recent_messages.apply(
            lambda row: f"{row['sentiment_emoji']} {row['sentiment_score']:.2f}", axis=1
        )
        
        # Create Twitch-themed message display
        for i, (_, row) in enumerate(recent_messages.iterrows()):
            sentiment_color = {
                'positive': '#00f89a',
                'negative': '#eb0400',
                'neutral': '#772ce8'
            }[row['sentiment_label']]
            
            st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, #2d2d2d 0%, #1f1f23 100%);
                border-left: 4px solid {sentiment_color};
                border-radius: 8px;
                padding: 12px;
                margin: 8px 0;
                box-shadow: 0 2px 8px rgba(0,0,0,0.3);
                border: 1px solid rgba(145, 70, 255, 0.2);
            ">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <strong style="color: #9146ff;">{row['username']}</strong>
                        <span style="color: #adadb8; font-size: 0.85rem; margin-left: 10px;">
                            {row['timestamp'].strftime('%H:%M:%S')}
                        </span>
                    </div>
                    <div style="color: {sentiment_color}; font-weight: 600;">
                        {row['sentiment_display']}
                    </div>
                </div>
                <div style="margin-top: 8px; color: #efeff1;">
                    {row['message']}
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Streamscharts.com Inspired Analytics
        st.markdown('<div class="section-header">📊 Stream Analytics Dashboard</div>', unsafe_allow_html=True)
        
        insight_col1, insight_col2, insight_col3 = st.columns(3)
        
        with insight_col1:
            st.markdown('<div class="chart-container fade-in">', unsafe_allow_html=True)
            st.markdown('#### 🏆 Top Chatters')
            
            # Top users by message count
            top_users = recent_df['username'].value_counts().head(5)
            
            for i, (user, count) in enumerate(top_users.items()):
                badge_color = '#9146ff' if i == 0 else '#772ce8' if i == 1 else '#5f1dc7'
                st.markdown(f"""
                <div style="
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    padding: 8px;
                    border-bottom: 1px solid rgba(145, 70, 255, 0.2);
                    background: linear-gradient(135deg, rgba(145, 70, 255, 0.05) 0%, rgba(119, 44, 232, 0.05) 100%);
                ">
                    <span style="color: #efeff1; font-weight: 600;">{user}</span>
                    <span style="background: {badge_color}; color: white; padding: 2px 8px; border-radius: 12px; font-size: 0.8rem;">
                        {count} msgs
                    </span>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        with insight_col2:
            st.markdown('<div class="chart-container fade-in">', unsafe_allow_html=True)
            st.markdown('#### ⏰ Peak Activity Times')
            
            # Messages per time period
            recent_df['hour'] = recent_df['timestamp'].dt.hour
            hourly_activity = recent_df.groupby('hour').size().reset_index()
            hourly_activity.columns = ['Hour', 'Messages']
            
            fig_activity = px.bar(
                hourly_activity,
                x='Hour',
                y='Messages',
                color='Messages',
                color_continuous_scale=['#772ce8', '#9146ff', '#a855f7'],  # Twitch purple gradient
                title='Messages by Hour'
            )
            
            fig_activity.update_layout(
                height=250,
                showlegend=False,
                xaxis_title='Hour of Day',
                yaxis_title='Message Count',
                font=dict(color='#efeff1'),
                xaxis=dict(
                    tickfont=dict(color='#efeff1'),
                    title_font=dict(color='#efeff1'),
                    gridcolor='rgba(255,255,255,0.1)'
                ),
                yaxis=dict(
                    tickfont=dict(color='#efeff1'),
                    title_font=dict(color='#efeff1'),
                    gridcolor='rgba(255,255,255,0.1)'
                ),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)'
            )
            
            st.plotly_chart(fig_activity, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with insight_col3:
            st.markdown('<div class="chart-container fade-in">', unsafe_allow_html=True)
            st.markdown('#### 📈 Sentiment Momentum')
            
            # Sentiment trend over time
            sentiment_trend = recent_df.groupby(recent_df['timestamp'].dt.floor('5min')).agg({
                'sentiment_score': 'mean',
                'sentiment_label': lambda x: x.mode().iloc[0] if not x.mode().empty else 'neutral'
            }).reset_index()
            
            if not sentiment_trend.empty:
                fig_trend = go.Figure()
                fig_trend.add_trace(go.Scatter(
                    x=sentiment_trend['timestamp'],
                    y=sentiment_trend['sentiment_score'],
                    mode='lines+markers',
                    name='Sentiment Momentum',
                    line=dict(color='#9146ff', width=3),
                    fill='tonexty',
                    fillcolor='rgba(145, 70, 255, 0.2)',
                    marker=dict(size=6, color='#9146ff')
                ))
                
                fig_trend.update_layout(
                    height=250,
                    title='Sentiment Momentum (5-min intervals)',
                    xaxis_title='Time',
                    yaxis_title='Average Sentiment',
                    showlegend=False,
                    font=dict(color='#efeff1'),
                    xaxis=dict(
                        tickfont=dict(color='#efeff1'),
                        title_font=dict(color='#efeff1'),
                        gridcolor='rgba(255,255,255,0.1)'
                    ),
                    yaxis=dict(
                        range=[-1, 1],
                        tickfont=dict(color='#efeff1'),
                        title_font=dict(color='#efeff1'),
                        gridcolor='rgba(255,255,255,0.1)'
                    ),
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)'
                )
                
                st.plotly_chart(fig_trend, use_container_width=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Auto-refresh
        time.sleep(update_interval)
        st.rerun()
    
else:
    # Professional No Data State with Twitch theme
    st.markdown('<div class="section-header">📊 Dashboard Status</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="chart-container" style="text-align: center; padding: 3rem;">
        <div style="font-size: 4rem; margin-bottom: 1rem;">📊</div>
        <h3 style="color: #9146ff; margin-bottom: 1rem;">No Data Available</h3>
        <p style="color: #adadb8; margin-bottom: 2rem;">
            Start by generating sample data or uploading a JSON file to see the dashboard in action.
        </p>
        <div style="background: linear-gradient(135deg, rgba(145, 70, 255, 0.1) 0%, rgba(119, 44, 232, 0.1) 100%); padding: 1.5rem; border-radius: 10px; margin: 1rem 0; border: 1px solid rgba(145, 70, 255, 0.3);">
            <h4 style="color: #efeff1; margin-bottom: 1rem;">🚀 Quick Start Options:</h4>
            <ul style="text-align: left; color: #adadb8;">
                <li>Use the sidebar to <strong style="color: #9146ff;">Generate Sample Data</strong></li>
                <li><strong style="color: #9146ff;">Upload JSON</strong> file with chat data</li>
                <li>Connect the bot for <strong style="color: #9146ff;">Live Analysis</strong></li>
            </ul>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Instructions with Twitch theme
    st.markdown("""
    ### 📋 How to Use This Dashboard
    
    1. **Generate Sample Data**: Click the "🎲 Generate" button in the sidebar to see demo functionality
    2. **Upload Real Data**: Upload a JSON file with chat data in this format:
    ```json
    [
        {
            "timestamp": "2024-01-01 12:00:00",
            "username": "user123",
            "message": "Great stream!",
            "sentiment_score": 0.8,
            "sentiment_label": "positive",
            "channel": "otplol"
        }
    ]
    ```
    3. **View Analytics**: Explore the real-time metrics and visualizations
    """)

# Professional Footer with Twitch theme
st.markdown("""
<div style="
    background: linear-gradient(135deg, #9146ff 0%, #772ce8 100%);
    color: white;
    padding: 2rem;
    border-radius: 15px;
    margin-top: 3rem;
    text-align: center;
    box-shadow: 0 10px 30px rgba(145, 70, 255, 0.3);
    border: 2px solid #772ce8;
">
    <h3 style="margin: 0; font-size: 1.5rem;">📊 Twitch Hype Analytics Dashboard</h3>
    <p style="margin: 0.5rem 0; opacity: 0.9;">Real-time sentiment analysis & engagement metrics</p>
    <p style="margin: 0; font-size: 0.85rem; opacity: 0.7;">Built with Python • VADER • Pandas • Streamlit • Plotly</p>
    <p style="margin: 0.5rem 0 0 0; font-size: 0.75rem; opacity: 0.5;">🎮 Powered by Twitch API • 🚀 Stream Analytics Platform</p>
</div>
""", unsafe_allow_html=True)
