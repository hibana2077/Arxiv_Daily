import urllib.parse
import urllib.request
import feedparser
import os
from datetime import datetime

INTERESTING_CATEGORIES = os.getenv("INTERESTS", "cs.IT,cs.CV,cs.LG,cs.NE").split(',')

def fetch_daily_cs_papers(date):
    base_url = 'http://export.arxiv.org/api/query?'

    # Format the date as required by arXiv API
    date_str = date.strftime('%Y%m%d')

    # Create the query parameters
    # Add 'cat:cs.*' to limit results to Computer Science
    search_query = f'cat:({" OR ".join([f"{cat}" for cat in INTERESTING_CATEGORIES])}) AND submittedDate:[{date_str}000000 TO {date_str}235959]'
    params = {
        'search_query': search_query,
        'start': 0,
        'max_results': 1000,  # Adjust as needed
        'sortBy': 'submittedDate',
        'sortOrder': 'descending'
    }

    # Encode the parameters and create the full URL
    query = urllib.parse.urlencode(params)
    url = base_url + query

    # Fetch the results
    with urllib.request.urlopen(url) as response:  
        parse = feedparser.parse(response.read())

    # Process and return the results
    papers = []
    for entry in parse.entries:
        papers.append({
            'title': entry.title,
            'authors': [author.name for author in entry.authors],
            'summary': entry.summary,
            'link': entry.link,
            'arxiv_comment': entry.arxiv_comment if 'arxiv_comment' in entry else '',
            'categories': [tag['term'] for tag in entry.tags if tag['scheme'] == 'http://arxiv.org/schemas/atom'],
            'published': datetime(*entry.published_parsed[:6])
        })

    return papers

if __name__ == '__main__':
    # Example usage
    sp_date = datetime(2024, 7, 20)
    cs_papers = fetch_daily_cs_papers(sp_date)
    print(f"The number of papers fetched: {len(cs_papers)}")