# Zap Filter Service

Lightweight Flask-based microservice deployed on Render.  
Receives JSON input from Zapier (title + description) and returns a simple relevance flag based on property movement keywords.  
This keeps filtering logic centralised across multiple Zaps — update the keyword list here, redeploy automatically via GitHub.

**Endpoint:** `/evaluate`  
**Method:** POST  
**Input:** 
{
  "title": "CBRE relocates HQ",
  "description": "Moves 200 staff into Broadgate Tower"
}
**Output:**
{
  "isRelevant": true
}

Built for the SkyLearn lead-generation system.
