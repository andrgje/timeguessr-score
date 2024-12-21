import json

def create_table(result):
    max = 0
    for data in result:
        if len(str(data[0]))> max:
            max = len(str(data[0]))

    table = '\n| Place |   Name' + (max-6)*' '+ ' | Score |   Date    |'
    for i,data in enumerate(result): 
        table = table + '\n' + '|  ' + str(i+1) + (4-len(str(i+1)))*' '+' | ' + str(data[0]) + ' | ' + str(data[1]) + ' | ' + str(data[2])[:2]+'/'+str(data[2])[2:4]+'/'+str(data[2])[5:] + ' |'

    return table



def generate_leaderboard_card(title,rows):
    """
    Generates an Adaptive Card JSON for a leaderboard based on input rows.

    Args:
        rows (list of tuples): A list of tuples where each tuple represents a row 
                               in the leaderboard in the format (Place, Name, Score, Date).
    
    Returns:
        str: The JSON string of the Adaptive Card.
    """
    # Table header definition
    card = {
        "type": "AdaptiveCard",
        "version": "1.2",
        "body": [
            {
                "type": "TextBlock",
                "text": f"{title}",
                "weight": "Bolder",
                "size": "Medium",
                "wrap": True,
                "horizontalAlignment": "Center"
            },
            {
                "type": "Table",
                "columns": [
                    {"width": "25px"},
                    {"width": "150px"},
                    {"width": "55px"},
                    {"width": "80git px"}
                ],
                "rows": []
            }
        ],
        "$schema": "http://adaptivecards.io/schemas/adaptive-card.json"
    }
    
    # Add the header row
    header_row = {
        "type": "TableRow",
        "style": "emphasis",
        "cells": [
            {"type": "TableCell", "items": [{"type": "TextBlock", "text": "Place", "weight": "Bolder", "wrap": True}]},
            {"type": "TableCell", "items": [{"type": "TextBlock", "text": "Name", "weight": "Bolder", "wrap": True}]},
            {"type": "TableCell", "items": [{"type": "TextBlock", "text": "Score", "weight": "Bolder", "wrap": True}]},
            {"type": "TableCell", "items": [{"type": "TextBlock", "text": "Date", "weight": "Bolder", "spacing":"None","wrap": True}]}
        ]
    }
    card["body"][1]["rows"].append(header_row)
    
    # Add rows dynamically from input
    for place, name, score, date in rows:
        row = {
            "type": "TableRow", 
            "cells": [
                {"type": "TableCell", "items": [{"type": "TextBlock", "text": str(place), "wrap": True}]},
                {"type": "TableCell", "items": [{"type": "TextBlock", "text": name, "wrap": True}]},
                {"type": "TableCell", "items": [{"type": "TextBlock", "text": str(score), "horizontalAlignment": "Center", "wrap": True}]},
                {"type": "TableCell", "items": [{"type": "TextBlock", "text": str(date), "spacing":"None", "wrap": True}]}
            ]
        }
        card["body"][1]["rows"].append(row)
    
    return json.dumps(card, indent=2)