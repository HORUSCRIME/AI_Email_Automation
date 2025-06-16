import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

def get_full_url(domain: str) -> str:
    """
    Constructs a full URL (with https://) from a given domain.
    Ensures that the URL is properly formatted for requests.

    Args:
        domain (str): The domain name (e.g., "dadaautorepair.com").

    Returns:
        str: The full URL (e.g., "https://dadaautorepair.com").
    """
    if not domain:
        return ""
    if not domain.startswith(('http://', 'https://')):
        return f"https://{domain}"
    return domain

def scrape_website_content(url: str):
    """
    Scrapes key content from a given URL, including title, meta description,
    and main text content from paragraphs and headings.

    Args:
        url (str): The URL of the website to scrape.

    Returns:
        dict: A dictionary containing 'title', 'meta_description', 'main_content', 'error'.
              Returns None for content fields if not found or on error.
    """
    if not url:
        print("Error: No URL provided for scraping.")
        return {
            "title": None,
            "meta_description": None,
            "main_content": None,
            "error": "No URL provided."
        }

    try:
        # Add a timeout to prevent hanging indefinitely
        response = requests.get(url, timeout=10)
        response.raise_for_status() # Raise an exception for HTTP errors (4xx or 5xx)

        soup = BeautifulSoup(response.text, 'lxml')

        # Extract Title
        title = soup.title.string if soup.title else None

        # Extract Meta Description
        meta_description = None
        meta_tag = soup.find('meta', attrs={'name': 'description'})
        if meta_tag and meta_tag.get('content'):
            meta_description = meta_tag['content'].strip()
        else:
            # Fallback for Open Graph description
            og_description_tag = soup.find('meta', attrs={'property': 'og:description'})
            if og_description_tag and og_description_tag.get('content'):
                meta_description = og_description_tag['content'].strip()

        # Extract Main Content (paragraphs and headings)
        main_content_elements = soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
        main_content = "\n".join([elem.get_text(strip=True) for elem in main_content_elements if elem.get_text(strip=True)])

        # Basic check for empty content (could indicate a non-HTML page or very sparse page)
        if not title and not meta_description and not main_content:
            print(f"Warning: Scraped content from {url} appears to be very sparse or empty.")

        return {
            "title": title,
            "meta_description": meta_description,
            "main_content": main_content,
            "error": None
        }

    except requests.exceptions.RequestException as e:
        print(f"Error accessing or scraping '{url}': {e}")
        return {
            "title": None,
            "meta_description": None,
            "main_content": None,
            "error": f"Failed to access or scrape website: {e}"
        }
    except Exception as e:
        print(f"An unexpected error occurred during scraping '{url}': {e}")
        return {
            "title": None,
            "meta_description": None,
            "main_content": None,
            "error": f"An unexpected error occurred: {e}"
        }

if __name__ == "__main__":
    # Example Usage:
    test_domain = "dadaautorepair.com" # Example from assignment
    test_url = get_full_url(test_domain)
    print(f"Scraping content from: {test_url}")
    scraped_data = scrape_website_content(test_url)

    if scraped_data["error"]:
        print(f"Scraping failed: {scraped_data['error']}")
    else:
        print(f"\nTitle: {scraped_data['title']}")
        print(f"\nMeta Description: {scraped_data['meta_description']}")
        print(f"\nMain Content (first 500 chars): \n{scraped_data['main_content'][:500]}...")

    print("\n--- Testing a known good site ---")
    good_site_data = scrape_website_content("https://www.google.com")
    print(f"Title: {good_site_data['title']}")
    print(f"Meta Description: {good_site_data['meta_description']}")
    print(f"Main Content (first 200 chars): \n{good_site_data['main_content'][:200]}...")

    print("\n--- Testing an invalid site ---")
    invalid_site_data = scrape_website_content("http://nonexistent-domain-12345.xyz")
    print(f"Invalid Site Error: {invalid_site_data['error']}")
