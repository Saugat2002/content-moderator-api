from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import numpy as np
from typing import Dict, Union
import logging

logger = logging.getLogger(__name__)


class SentimentAnalyzer:
    def __init__(self):
        # Load pre-trained model and tokenizer
        self.model_name = "finiteautomata/bertweet-base-sentiment-analysis"
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(self.model_name)
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)
        logger.info(f"Initialized sentiment analyzer with model: {self.model_name}")

    def analyze_sentiment(
        self, text: str
    ) -> Dict[str, Union[float, Dict[str, float], str]]:
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

            # Map scores to sentiment categories (3 classes: negative, neutral, positive)
            sentiment_scores = {
                "negative": float(scores[0]),
                "neutral": float(scores[1]),
                "positive": float(scores[2]),
            }

            # Calculate overall sentiment score (-1 to 1)
            sentiment_score = scores[2] - scores[0]  # positive - negative

            # Get dominant emotion based on sentiment
            if sentiment_score < -0.5:
                dominant_emotion = "anger"
            elif sentiment_score < 0:
                dominant_emotion = "disappointment"
            elif sentiment_score < 0.5:
                dominant_emotion = "neutral"
            else:
                dominant_emotion = "joy"

            # Calculate confidence
            confidence = float(max(scores))

            return {
                "sentiment_score": float(sentiment_score),
                "confidence": float(confidence),
                "dominant_emotion": dominant_emotion,
                "raw_scores": sentiment_scores,
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
        elif score < -0.2:
            return "negative"
        elif score < 0.2:
            return "neutral"
        elif score < 0.5:
            return "positive"
        else:
            return "very_positive"
