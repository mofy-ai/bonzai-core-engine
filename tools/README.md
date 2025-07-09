# 🐻 Mama Bear's Intelligent Web Scraper

## ADHD-Friendly Web Content Extraction & Mem0 Memory Tool

Created with love for Nathan's neurodivergent needs ❤️

### 🌟 Features

- **Smart Content Extraction** - Removes ads, navigation, and clutter
- **ADHD-Optimized Formatting** - Clear structure, bullet points, manageable chunks
- **Mem0-Ready Output** - Automatically formats content for memory upload
- **Family-Safe Content** - Built-in content filtering
- **Progress Indicators** - Perfect for hyperfocus management
- **Multiple Export Formats** - JSON, Markdown, Text, and Mem0 chunks

### 🚀 Quick Start

1. **Setup** (run once):
   ```powershell
   .\tools\setup_scraper.ps1
   ```

2. **Scrape a website**:
   ```python
   python tools/scraper_examples.py
   ```

3. **Custom scraping**:
   ```python
   from scraper_examples import scrape_and_memorize
   scrape_and_memorize("https://example.com")
   ```

### 📁 File Structure

```
tools/
├── mama_bear_web_scraper.py    # Main scraper class
├── scraper_examples.py         # Easy usage examples
├── scraper_requirements.txt    # Dependencies
├── setup_scraper.ps1          # Windows setup script
└── README.md                  # This file

scraped_websites/              # Output directory (created automatically)
├── Article_Title_20250709_143000.md      # ADHD-friendly Markdown
├── Article_Title_20250709_143000.json    # Complete data structure
├── Article_Title_20250709_143000.txt     # Plain text version
└── Article_Title_20250709_143000_mem0_chunks.json  # Mem0-ready chunks
```

### 🧠 Mem0 Integration

The scraper automatically creates optimized memory chunks for Mem0:

- **Metadata Chunk**: URL, title, and context information
- **Content Chunks**: Manageable 500-character pieces with semantic breaks
- **Automatic Tagging**: Content tagged for easy retrieval
- **Graph-Ready Format**: Structured for Mem0's graph database

### 🎯 ADHD-Friendly Features

- **Clear Progress Indicators** - Shows what's happening during scraping
- **Manageable Chunk Sizes** - 500 characters max per memory chunk
- **Key Points Extraction** - Bullet-point summaries for quick reading
- **Reading Time Estimates** - Know how long content will take to read
- **Visual Organization** - Markdown format with headers and structure

### 📖 Usage Examples

#### Single Website
```python
from scraper_examples import scrape_and_memorize

# Scrape and save locally
content, files = scrape_and_memorize("https://example.com")

# With Mem0 upload
content, files = scrape_and_memorize("https://example.com", "your-mem0-api-key")
```

#### Batch Scraping
```python
from scraper_examples import batch_scrape

urls = [
    "https://site1.com",
    "https://site2.com", 
    "https://site3.com"
]

results = batch_scrape(urls, "your-mem0-api-key")
```

#### Advanced Usage
```python
from mama_bear_web_scraper import MamaBearWebScraper

scraper = MamaBearWebScraper(output_dir="my_research")
content = scraper.scrape_website("https://example.com", include_images=True)

# Save in specific formats
files = scraper.save_content(content, formats=['markdown', 'json'])

# Upload to Mem0
import mem0
client = mem0.Client(api_key="your-key")
memory_ids = scraper.upload_to_mem0(content, client)
```

### 🔧 Configuration

#### Environment Variables
```powershell
# Set Mem0 API key for automatic uploads
$env:MEM0_API_KEY = "your-mem0-api-key-here"
```

#### Scraper Settings
The scraper can be customized:
```python
scraper = MamaBearWebScraper(
    output_dir="custom_folder",     # Where to save files
    max_chunk_size=400,             # Memory chunk size (default: 500)
    reading_speed_wpm=150          # Reading speed for time estimates
)
```

### 📊 Output Formats

#### Markdown (ADHD-Friendly)
- Clear headings and structure
- Bullet points for key information
- Reading time and word count
- Image and link sections
- Technical metadata

#### JSON (Complete Data)
- All extracted information
- Mem0-ready chunks
- Metadata and timestamps
- Perfect for programmatic use

#### Mem0 Chunks (Memory Upload)
- Optimized for semantic search
- Proper tagging and categorization
- Source attribution
- Timestamp tracking

### 🛠️ Dependencies

- `requests` - Web page fetching
- `beautifulsoup4` - HTML parsing
- `lxml` - Fast XML/HTML processing
- `mem0ai` - Memory system integration

### 🔍 Troubleshooting

#### Common Issues

**"Module not found" error**:
```powershell
# Re-run setup
.\tools\setup_scraper.ps1
```

**"Permission denied" error**:
```powershell
# Run PowerShell as Administrator
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**Mem0 upload fails**:
```python
# Check API key
import os
print(os.getenv('MEM0_API_KEY'))
```

### 🎉 Success Metrics

After scraping, you'll see:
- **Title**: Extracted page title
- **Word Count**: Total words in content
- **Reading Time**: Estimated minutes to read
- **Key Points**: Number of bullet points extracted
- **Memory Chunks**: Number of Mem0-ready pieces created
- **Images/Links**: Additional resources found

### 🐻 Mama Bear Says

This scraper is designed specifically for Nathan's ADHD needs:

- ✅ **Clear Structure** - No overwhelming walls of text
- ✅ **Progress Feedback** - Always know what's happening
- ✅ **Manageable Chunks** - Content broken into digestible pieces
- ✅ **Multiple Formats** - Choose what works best for you
- ✅ **Memory Integration** - Automatically feeds your AI family

Happy scraping! Remember: the goal is to gather information efficiently while staying organized and focused. 🎯

---

*Built with love by Mama Bear for the Bonzai AI Family* ❤️
