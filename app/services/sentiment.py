from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import numpy as np
from typing import Dict, Tuple, Union
import logging

logger = logging.getLogger(__name__)


class SentimentAnalyzer:
    def __init__(self):
        # Load pre-trained model and tokenizer
        self.model_name = "nlptown/bert-base-multilingual-uncased-sentiment"
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(self.model_name)
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)
        logger.info(f"Initialized sentiment analyzer with model: {self.model_name}")

    def analyze_sentiment(self, text: str) -> Dict[str, Union[float, Dict[str, float]]]:
        """
        Analyze the sentiment of the given text using BERT.
        Returns a dictionary with sentiment scores.
        """
        try:
            # Tokenize and prepare input
            inputs = self.tokenizer(
                text, return_tensors="pt", truncation=True, max_length=512, padding=True
            ).to(self.device)

            # Get model predictions
            with torch.no_grad():
                outputs = self.model(**inputs)
                scores = torch.softmax(outputs.logits, dim=1)
                scores = scores.cpu().numpy()[0]

            # Convert scores to sentiment metrics
            # The model outputs 5 classes (1-5 stars), we'll convert to a -1 to 1 scale
            sentiment_score = (np.sum(scores * np.array([1, 2, 3, 4, 5])) - 3) / 2

            # Calculate confidence
            confidence = float(np.max(scores))

            return {
                "sentiment_score": float(sentiment_score),
                "confidence": float(confidence),
                "raw_scores": {
                    "very_negative": float(scores[0]),
                    "negative": float(scores[1]),
                    "neutral": float(scores[2]),
                    "positive": float(scores[3]),
                    "very_positive": float(scores[4]),
                },
            }

        except Exception as e:
            logger.error(f"Error in sentiment analysis: {str(e)}")
            raise

    def get_sentiment_label(self, score: float) -> str:
        """
        Convert sentiment score to label.
        """
        if score < -0.5:
            return "very_negative"
        elif score < 0.0:
            return "negative"
        elif score < 0.5:
            return "neutral"
        elif score < 0.8:
            return "positive"
        else:
            return "very_positive"
