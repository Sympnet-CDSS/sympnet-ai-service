from typing import List, Dict
import random

class HypothesisAgent:
    """Agent de génération d'hypothèses diagnostiques"""
    
    def __init__(self, verbose: bool = True):
        self.verbose = verbose
        self.diagnostic_rules = self._init_diagnostic_rules()
        if verbose:
            print("✅ HypothesisAgent initialized")
    
    def _init_diagnostic_rules(self):
        return [
            {
                "diagnosis": "PNEUMONIE",
                "symptoms": ["FIÈVRE", "TOUX", "DIFFICULTÉ RESPIRATOIRE", "DOULEUR THORACIQUE", "TOUX GRASSE"],
                "base_score": 0.85,
                "explanation": "Infection pulmonaire avec signes respiratoires et fièvre",
                "recommendations": [
                    "Radiographie pulmonaire",
                    "NFS et CRP",
                    "Antibiothérapie adaptée",
                    "Surveillance de la saturation en oxygène",
                    "Consultation pneumologique si nécessaire"
                ]
            },
            {
                "diagnosis": "BRONCHITE AIGUË",
                "symptoms": ["TOUX", "TOUX GRASSE", "FIÈVRE", "COURBATURES"],
                "base_score": 0.70,
                "explanation": "Inflammation des bronches avec toux productive",
                "recommendations": [
                    "Repos et hydratation",
                    "Traitement symptomatique",
                    "Éviter les irritants",
                    "Consultation si persistance > 3 semaines"
                ]
            },
            {
                "diagnosis": "GRIPPE",
                "symptoms": ["FIÈVRE", "COURBATURES", "MAUX DE TÊTE", "FATIGUE", "TOUX SÈCHE"],
                "base_score": 0.80,
                "explanation": "Infection virale saisonnière",
                "recommendations": [
                    "Repos au domicile",
                    "Antipyrétiques",
                    "Hydratation abondante",
                    "Isolement pour éviter la contagion",
                    "Consultation si signes de gravité"
                ]
            },
            {
                "diagnosis": "COVID-19",
                "symptoms": ["FIÈVRE", "TOUX SÈCHE", "FATIGUE", "PERTE GOÛT", "PERTE ODORAT"],
                "base_score": 0.75,
                "explanation": "Infection virale respiratoire (SARS-CoV-2)",
                "recommendations": [
                    "Test PCR ou antigénique",
                    "Isolement",
                    "Surveillance de la saturation",
                    "Consultation téléphonique",
                    "Traitement symptomatique"
                ]
            },
            {
                "diagnosis": "GASTRO-ENTÉRITE",
                "symptoms": ["NAUSÉES", "VOMISSEMENTS", "DIARRHÉE", "DOULEUR ABDOMINALE"],
                "base_score": 0.78,
                "explanation": "Inflammation du tube digestif",
                "recommendations": [
                    "Réhydratation orale",
                    "Régime adapté",
                    "Repos digestif",
                    "Consultation si signes de déshydratation"
                ]
            },
            {
                "diagnosis": "MIGRAINE",
                "symptoms": ["MAUX DE TÊTE", "NAUSÉES"],
                "base_score": 0.65,
                "explanation": "Céphalée pulsatile unilatérale",
                "recommendations": [
                    "Repos au calme dans l'obscurité",
                    "Antalgiques",
                    "Hydratation",
                    "Consulter si fréquence > 2/semaine"
                ]
            },
            {
                "diagnosis": "RHINOPHARYNGITE",
                "symptoms": ["NEZ QUI COULE", "MAL DE GORGE", "TOUX", "FATIGUE"],
                "base_score": 0.60,
                "explanation": "Infection virale des voies respiratoires supérieures",
                "recommendations": [
                    "Repos",
                    "Hydratation",
                    "Lavages de nez",
                    "Traitement symptomatique"
                ]
            }
        ]
    
    def generate_hypotheses(self, symptoms: List[str], top_k: int = 5) -> List[Dict]:
        symptom_names = [s.upper() if isinstance(s, str) else s.get("name", "").upper() for s in symptoms]
        hypotheses = []
        
        for rule in self.diagnostic_rules:
            match_count = sum(1 for s in rule["symptoms"] if s in symptom_names)
            score = rule["base_score"] * (match_count / max(len(rule["symptoms"]), 1))
            score = max(0.1, min(0.95, score + random.uniform(-0.05, 0.05)))
            
            if score > 0.3:
                hypotheses.append({
                    "diagnosis": rule["diagnosis"],
                    "confidence": round(score, 3),
                    "score": round(score, 3),
                    "explanation": rule["explanation"],
                    "supporting_evidence": [s for s in rule["symptoms"] if s in symptom_names],
                    "recommendations": rule["recommendations"]
                })
        
        hypotheses.sort(key=lambda x: x["score"], reverse=True)
        return hypotheses[:top_k]