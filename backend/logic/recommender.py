def recommend_visuals(profile):
    recommendations = []
    for col in profile:
        if col['type'] == "Numeric":
            recommendations.append({
                "chart": "Clustered Bar Chart",
                "insight": f"Analysis of {col['column']} shows significant variance. Use this to compare top performers.",
                "fields": {"values": col['column']}
            })
        elif col['type'] == "DateTime":
            recommendations.append({
                "chart": "Line Chart",
                "insight": "Time-series data detected. This chart identifies seasonal trends over time.",
                "fields": {"axis": col['column']}
            })
    return recommendations