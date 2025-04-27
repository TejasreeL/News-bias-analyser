from transformers import pipeline
from textblob import TextBlob

# Load summarizer
summarizer = pipeline('summarization', model='facebook/bart-large-cnn')

def summarize(text):
    if len(text.split()) < 50:  # If text too short, don't summarize
        return text
    max_len = min(130, int(len(text.split()) * 0.8))  # adjust max_length
    summarized = summarizer(text, max_length=max_len, min_length=30, do_sample=False)[0]['summary_text']
    return summarized

def analyze_bias(text):
    blob = TextBlob(text)
    sentiment = blob.sentiment.polarity  # -1 (negative) to +1 (positive)
    subjectivity = blob.sentiment.subjectivity  # 0 (objective) to 1 (subjective)
    return sentiment, subjectivity

# sample = """The economy is booming according to government reports, but critics argue that the benefits are unevenly distributed."""
# print("SUMMARY:")
# print(summarize(sample))
# print("\nBIAS ANALYSIS:")
# print(analyze_bias(sample))