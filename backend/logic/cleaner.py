import pandas as pd
import numpy as np

def clean_data(df):
    # 1. Handle Missing Values - Objective 2
    # Fills numeric gaps with the mean and categorical gaps with 'Unknown'
    for col in df.columns:
        if df[col].dtype in ['int64', 'float64']:
            df[col] = df[col].fillna(df[col].mean())
        else:
            df[col] = df[col].fillna("Unknown")
            
    # 2. Outlier Detection (Heuristic Rules) - Objective 2
    # Uses the Interquartile Range (IQR) to flag potential data errors
    outliers = {}
    for col in df.select_dtypes(include=[np.number]).columns:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        count = ((df[col] < (Q1 - 1.5 * IQR)) | (df[col] > (Q3 + 1.5 * IQR))).sum()
        outliers[col] = int(count)
        
    return df, outliers