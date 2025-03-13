import openai
import requests
import os
from flask import Flask, jsonify

app = Flask(__name__)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
GROK_API_KEY = os.getenv("GROK_API_KEY")

openai.api_key = OPENAI_API_KEY

def summarize_text(text):
    try:
        client = openai.OpenAI()
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Summarize this news article in 2 sentences."},
                {"role": "user", "content": text}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

def get_latest_news():
    try:
        url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={NEWS_API_KEY}"
        response = requests.get(url)
        data = response.json()
        if data["status"] != "ok":
            return {"error": "Failed to fetch news"}
        articles = data.get("articles", [])[:5]
        news_list = []
        for article in articles:
            title = article.get("title", "No Title")
            content = article.get("content", "No Content Available")
            summary = summarize_text(content)
            news_list.append({
                "title": title,
                "summary": summary,
                "source": article.get("url", "#")
            })
        return news_list
    except Exception as e:
        return {"error": str(e)}

@app.route('/')
def home():
    return "HaveYourSay API is running! Try /get-news"

@app.route('/get-news')
def fetch_news():
    news = get_latest_news()
    return jsonify(news)

if __name__ == '__main__':
    port = int(os.getenv("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=False)
