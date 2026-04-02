from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from datetime import datetime

def generate_report(prediction, risk, confidence, advice, symptoms, future_persona):
    file_path = "health_report.pdf"
    
    doc = SimpleDocTemplate(file_path, pagesize=letter)
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle('CustomTitle', parent=styles['Title'], fontSize=24, textColor=colors.HexColor('#667eea'))
    heading_style = ParagraphStyle('Heading', parent=styles['Heading2'], fontSize=16, textColor=colors.HexColor('#764ba2'))
    
    content = []
    
    # Header
    content.append(Paragraph("MediScan AI+ Health Report", title_style))
    content.append(Paragraph(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal']))
    content.append(Spacer(1, 20))
    
    # Diagnosis Summary
    content.append(Paragraph("Diagnosis Summary", heading_style))
    content.append(Paragraph(f"<b>Predicted Disease:</b> {prediction}", styles['Normal']))
    content.append(Paragraph(f"<b>Confidence Score:</b> {confidence}%", styles['Normal']))
    content.append(Paragraph(f"<b>Risk Level:</b> {risk}", styles['Normal']))
    content.append(Spacer(1, 10))
    
    # Symptoms
    content.append(Paragraph("Symptoms Reported", heading_style))
    symptom_text = ", ".join([f"{s.replace('_', ' ').title()}" for s, v in symptoms.items() if v > 0])
    content.append(Paragraph(symptom_text if symptom_text else "No symptoms reported", styles['Normal']))
    content.append(Spacer(1, 10))
    
    # Medical Advice
    content.append(Paragraph("Medical Advice", heading_style))
    content.append(Paragraph(advice, styles['Normal']))
    content.append(Spacer(1, 10))
    
    # Future Projection
    content.append(Paragraph("Health Outlook", heading_style))
    content.append(Paragraph(f"<b>If Ignored:</b> {future_persona['bad']}", styles['Normal']))
    content.append(Paragraph(f"<b>If Treated:</b> {future_persona['good']}", styles['Normal']))
    content.append(Spacer(1, 20))
    
    # Footer
    content.append(Paragraph("This report is AI-generated and should not replace professional medical advice.", 
                           ParagraphStyle('Footer', parent=styles['Italic'], fontSize=8, textColor=colors.grey)))
    
    doc.build(content)
    return file_path