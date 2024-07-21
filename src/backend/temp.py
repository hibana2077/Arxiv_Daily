import urllib.parse
import urllib.request
import feedparser
from datetime import datetime

def fetch_daily_cs_papers(date):
  base_url = 'http://export.arxiv.org/api/query?'

  # Format the date as required by arXiv API
  date_str = date.strftime('%Y%m%d')

  # Create the query parameters
  # Add 'cat:cs.*' to limit results to Computer Science
  search_query = f'cat:cs.* AND submittedDate:[{date_str}000000 TO {date_str}235959]'
  params = {
      'search_query': search_query,
      'start': 0,
      'max_results': 100,  # Adjust as needed
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
          'categories': [tag['term'] for tag in entry.tags if tag['scheme'] == 'http://arxiv.org/schemas/atom'],
          'published': datetime(*entry.published_parsed[:6])
      })

  return papers

if __name__ == '__main__':
    # Example usage
    today = datetime.now()
    yesterday = today.replace(day=today.day - 3)
    cs_papers = fetch_daily_cs_papers(yesterday)
    for paper in cs_papers:
        print(f"Title: {paper['title']}")
        print(f"Authors: {', '.join(paper['authors'])}")
        print(f"Categories: {', '.join(paper['categories'])}")
        print(f"Link: {paper['link']}")
        # print(f"Published: {paper['published']}")
        print("---")