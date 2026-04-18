from typing import List, Dict
import random

class ValidatorAgent:
    """Agent de validation clinique"""
    
    def __init__(self, verbose: bool = True):
        self.verbose = verbose
        self.validation_results = []
        if verbose:
            print("✅ ValidatorAgent initialized")
    
    def validate_hypotheses(self, hypotheses: List[Dict]) -> List[Dict]:
        validated = []
        self.validation_results = []
        
        for hyp in hypotheses:
            # Score de validation basé sur plusieurs facteurs
            base_score = hyp.get("score", 0.5)
            
            # Ajustement selon le nombre de symptômes supportants
            evidence_count = len(hyp.get("supporting_evidence", []))
            evidence_factor = min(0.3, evidence_count * 0.05)
            
            validation_score = min(0.95, base_score + evidence_factor)
            
            validated_hyp = hyp.copy()
            validated_hyp["validation_score"] = round(validation_score, 3)
            validated_hyp["is_validated"] = validation_score > 0.5
            
            self.validation_results.append({
                "diagnosis": hyp["diagnosis"],
                "validation_score": validation_score,
                "is_validated": validation_score > 0.5
            })
            
            validated.append(validated_hyp)
        
        return validated
    
    def get_validation_results(self) -> List[Dict]:
        return self.validation_results