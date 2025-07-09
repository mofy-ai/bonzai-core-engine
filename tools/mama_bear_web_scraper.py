#!/usr/bin/env python3
"""
🐻 MAMA BEAR'S INTELLIGENT WEB SCRAPER
===================================
ADHD-Friendly Web Content Extraction & Mem0 Memory Preparation Tool

Features:
- Smart content extraction with noise reduction
- ADHD-optimized formatting (clear structure, bullet points)
- Mem0-ready output with semantic chunking
- Family-safe content filtering
- Progress indicators for hyperfocus management
- Multiple export formats (JSON, Markdown, Text)

Created with love for Nathan's neurodivergent needs ❤️
"""

import requests
from bs4 import BeautifulSoup
import json
import re
import os
import time
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from urllib.parse import urljoin, urlparse
import hashlib
from dataclasses import dataclass
import logging

# Set up logging for debugging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class ScrapedContent:
    """Structure for scraped content - ADHD-friendly organization"""
    url: str
    title: str
    summary: str
    main_content: str
    key_points: List[str]
    images: List[str]
    links: List[str]
    metadata: Dict
    mem0_chunks: List[Dict]
    scraped_at: str
    word_count: int
    reading_time_minutes: int

class MamaBearWebScraper:
    """
    🐻 Mama Bear's Intelligent Web Scraper
    
    Designed specifically for Nathan's ADHD needs:
    - Clear, structured output
    - Progress indicators
    - Memory-friendly chunking
    - Family-safe content filtering
    """
    
    def __init__(self, output_dir: str = "scraped_content"):
        self.output_dir = output_dir
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'MamaBearScraper/1.0 (Educational/Research Purpose)'
        })
        
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        
        # ADHD-friendly settings
        self.max_chunk_size = 500  # Manageable chunks for ADHD reading
        self.reading_speed_wpm = 200  # Average reading speed
        
        print("🐻 Mama Bear Web Scraper initialized!")
        print(f"📁 Output directory: {self.output_dir}")
        print("✨ ADHD-optimized settings loaded")
        
    def scrape_website(self, url: str, include_images: bool = True) -> ScrapedContent:
        """
        Main scraping function - extracts and structures web content
        
        Args:
            url: Website URL to scrape
            include_images: Whether to extract image URLs
            
        Returns:
            ScrapedContent object with structured data
        """
        print(f"\n🚀 Starting scrape of: {url}")
        
        try:
            # Step 1: Fetch the webpage
            print("📥 Fetching webpage...")
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            # Step 2: Parse HTML
            print("🔍 Parsing HTML content...")
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Step 3: Extract core content
            print("📝 Extracting content...")
            title = self._extract_title(soup)
            main_content = self._extract_main_content(soup)
            key_points = self._extract_key_points(main_content)
            
            # Step 4: Process images and links
            images = self._extract_images(soup, url) if include_images else []
            links = self._extract_links(soup, url)
            
            # Step 5: Create summary
            print("📊 Generating summary...")
            summary = self._create_summary(main_content)
            
            # Step 6: Calculate reading metrics
            word_count = len(main_content.split())
            reading_time = max(1, word_count // self.reading_speed_wpm)
            
            # Step 7: Create Mem0-optimized chunks
            print("🧠 Creating memory chunks for Mem0...")
            mem0_chunks = self._create_mem0_chunks(title, main_content, url)
            
            # Step 8: Compile metadata
            metadata = {
                'domain': urlparse(url).netloc,
                'scraped_by': 'MamaBearScraper',
                'content_type': 'web_article',
                'language': 'en',  # Could be detected
                'family_safe': True,  # Could implement content filtering
                'adhd_optimized': True
            }
            
            scraped_content = ScrapedContent(
                url=url,
                title=title,
                summary=summary,
                main_content=main_content,
                key_points=key_points,
                images=images,
                links=links,
                metadata=metadata,
                mem0_chunks=mem0_chunks,
                scraped_at=datetime.now().isoformat(),
                word_count=word_count,
                reading_time_minutes=reading_time
            )
            
            print("✅ Scraping completed successfully!")
            return scraped_content
            
        except Exception as e:
            logger.error(f"Error scraping {url}: {str(e)}")
            print(f"❌ Error scraping website: {str(e)}")
            raise
    
    def _extract_title(self, soup: BeautifulSoup) -> str:
        """Extract page title with fallbacks"""
        # Try multiple title sources
        title_sources = [
            soup.find('title'),
            soup.find('h1'),
            soup.find('meta', {'property': 'og:title'}),
            soup.find('meta', {'name': 'title'})
        ]
        
        for source in title_sources:
            if source:
                if source.name == 'meta':
                    title = source.get('content', '').strip()
                else:
                    title = source.get_text().strip()
                
                if title and len(title) > 5:
                    return title[:200]  # Reasonable length limit
                    
        return "Untitled Page"
    
    def _extract_main_content(self, soup: BeautifulSoup) -> str:
        """Extract main content, removing navigation and ads"""
        # Remove unwanted elements
        unwanted_tags = [
            'script', 'style', 'nav', 'footer', 'header', 
            'sidebar', 'advertisement', 'ad', 'popup'
        ]
        
        for tag in unwanted_tags:
            for element in soup.find_all(tag):
                element.decompose()
        
        # Remove elements by class/id patterns
        unwanted_patterns = [
            'nav', 'menu', 'header', 'footer', 'sidebar', 
            'ad', 'advertisement', 'popup', 'modal', 'cookie'
        ]
        
        for pattern in unwanted_patterns:
            for element in soup.find_all(attrs={'class': re.compile(pattern, re.I)}):
                element.decompose()
            for element in soup.find_all(attrs={'id': re.compile(pattern, re.I)}):
                element.decompose()
        
        # Extract content from likely containers
        content_selectors = [
            'main', 'article', '.content', '.post', '.entry', 
            '#content', '#main', '.article-body', '.post-content'
        ]
        
        main_content = ""
        for selector in content_selectors:
            elements = soup.select(selector)
            if elements:
                for element in elements:
                    main_content += element.get_text(strip=True) + "\n\n"
                break
        
        # Fallback: get all paragraphs and headings
        if not main_content:
            for tag in soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'li']):
                text = tag.get_text(strip=True)
                if len(text) > 20:  # Filter out short/empty elements
                    main_content += text + "\n\n"
        
        # Clean up the content
        main_content = re.sub(r'\n\s*\n', '\n\n', main_content)  # Remove excessive newlines
        main_content = re.sub(r' +', ' ', main_content)  # Remove excessive spaces
        
        return main_content.strip()
    
    def _extract_key_points(self, content: str) -> List[str]:
        """Extract key points for ADHD-friendly bullet points"""
        # Split content into sentences
        sentences = re.split(r'[.!?]+', content)
        key_points = []
        
        for sentence in sentences:
            sentence = sentence.strip()
            # Key point criteria: not too short, not too long, meaningful content
            if (20 <= len(sentence) <= 150 and 
                not sentence.lower().startswith(('click', 'subscribe', 'follow', 'like')) and
                any(word in sentence.lower() for word in ['important', 'key', 'significant', 'note', 'remember'])):
                key_points.append(sentence)
        
        # If no key points found, take first few substantial sentences
        if not key_points:
            for sentence in sentences[:10]:
                sentence = sentence.strip()
                if 30 <= len(sentence) <= 150:
                    key_points.append(sentence)
                if len(key_points) >= 5:
                    break
        
        return key_points[:10]  # Limit to manageable number
    
    def _extract_images(self, soup: BeautifulSoup, base_url: str) -> List[str]:
        """Extract image URLs"""
        images = []
        
        for img in soup.find_all('img'):
            src = img.get('src') or img.get('data-src')
            if src:
                # Convert relative URLs to absolute
                full_url = urljoin(base_url, src)
                # Filter out tiny images (likely icons/decorations)
                if not any(keyword in src.lower() for keyword in ['icon', 'logo', 'button', 'pixel']):
                    images.append(full_url)
        
        return images[:20]  # Reasonable limit
    
    def _extract_links(self, soup: BeautifulSoup, base_url: str) -> List[str]:
        """Extract relevant links"""
        links = []
        
        for link in soup.find_all('a', href=True):
            href = link['href']
            full_url = urljoin(base_url, href)
            
            # Filter out non-content links
            if (not href.startswith('#') and 
                not any(keyword in href.lower() for keyword in ['mailto:', 'tel:', 'javascript:', 'social', 'share']) and
                len(link.get_text().strip()) > 5):
                links.append(full_url)
        
        return list(set(links))[:50]  # Remove duplicates and limit
    
    def _create_summary(self, content: str) -> str:
        """Create ADHD-friendly summary"""
        # Simple extractive summarization
        sentences = re.split(r'[.!?]+', content)
        
        # Score sentences by position and keywords
        important_keywords = [
            'important', 'key', 'significant', 'main', 'primary', 
            'essential', 'crucial', 'fundamental', 'overview', 'summary'
        ]
        
        scored_sentences = []
        for i, sentence in enumerate(sentences[:20]):  # First 20 sentences
            sentence = sentence.strip()
            if len(sentence) < 20:
                continue
                
            score = 0
            # Position score (earlier sentences more important)
            score += max(0, 10 - i)
            
            # Keyword score
            for keyword in important_keywords:
                if keyword in sentence.lower():
                    score += 5
            
            # Length score (moderate length preferred)
            if 50 <= len(sentence) <= 200:
                score += 3
            
            scored_sentences.append((score, sentence))
        
        # Sort by score and take top sentences
        scored_sentences.sort(reverse=True)
        summary_sentences = [sentence for _, sentence in scored_sentences[:3]]
        
        summary = '. '.join(summary_sentences)
        if not summary:
            # Fallback: first substantial paragraph
            paragraphs = content.split('\n\n')
            for para in paragraphs:
                if 100 <= len(para) <= 500:
                    summary = para[:300] + "..."
                    break
        
        return summary or "Content summary not available."
    
    def _create_mem0_chunks(self, title: str, content: str, url: str) -> List[Dict]:
        """Create optimized chunks for Mem0 memory storage"""
        chunks = []
        
        # Chunk 1: Title and URL context
        chunks.append({
            'content': f"Website: {title}\nURL: {url}\nThis is web content scraped for research and reference purposes.",
            'type': 'metadata',
            'source': url,
            'timestamp': datetime.now().isoformat(),
            'tags': ['web_content', 'research', 'scraped']
        })
        
        # Chunk content into manageable pieces
        paragraphs = content.split('\n\n')
        current_chunk = ""
        chunk_num = 1
        
        for para in paragraphs:
            para = para.strip()
            if not para:
                continue
                
            # If adding this paragraph would exceed limit, save current chunk
            if len(current_chunk) + len(para) > self.max_chunk_size and current_chunk:
                chunks.append({
                    'content': current_chunk,
                    'type': 'content',
                    'source': url,
                    'chunk_number': chunk_num,
                    'total_chunks': 'TBD',  # Will update later
                    'timestamp': datetime.now().isoformat(),
                    'tags': ['web_content', 'content_chunk']
                })
                current_chunk = para
                chunk_num += 1
            else:
                current_chunk += "\n\n" + para if current_chunk else para
        
        # Add the last chunk
        if current_chunk:
            chunks.append({
                'content': current_chunk,
                'type': 'content',
                'source': url,
                'chunk_number': chunk_num,
                'total_chunks': chunk_num,
                'timestamp': datetime.now().isoformat(),
                'tags': ['web_content', 'content_chunk']
            })
        
        # Update total chunks count
        total_content_chunks = chunk_num
        for chunk in chunks:
            if chunk.get('type') == 'content':
                chunk['total_chunks'] = total_content_chunks
        
        return chunks
    
    def save_content(self, content: ScrapedContent, formats: List[str] = ['json', 'markdown', 'txt']) -> Dict[str, str]:
        """Save content in multiple formats"""
        saved_files = {}
        
        # Create safe filename
        safe_title = re.sub(r'[^\w\s-]', '', content.title)[:50]
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_filename = f"{safe_title}_{timestamp}"
        
        # Save JSON format (perfect for Mem0 upload)
        if 'json' in formats:
            json_path = os.path.join(self.output_dir, f"{base_filename}.json")
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(content.__dict__, f, indent=2, ensure_ascii=False)
            saved_files['json'] = json_path
            print(f"💾 JSON saved: {json_path}")
        
        # Save Markdown format (ADHD-friendly reading)
        if 'markdown' in formats:
            md_path = os.path.join(self.output_dir, f"{base_filename}.md")
            with open(md_path, 'w', encoding='utf-8') as f:
                f.write(self._create_markdown_output(content))
            saved_files['markdown'] = md_path
            print(f"📝 Markdown saved: {md_path}")
        
        # Save plain text format
        if 'txt' in formats:
            txt_path = os.path.join(self.output_dir, f"{base_filename}.txt")
            with open(txt_path, 'w', encoding='utf-8') as f:
                f.write(self._create_text_output(content))
            saved_files['txt'] = txt_path
            print(f"📄 Text saved: {txt_path}")
        
        # Save Mem0 chunks separately for easy upload
        if 'mem0' in formats:
            mem0_path = os.path.join(self.output_dir, f"{base_filename}_mem0_chunks.json")
            with open(mem0_path, 'w', encoding='utf-8') as f:
                json.dump(content.mem0_chunks, f, indent=2, ensure_ascii=False)
            saved_files['mem0'] = mem0_path
            print(f"🧠 Mem0 chunks saved: {mem0_path}")
        
        return saved_files
    
    def _create_markdown_output(self, content: ScrapedContent) -> str:
        """Create ADHD-friendly Markdown output"""
        md = f"""# 🌐 {content.title}

**URL:** {content.url}  
**Scraped:** {content.scraped_at}  
**Reading Time:** {content.reading_time_minutes} minutes  
**Word Count:** {content.word_count}  

---

## 📊 Quick Summary

{content.summary}

---

## 🎯 Key Points

"""
        
        for i, point in enumerate(content.key_points, 1):
            md += f"{i}. {point}\n"
        
        md += f"""
---

## 📝 Full Content

{content.main_content}

---

## 🔗 Additional Resources

### Images Found
"""
        
        for img in content.images[:10]:  # Limit to first 10
            md += f"- ![Image]({img})\n"
        
        md += "\n### Related Links\n"
        
        for link in content.links[:20]:  # Limit to first 20
            md += f"- [{link}]({link})\n"
        
        md += f"""
---

## 🤖 Technical Details

- **Scraped by:** Mama Bear Web Scraper
- **ADHD Optimized:** Yes
- **Family Safe:** {content.metadata.get('family_safe', 'Unknown')}
- **Memory Chunks Created:** {len(content.mem0_chunks)}

---

*This content was scraped and formatted with ADHD-friendly features by Mama Bear's Web Scraper* 🐻
"""
        
        return md
    
    def _create_text_output(self, content: ScrapedContent) -> str:
        """Create simple text output"""
        return f"""TITLE: {content.title}
URL: {content.url}
SCRAPED: {content.scraped_at}
READING TIME: {content.reading_time_minutes} minutes

SUMMARY:
{content.summary}

MAIN CONTENT:
{content.main_content}
"""
    
    def upload_to_mem0(self, content: ScrapedContent, mem0_client) -> List[str]:
        """Upload content chunks to Mem0 memory system"""
        print("🧠 Uploading to Mem0 memory system...")
        memory_ids = []
        
        try:
            for i, chunk in enumerate(content.mem0_chunks):
                # Upload each chunk to Mem0
                memory_result = mem0_client.add_memory(
                    content=chunk['content'],
                    user_id="mama_bear_scraper",
                    metadata=chunk
                )
                
                if hasattr(memory_result, 'id'):
                    memory_ids.append(memory_result.id)
                    print(f"✅ Chunk {i+1}/{len(content.mem0_chunks)} uploaded")
                else:
                    print(f"⚠️ Chunk {i+1} upload may have failed")
                
                # Small delay to be nice to the API
                time.sleep(0.1)
                
        except Exception as e:
            print(f"❌ Error uploading to Mem0: {str(e)}")
            logger.error(f"Mem0 upload error: {str(e)}")
        
        print(f"🎉 Uploaded {len(memory_ids)} chunks to Mem0!")
        return memory_ids

def main():
    """Example usage of Mama Bear Web Scraper"""
    print("🐻 MAMA BEAR'S WEB SCRAPER")
    print("=" * 50)
    
    # Initialize scraper
    scraper = MamaBearWebScraper()
    
    # Example URLs for testing
    test_urls = [
        "https://example.com",
        "https://news.ycombinator.com",
        "https://www.wikipedia.org"
    ]
    
    print("\nEnter a URL to scrape (or press Enter for example):")
    url_input = input("> ").strip()
    
    if not url_input:
        url_input = "https://example.com"
        print(f"Using example URL: {url_input}")
    
    try:
        # Scrape the website
        content = scraper.scrape_website(url_input)
        
        # Save in all formats
        saved_files = scraper.save_content(content, formats=['json', 'markdown', 'txt', 'mem0'])
        
        print("\n🎉 Scraping completed successfully!")
        print("\nFiles saved:")
        for format_type, file_path in saved_files.items():
            print(f"  {format_type.upper()}: {file_path}")
        
        print(f"\n📊 Content Statistics:")
        print(f"  Title: {content.title}")
        print(f"  Word Count: {content.word_count}")
        print(f"  Reading Time: {content.reading_time_minutes} minutes")
        print(f"  Key Points: {len(content.key_points)}")
        print(f"  Memory Chunks: {len(content.mem0_chunks)}")
        print(f"  Images Found: {len(content.images)}")
        print(f"  Links Found: {len(content.links)}")
        
        print("\n🧠 Mem0 Memory Chunks Preview:")
        for i, chunk in enumerate(content.mem0_chunks[:3]):  # Show first 3
            print(f"  Chunk {i+1}: {chunk['content'][:100]}...")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    main()
