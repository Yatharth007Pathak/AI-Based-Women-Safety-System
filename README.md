# AI-Based Women Safety Analytics System

## 🚨 Overview

The AI-Based Women Safety Analytics System is a full-stack, multi-modal AI-powered safety platform designed to provide proactive and real-time protection for women.

The system integrates:

- Real-time facial emotion detection (CNN)
- Distress sound detection (MFCC + ML)
- Crime-prone area prediction
- Geo-fencing based risk alerts
- Live location tracking
- Automated SOS triggering
- SMS & Email emergency notifications
- JWT-secured authentication
- MySQL-based logging system

This project demonstrates the practical application of Artificial Intelligence, Machine Learning, Computer Vision, Audio Processing, and Geospatial Intelligence in a real-world safety solution.

---

## 🎯 Key Features

### 🔐 Authentication System
- Secure user registration & login
- JWT-based authentication
- Password hashing using bcrypt

### 📍 Live Location Tracking
- Real-time GPS tracking via browser
- Google Maps integration
- Location sharing in alerts

### 🧠 Emotion Detection (AI Vision)
- CNN trained on FER2013 dataset
- Detects Fear, Sadness, etc.
- Auto-SOS triggered on continuous fear detection

### 🎤 Distress Sound Detection
- MFCC feature extraction using Librosa
- MLP-based scream classification
- Auto-SOS triggered on repeated distress detection

### 🔥 Crime Heatmap Visualization
- Crime data stored in MySQL
- Google Maps Heatmap overlay
- Risk score-based weighted zones

### 🚧 Geo-Fencing Risk Alert
- Haversine distance calculation
- Automatic warning when entering high-risk zone
- Optional auto-SOS trigger

### 🚨 Emergency Alert System
- Twilio SMS integration
- Gmail SMTP email alerts
- Live Google Maps location link included

### 📊 Logging System
- Alert logging in database
- Server error logging
- Thread-safe AI session counters

---

## 🏗 System Architecture

Frontend (HTML, CSS, JS)  
⬇  
Flask Backend APIs  
⬇  
AI Models (Vision + Audio + Crime ML)  
⬇  
MySQL Database  
⬇  
Twilio & Email Services  

---

## 🛠 Tech Stack

### Backend
- Python
- Flask
- Flask-JWT-Extended
- Flask-Bcrypt
- MySQL

### Artificial Intelligence
- TensorFlow / Keras
- OpenCV
- Librosa
- Scikit-learn
- Random Forest
- MLP Classifier

### Frontend
- HTML5
- CSS3
- JavaScript
- Google Maps API

### Alerts & Services
- Twilio SMS API
- Gmail SMTP
- Geolocation API

---


---

## Database Schema

Tables included:

- users
- emergency_contacts
- alert_logs
- crime_data

Database file: `women_safety_db.sql`

---


## ⚙ Installation Guide

### 1️⃣ Clone the Repository
```bash
git clone <your-repo-link>
cd AI-Based-Women-Safety-Analytics-System
```

### 2️⃣ Create Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Configure Environment Variables
Create .env file inside backend folder:
```
TWILIO_ACCOUNT_SID=your_sid
TWILIO_AUTH_TOKEN=your_token
TWILIO_PHONE_NUMBER=your_twilio_number

EMAIL_ADDRESS=your_email@gmail.com
EMAIL_PASSWORD=your_gmail_app_password
```

### 5️⃣ Setup MySQL Database
Import:
```
women_safety_db.sql
```

### 6️⃣ Run Backend
```bash
cd backend
python app.py
```

### 7️⃣ Open Frontend
Open:
```
frontend/index.html
```


## 🤖 AI Models

### Emotion Detection

Dataset: FER2013  
Model: CNN  
Output: 7 emotions  

### Sound Detection

Features: MFCC  
Model: MLP  
Output: Distress / Normal  

### Crime Prediction

Model: Random Forest  
Output: Risk Score  
```
