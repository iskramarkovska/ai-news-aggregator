from transformers import pipeline
import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer 
from functools import lru_cache


try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords', quiet=True)


@lru_cache(maxsize=1)
def get_summarizer():
    """
    Load and cache the summarization model.
    Using facebook/bart-large-cnn - trained for summarization.
    """

    try:
        summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
        return summarizer
    except Exception as e:
        print(f"Error loading summarization model: {e}")
        return None
    

def summarize_article(text, max_length=130, min_length=30):
    """
    Summarize article text using BART model.
    Returns a concise summary or None if it fails.
    """

    if not text or len(text.strip()) < 100:
        return None
    
    summarizer = get_summarizer()
    if not summarizer:
        return None

    try:
        max_input_length = 1024
        text = text[:max_input_length * 4]
        
        summary = summarizer(text, max_length=max_length, min_length=min_length, do_sample=False)
        return summary[0]['summary_text']
    
    except Exception as e:
        print(f"Error summarizing text: {e}")
        return None

def extract_keywords(text, num_keywords=5):
    """
    Extract top keywords from text using TF-IDF.
    Returns comma-seperated keywords or empty string if it fails.
    """
    if not text or len(text.strip()) < 50:
        return ''
    
    import re
    text = re.sub(r'\[\+\d+ chars?\]', '', text)
    text = re.sub(r'\d{3,}', '', text)
    
    try:
        stop_words = stopwords.words('english')
        custom_stop_words = [
            'chars', 'char', 'characters',
            '1000', '2000', '3000', '4000', '5000'
        ]
        stop_words = stop_words + custom_stop_words

        vectorizer = TfidfVectorizer(
            max_features=num_keywords,
            stop_words=stop_words,
            ngram_range=(1, 2)  # consider both single words and two-word phrases
        )
        # analyzes text and calculates TF-IDF scores
        # returns a matrix
        tfidf_matrix = vectorizer.fit_transform([text])
        feature_names = vectorizer.get_feature_names_out()

        keywords = list(feature_names)
        return ', '.join(keywords)
    
    except Exception as e:
        print(f"Error extracting keywords: {e}")
        return ''
    



