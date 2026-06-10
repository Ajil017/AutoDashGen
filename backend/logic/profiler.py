import pandas as pd

def profile_data(filepath):
    df = pd.read_csv(filepath)
    profile = {
        "columns": [],
        "summary": df.describe(include='all').to_dict()
    }
    
    for col in df.columns:
        dtype = str(df[col].dtype)
        # Logic to map Python types to Power BI categories
        bi_type = "Categorical"
        if "int" in dtype or "float" in dtype:
            bi_type = "Numeric"
        elif "datetime" in dtype or "date" in dtype:
            bi_type = "Date"
            
        profile["columns"].append({"name": col, "type": bi_type})
    
    return profile