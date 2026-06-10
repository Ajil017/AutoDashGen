from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import os

# Import your custom logic modules
from logic.profiler import profile_data
from logic.recommender import recommend_visuals
from logic.generator import generate_power_bi_artifacts
from logic.theme_generator import generate_pbi_theme
from logic.cleaner import clean_data

app = Flask(__name__)
CORS(app)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# --- 1. DATA PROFILING MODULE ---
def profile_dataset(df):
    report = []
    for col in df.columns:
        dtype = str(df[col].dtype)
        if 'int' in dtype or 'float' in dtype:
            type_label = "Numeric"
        elif 'datetime' in dtype:
            type_label = "Date/Time"
        else:
            type_label = "Categorical"
        
        report.append({
            "column": col,
            "type": type_label,
            "missing": int(df[col].isnull().sum())
        })
    return report

# --- 2. SCRIPT GENERATOR (DAX & M-QUERY) ---
def generate_artifacts(df, filename, profile):
    # Generate Power Query (M) Code
    m_code = f'let\n    Source = Csv.Document(File.Contents("C:\\Users\\Public\\{filename}"),[Delimiter=",", Columns={len(df.columns)}, Encoding=65001, QuoteStyle=QuoteStyle.None]),\n    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true])\nin\n    #"Promoted Headers"'
    
    # Generate DAX Measures
    dax_measures = []
    for item in profile:
        if item['type'] == "Numeric":
            dax_measures.append(f"Total {item['column']} = SUM('{item['column']}')")
            dax_measures.append(f"Average {item['column']} = AVERAGE('{item['column']}')")
            
    return {"m_query": m_code, "dax": dax_measures}

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files['file']
    path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(path)
    
    # Process
    df = pd.read_csv(path)
    profile = profile_dataset(df)
    recommendations = recommend_visuals(profile)
    artifacts = generate_artifacts(df, file.filename, profile)
    
    return jsonify({
        "status": "success",
        "profile": profile,
        "recommendations": recommendations,
        "artifacts": artifacts
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)

    from logic.pbip_builder import create_pbip_structure

@app.route('/export/<filename>', methods=['GET'])
def export_dashboard(filename):
    # This route will wrap the generated scripts into the PBIP folder
    # In a real scenario, you'd pull the cached profile/artifacts
    project_name = filename.split('.')[0]
    output_dir = 'output_dashboard'
    os.makedirs(output_dir, exist_ok=True)
    
    # Mock data for demonstration - in production, this comes from the /upload state
    m_code = "Source = Csv.Document(...)" 
    dax = ["Total Sales = SUM(Sales)"]
    
    path = create_pbip_structure(project_name, output_dir, m_code, dax)
    
    return jsonify({"message": "Dashboard structure created", "path": path})


@app.route('/')
def home():
    return {"message": "AutoDashGen AI Engine is Live!", "status": "Ready"}

from logic.theme_generator import generate_pbi_theme

@app.route('/download-theme', methods=['GET'])
def download_theme():
    # Provides the Theme Configuration JSON [cite: 68]
    theme_json = generate_pbi_theme()
    return theme_json, 200, {'Content-Type': 'application/json', 'Content-Disposition': 'attachment; filename=theme.json'}