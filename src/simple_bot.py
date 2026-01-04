import asyncio
import websockets
import json
import ssl
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd
from datetime import datetime

class SimpleTwitchBot:
    def __init__(self, channel='ninja'):
        self.channel = channel.lower()
        self.nickname = "justinfan12345"  # Anonymous viewer
        self.running = False
        
        # Initialize sentiment analyzer
        self.analyzer = SentimentIntensityAnalyzer()
        
        # Initialize data storage
        self.messages_df = pd.DataFrame(columns=[
            'timestamp', 'username', 'message', 'sentiment_score', 
            'sentiment_label', 'channel'
        ])
        print(f"Initialized sentiment analyzer and data storage for {self.channel}")
        
    async def connect(self):
        """Connect to Twitch IRC using websockets"""
        uri = "wss://irc-ws.chat.twitch.tv:443"
        
        while self.running:
            try:
                print(f"Attempting to connect to {uri}...")
                async with websockets.connect(uri) as websocket:
                    print(f"Connected to Twitch IRC for channel: {self.channel}")
                    
                    # Send authentication and join commands
                    print("Sending authentication...")
                    await websocket.send("PASS SCHMOOPIIE")  # Anonymous password
                    await websocket.send(f"NICK {self.nickname}")
                    await websocket.send(f"USER {self.nickname} 8 * :{self.nickname}")
                    
                    # Wait a moment for authentication
                    await asyncio.sleep(1)
                    
                    print(f"Joining #{self.channel}...")
                    await websocket.send(f"JOIN #{self.channel}")
                    
                    print(f"Joined #{self.channel}")
                    
                    # Listen for messages
                    while self.running:
                        try:
                            message = await asyncio.wait_for(websocket.recv(), timeout=300)
                            await self.handle_message(message)
                        except asyncio.TimeoutError:
                            # Send PING to keep connection alive
                            await websocket.send("PING :tmi.twitch.tv")
                        except websockets.exceptions.ConnectionClosed:
                            print("Connection closed, attempting to reconnect...")
                            break
                            
            except Exception as e:
                print(f"Connection error: {e}")
                if self.running:
                    print("Retrying in 5 seconds...")
                    await asyncio.sleep(5)
            
    def analyze_sentiment(self, message):
        """Analyze sentiment of a message using VADER"""
        scores = self.analyzer.polarity_scores(message)
        
        # Determine sentiment label
        if scores['compound'] >= 0.05:
            label = 'positive'
        elif scores['compound'] <= -0.05:
            label = 'negative'
        else:
            label = 'neutral'
            
        return {
            'compound': scores['compound'],
            'positive': scores['pos'],
            'negative': scores['neg'],
            'neutral': scores['neu'],
            'label': label
        }
    
    def store_message(self, username, message, sentiment_data):
        """Store message and sentiment data in DataFrame"""
        new_row = {
            'timestamp': datetime.now(),
            'username': username,
            'message': message,
            'sentiment_score': sentiment_data['compound'],
            'sentiment_label': sentiment_data['label'],
            'channel': self.channel
        }
        
        self.messages_df = pd.concat([self.messages_df, pd.DataFrame([new_row])], ignore_index=True)
        
        # Keep only last 1000 messages to manage memory
        if len(self.messages_df) > 1000:
            self.messages_df = self.messages_df.tail(1000)
    
    def get_hype_metrics(self):
        """Calculate current hype metrics"""
        if len(self.messages_df) == 0:
            return {'hype_score': 0, 'message_count': 0, 'sentiment_breakdown': {}}
        
        # Recent messages (last 50)
        recent_messages = self.messages_df.tail(50)
        
        # Calculate hype score (average sentiment)
        hype_score = recent_messages['sentiment_score'].mean()
        
        # Sentiment breakdown
        sentiment_counts = recent_messages['sentiment_label'].value_counts().to_dict()
        
        return {
            'hype_score': round(hype_score, 3),
            'message_count': len(recent_messages),
            'sentiment_breakdown': sentiment_counts
        }
    
    async def handle_message(self, raw_message):
        """Parse and handle IRC messages"""
        if raw_message.startswith("PING"):
            return  # Ignore PING messages
            
        # Parse PRIVMSG (chat messages)
        if "PRIVMSG" in raw_message:
            try:
                # Extract username and message content
                parts = raw_message.split("PRIVMSG")
                if len(parts) > 1:
                    user_part = parts[0]
                    message_part = parts[1]
                    
                    # Extract username
                    username = user_part.split(":")[1].split("!")[0].strip()
                    
                    # Extract message content
                    message_content = message_part.split(":", 1)[1].strip()
                    
                    # Analyze sentiment
                    sentiment = self.analyze_sentiment(message_content)
                    
                    # Store message
                    self.store_message(username, message_content, sentiment)
                    
                    # Get current hype metrics
                    metrics = self.get_hype_metrics()
                    
                    # Display with sentiment info
                    sentiment_emoji = {
                        'positive': '😊',
                        'negative': '😠', 
                        'neutral': '😐'
                    }
                    
                    print(f"[{self.channel}] {username}: {message_content} {sentiment_emoji[sentiment['label']]} ({sentiment['compound']:.2f})")
                    print(f"📊 Current Hype: {metrics['hype_score']:.2f} | Messages: {metrics['message_count']} | {metrics['sentiment_breakdown']}")
                    print("-" * 80)
                    
            except Exception as e:
                print(f"Error parsing message: {e}")
                
    async def start(self):
        """Start the bot"""
        print(f"Starting Simple Twitch Bot for channel: {self.channel}")
        self.running = True
        await self.connect()

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    bot = SimpleTwitchBot(channel='ninja')
    try:
        loop.run_until_complete(bot.start())
    except KeyboardInterrupt:
        print("\nBot stopped by user")
        bot.running = False
