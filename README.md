# News-bias-analyser
This project implements an **NLP-powered dashboard** to analyze and compare bias in news articles from **BBC, CNN, and FOX News**. It scrapes headlines, summarizes content, and uses sentiment analysis, subjectivity scoring, and keyword inspection to uncover potential bias.

## Key Features
- Scrapes real-time news articles using **Google SERP API**
- Summarizes articles using **facebook/bart-large-cnn**
- Identifies **biased words**
- Analyzes **sentiment** and **subjectivity**
- Visualizes data with an **interactive scatter plot**

## Project Workflow
### 1. Article Scraping
Scraped top headlines from BBC, CNN, and FOX News based on a user-provided query using **Google SerpAPI**

![Screenshot 2025-06-29 150231](https://github.com/user-attachments/assets/d60109f4-4d63-4b56-9ed6-e2ae0e419473)

### 2. Text Preprocessing
- Removed links, punctuation, special characters
- Normalized whitespace and lowercase text
- Stripped HTML tags
  
![Screenshot 2025-06-29 150400](https://github.com/user-attachments/assets/fac6683d-b9ff-4453-a641-956d7bba05e7)

### 3. Summarization
Used BART from HuggingFace, **facebook/bart-large-cnn**, to generate concise article summaries

![Screenshot 2025-06-29 150507](https://github.com/user-attachments/assets/e8b2d9ff-0bc7-45e4-b4f0-107ee1c8966e)

### 4. Sentiment & Bias Detection
- **Polarity**: Value between -1 (very negative) and +1 (very positive)
- **Subjectivity**: Value between 0 (objective) and 1 (subjective)
- Extract **Sentiment** from the summary: positive, neutral, negative
  
![Screenshot 2025-06-29 150512](https://github.com/user-attachments/assets/fc54082d-1e3c-4049-bc51-c13604f71094)

### 5. Visualization Dashboard
![Screenshot 2025-06-29 150654](https://github.com/user-attachments/assets/d0cd6eed-49ec-4ad2-8960-0da777bed6ca)

An interactive scatter plot is presented to understand the bias of each article, and of a particular news channel as well:
- **X-axis**: Sentiment polarity
- **Y-axis**: Subjectivity
- **Color coded blobs**: News source (BBC/CNN/FOX)
- **Hover Info**: Headline + full summary
- **Click**: Opens full article in browser
  
![Screenshot 2025-06-29 150601](https://github.com/user-attachments/assets/120abc9d-1a03-4c76-8fc3-5444648d6089)
