# Add the project root to the PYTHONPATH
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.model_loader import model, vect
from utils.feature_engineering import feature_transformation
from utils.encoders import prepare_features

print(model)