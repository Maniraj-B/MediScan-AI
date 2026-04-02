from flask import Flask, render_template, request, session, jsonify, send_file
import json
import requests
import uuid
from model import DiseaseModel
from blockchain import Blockchain
from report import generate_report
from utils import calculate_risk, get_advice, future_persona, mental_health_response, get_weather_health_advice

app = Flask(__name__)
app.secret_key = 'mediscan-ai-super-secret-key-2025'

# Initialize ML Model (auto-generates synthetic dataset if missing)
model = DiseaseModel('dataset/dataset.csv')

# Global blockchain (stores all records with username)
blockchain = Blockchain()

@app.route('/')
def index():
    if 'user_id' not in session:
        session['user_id'] = str(uuid.uuid4())
        session['username'] = 'Guest'
    
    # Fetch COVID stats from external API
    covid_stats = {}
    try:
        response = requests.get('https://disease.sh/v3/covid-19/all', timeout=5)
        if response.status_code == 200:
            data = response.json()
            covid_stats = {
                'cases': data.get('cases', 'N/A'),
                'deaths': data.get('deaths', 'N/A'),
                'recovered': data.get('recovered', 'N/A'),
                'todayCases': data.get('todayCases', 0)
            }
    except:
        covid_stats = {'error': 'Unable to fetch live data'}
    
    # Get weather-based health advice
    weather_advice = get_weather_health_advice()
    
    return render_template('index.html', 
                         covid_stats=covid_stats,
                         weather_advice=weather_advice,
                         username=session.get('username', 'Guest'))

@app.route('/predict', methods=['POST'])
def predict():
    # Get user inputs
    username = request.form.get('username', session.get('username', 'Guest'))
    session['username'] = username
    
    # Collect symptoms (checkboxes + severity from slider if available)
    symptom_input = {}
    feature_list = model.get_feature_list()
    
    for feature in feature_list:
        # Checkbox value: 'on' if checked, else 0
        val = request.form.get(feature, '0')
        # Severity sliders: if present, override checkbox
        severity = request.form.get(f'{feature}_severity')
        if severity:
            val = severity
        symptom_input[feature] = 1 if val == 'on' else int(val) if val.isdigit() else 0
    
    # Get prediction
    result = model.predict(symptom_input)
    
    if 'error' in result:
        return render_template('error.html', error=result['error'])
    
    prediction = result['prediction']
    confidence = result['confidence']
    
    # Calculate symptom count and risk
    symptom_count = sum(1 for v in symptom_input.values() if v > 0)
    risk = calculate_risk(symptom_count)
    advice = get_advice(risk, prediction)
    future = future_persona(risk)
    
    # Store prediction in blockchain with user context
    record = {
        'user': username,
        'timestamp': __import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'symptoms': {k: v for k, v in symptom_input.items() if v > 0},
        'prediction': prediction,
        'confidence': confidence,
        'risk': risk,
        'advice': advice
    }
    blockchain.add_block(record)
    
    # Store last prediction in session for PDF download
    session['last_prediction'] = record
    
    # Get probability distribution for chart
    prob_dist = result.get('prob_dist', {})
    
    return render_template('result.html',
                         prediction=prediction,
                         confidence=confidence,
                         risk=risk,
                         advice=advice,
                         future=future,
                         symptoms=symptom_input,
                         prob_dist=prob_dist,
                         username=username)

@app.route('/mental', methods=['POST'])
def mental():
    mood = request.form.get('mood', 'neutral')
    response_text = mental_health_response(mood)
    return response_text

@app.route('/chatbot', methods=['POST'])
def chatbot():
    user_msg = request.form.get('msg', '').lower()
    
    # Intent-based responses with external API integration
    if 'weather' in user_msg or 'climate' in user_msg:
        advice = get_weather_health_advice()
        return f"🌤️ {advice}"
    
    elif 'covid' in user_msg or 'corona' in user_msg:
        try:
            resp = requests.get('https://disease.sh/v3/covid-19/all', timeout=3)
            data = resp.json()
            return f"🦠 Global COVID-19: {data.get('cases', 'N/A'):,} cases, {data.get('deaths', 'N/A'):,} deaths, {data.get('recovered', 'N/A'):,} recovered. Stay safe!"
        except:
            return "COVID data temporarily unavailable. Please check WHO website."
    
    elif 'symptom' in user_msg or 'sick' in user_msg:
        return "🤒 Common symptoms: fever, cough, fatigue, headache, nausea, sore throat. Use our symptom checker for AI diagnosis."
    
    elif 'mental' in user_msg or 'stress' in user_msg or 'anxiety' in user_msg:
        return "🧠 Take care of your mental health! Try deep breathing, talk to someone, or use our mood tracker above. You're not alone."
    
    elif 'report' in user_msg or 'pdf' in user_msg:
        return "📄 You can download your health report as PDF from the results page using the 'Download Report' button."
    
    elif 'blockchain' in user_msg:
        return "🔗 Your health records are secured on an immutable blockchain. Visit the Blockchain Records page to view the chain."
    
    else:
        return "💡 I'm MediScan AI Assistant. Ask me about symptoms, COVID stats, weather health tips, mental health, or blockchain records!"
    
@app.route('/blockchain')
def view_blockchain():
    username = session.get('username', 'Guest')
    # Filter chain for current user (startup feature)
    user_blocks = [block for block in blockchain.get_chain() 
                  if isinstance(block.data, dict) and block.data.get('user') == username]
    
    # Also include genesis block info
    full_chain = blockchain.get_chain()
    
    return render_template('blockchain.html', 
                         user_blocks=user_blocks,
                         all_blocks=full_chain,
                         username=username)

@app.route('/download')
def download_report():
    last_pred = session.get('last_prediction')
    if not last_pred:
        return "No prediction found. Please run a diagnosis first.", 400
    
    filepath = generate_report(
        prediction=last_pred['prediction'],
        risk=last_pred['risk'],
        confidence=last_pred['confidence'],
        advice=last_pred['advice'],
        symptoms=last_pred.get('symptoms', {}),
        future_persona=future_persona(last_pred['risk'])
    )
    return send_file(filepath, as_attachment=True)

@app.route('/api/symptom-radar')
def symptom_radar_data():
    """API endpoint for radar chart data (used in result page)"""
    last_pred = session.get('last_prediction', {})
    symptoms = last_pred.get('symptoms', {})
    return jsonify(symptoms)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)