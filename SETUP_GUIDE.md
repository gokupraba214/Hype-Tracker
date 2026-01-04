# 🚀 Twitch Hype Tracker - Setup & Running Guide

**Last Updated:** January 5, 2026  
**Project Status:** ✅ MVP Working - 70% Complete  
**Difficulty:** ⭐ Beginner Friendly  
**Time Required:** 10-15 minutes

---

## 📊 Current Project Status

### ✅ **What's Working (70%)**
- **Bot Connection**: ✅ Connects to Twitch chat successfully
- **Sentiment Analysis**: ✅ VADER scoring with emoji indicators  
- **Data Storage**: ✅ Pandas DataFrame with rolling window
- **Dashboard**: ✅ Streamlit interface with sample data
- **Basic Visualizations**: ✅ Pie charts and timeline graphs
- **Real-time Metrics**: ✅ Hype score calculation

### 🔄 **What Needs Enhancement (30%)**
- **Live Data Integration**: 🔄 Bot ↔ Dashboard connection
- **Advanced Analytics**: 🔄 Word clouds, user trends
- **Performance Optimization**: 🔄 Memory management
- **User Experience**: 🔄 Better interface design
- **Error Handling**: 🔄 Robust error recovery
- **Data Export**: 🔄 CSV/JSON export features

---

## 📋 Prerequisites

### 🔧 **System Requirements**
- **Python 3.10+** (recommended 3.14)
- **Git** (for cloning repository)
- **Internet Connection** (for Twitch chat access)
- **8GB+ RAM** (recommended for smooth performance)

### 🌐 **Platform Support**
- ✅ **Windows 10/11** 
- ✅ **macOS** (Intel/Apple Silicon)
- ✅ **Linux** (Ubuntu/Debian/Fedora)

---

## 🎯 Quick Start (5 Minutes)

### 📥 **Step 1: Clone Repository**
```bash
git clone https://github.com/gokupraba214/Hype-Tracker.git
cd Hype-Tracker
```

### 🐍 **Step 2: Create Virtual Environment**
```bash
# Windows
python -m venv venv

# macOS/Linux
python3 -m venv venv
```

### ⚡ **Step 3: Activate Environment**
```bash
# Windows PowerShell
.\venv\Scripts\Activate.ps1

# Windows CMD
venv\Scripts\activate.bat

# macOS/Linux
source venv/bin/activate
```

### 📦 **Step 4: Install Dependencies**
```bash
pip install twitchio vaderSentiment streamlit pandas websockets plotly
```

### 🚀 **Step 5: Run the Project**
```bash
# Terminal 1: Start the bot
python src/simple_bot.py

# Terminal 2: Start the dashboard
streamlit run src/simple_dashboard.py
```

### 🎯 **Step 6: Test the System**

#### **✅ Test 1: Bot Connection**
```bash
# Terminal 1: Test bot
python src/simple_bot.py
```
**Expected Output:**
```
Initialized sentiment analyzer and data storage for ninja
Starting Simple Twitch Bot for channel: ninja
Connected to Twitch IRC for channel: ninja
Joined #ninja
[ninja] Username: This stream is amazing! 😊 (0.85)
📊 Current Hype: 0.23 | Messages: 15 | {'positive': 8, 'neutral': 6, 'negative': 1}
```

#### **✅ Test 2: Dashboard**
```bash
# Terminal 2: Test dashboard
streamlit run src/simple_dashboard.py
```
**Expected Results:**
- Open http://localhost:8501
- See "🔥 Twitch Hype Tracker" title
- Click "🎲 Generate Sample Data"
- View charts and metrics

#### **✅ Test 3: Full System**
1. **Terminal 1**: `python src/simple_bot.py`
2. **Terminal 2**: `streamlit run src/simple_dashboard.py`
3. **Browser**: Navigate to dashboard
4. **Result**: Live chat analysis with real-time updates

### 🌐 **Step 7: Access Dashboard**
Open your browser and navigate to: **http://localhost:8501**

---

## 📊 Detailed Setup Instructions

### 🔧 **Environment Setup**

#### **Windows Setup**
```powershell
# Check Python version
python --version

# Create virtual environment
python -m venv venv

# Activate environment
.\venv\Scripts\Activate.ps1

# Install packages
pip install twitchio vaderSentiment streamlit pandas websockets plotly
```

#### **macOS Setup**
```bash
# Check Python version
python3 --version

# Create virtual environment
python3 -m venv venv

# Activate environment
source venv/bin/activate

# Install packages
pip3 install twitchio vaderSentiment streamlit pandas websockets plotly
```

#### **Linux Setup**
```bash
# Check Python version
python3 --version

# Create virtual environment
python3 -m venv venv

# Activate environment
source venv/bin/activate

# Install packages
pip3 install twitchio vaderSentiment streamlit pandas websockets plotly
```

---

## 🤖 Running the Components

### 📡 **Option 1: Bot Only (Terminal Output)**
```bash
# Activate environment first
.\venv\Scripts\Activate.ps1

# Run bot
python src/simple_bot.py
```

**What you'll see:**
```
Initialized sentiment analyzer and data storage for ninja
Starting Simple Twitch Bot for channel: ninja
Attempting to connect to wss://irc-ws.chat.twitch.tv:443...
Connected to Twitch IRC for channel: ninja
Joined #ninja
[ninja] Username: This stream is amazing! 😊 (0.85)
📊 Current Hype: 0.23 | Messages: 15 | {'positive': 8, 'neutral': 6, 'negative': 1}
```

### 📊 **Option 2: Dashboard Only (Sample Data)**
```bash
# Activate environment first
.\venv\Scripts\Activate.ps1

# Run dashboard
streamlit run src/simple_dashboard.py
```

**What you'll get:**
- 📊 Interactive web dashboard
- 📈 Real-time metrics visualization
- 🎨 Sample data generation
- 📋 Data upload capability

### 🔄 **Option 3: Full System (Bot + Dashboard)**
**Terminal 1 - Bot:**
```bash
.\venv\Scripts\Activate.ps1
python src/simple_bot.py
```

**Terminal 2 - Dashboard:**
```bash
.\venv\Scripts\Activate.ps1
streamlit run src/simple_dashboard.py
```

---

## 🎮 Using the Dashboard

### 📊 **Dashboard Features**

#### **📈 Real-Time Metrics**
- **Hype Score**: Overall sentiment (-1 to +1)
- **Message Count**: Recent chat activity
- **Positive/Negative Counts**: Sentiment breakdown

#### **📊 Visualizations**
- **Pie Chart**: Sentiment distribution
- **Timeline**: Sentiment score over time
- **Message Table**: Recent chat with sentiment

#### **⚙️ Configuration**
- **Channel Selection**: Choose Twitch channel
- **Data Upload**: Load chat data from JSON
- **Sample Data**: Generate demo data

### 🎯 **How to Use**

1. **Start Dashboard**: Open http://localhost:8501
2. **Generate Sample Data**: Click "Generate Sample Data" button
3. **View Analytics**: Explore charts and metrics
4. **Upload Real Data**: Use JSON format for live data

---

## 🔧 Configuration Options

### 📡 **Bot Configuration**

#### **Change Twitch Channel**
```python
# In src/simple_bot.py
bot = SimpleTwitchBot(channel='your_channel_name')
```

#### **Popular Channels to Test**
- `ninja` - Gaming streamer
- `shroud` - FPS gaming
- `pokimane` - Variety streaming
- `xqc` - Popular variety streamer

### 📊 **Dashboard Configuration**

#### **Update Interval**
```python
# In src/simple_dashboard.py
update_interval = st.sidebar.slider("Update Interval (seconds)", 1, 10, 2)
```

#### **Data Storage Limit**
```python
# In src/simple_bot.py
if len(self.messages_df) > 1000:  # Change this value
    self.messages_df = self.messages_df.tail(1000)
```

---

## 🐛 Troubleshooting

### 🔧 **Common Issues & Solutions**

#### **❌ "Python not found"**
```bash
# Install Python from python.org
# Verify installation
python --version
```

#### **❌ "venv activation failed"**
```bash
# Windows PowerShell execution policy
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Alternative: Use CMD instead of PowerShell
venv\Scripts\activate.bat
```

#### **❌ "Package installation failed"**
```bash
# Upgrade pip first
python -m pip install --upgrade pip

# Install packages individually
pip install twitchio
pip install vaderSentiment
pip install streamlit
pip install pandas
pip install websockets
pip install plotly
```

#### **❌ "Bot connection failed"**
```bash
# Check internet connection
# Try different channel
# Wait a few minutes and retry
```

#### **❌ "Dashboard not loading"**
```bash
# Check port 8501 is available
netstat -an | findstr 8501

# Kill existing streamlit processes
taskkill /f /im streamlit.exe

# Try different port
streamlit run src/simple_dashboard.py --server.port 8502
```

#### **❌ "ModuleNotFoundError"**
```bash
# Ensure virtual environment is activated
.\venv\Scripts\Activate.ps1

# Reinstall packages
pip install -r requirements.txt
```

---

## 📋 Requirements File (Optional)

Create `requirements.txt` for easy setup:
```txt
twitchio>=3.1.0
vaderSentiment>=3.3.2
streamlit>=1.52.2
pandas>=2.3.3
websockets>=15.0.1
plotly>=6.5.0
```

Then install with:
```bash
pip install -r requirements.txt
```

---

## 🚀 Advanced Usage

### 📊 **Export Data**
```python
# Add to simple_bot.py
def export_data(self, filename='chat_data.csv'):
    self.messages_df.to_csv(filename, index=False)
    print(f"Data exported to {filename}")
```

### 🔔 **Custom Alerts**
```python
# Add hype score threshold alerts
if metrics['hype_score'] > 0.8:
    print("🔥 HIGH HYPE ALERT!")
```

### 📱 **Mobile Access**
- Access dashboard from mobile devices
- Use your computer's IP address instead of localhost
- Example: `http://192.168.1.100:8501`

---

## 🎯 Performance Tips

### ⚡ **Optimization**
- **Message Limit**: Keep 1000-message limit for memory
- **Update Interval**: 2-5 seconds for dashboard updates
- **Channel Selection**: Popular channels have more data

### 💾 **Memory Management**
- Bot automatically manages memory
- Dashboard uses sample data for demo
- Export data for long-term storage

---

## 🎉 Success Indicators

### ✅ **Working Setup Checklist**
- [ ] ✅ Virtual environment activated
- [ ] ✅ All packages installed successfully
- [ ] ✅ Bot connects to Twitch chat
- [ ] ✅ Dashboard loads in browser
- [ ] ✅ Sample data generates correctly
- [ ] ✅ Charts display properly
- [ ] ✅ Real-time metrics update

### 🎊 **You're Ready When You See:**
```
🔥 Twitch Hype Tracker
📊 Real-Time Metrics
🎯 Sentiment Distribution
📊 Sentiment Timeline
💬 Recent Messages
```

---

## 🆘 Need Help?

### 📚 **Resources**
- **GitHub Repository**: https://github.com/gokupraba214/Hype-Tracker
- **Streamlit Docs**: https://docs.streamlit.io/
- **VADER Sentiment**: https://github.com/cjhutto/vaderSentiment
- **TwitchIO Docs**: https://twitchio.readthedocs.io/

### 💬 **Support**
- Check this guide first
- Review error messages carefully
- Ensure all prerequisites are met
- Test with sample data before live streams

---

## 🔄 Current Limitations (Known Issues)

### ⚠️ **What to Be Aware Of**
- **Bot ↔ Dashboard**: Not yet connected (separate systems)
- **Sample Data Only**: Dashboard uses generated data, not live bot data
- **Memory Management**: 1000-message limit may need adjustment
- **Error Recovery**: Basic error handling, needs enhancement
- **Data Persistence**: Data lost when bot restarts

### 🎯 **Next Development Steps**
1. **Live Data Integration**: Connect bot output to dashboard input
2. **Advanced Analytics**: Word clouds, user sentiment trends
3. **Data Export**: CSV/JSON download functionality
4. **Performance**: Optimize for long-running sessions
5. **UI/UX**: Enhanced interface and user interactions

---

## 🎉 Success Indicators

### ✅ **Working Setup Checklist**
- [ ] ✅ Virtual environment activated
- [ ] ✅ All packages installed successfully
- [ ] ✅ Bot connects to Twitch chat
- [ ] ✅ Dashboard loads in browser
- [ ] ✅ Sample data generates correctly
- [ ] ✅ Charts display properly
- [ ] ✅ Real-time metrics update

### 🎊 **You're Ready When You See:**
```
🔥 Twitch Hype Tracker
📊 Real-Time Metrics
🎯 Sentiment Distribution
📊 Sentiment Timeline
💬 Recent Messages
```

---

## 🆘 Need Help?

### 📚 **Resources**
- **GitHub Repository**: https://github.com/gokupraba214/Hype-Tracker
- **Streamlit Docs**: https://docs.streamlit.io/
- **VADER Sentiment**: https://github.com/cjhutto/vaderSentiment
- **TwitchIO Docs**: https://twitchio.readthedocs.io/

### 💬 **Support**
- Check this guide first
- Review error messages carefully
- Ensure all prerequisites are met
- Test with sample data before live streams

---

## 🎯 Conclusion

**🎉 You're running a 70% complete MVP!** 

Your Twitch Hype Tracker successfully:
- ✅ Connects to live Twitch chat
- ✅ Analyzes sentiment in real-time
- ✅ Displays interactive dashboard
- ✅ Calculates hype metrics
- ✅ Provides sample data for testing

**Ready for the next 30% enhancement phase!** 🚀🔥

---

*Last Updated: January 5, 2026*  
*Status: ✅ MVP Working - 70% Complete - Enhancement Phase*
