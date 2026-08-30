import os
import joblib
from pathlib import Path

# Get the absolute path to the project root directory
PROJECT_ROOT = Path(__file__).resolve().parent.parent
MODELS_DIR = PROJECT_ROOT / "models"

WESAD_MODEL_PATH = MODELS_DIR / "ExtraTreeWESADModel01.pkl"
MMASH_MODEL_PATH = MODELS_DIR / "MultiLayerPerceptron_MLP_MMASH_Model01.pkl"

def load_models():
    print(f"Looking for models in: {MODELS_DIR}")
    
    if not WESAD_MODEL_PATH.exists():
        raise FileNotFoundError(f"WESAD model file missing: {WESAD_MODEL_PATH}\nPlease place the model file in the 'models' directory.")
    
    if not MMASH_MODEL_PATH.exists():
        raise FileNotFoundError(f"MMASH model file missing: {MMASH_MODEL_PATH}\nPlease place the model file in the 'models' directory.")

    print("Loading WESAD model...")
    wesad_model = joblib.load(WESAD_MODEL_PATH)
    print(f"WESAD Model loaded. Type: {type(wesad_model)}")

    print("Loading MMASH model...")
    mmash_model = joblib.load(MMASH_MODEL_PATH)
    print(f"MMASH Model loaded. Type: {type(mmash_model)}")
    
    return wesad_model, mmash_model

if __name__ == "__main__":
    try:
        load_models()
        print("Models loaded successfully.")
    except Exception as e:
        print(f"Error loading models: {e}")
