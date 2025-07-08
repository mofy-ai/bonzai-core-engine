"""
Scraping API routes for Live API Studio
Provides URL scraping with sub-URL discovery and agent coordination
"""

from flask import Blueprint, request, jsonify, current_app
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time
import uuid
from datetime import datetime
from typing import Dict, List, Optional, Set
import re
import concurrent.futures
import threading

scrape_bp = Blueprint('scrape', __name__)

# Global storage for scraping sessions
scraping_sessions = {}
scraping_lock = threading.Lock()

class ScrapingSession:
    def __init__(self, session_id: str, base_url: str, max_depth: int = 2):
        self.session_id = session_id
        self.base_url = base_url
        self.max_depth = max_depth
        self.discovered_urls = set()
        self.scraped_data = {}
        self.status = 'initialized'
        self.progress = 0
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
        self.errors = []
        
    def to_dict(self):
        return {
            'session_id': self.session_id,
            'base_url': self.base_url,
            'max_depth': self.max_depth,
            'discovered_urls': list(self.discovered_urls),
            'scraped_count': len(self.scraped_data),
            'status': self.status,
            'progress': self.progress,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'errors': self.errors
        }

def extract_links(html_content: str, base_url: str) -> Set[str]:
    """Extract all links from HTML content"""
    try:
        soup = BeautifulSoup(html_content, 'html.parser')
        links = set()
        
        for link in soup.find_all('a', href=True):
            href = link['href']
            full_url = urljoin(base_url, href)
            
            # Only include HTTP/HTTPS URLs from the same domain
            parsed_base = urlparse(base_url)
            parsed_url = urlparse(full_url)
            
            if (parsed_url.scheme in ['http', 'https'] and 
                parsed_url.netloc == parsed_base.netloc):
                links.add(full_url)
        
        return links
    except Exception as e:
        current_app.logger.error(f"Error extracting links: {str(e)}")
        return set()

def scrape_single_url(url: str, timeout: int = 10) -> Dict:
    """Scrape a single URL and extract content"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract metadata
        title = soup.find('title')
        title_text = title.get_text().strip() if title else 'No title'
        
        # Extract description
        description = soup.find('meta', attrs={'name': 'description'})
        description_text = description.get('content', '') if description else ''
        
        # Extract main content (try multiple selectors)
        content_selectors = [
            'main', 'article', '.content', '#content', 
            '.post-content', '.entry-content', 'body'
        ]
        
        content_text = ''
        for selector in content_selectors:
            content_elem = soup.select_one(selector)
            if content_elem:
                content_text = content_elem.get_text(separator=' ', strip=True)
                break
        
        # Extract links for sub-URL discovery
        links = extract_links(str(soup), url)
        
        return {
            'url': url,
            'title': title_text,
            'description': description_text,
            'content': content_text[:5000],  # Limit content length
            'links': list(links),
            'status_code': response.status_code,
            'scraped_at': datetime.utcnow().isoformat(),
            'success': True
        }
        
    except requests.RequestException as e:
        return {
            'url': url,
            'error': f"Request error: {str(e)}",
            'scraped_at': datetime.utcnow().isoformat(),
            'success': False
        }
    except Exception as e:
        return {
            'url': url,
            'error': f"Parsing error: {str(e)}",
            'scraped_at': datetime.utcnow().isoformat(),
            'success': False
        }

@scrape_bp.route('/start', methods=['POST'])
def start_scraping():
    """Start a new scraping session with sub-URL discovery"""
    try:
        data = request.get_json()
        base_url = data.get('url')
        max_depth = data.get('max_depth', 2)
        session_id = data.get('session_id', str(uuid.uuid4()))
        
        if not base_url:
            return jsonify({
                'success': False,
                'error': 'URL is required'
            }), 400
        
        # Validate URL
        try:
            parsed = urlparse(base_url)
            if not parsed.scheme or not parsed.netloc:
                raise ValueError("Invalid URL format")
        except Exception:
            return jsonify({
                'success': False,
                'error': 'Invalid URL format'
            }), 400
        
        # Create scraping session
        session = ScrapingSession(session_id, base_url, max_depth)
        
        with scraping_lock:
            scraping_sessions[session_id] = session
        
        # Start scraping in background thread
        def scrape_worker():
            try:
                session.status = 'running'
                session.updated_at = datetime.utcnow()
                
                urls_to_scrape = {base_url}
                scraped_urls = set()
                current_depth = 0
                
                while urls_to_scrape and current_depth <= max_depth:
                    current_batch = list(urls_to_scrape - scraped_urls)
                    urls_to_scrape.clear()
                    
                    # Scrape current batch with threading
                    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
                        future_to_url = {
                            executor.submit(scrape_single_url, url): url 
                            for url in current_batch
                        }
                        
                        for future in concurrent.futures.as_completed(future_to_url):
                            url = future_to_url[future]
                            try:
                                result = future.result()
                                session.scraped_data[url] = result
                                scraped_urls.add(url)
                                
                                # Add discovered links for next depth level
                                if result.get('success') and current_depth < max_depth:
                                    for link in result.get('links', []):
                                        if link not in scraped_urls:
                                            urls_to_scrape.add(link)
                                            session.discovered_urls.add(link)
                                
                                # Update progress
                                session.progress = min(90, (len(scraped_urls) / max(len(current_batch), 1)) * 100)
                                session.updated_at = datetime.utcnow()
                                
                            except Exception as e:
                                error_msg = f"Error scraping {url}: {str(e)}"
                                session.errors.append(error_msg)
                                current_app.logger.error(error_msg)
                    
                    current_depth += 1
                
                session.status = 'completed'
                session.progress = 100
                session.updated_at = datetime.utcnow()
                
            except Exception as e:
                session.status = 'error'
                session.errors.append(f"Session error: {str(e)}")
                session.updated_at = datetime.utcnow()
                current_app.logger.error(f"Scraping session error: {str(e)}")
        
        # Start background thread
        thread = threading.Thread(target=scrape_worker)
        thread.daemon = True
        thread.start()
        
        return jsonify({
            'success': True,
            'session_id': session_id,
            'message': 'Scraping session started',
            'session': session.to_dict()
        })
        
    except Exception as e:
        current_app.logger.error(f"Error starting scraping: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@scrape_bp.route('/status/<session_id>', methods=['GET'])
def get_scraping_status(session_id):
    """Get status of a scraping session"""
    try:
        with scraping_lock:
            session = scraping_sessions.get(session_id)
        
        if not session:
            return jsonify({
                'success': False,
                'error': 'Session not found'
            }), 404
        
        return jsonify({
            'success': True,
            'session': session.to_dict()
        })
        
    except Exception as e:
        current_app.logger.error(f"Error getting scraping status: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@scrape_bp.route('/results/<session_id>', methods=['GET'])
def get_scraping_results(session_id):
    """Get results from a scraping session"""
    try:
        with scraping_lock:
            session = scraping_sessions.get(session_id)
        
        if not session:
            return jsonify({
                'success': False,
                'error': 'Session not found'
            }), 404
        
        # Filter results based on query parameters
        include_content = request.args.get('include_content', 'false').lower() == 'true'
        successful_only = request.args.get('successful_only', 'false').lower() == 'true'
        
        results = {}
        for url, data in session.scraped_data.items():
            if successful_only and not data.get('success'):
                continue
            
            result = data.copy()
            if not include_content:
                result.pop('content', None)
            
            results[url] = result
        
        return jsonify({
            'success': True,
            'session_id': session_id,
            'results': results,
            'summary': {
                'total_urls': len(session.scraped_data),
                'successful_urls': len([d for d in session.scraped_data.values() if d.get('success')]),
                'discovered_urls': len(session.discovered_urls),
                'status': session.status,
                'progress': session.progress
            }
        })
        
    except Exception as e:
        current_app.logger.error(f"Error getting scraping results: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@scrape_bp.route('/sessions', methods=['GET'])
def list_scraping_sessions():
    """List all scraping sessions"""
    try:
        with scraping_lock:
            sessions = {
                session_id: session.to_dict() 
                for session_id, session in scraping_sessions.items()
            }
        
        return jsonify({
            'success': True,
            'sessions': sessions
        })
        
    except Exception as e:
        current_app.logger.error(f"Error listing scraping sessions: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@scrape_bp.route('/session/<session_id>', methods=['DELETE'])
def delete_scraping_session(session_id):
    """Delete a scraping session"""
    try:
        with scraping_lock:
            if session_id in scraping_sessions:
                del scraping_sessions[session_id]
                return jsonify({
                    'success': True,
                    'message': 'Session deleted successfully'
                })
            else:
                return jsonify({
                    'success': False,
                    'error': 'Session not found'
                }), 404
        
    except Exception as e:
        current_app.logger.error(f"Error deleting scraping session: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@scrape_bp.route('/quick', methods=['POST'])
def quick_scrape():
    """Quick scrape of a single URL without session management"""
    try:
        data = request.get_json()
        url = data.get('url')
        
        if not url:
            return jsonify({
                'success': False,
                'error': 'URL is required'
            }), 400
        
        result = scrape_single_url(url)
        
        return jsonify({
            'success': True,
            'result': result
        })
        
    except Exception as e:
        current_app.logger.error(f"Error in quick scrape: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# Error handlers
@scrape_bp.errorhandler(400)
def bad_request(error):
    return jsonify({
        'success': False,
        'error': 'Bad request - invalid scraping parameters'
    }), 400

@scrape_bp.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 'Scraping resource not found'
    }), 404

@scrape_bp.errorhandler(500)
def internal_error(error):
    return jsonify({
        'success': False,
        'error': 'Internal server error in scraping service'
    }), 500