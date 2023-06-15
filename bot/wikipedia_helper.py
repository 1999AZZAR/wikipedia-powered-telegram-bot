# bot/wikipedia_helper.py

import os
import wikipedia
from dotenv import load_dotenv

load_dotenv()

wiki_language = os.getenv('WIKIPEDIA_LANGUAGE', 'en')

def wikipedia_summary(title: str, language=wiki_language) -> str:
    """Get the summary of a Wikipedia article."""
    try:
        summary = wikipedia.summary(title, sentences=3, auto_suggest=False, redirect=True)
        return summary
    except Exception as e:
        return str(e)

def wikipedia_url(title: str, language=wiki_language) -> str:
    """Get the URL of a Wikipedia article."""
    try:
        page = wikipedia.page(title)
        return page.url
    except Exception as e:
        return str(e)

def wikipedia_search(query):
    try:
        search_results = wikipedia.search(query, results=10)
        results = []
        for i, result in enumerate(search_results):
            url = wikipedia_url(result)
            summary = wikipedia_summary(result)
            results.append({
                'title': result,
                'url': url,
                'summary': summary
            })
        return results
    except Exception as e:
        return str(e)
