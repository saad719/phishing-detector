import ipaddress
import re
import urllib.request
from bs4 import BeautifulSoup
import socket
import requests
from googlesearch import search
import whois
from datetime import date
from urllib.parse import urlparse

class Urlcheck:
     def __init__(self, url):
        self.features = []
        self.url = url
        self.domain = ""
        self.whois_response = None
        self.urlparse = None
        self.response = None
        self.soup = None
        self.valid = None

        try:
            self.response = requests.get(url)
            self.soup = BeautifulSoup(self.response.text, 'html.parser')
        except requests.exceptions.RequestException as e:
            print(f"Error fetching URL: {e}")
            self.response = None
            self.soup = None
            self.valid = 0
            

        try:
            self.urlparse = urlparse(url)
            self.domain = self.urlparse.netloc
        except Exception as e:
            print(f"Error parsing URL: {e}")
            self.urlparse = None
            self.domain = ""
            self.valid = 0
           

        try:
            self.whois_response = whois.whois(self.domain)
        except Exception as e:
            print(f"Error fetching WHOIS data: {e}")
            self.whois_response = None
            self.valid = 0

     def getValidity(self):
        return self.valid
           





class FeatureExtraction:
    def __init__(self, url):
        self.features = []
        self.url = url
        self.domain = ""
        self.whois_response = None
        self.urlparse = None
        self.response = None
        self.soup = None

        try:
            self.response = requests.get(url)
            self.soup = BeautifulSoup(self.response.text, 'html.parser')
        except requests.exceptions.RequestException as e:
            print(f"Error fetching URL: {e}")
            self.response = None
            self.soup = None

        try:
            self.urlparse = urlparse(url)
            self.domain = self.urlparse.netloc
        except Exception as e:
            print(f"Error parsing URL: {e}")
            self.urlparse = None
            self.domain = ""

        try:
            self.whois_response = whois.whois(self.domain)
        except Exception as e:
            print(f"Error fetching WHOIS data: {e}")
            self.whois_response = None

        # Add features
        self.features.append(1)
        self.features.append(self.UsingIp())
        self.features.append(self.longUrl())
        self.features.append(self.shortUrl())
        self.features.append(self.symbol())
        self.features.append(self.redirecting())
        self.features.append(self.prefixSuffix())
        self.features.append(self.SubDomains())
        self.features.append(self.Hppts())
        self.features.append(self.DomainRegLen())
        self.features.append(self.Favicon())
        self.features.append(self.NonStdPort())
        self.features.append(self.HTTPSDomainURL())
        self.features.append(self.RequestURL())
        self.features.append(self.AnchorURL())
        self.features.append(self.LinksInScriptTags())
        self.features.append(self.ServerFormHandler())
        self.features.append(self.InfoEmail())
        self.features.append(self.AbnormalURL())
        self.features.append(self.WebsiteForwarding())
        self.features.append(self.StatusBarCust())
        self.features.append(self.DisableRightClick())
        self.features.append(self.UsingPopupWindow())
        self.features.append(self.IframeRedirection())
        self.features.append(self.AgeofDomain())
        self.features.append(self.DNSRecording())
        self.features.append(self.WebsiteTraffic())
        self.features.append(self.PageRank())
        self.features.append(self.GoogleIndex())
        self.features.append(self.LinksPointingToPage())
        self.features.append(self.StatsReport())

    # 1. UsingIp
    def UsingIp(self):
        try:
            ipaddress.ip_address(self.url)
            return -1
        except ValueError:
            return 1

    # 2. longUrl
    def longUrl(self):
        url_length = len(self.url)
        if url_length < 54:
            return 1
        elif url_length <= 75:
            return 0
        else:
            return -1

    # 3. shortUrl
    def shortUrl(self):
        short_url_patterns = r'bit\.ly|goo\.gl|shorte\.st|go2l\.ink|x\.co|ow\.ly|t\.co|tinyurl|tr\.im|is\.gd|cli\.gs|'
        match = re.search(short_url_patterns, self.url)
        return -1 if match else 1

    # 4. Symbol@
    def symbol(self):
        return -1 if "@" in self.url else 1

    # 5. Redirecting//
    def redirecting(self):
        return -1 if self.url.count("//") > 1 else 1

    # 6. prefixSuffix
    def prefixSuffix(self):
        try:
            return -1 if "-" in self.domain else 1
        except:
            return -1

    # 7. SubDomains
    def SubDomains(self):
        dot_count = self.url.count(".")
        if dot_count == 1:
            return 1
        elif dot_count == 2:
            return 0
        else:
            return -1

    # 8. HTTPS
    def Hppts(self):
        try:
            return 1 if self.urlparse and 'https' in self.urlparse.scheme else -1
        except:
            return -1

    # 9. DomainRegLen
    def DomainRegLen(self):
        try:
            expiration_date = self.whois_response.expiration_date
            creation_date = self.whois_response.creation_date

            if isinstance(expiration_date, list):
                expiration_date = expiration_date[0]
            if isinstance(creation_date, list):
                creation_date = creation_date[0]

            age = (expiration_date.year - creation_date.year) * 12 + (expiration_date.month - creation_date.month)
            return 1 if age >= 12 else -1
        except:
            return -1

    # 10. Favicon
    def Favicon(self):
        try:
            if self.soup:
                for link in self.soup.find_all('link', href=True):
                    if self.url in link['href'] or self.domain in link['href']:
                        return 1
            return -1
        except:
            return -1

    # 11. NonStdPort
    def NonStdPort(self):
        try:
            if ":" in self.domain:
                return -1
            return 1
        except:
            return -1

    # 12. HTTPSDomainURL
    def HTTPSDomainURL(self):
        try:
            return -1 if 'https' in self.domain else 1
        except:
            return -1

    # 13. RequestURL
    def RequestURL(self):
        success = 0
        i = 0
        try:
            if self.soup:
                for tag in ['img', 'audio', 'embed', 'iframe']:
                    for element in self.soup.find_all(tag, src=True):
                        dots = re.findall(r'\.', element['src'])
                        if self.url in element['src'] or self.domain in element['src'] or len(dots) == 1:
                            success += 1
                        i += 1

                percentage = success / float(i) * 100 if i > 0 else 0
                if percentage < 22.0:
                    return 1
                elif 22.0 <= percentage < 61.0:
                    return 0
                else:
                    return -1
        except:
            return -1

    # 14. AnchorURL
    def AnchorURL(self):
        unsafe = 0
        i = 0
        try:
            if self.soup:
                for a in self.soup.find_all('a', href=True):
                    if "#" in a['href'] or "javascript" in a['href'].lower() or "mailto" in a['href'].lower():
                        unsafe += 1
                    elif not (self.url in a['href'] or self.domain in a['href']):
                        unsafe += 1
                    i += 1

                percentage = unsafe / float(i) * 100 if i > 0 else 0
                if percentage < 31.0:
                    return 1
                elif 31.0 <= percentage < 67.0:
                    return 0
                else:
                    return -1
        except:
            return -1

    # 15. LinksInScriptTags
    def LinksInScriptTags(self):
        success = 0
        i = 0
        try:
            if self.soup:
                for tag in ['link', 'script']:
                    for element in self.soup.find_all(tag, src=True):
                        dots = re.findall(r'\.', element['src'])
                        if self.url in element['src'] or self.domain in element['src'] or len(dots) == 1:
                            success += 1
                        i += 1

                percentage = success / float(i) * 100 if i > 0 else 0
                if percentage < 17.0:
                    return 1
                elif 17.0 <= percentage < 81.0:
                    return 0
                else:
                    return -1
        except:
            return -1

    # 16. ServerFormHandler
    def ServerFormHandler(self):
        try:
            if self.soup:
                for form in self.soup.find_all('form', action=True):
                    if form['action'] == "" or form['action'] == "about:blank" or not (self.url in form['action'] or self.domain in form['action']):
                        return -1
            return 1
        except:
            return -1

    # 17. InfoEmail
    def InfoEmail(self):
        try:
            if re.findall(r"[mailto:|mail\(\)]", self.response.text):
                return -1
            return 1
        except:
            return -1

    # 18. AbnormalURL
    def AbnormalURL(self):
        try:
            if self.response.text == str(self.whois_response):
                return 1
            return -1
        except:
            return -1

    # 19. WebsiteForwarding
    def WebsiteForwarding(self):
        try:
            if len(self.response.history) <= 1:
                return 1
            return -1
        except:
            return -1

    # 20. StatusBarCust
    def StatusBarCust(self):
        try:
            if self.soup:
                if self.soup.find("script", {"type": "text/javascript"}):
                    return -1
            return 1
        except:
            return -1

    # 21. DisableRightClick
    def DisableRightClick(self):
        try:
            if self.soup:
                if "oncontextmenu" in str(self.soup):
                    return -1
            return 1
        except:
            return -1

    # 22. UsingPopupWindow
    def UsingPopupWindow(self):
        try:
            if self.soup:
                if "window.open" in str(self.soup):
                    return -1
            return 1
        except:
            return -1

    # 23. IframeRedirection
    def IframeRedirection(self):
        try:
            if self.soup:
                if self.soup.find('iframe'):
                    return -1
            return 1
        except:
            return -1

    # 24. AgeofDomain
    def AgeofDomain(self):
        try:
            if self.whois_response:
                creation_date = self.whois_response.creation_date
                current_date = date.today()
                domain_age = (current_date - creation_date).days
                return 1 if domain_age > 365 else -1
            return -1
        except:
            return -1

    # 25. DNSRecording
    def DNSRecording(self):
        try:
            if self.whois_response:
                if self.whois_response.domain_name:
                    return 1
            return -1
        except:
            return -1

    # 26. WebsiteTraffic
    def WebsiteTraffic(self):
        try:
            if self.response.status_code == 200:
                return 1
            return -1
        except:
            return -1

    # 27. PageRank
    def PageRank(self):
        try:
            return 1 if "PageRank" in self.response.text else -1
        except:
            return -1

    # 28. GoogleIndex
    def GoogleIndex(self):
        try:
            if self.url in search(self.url, num_results=10):
                return 1
            return -1
        except:
            return -1

    # 29. LinksPointingToPage
    def LinksPointingToPage(self):
        try:
            if self.soup:
                return 1 if len(self.soup.find_all('a')) > 5 else -1
            return -1
        except:
            return -1

    # 30. StatsReport
    def StatsReport(self):
        try:
            if "statistics" in self.response.text:
                return 1
            return -1
        except:
            return -1
    def getFeaturesList(self):
        return self.features
