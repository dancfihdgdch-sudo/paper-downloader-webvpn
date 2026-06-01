#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Paper Downloader via WebVPN
Automatically download academic papers using DOI through school WebVPN
"""

import requests
import re
import time
from urllib.parse import quote, urlencode
from bs4 import BeautifulSoup
from config import WEBVPN_URL, WEBVPN_USERNAME, WEBVPN_PASSWORD, DOWNLOAD_DIR, TIMEOUT, RETRY_TIMES, HEADERS

class WebVPNSession:
    """
    Handle WebVPN login and session management
    """
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(HEADERS)
        self.webvpn_url = WEBVPN_URL
        self.username = WEBVPN_USERNAME
        self.password = WEBVPN_PASSWORD
        self.is_logged_in = False
    
    def login(self):
        """
        Login to WebVPN
        """
        print("[*] Attempting to login to WebVPN...")
        
        try:
            # Get login page to extract any required tokens
            login_url = f"{self.webvpn_url}/login"
            response = self.session.get(login_url, timeout=TIMEOUT)
            
            # Prepare login data
            login_data = {
                'username': self.username,
                'password': self.password
            }
            
            # Post login request
            response = self.session.post(login_url, data=login_data, timeout=TIMEOUT)
            
            if response.status_code == 200:
                print("[+] WebVPN login successful!")
                self.is_logged_in = True
                return True
            else:
                print(f"[-] WebVPN login failed with status code {response.status_code}")
                return False
        
        except Exception as e:
            print(f"[-] WebVPN login error: {str(e)}")
            return False
    
    def get_proxy_url(self, target_url):
        """
        Convert target URL to WebVPN proxy URL
        e.g., https://example.com/path -> https://webvpn.hebmu.edu.cn/https/encoded_url
        """
        # Remove protocol and encode the URL
        target_url = target_url.replace('https://', '').replace('http://', '')
        encoded = quote(target_url, safe='')
        
        # Create WebVPN proxy URL
        proxy_url = f"{self.webvpn_url}/https/{encoded}"
        return proxy_url

class DOIDownloader:
    """
    Handle DOI resolution and paper downloading
    """
    def __init__(self, webvpn_session):
        self.session = webvpn_session.session
        self.webvpn = webvpn_session
    
    def resolve_doi(self, doi):
        """
        Resolve DOI to get the actual paper URL
        """
        print(f"[*] Resolving DOI: {doi}")
        
        try:
            # Direct DOI resolution
            doi_url = f"https://doi.org/{doi}"
            
            response = self.session.head(
                doi_url,
                allow_redirects=True,
                timeout=TIMEOUT,
                headers=HEADERS
            )
            
            final_url = response.url
            print(f"[+] DOI resolved to: {final_url}")
            return final_url
        
        except Exception as e:
            print(f"[-] DOI resolution error: {str(e)}")
            return None
    
    def download_from_yiigle(self, doi):
        """
        Download paper from YIIGLE medical database
        Handles Chinese medical journals
        """
        print(f"[*] Attempting to download from YIIGLE database...")
        
        try:
            # Search YIIGLE for the DOI
            search_url = f"https://www.yiigle.com/search?q={doi}"
            
            response = self.session.get(search_url, timeout=TIMEOUT, headers=HEADERS)
            
            if response.status_code == 200:
                # Parse search results
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Look for PDF download link
                pdf_links = soup.find_all('a', href=re.compile(r'\.pdf$', re.I))
                
                if pdf_links:
                    pdf_url = pdf_links[0]['href']
                    if not pdf_url.startswith('http'):
                        pdf_url = f"https://www.yiigle.com{pdf_url}"
                    
                    print(f"[+] Found PDF link: {pdf_url}")
                    return pdf_url
                else:
                    print("[-] No PDF link found in YIIGLE search results")
                    return None
            else:
                print(f"[-] YIIGLE search failed with status code {response.status_code}")
                return None
        
        except Exception as e:
            print(f"[-] YIIGLE download error: {str(e)}")
            return None
    
    def download_paper(self, paper_url, filename=None):
        """
        Download paper PDF from URL
        """
        if not paper_url:
            print("[-] Invalid paper URL")
            return False
        
        print(f"[*] Downloading paper from: {paper_url}")
        
        # Generate filename if not provided
        if not filename:
            filename = paper_url.split('/')[-1]
            if not filename.endswith('.pdf'):
                filename = f"{filename}.pdf"
        
        filepath = f"{DOWNLOAD_DIR}/{filename}"
        
        try:
            for attempt in range(RETRY_TIMES):
                try:
                    response = self.session.get(
                        paper_url,
                        timeout=TIMEOUT,
                        headers=HEADERS,
                        stream=True
                    )
                    
                    if response.status_code == 200:
                        with open(filepath, 'wb') as f:
                            for chunk in response.iter_content(chunk_size=8192):
                                if chunk:
                                    f.write(chunk)
                        
                        print(f"[+] Paper downloaded successfully!")
                        print(f"[+] Saved to: {filepath}")
                        return True
                    else:
                        print(f"[-] Download failed with status code {response.status_code}")
                        if attempt < RETRY_TIMES - 1:
                            print(f"[*] Retrying... (Attempt {attempt + 2}/{RETRY_TIMES})")
                            time.sleep(2)
                
                except requests.exceptions.Timeout:
                    print(f"[-] Request timeout on attempt {attempt + 1}/{RETRY_TIMES}")
                    if attempt < RETRY_TIMES - 1:
                        time.sleep(2)
            
            return False
        
        except Exception as e:
            print(f"[-] Download error: {str(e)}")
            return False

def main():
    """
    Main function to download a paper by DOI
    """
    print("="*60)
    print("Paper Downloader via WebVPN")
    print("="*60)
    
    # Get DOI from user
    doi = input("\nEnter DOI (e.g., 10.3760/cma.j.cn121094-20241101-00500): ").strip()
    
    if not doi:
        print("[-] No DOI provided. Exiting.")
        return
    
    # Initialize WebVPN session
    webvpn = WebVPNSession()
    
    # Check if credentials are configured
    if not webvpn.username or not webvpn.password:
        print("\n[-] WebVPN credentials not configured!")
        print("[*] Please configure .env file with your credentials:")
        print("    1. Copy .env.example to .env")
        print("    2. Edit .env with your student ID and password")
        return
    
    # Login to WebVPN
    if not webvpn.login():
        print("[-] Failed to login to WebVPN. Exiting.")
        return
    
    # Initialize downloader
    downloader = DOIDownloader(webvpn)
    
    # Try to resolve DOI
    paper_url = downloader.resolve_doi(doi)
    
    # If direct DOI resolution fails, try YIIGLE
    if not paper_url:
        paper_url = downloader.download_from_yiigle(doi)
    
    # Download the paper
    if paper_url:
        # Extract DOI suffix as filename
        filename = f"paper_{doi.split('/')[-1]}.pdf"
        downloader.download_paper(paper_url, filename)
    else:
        print("[-] Could not find paper URL. Please try manually accessing the database through WebVPN.")
    
    print("\n" + "="*60)
    print("Done!")
    print("="*60)

if __name__ == '__main__':
    main()
