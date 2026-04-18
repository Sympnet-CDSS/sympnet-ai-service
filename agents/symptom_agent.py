import re
from typing import List, Dict, Optional
import random

class SymptomAgent:
    """Agent d'extraction de symptômes"""
    
    def __init__(self, verbose: bool = True):
        self.verbose = verbose
        self.symptom_db = self._init_symptom_db()
        if verbose:
            print("✅ SymptomAgent initialized")
    
    def _init_symptom_db(self):
        return [
            {"name": "FIÈVRE", "patterns": ["fievre", "fièvre", "fever", "température", "38", "39", "40"], "type": "CONSTITUTIONAL", "severity": "HIGH"},
            {"name": "TOUX", "patterns": ["toux", "cough", "tousse"], "type": "RESPIRATORY", "severity": "MEDIUM"},
            {"name": "TOUX GRASSE", "patterns": ["toux grasse", "productive", "expectorations", "crachats"], "type": "RESPIRATORY", "severity": "MEDIUM"},
            {"name": "TOUX SÈCHE", "patterns": ["toux sèche", "dry cough", "non-productive"], "type": "RESPIRATORY", "severity": "MEDIUM"},
            {"name": "DIFFICULTÉ RESPIRATOIRE", "patterns": ["difficulté respirer", "essoufflement", "dyspnée", "shortness of breath"], "type": "RESPIRATORY", "severity": "HIGH"},
            {"name": "DOULEUR THORACIQUE", "patterns": ["douleur thoracique", "chest pain", "poitrine"], "type": "CARDIOVASCULAR", "severity": "HIGH"},
            {"name": "MAUX DE TÊTE", "patterns": ["mal de tête", "migraine", "headache", "céphalée"], "type": "NEUROLOGICAL", "severity": "MEDIUM"},
            {"name": "FATIGUE", "patterns": ["fatigue", "fatigué", "épuisé", "tired", "weakness"], "type": "CONSTITUTIONAL", "severity": "LOW"},
            {"name": "NAUSÉES", "patterns": ["nausée", "nausea", "mal au cœur"], "type": "GASTROINTESTINAL", "severity": "LOW"},
            {"name": "VOMISSEMENTS", "patterns": ["vomissement", "vomiting", "vomi"], "type": "GASTROINTESTINAL", "severity": "MEDIUM"},
            {"name": "DIARRHÉE", "patterns": ["diarrhée", "diarrhea", "selles liquides"], "type": "GASTROINTESTINAL", "severity": "MEDIUM"},
            {"name": "DOULEUR ABDOMINALE", "patterns": ["douleur abdominale", "mal au ventre", "stomach pain"], "type": "GASTROINTESTINAL", "severity": "MEDIUM"},
            {"name": "COURBATURES", "patterns": ["courbatures", "myalgie", "muscle pain", "body aches"], "type": "MUSCULOSKELETAL", "severity": "LOW"},
            {"name": "FRISSONS", "patterns": ["frissons", "chills", "frissonne"], "type": "CONSTITUTIONAL", "severity": "LOW"},
            {"name": "PERTE GOÛT", "patterns": ["perte goût", "agueusie", "loss of taste"], "type": "NEUROLOGICAL", "severity": "MEDIUM"},
            {"name": "PERTE ODORAT", "patterns": ["perte odorat", "anosmie", "loss of smell"], "type": "NEUROLOGICAL", "severity": "MEDIUM"},
            {"name": "MAL DE GORGE", "patterns": ["mal de gorge", "gorge irritée", "sore throat"], "type": "ENT", "severity": "LOW"},
            {"name": "NEZ QUI COULE", "patterns": ["nez qui coule", "rhinorrhée", "runny nose"], "type": "ENT", "severity": "LOW"},
        ]
    
    def extract_symptoms(self, text: str) -> List[Dict]:
        text_lower = text.lower()
        found_symptoms = []
        
        for symptom in self.symptom_db:
            for pattern in symptom["patterns"]:
                if pattern in text_lower:
                    found_symptoms.append({
                        "symptom": symptom["name"],
                        "type": symptom["type"],
                        "severity": symptom["severity"],
                        "confidence": round(random.uniform(0.7, 0.95), 3),
                        "source": "keyword_match"
                    })
                    break
        
        # Dédupliquer
        unique = []
        seen = set()
        for s in found_symptoms:
            if s["symptom"] not in seen:
                unique.append(s)
                seen.add(s["symptom"])
        
        return unique
    
    def extract_from_text(self, text: str) -> Dict:
        symptoms = self.extract_symptoms(text)
        return {
            "text": text,
            "symptoms": symptoms,
            "metadata": {
                "total_symptoms": len(symptoms),
                "methods_used": ["keyword_match"],
                "severity_levels": list(set(s["severity"] for s in symptoms))
            }
        }