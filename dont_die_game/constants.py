# Evidence and corresponding tools 
evidence_tool_map = {
    "EMF Level 5": "EMF Reader",
    "Spirit Box": "Spirit Box",
    "Fingerprints": "UV Light",
    "Ghost Writing": "Ghost Writing Book",
    "Freezing Temperatures": "Thermometer",
    "Ghost Orb": "Video Camera",
}

# Ghost types and their required evidence (3 evidences)
ghost_types = {
    "Spirit": ["EMF Level 5", "Spirit Box", "Ghost Writing"],
    "Banshee": ["Fingerprints", "EMF Level 5", "Spirit Box"],
    "Yokai": ["Fingerprints", "Ghost Orb", "Ghost Writing"],
    "Thaye": ["EMF Level 5", "Ghost Orb", "Freezing Temperatures"],
    "Demon": ["Freezing Temperatures", "Fingerprints", "Spirit Box"],
    "Yurei": ["Ghost Orb", "Ghost Writing", "Freezing Temperatures"],
}

# Tools list extracted from the evidence_tool_map
tools = []
for tool in evidence_tool_map.values():
    tools.append(tool)
