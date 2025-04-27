import dash
from dash import dcc, html, Input, Output, State, ctx
import pandas as pd
import plotly.express as px
from textblob import TextBlob
import nltk
from nltk.tokenize import word_tokenize

# Import your custom modules
from scrape import search_bbc, search_cnn, search_fox, get_article_text, get_article_title
from clean import clean_text
from analyze import summarize, analyze_bias

# Initialize Dash app
app = dash.Dash(__name__)
app.title = "News Bias Explorer"

# Global DataFrame to store all results
global_df = pd.DataFrame(columns=[
    'Sentiment', 'Subjectivity', 'Source', 'Title', 'Summary', 'URL', 'PosWords', 'NegWords'
])

# Helper function to extract positive and negative words
def extract_pos_neg_words(text):
    positive = []
    negative = []
    words = word_tokenize(text)
    for word in words:
        blob = TextBlob(word)
        polarity = blob.sentiment.polarity
        if polarity > 0.3:
            positive.append(word)
        elif polarity < -0.3:
            negative.append(word)
    return list(set(positive)), list(set(negative))

# App Layout
app.layout = html.Div([
    html.H1("📰 News Bias Explorer", style={'textAlign': 'center', 'marginBottom': '30px'}),

    html.Div([
        dcc.Input(id='topic-input', type='text', placeholder='Enter a topic...', style={'width': '50%', 'padding': '10px'}),
        html.Button('Search', id='search-button', n_clicks=0, style={'marginLeft': '10px'}),
    ], style={'textAlign': 'center'}),

    html.Br(),

    dcc.Loading(
        id="loading",
        type="circle",
        children=[html.Div(id='progress-output', style={'textAlign': 'center'})]
    ),

    html.Br(),

    dcc.Graph(id='scatter-plot'),

    html.Div(id='article-popup', style={
        'position': 'fixed',
        'top': '100px',
        'right': '50px',
        'width': '400px',
        'backgroundColor': '#f9f9f9',
        'padding': '20px',
        'border': '1px solid #ccc',
        'borderRadius': '10px',
        'boxShadow': '2px 2px 10px rgba(0,0,0,0.1)',
        'display': 'none'
    })
])

# Callback to fetch and process articles when Search is clicked
@app.callback(
    Output('progress-output', 'children'),
    Output('scatter-plot', 'figure'),
    Input('search-button', 'n_clicks'),
    State('topic-input', 'value'),
    prevent_initial_call=True
)
def update_articles(n_clicks, topic):
    global global_df

    # Initialize storage lists
    sentiments, subjectivities, sources, titles, summaries, urls, poswords_list, negwords_list = [], [], [], [], [], [], [], []

    if not topic:
        return "❗ Please enter a topic!", dash.no_update

    progress_messages = []

    # Search articles
    bbc_urls = search_bbc(topic)
    cnn_urls = search_cnn(topic)
    fox_urls = search_fox(topic)

    progress_messages.append(f"📡 Found {len(bbc_urls)} BBC articles.")
    progress_messages.append(f"📡 Found {len(cnn_urls)} CNN articles.")
    progress_messages.append(f"📡 Found {len(fox_urls)} FOX articles.")

    all_sources = [
        (bbc_urls, "BBC"),
        (cnn_urls, "CNN"),
        (fox_urls, "FOX")
    ]

    # Process each article
    for urls_list, source_name in all_sources:
        for idx, url in enumerate(urls_list[:10]):  # limit to 10 articles per source
            try:
                text = get_article_text(url)

                if not text or len(text.split()) < 100:
                    progress_messages.append(f"⚠️ Skipped short or empty article {idx+1} from {source_name}")
                    continue

                title = get_article_title(url)
                clean = clean_text(text)
                summary = summarize(clean)
                sentiment, subjectivity = analyze_bias(summary)
                poswords, negwords = extract_pos_neg_words(summary)

                sentiments.append(sentiment)
                subjectivities.append(subjectivity)
                sources.append(source_name)
                titles.append(title)
                summaries.append(summary)
                urls.append(url)
                poswords_list.append(poswords)
                negwords_list.append(negwords)

                progress_messages.append(f"✅ Processed {source_name} article {idx+1}: {title[:40]}...")

            except Exception as e:
                progress_messages.append(f"❌ Error processing article {idx+1} from {source_name}: {e}")

    # Create a new DataFrame
    global_df = pd.DataFrame({
        'Sentiment': sentiments,
        'Subjectivity': subjectivities,
        'Source': sources,
        'Title': titles,
        'Summary': summaries,
        'URL': urls,
        'PosWords': poswords_list,
        'NegWords': negwords_list
    })

    # Create scatter plot
    fig = px.scatter(
        global_df,
        x="Sentiment",
        y="Subjectivity",
        color="Source",
        hover_data=["Title"],
        title=f"News Bias Analysis: {topic}",
        width=1100,
        height=700
    )
    fig.update_traces(marker=dict(size=14, line=dict(width=2, color='DarkSlateGrey')))

    return html.Div([html.P(msg) for msg in progress_messages]), fig

# Callback to display article details on click
@app.callback(
    Output('article-popup', 'children'),
    Output('article-popup', 'style'),
    Input('scatter-plot', 'clickData'),
    prevent_initial_call=True
)
def display_article(clickData):
    if clickData:
        idx = clickData['points'][0]['pointIndex']
        article = global_df.iloc[idx]

        content = html.Div([
            html.H3(article['Title']),
            html.P(article['Summary']),
            html.Hr(),
            html.P(f"🌟 Positive Words: {', '.join(article['PosWords'])}"),
            html.P(f"⚡ Negative Words: {', '.join(article['NegWords'])}"),
            html.A("🔗 Read Full Article", href=article['URL'], target="_blank", style={'color': 'blue', 'textDecoration': 'underline'}),
            html.Br(),
            html.Button('Close', id='close-btn', n_clicks=0)
        ])

        style = {
            'position': 'fixed',
            'top': '100px',
            'right': '50px',
            'width': '400px',
            'backgroundColor': '#f9f9f9',
            'padding': '20px',
            'border': '1px solid #ccc',
            'borderRadius': '10px',
            'boxShadow': '2px 2px 10px rgba(0,0,0,0.1)',
            'display': 'block'
        }
        return content, style
    else:
        return None, {'display': 'none'}

# Run the server
if __name__ == '__main__':
    app.run(debug=True)
