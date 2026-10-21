"""Simple file-based storage for research history and analytics"""
import json
import os
from datetime import datetime
from typing import List, Dict, Optional
from pathlib import Path

STORAGE_DIR = Path("app/database/data")
STORAGE_DIR.mkdir(parents=True, exist_ok=True)

HISTORY_FILE = STORAGE_DIR / "research_history.json"
SETTINGS_FILE = STORAGE_DIR / "settings.json"


class ResearchHistory:
    """Manage research history and analytics"""
    
    @staticmethod
    def add_research(result: Dict) -> None:
        """Add a research result to history"""
        history = ResearchHistory.get_all()
        
        # Create entry
        entry = {
            "id": result.get("id"),
            "timestamp": datetime.now().isoformat(),
            "company_name": result.get("company", {}).get("name"),
            "company_url": result.get("company", {}).get("url"),
            "industry": result.get("company", {}).get("industry"),
            "location": result.get("company", {}).get("location"),
            "intent_score": result.get("intent_score", {}).get("overall", 0),
            "recommendation": result.get("intent_score", {}).get("recommendation"),
            "research_time": result.get("metadata", {}).get("research_time_seconds", 0),
            "cost": result.get("metadata", {}).get("cost_usd", 0.0),
        }
        
        history.append(entry)
        
        # Save
        with open(HISTORY_FILE, 'w') as f:
            json.dump(history, f, indent=2)
    
    @staticmethod
    def get_all() -> List[Dict]:
        """Get all research history"""
        if not HISTORY_FILE.exists():
            return []
        
        try:
            with open(HISTORY_FILE, 'r') as f:
                return json.load(f)
        except:
            return []
    
    @staticmethod
    def get_recent(limit: int = 10) -> List[Dict]:
        """Get recent researches"""
        history = ResearchHistory.get_all()
        return sorted(history, key=lambda x: x['timestamp'], reverse=True)[:limit]
    
    @staticmethod
    def get_analytics() -> Dict:
        """Get analytics summary"""
        history = ResearchHistory.get_all()
        
        if not history:
            return {
                "total_researches": 0,
                "avg_intent_score": 0,
                "high_priority_count": 0,
                "total_cost": 0.0,
                "total_time": 0,
                "top_industries": []
            }
        
        # Calculate metrics
        scores = [h['intent_score'] for h in history if h.get('intent_score')]
        high_priority = [h for h in history if h.get('intent_score', 0) >= 80]
        
        # Industry breakdown
        industries = {}
        for h in history:
            ind = h.get('industry') or 'Unknown'
            industries[ind] = industries.get(ind, 0) + 1
        
        top_industries = sorted(
            [{"industry": k, "count": v} for k, v in industries.items()],
            key=lambda x: x['count'],
            reverse=True
        )[:5]
        
        return {
            "total_researches": len(history),
            "avg_intent_score": round(sum(scores) / len(scores), 1) if scores else 0,
            "high_priority_count": len(high_priority),
            "total_cost": round(sum(h.get('cost', 0) for h in history), 4),
            "total_time": sum(h.get('research_time', 0) for h in history),
            "top_industries": top_industries
        }


class Settings:
    """Manage application settings"""
    
    @staticmethod
    def get() -> Dict:
        """Get current settings"""
        if not SETTINGS_FILE.exists():
            return {
                "research_depth": "standard",
                "discovery_limit": 10,
                "email": "user@example.com"
            }
        
        try:
            with open(SETTINGS_FILE, 'r') as f:
                return json.load(f)
        except:
            return {}
    
    @staticmethod
    def update(settings: Dict) -> None:
        """Update settings"""
        current = Settings.get()
        current.update(settings)
        
        with open(SETTINGS_FILE, 'w') as f:
            json.dump(current, f, indent=2)


class UsageTracking:
    """Track API usage"""
    
    @staticmethod
    def get_usage() -> Dict:
        """Get current month usage"""
        history = ResearchHistory.get_all()
        
        # Filter current month
        now = datetime.now()
        current_month = [
            h for h in history 
            if datetime.fromisoformat(h['timestamp']).month == now.month
            and datetime.fromisoformat(h['timestamp']).year == now.year
        ]
        
        return {
            "api_calls": len(current_month),
            "limit": 1000,  # Free tier limit
            "percentage": round((len(current_month) / 1000) * 100, 1)
        }
