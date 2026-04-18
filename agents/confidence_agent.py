from typing import Dict, List
import numpy as np

class ConfidenceAgent:
    """Agent de calcul de scores de confiance"""
    
    def __init__(self, verbose: bool = True):
        self.verbose = verbose
        if verbose:
            print("✅ ConfidenceAgent initialized")
    
    def compute_confidence_score(self, 
                                hypothesis_probs: Dict[str, float],
                                validation_scores: Dict[str, float],
                                xai_scores: Dict[str, float],
                                symptoms_count: int = 0) -> Dict:
        """
        Calcule un score de confiance composite
        """
        # 1. Incertitude épistémique
        if hypothesis_probs:
            max_prob = max(hypothesis_probs.values())
            epistemic_uncertainty = 1 - max_prob
        else:
            max_prob = 0.5
            epistemic_uncertainty = 0.5
        
        # 2. Score de validation clinique
        if validation_scores:
            clinical_consistency = np.mean(list(validation_scores.values()))
        else:
            clinical_consistency = 0.5
        
        # 3. Score d'explicabilité
        if xai_scores:
            explainability_score = np.mean(list(xai_scores.values()))
        else:
            explainability_score = 0.6
        
        # 4. Facteur de richesse symptomatique
        symptom_richness = min(0.9, symptoms_count / 10)
        
        # 5. Score composite
        composite_score = (
            (1 - epistemic_uncertainty) * 0.4 +
            clinical_consistency * 0.3 +
            explainability_score * 0.2 +
            symptom_richness * 0.1
        )
        
        # Normaliser entre 0.2 et 0.95
        composite_score = max(0.2, min(composite_score, 0.95))
        
        # Niveau de confiance
        if composite_score >= 0.8:
            confidence_level = "HIGH"
        elif composite_score >= 0.6:
            confidence_level = "MEDIUM"
        else:
            confidence_level = "LOW"
        
        return {
            "overall_confidence": round(composite_score, 3),
            "confidence_level": confidence_level,
            "epistemic_uncertainty": round(epistemic_uncertainty, 3),
            "clinical_consistency": round(clinical_consistency, 3),
            "explainability_score": round(explainability_score, 3),
            "symptom_richness": round(symptom_richness, 3),
            "top_hypothesis_prob": round(max_prob, 3)
        }