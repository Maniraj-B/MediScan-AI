# MediScan AI+

### AI-Powered Health Intelligence Platform with Blockchain Trust

---

## Overview

MediScan AI+ is a full-stack AI-driven health assistant designed to predict diseases, guide user actions, and ensure secure medical history tracking.

Unlike typical symptom checkers, MediScan goes beyond diagnosis by:

* Providing actionable recommendations
* Showing future health outcomes
* Maintaining tamper-proof health records using blockchain

---

## Key Features

### 1. AI Disease Prediction

* Uses Machine Learning (Random Forest)
* Predicts disease based on symptoms
* Displays confidence score

---

### 2. Smart Risk Assessment

* Classifies users into:

  * Low Risk
  * Medium Risk
  * High Risk
* Based on symptom intensity

---

### 3. Actionable Recommendations

* Personalized advice based on risk level
* Encourages timely medical intervention

---

### 4. Future Health Persona

* Simulates:

  * What happens if ignored
  * What happens if treated
* Helps users make informed decisions

---

### 5. Blockchain Health Records

* Each diagnosis is stored as a block
* Ensures:

  * Data integrity
  * Tamper-proof history
* Enables trusted medical tracking

---

### 6. Downloadable Health Report

* Generates PDF with:

  * Prediction
  * Risk
  * Advice

---

### 7. Minimal AI Chat Assistant

* Provides quick symptom-based guidance
* Lightweight and responsive

---

### 8. Mental Health Support

* Mood-based suggestions
* Supports holistic well-being

---

## Tech Stack

| Layer            | Technology                   |
| ---------------- | ---------------------------- |
| Frontend         | HTML, CSS, JavaScript        |
| Backend          | Flask (Python)               |
| Machine Learning | Scikit-learn (Random Forest) |
| Data Handling    | Pandas                       |
| Blockchain       | Custom Python Implementation |
| Reports          | ReportLab                    |

---

## Project Structure

```
mediscan-ai/
│
├── app.py
├── model.py
├── blockchain.py
├── utils.py
├── report.py
│
├── dataset/
│   └── dataset.csv
│
├── templates/
│   ├── index.html
│   ├── result.html
│   ├── blockchain.html
│
├── static/
│   ├── css/style.css
│
├── requirements.txt
└── README.md
```

---

## Installation and Setup

### 1. Clone Repository

```
git clone <your-repo-link>
cd mediscan-ai
```

---

### 2. Install Dependencies

```
pip install -r requirements.txt
```

---

### 3. Run Application

```
python app.py
```

---

### 4. Open in Browser

```
http://127.0.0.1:5000/
```

---

## How It Works

1. User selects symptoms
2. Machine learning model predicts disease
3. System calculates risk level
4. Provides:

   * Advice
   * Future outcome insights
5. Stores result in blockchain
6. Generates downloadable report

---

## Why Blockchain

Healthcare data must be:

* Secure
* Tamper-proof
* Reliable

This system ensures that once medical data is recorded, it cannot be altered.

---

## Use Cases

* Early disease detection
* Preventive healthcare
* Digital health records
* Patient awareness systems

---

## Disclaimer

This application is for educational and demonstration purposes only.
It is not a substitute for professional medical advice.

---

## Innovation Highlights

* Combines AI and blockchain in healthcare
* Introduces future health simulation
* Focuses on decision-making rather than just prediction

---

## Author

Bonkuri Maniraj
IIIT Kottayam

---

## Future Scope

* Integration with healthcare systems
* Mobile application development
* Real-time health data integration
* Advanced AI models

---

## Tagline

"Do not just detect illness — understand, act, and prevent."
