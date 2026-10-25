from flask import Flask, jsonify
from urllib.parse import unquote
import re
app = Flask('Sentiment Analyzer')
POSITIVE = {'fantastic', 'excellent', 'great', 'good', 'wonderful', 'amazing', 'love', 'helpful', 'friendly', 'best', 'fast', 'smooth', 'recommend', 'services', 'service'}
NEGATIVE = {'bad', 'poor', 'terrible', 'awful', 'hate', 'rude', 'slow', 'worst', 'broken', 'disappointed'}

@app.get('/')
def home():
    return 'Welcome to the Sentiment Analyzer. Use /analyze/<text>.'

@app.get('/analyze/<path:input_txt>')
def analyze_sentiment(input_txt):
    words = set(re.findall(r"[a-z]+", unquote(input_txt).lower()))
    positive = len(words & POSITIVE)
    negative = len(words & NEGATIVE)
    sentiment = 'positive' if positive > negative else ('negative' if negative > positive else 'neutral')
    return jsonify({'sentiment': sentiment})

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5050, debug=False)
