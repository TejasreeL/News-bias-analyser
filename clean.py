import re
import nltk
from nltk.corpus import stopwords

nltk.download('stopwords')

def clean_text(text):
    text = re.sub(r'\s+', ' ', text)  # remove extra spaces
    text = re.sub(r'\[[^\]]*\]', '', text)  # remove [text]
    text = re.sub(r'https?://\S+', '', text)  # remove URLs
    text = re.sub(r'[^A-Za-z0-9\s]', '', text)  # remove special chars
    words = text.lower().split()
    words = [word for word in words if word not in stopwords.words('english')]
    return ' '.join(words)

sample = "This is a test text!! Visit https://test.com for more [info]."
print(clean_text(sample))