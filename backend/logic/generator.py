
import json

def generate_power_bi_artifacts(df_columns, filename):
    # 1. Power Query (M) Generator - Objective 4
    # This script allows the user to paste directly into the 'Advanced Editor'
    m_query = f"""
    let
        Source = Csv.Document(File.Contents("C:\\Data\\{filename}"),[Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.None]),
        #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
        #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers", {
            {", ".join([f'"{col}"' for col in df_columns])}
        })
    in
        #"Changed Type"
    """

    # 2. DAX Measure Generator - Objective 4
    # Generates standard business intelligence metrics
    dax_measures = []
    for col in df_columns:
        dax_measures.append(f"Total {col} = SUM('{filename.split('.')[0]}'[ {col} ])")
        dax_measures.append(f"Avg {col} = AVERAGE('{filename.split('.')[0]}'[ {col} ])")

    return {
        "m_query": m_query,
        "dax": dax_measures
    }