from typing import List, Dict, Optional

class XAIAgent:
    """Agent d'explicabilité"""
    
    def __init__(self, verbose: bool = True):
        self.verbose = verbose
        if verbose:
            print("✅ XAIAgent initialized")
    
    def explain_hypothesis(self, symptoms: List[str], hypothesis: Dict) -> Dict:
        """Génère des explications pour une hypothèse"""
        diagnosis = hypothesis.get("diagnosis", "Unknown")
        confidence = hypothesis.get("confidence", 0.5)
        
        explanations = {
            "hypothesis": diagnosis,
            "confidence": confidence,
            "key_factors": self._get_key_factors(symptoms, diagnosis),
            "alternative_considerations": self._get_alternatives(diagnosis),
            "recommended_actions": hypothesis.get("recommendations", [])[:3]
        }
        
        return explanations
    
    def _get_key_factors(self, symptoms: List[str], diagnosis: str) -> List[str]:
        factors = []
        
        # Mapping diagnostic -> symptômes clés
        key_symptoms_map = {
            "PNEUMONIE": ["FIÈVRE", "TOUX", "DIFFICULTÉ RESPIRATOIRE"],
            "GRIPPE": ["FIÈVRE", "COURBATURES", "FATIGUE"],
            "COVID-19": ["PERTE GOÛT", "PERTE ODORAT", "FIÈVRE"],
            "GASTRO-ENTÉRITE": ["NAUSÉES", "VOMISSEMENTS", "DIARRHÉE"],
            "BRONCHITE AIGUË": ["TOUX", "TOUX GRASSE"],
            "RHINOPHARYNGITE": ["NEZ QUI COULE", "MAL DE GORGE"]
        }
        
        key_symptoms = key_symptoms_map.get(diagnosis, [])
        for symptom in symptoms:
            if symptom.upper() in key_symptoms or symptom.upper() in [s.upper() for s in symptoms]:
                factors.append(f"Présence de {symptom.lower()}")
        
        if not factors:
            factors = ["Combinaison de symptômes caractéristiques"]
        
        return factors[:3]
    
    def _get_alternatives(self, diagnosis: str) -> List[str]:
        alternatives_map = {
            "PNEUMONIE": ["Bronchite aiguë", "Embolie pulmonaire", "Insuffisance cardiaque"],
            "GRIPPE": ["COVID-19", "Rhume", "Angine"],
            "COVID-19": ["Grippe", "Bronchite", "Pneumonie"],
            "GASTRO-ENTÉRITE": ["Intoxication alimentaire", "Appendicite", "Colite"],
            "BRONCHITE AIGUË": ["Pneumonie", "Asthme", "Rhume"],
            "RHINOPHARYNGITE": ["Grippe", "Allergies", "Sinusite"]
        }
        return alternatives_map.get(diagnosis, ["Autres diagnostics possibles"])