import json  # Add this line at the very top

def generate_pbi_theme():
    theme = {
        "name": "AutoDashGen Default",
        "visualStyles": {
            "*": {
                "*": {
                    "background": [{"show": True, "transparency": 0}],
                    "visualTooltip": [{"type": "Default"}]
                }
            }
        }
    }
    return json.dumps(theme, indent=4)

import json

def generate_theme():
    # Defines the visual schema for the Power BI Dashboard Output
    theme_data = {
        "name": "AutoDashGen_Professional",
        "dataColors": ["#118DFF", "#12239E", "#E66C37", "#6B007B", "#E044A7"],
        "visualStyles": {
            "*": {
                "*": {
                    "background": [{"show": True, "transparency": 0}],
                    "border": [{"show": True}]
                }
            }
        }
    }
    return json.dumps(theme_data, indent=4)