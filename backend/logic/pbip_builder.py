import os
import json

def build_export_package(filename, artifacts, theme_json):
    project_name = filename.split('.')[0]
    folder_path = os.path.join('output_dashboard', project_name)
    os.makedirs(folder_path, exist_ok=True)
    
    # Save Power Query Script
    with open(os.path.join(folder_path, "Transform_Data.m"), "w") as f:
        f.write(artifacts['m_query'])
        
    # Save DAX Measures
    with open(os.path.join(folder_path, "Measures.dax"), "w") as f:
        f.write("\n".join(artifacts['dax']))
        
    # Save Theme JSON for Visual Branding
    with open(os.path.join(folder_path, "Theme.json"), "w") as f:
        f.write(theme_json)
        
    return folder_path