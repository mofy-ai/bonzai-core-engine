#!/usr/bin/env python3
"""
🐻 MAMA BEAR'S WEB SCRAPER - EASY USAGE EXAMPLE
==============================================

Simple example showing how to use the web scraper with Mem0 integration.
Perfect for Nathan's ADHD workflow - clear, structured, easy to understand.
"""

from mama_bear_web_scraper import MamaBearWebScraper
import mem0
import os

def scrape_and_memorize(url: str, mem0_api_key: str = None):
    """
    Simple function to scrape a website and upload to Mem0
    
    Args:
        url: Website URL to scrape
        mem0_api_key: Your Mem0 API key (optional, will use env var if not provided)
    """
    
    print(f"🐻 Mama Bear is scraping: {url}")
    print("=" * 60)
    
    # Initialize scraper
    scraper = MamaBearWebScraper(output_dir="scraped_websites")
    
    try:
        # Scrape the website
        print("📥 Extracting content...")
        content = scraper.scrape_website(url)
        
        # Save to files (for your reading)
        print("💾 Saving files...")
        saved_files = scraper.save_content(content, formats=['markdown', 'json', 'mem0'])
        
        # Upload to Mem0 if API key available
        if mem0_api_key or os.getenv('MEM0_API_KEY'):
            try:
                print("🧠 Connecting to Mem0...")
                mem0_client = mem0.Client(api_key=mem0_api_key or os.getenv('MEM0_API_KEY'))
                
                print("📤 Uploading to memory...")
                memory_ids = scraper.upload_to_mem0(content, mem0_client)
                
                print(f"✅ Successfully uploaded {len(memory_ids)} memory chunks!")
                
            except Exception as e:
                print(f"⚠️ Mem0 upload failed: {str(e)}")
                print("💡 Content saved locally - you can upload manually later")
        
        else:
            print("🔑 No Mem0 API key found - skipping memory upload")
            print("💡 Set MEM0_API_KEY environment variable to enable auto-upload")
        
        # Show results
        print("\n🎉 SCRAPING COMPLETE!")
        print(f"📖 Title: {content.title}")
        print(f"📊 Word Count: {content.word_count:,}")
        print(f"⏱️ Reading Time: {content.reading_time_minutes} minutes")
        print(f"🎯 Key Points: {len(content.key_points)}")
        print(f"🧠 Memory Chunks: {len(content.mem0_chunks)}")
        
        print("\n📁 Files Saved:")
        for format_type, file_path in saved_files.items():
            print(f"  {format_type.upper()}: {file_path}")
        
        print("\n🧠 Memory Preview:")
        for i, chunk in enumerate(content.mem0_chunks[:2]):
            print(f"  Chunk {i+1}: {chunk['content'][:150]}...")
        
        return content, saved_files
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return None, None

def batch_scrape(urls: list, mem0_api_key: str = None):
    """
    Scrape multiple URLs in batch
    
    Args:
        urls: List of URLs to scrape
        mem0_api_key: Your Mem0 API key
    """
    
    print(f"🐻 Mama Bear batch scraping {len(urls)} websites...")
    print("=" * 60)
    
    results = []
    
    for i, url in enumerate(urls, 1):
        print(f"\n📍 Processing {i}/{len(urls)}: {url}")
        content, files = scrape_and_memorize(url, mem0_api_key)
        
        if content:
            results.append({
                'url': url,
                'title': content.title,
                'word_count': content.word_count,
                'files': files
            })
        
        # Small break between requests to be nice
        if i < len(urls):
            print("⏳ Taking a short break...")
            import time
            time.sleep(2)
    
    print(f"\n🎉 BATCH COMPLETE! Processed {len(results)} websites successfully.")
    return results

# Example usage
if __name__ == "__main__":
    print("🐻 MAMA BEAR'S WEB SCRAPER EXAMPLES")
    print("=" * 50)
    
    # Single website example
    print("\n1️⃣ Single Website Scraping:")
    scrape_and_memorize("https://example.com")
    
    # Batch scraping example
    print("\n2️⃣ Batch Scraping Example:")
    example_urls = [
        "https://www.wikipedia.org",
        "https://news.ycombinator.com",
        "https://github.com"
    ]
    
    batch_scrape(example_urls)
    
    print("\n🐻 Mama Bear says: All done! Check the 'scraped_websites' folder for your files!")
