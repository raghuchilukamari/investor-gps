from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from typing import Dict, List, Union
import numpy as np

class SentimentService:
    def __init__(self):
        self.vader = SentimentIntensityAnalyzer()
    
    def analyze_text(self, text: str) -> Dict[str, float]:
        """Analyze text using both TextBlob and VADER"""
        # TextBlob analysis
        blob = TextBlob(text)
        textblob_sentiment = blob.sentiment.polarity
        
        # VADER analysis
        vader_scores = self.vader.polarity_scores(text)
        
        # Combine scores (weighted average)
        combined_score = (textblob_sentiment + vader_scores['compound']) / 2
        
        return {
            "textblob_score": textblob_sentiment,
            "vader_score": vader_scores['compound'],
            "combined_score": combined_score,
            "vader_details": vader_scores
        }
    
    def get_sentiment_label(self, score: float) -> str:
        """Convert sentiment score to label"""
        if score >= 0.05:
            return "bullish"
        elif score <= -0.05:
            return "bearish"
        return "neutral"
    
    def analyze_texts(self, texts: List[str]) -> Dict[str, Union[float, str, Dict]]:
        """Analyze multiple texts and return aggregate sentiment"""
        if not texts:
            return {
                "sentiment_score": 0.0,
                "sentiment_label": "neutral",
                "confidence": 0.0,
                "sample_size": 0
            }
        
        scores = [self.analyze_text(text)["combined_score"] for text in texts]
        avg_score = np.mean(scores)
        std_score = np.std(scores)
        
        return {
            "sentiment_score": avg_score,
            "sentiment_label": self.get_sentiment_label(avg_score),
            "confidence": 1 - min(std_score, 1),  # Convert std to confidence
            "sample_size": len(texts)
        }
    
    def analyze_earnings_call(self, transcript: str) -> Dict[str, Union[float, str, Dict]]:
        """Analyze earnings call transcript"""
        # Split transcript into sentences
        blob = TextBlob(transcript)
        sentences = [str(sentence) for sentence in blob.sentences]
        
        # Analyze each sentence
        sentence_scores = [self.analyze_text(sentence)["combined_score"] for sentence in sentences]
        
        # Calculate statistics
        avg_score = np.mean(sentence_scores)
        std_score = np.std(sentence_scores)
        
        # Identify key topics and their sentiment
        topics = {}
        for sentence in sentences:
            blob = TextBlob(sentence)
            for noun in blob.noun_phrases:
                if noun not in topics:
                    topics[noun] = []
                topics[noun].append(self.analyze_text(sentence)["combined_score"])
        
        # Calculate topic sentiments
        topic_sentiments = {
            topic: np.mean(scores) 
            for topic, scores in topics.items() 
            if len(scores) >= 3  # Only include topics mentioned at least 3 times
        }
        
        return {
            "overall_sentiment": {
                "score": avg_score,
                "label": self.get_sentiment_label(avg_score),
                "confidence": 1 - min(std_score, 1)
            },
            "topic_sentiments": topic_sentiments,
            "sample_size": len(sentences)
        } 