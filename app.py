from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Optional
import uvicorn
import os
import tempfile
from datetime import datetime
import logging

# Import agents
from agents.symptom_agent import SymptomAgent
from agents.hypothesis_agent import HypothesisAgent
from agents.validator_agent import ValidatorAgent
from agents.xai_agent import XAIAgent
from agents.confidence_agent import ConfidenceAgent
from utils.speech_recognition import SpeechRecognizer

# Configuration logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI
app = FastAPI(
    title="SympNet AI Multi-Agent Service",
    description="Système d'Aide à la Décision Médicale avec IA Multi-Agents",
    version="2.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize agents
logger.info("Initializing AI Agents...")
symptom_agent = SymptomAgent(verbose=True)
hypothesis_agent = HypothesisAgent(verbose=True)
validator_agent = ValidatorAgent(verbose=True)
xai_agent = XAIAgent(verbose=True)
confidence_agent = ConfidenceAgent(verbose=True)
speech_recognizer = SpeechRecognizer()
logger.info("All agents initialized successfully")

# Pydantic models
class SymptomAnalysisRequest(BaseModel):
    text: str
    language: str = "fr"

class SymptomAnalysisResponse(BaseModel):
    symptoms: List[Dict]
    text: str
    metadata: Dict

class DiagnosisRequest(BaseModel):
    symptoms: List[str] = []
    patient_text: Optional[str] = None

class DiagnosisResponse(BaseModel):
    hypotheses: List[Dict]
    confidence_scores: Dict
    validation_results: List[Dict]
    recommendations: List[str]
    processing_time: float

class VoiceDiagnoseResponse(BaseModel):
    transcribed_text: str
    symptoms: List[Dict]
    diagnosis: Dict

# Routes
@app.get("/")
async def root():
    return {
        "service": "SympNet AI Multi-Agent Service",
        "version": "2.0.0",
        "status": "running",
        "agents": ["symptom", "hypothesis", "validator", "xai", "confidence"],
        "endpoints": [
            "/analyze-symptoms",
            "/diagnose",
            "/voice-to-text",
            "/voice-diagnose",
            "/health"
        ]
    }

@app.get("/health")
async def health():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.post("/analyze-symptoms", response_model=SymptomAnalysisResponse)
async def analyze_symptoms(request: SymptomAnalysisRequest):
    """Analyse un texte pour extraire les symptômes"""
    try:
        result = symptom_agent.extract_from_text(request.text)
        return SymptomAnalysisResponse(
            symptoms=result["symptoms"],
            text=result["text"],
            metadata=result["metadata"]
        )
    except Exception as e:
        logger.error(f"Error in analyze_symptoms: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/diagnose", response_model=DiagnosisResponse)
async def diagnose(request: DiagnosisRequest):
    """Diagnostic complet multi-agents"""
    import time
    start_time = time.time()
    
    try:
        # 1. Extraire symptômes si texte fourni
        symptoms = request.symptoms
        if request.patient_text and not symptoms:
            extraction = symptom_agent.extract_from_text(request.patient_text)
            symptoms = [s["symptom"] for s in extraction["symptoms"]]
        
        logger.info(f"Symptoms detected: {symptoms}")
        
        # 2. Générer hypothèses
        hypotheses = hypothesis_agent.generate_hypotheses(symptoms, top_k=5)
        logger.info(f"Generated {len(hypotheses)} hypotheses")
        
        # 3. Valider hypothèses
        validated_hypotheses = validator_agent.validate_hypotheses(hypotheses)
        
        # 4. Calculer scores de confiance
        confidence_scores = confidence_agent.compute_confidence_score(
            hypothesis_probs={h["diagnosis"]: h["confidence"] for h in validated_hypotheses[:3]},
            validation_scores={h["diagnosis"]: h.get("validation_score", 0.5) for h in validated_hypotheses[:3]},
            xai_scores={},
            symptoms_count=len(symptoms)
        )
        
        # 5. Générer recommandations
        recommendations = []
        top_diagnosis = validated_hypotheses[0] if validated_hypotheses else None
        if top_diagnosis and "recommendations" in top_diagnosis:
            recommendations = top_diagnosis["recommendations"][:5]
        
        processing_time = time.time() - start_time
        logger.info(f"Diagnosis completed in {processing_time:.3f}s")
        
        return DiagnosisResponse(
            hypotheses=validated_hypotheses[:5],
            confidence_scores=confidence_scores,
            validation_results=validator_agent.get_validation_results() if hasattr(validator_agent, 'get_validation_results') else [],
            recommendations=recommendations,
            processing_time=round(processing_time, 3)
        )
        
    except Exception as e:
        logger.error(f"Error in diagnose: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/voice-to-text")
async def voice_to_text(audio: UploadFile = File(...)):
    """Convertit un fichier audio en texte"""
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            content = await audio.read()
            tmp.write(content)
            tmp_path = tmp.name
        
        text = speech_recognizer.transcribe(tmp_path, language="fr-FR")
        os.unlink(tmp_path)
        
        return {"text": text, "success": True}
        
    except Exception as e:
        logger.error(f"Error in voice-to-text: {e}")
        return {"text": "", "success": False, "error": str(e)}

@app.post("/voice-diagnose")
async def voice_diagnose(audio: UploadFile = File(...)):
    """Diagnostic à partir d'un fichier audio"""
    import time
    start_time = time.time()
    
    try:
        # Transcrire
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            content = await audio.read()
            tmp.write(content)
            tmp_path = tmp.name
        
        text = speech_recognizer.transcribe(tmp_path, language="fr-FR")
        os.unlink(tmp_path)
        
        # Analyser
        extraction = symptom_agent.extract_from_text(text)
        symptoms = [s["symptom"] for s in extraction["symptoms"]]
        
        # Générer hypothèses
        hypotheses = hypothesis_agent.generate_hypotheses(symptoms, top_k=5)
        validated_hypotheses = validator_agent.validate_hypotheses(hypotheses)
        
        # Calculer confiance
        confidence_scores = confidence_agent.compute_confidence_score(
            hypothesis_probs={h["diagnosis"]: h["confidence"] for h in validated_hypotheses[:3]},
            validation_scores={h["diagnosis"]: h.get("validation_score", 0.5) for h in validated_hypotheses[:3]},
            xai_scores={},
            symptoms_count=len(symptoms)
        )
        
        processing_time = time.time() - start_time
        
        return {
            "transcribed_text": text,
            "symptoms": extraction["symptoms"],
            "diagnosis": {
                "hypotheses": validated_hypotheses[:5],
                "confidence_scores": confidence_scores,
                "recommendations": validated_hypotheses[0]["recommendations"] if validated_hypotheses else [],
                "processing_time": round(processing_time, 3)
            }
        }
        
    except Exception as e:
        logger.error(f"Error in voice-diagnose: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    print("=" * 60)
    print("🚀 SympNet AI Multi-Agent Service")
    print("=" * 60)
    print("📍 Service démarré sur http://localhost:8000")
    print("📋 Documentation: http://localhost:8000/docs")
    print("=" * 60)
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)