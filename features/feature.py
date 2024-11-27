import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import whois

class ExtractInfo:
    def __init__(self, url):
        self.url = url
        self.domain = urlparse(url).netloc
        self.response = None
        self.soup = None
        self.initialize_response()

    def initialize_response(self):
        try:
            self.response = requests.get(self.url, timeout=10)
            if self.response.status_code == 200:
                self.soup = BeautifulSoup(self.response.text, 'html.parser')
            else:
                print(f"Failed to fetch the URL: {self.url}, Status Code: {self.response.status_code}")
        except requests.RequestException as e:
            print(f"An error occurred while fetching the URL: {self.url}. Error: {e}")

    def Favicon(self):
        try:
            if not self.soup:
                print("Soup object is not initialized.")
                return None
            icon = self.soup.find("link", rel="shortcut icon")
            if icon and icon['href']:
                return icon['href']
            return f"http://{self.domain}/favicon.ico"
        except Exception as e:
            print(f"Error finding favicon: {e}")
            return None

    def RequestURL(self):
        try:
            if not self.soup:
                print("Soup object is not initialized.")
                return None
            total_links = 0
            external_links = 0
            for tag in self.soup.find_all('a', href=True):
                total_links += 1
                href = tag['href']
                parsed = urlparse(href)
                if parsed.netloc and parsed.netloc != self.domain:
                    external_links += 1
            return {"Total Links": total_links, "External Links": external_links}
        except Exception as e:
            print(f"Error processing request URLs: {e}")
            return None

    def LinksInScriptTags(self):
        try:
            if not self.soup:
                print("Soup object is not initialized.")
                return None
            total_scripts = 0
            external_scripts = 0
            for tag in self.soup.find_all(['script', 'link'], src=True):
                total_scripts += 1
                src = tag.get('src') or tag.get('href')
                parsed = urlparse(src)
                if parsed.netloc and parsed.netloc != self.domain:
                    external_scripts += 1
            return {"Total Scripts": total_scripts, "External Scripts": external_scripts}
        except Exception as e:
            print(f"Error processing script tags: {e}")
            return None

    def InfoEmail(self):
        try:
            if not self.soup:
                print("Soup object is not initialized.")
                return None
            emails = set()
            for text in self.soup.stripped_strings:
                if "@" in text:
                    emails.add(text)
            return list(emails)
        except Exception as e:
            print(f"Error extracting emails: {e}")
            return None

    def WhoisDomain(self):
        try:
            domain_info = whois.whois(self.domain)
            return {
                "Domain Name": domain_info.domain_name,
                "Registrar": domain_info.registrar,
                "Creation Date": domain_info.creation_date,
                "Expiration Date": domain_info.expiration_date,
            }
        except Exception as e:
            print(f"Error fetching WHOIS data: {e}")
            return None

# Example usage
if __name__ == "__main__":
    url = "https://mail.google.com/mail/u/0/#sent/QgrcJHsHqfTHbCzznMPkPLcZvRjGFXzLjSv"
    extractor = ExtractInfo(url)

    print("Favicon:", extractor.Favicon())
    print("Request URL Info:", extractor.RequestURL())
    print("Script Links Info:", extractor.LinksInScriptTags())
    print("Emails:", extractor.InfoEmail())
    print("WHOIS Info:", extractor.WhoisDomain())
