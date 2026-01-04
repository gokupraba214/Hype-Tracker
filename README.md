# 🔥 Twitch Hype Tracker

## Overview
Twitch Hype Tracker is a **local-first, real-time analytics system** that connects to a live Twitch chat, performs sentiment analysis on messages, and visualizes the stream’s overall **Hype Level** over time.

The project emphasizes **system design, streaming data processing, and concurrency**, rather than batch or static data analysis.

---

## 🎯 Project Objectives
- Ingest **live Twitch chat messages** in real time
- Analyze message sentiment using **NLP**
- Compute a rolling “Hype Level” metric
- Visualize hype trends through a live dashboard
- Maintain a clean, extensible system architecture

---

## 🧠 System Architecture (Level 0 DFD)

```plantuml
@startuml
!theme plain
actor "Twitch Chat" as Chat
node "Python Backend" {
    component "TwitchIO Collector" as Collector
    component "Sentiment Analyzer (VADER)" as NLP
}
database "In-Memory Data Store (Pandas)" as Storage
node "Streamlit Dashboard" as UI

Chat -> Collector : Real-time IRC Messages
Collector -> NLP : Raw Text
NLP -> Storage : Sentiment Scores (-1 to +1)
Storage -> UI : Rolling Average Data
UI -> User : Visual Hype Indicator
@enduml
