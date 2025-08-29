import asyncio
import logging
import sys
from pathlib import Path

# Configure logging for detailed output
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)

try:
    from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode
    print("✓ Successfully imported Crawl4AI components")
except ImportError as e:
    print(f"✗ Failed to import Crawl4AI: {e}")
    sys.exit(1)

async def test_basic_crawling():
    """Test basic crawling without LLM extraction first."""
    print("\n=== Testing Basic Page Crawling ===")
    
    browser_config = BrowserConfig(
        headless=False,  # Keep visible for debugging
        browser_type="chromium",
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
    )
    
    test_url = "https://remoteok.com/remote-dev-jobs"
    
    async with AsyncWebCrawler(config=browser_config) as crawler:
        try:
            print(f"Attempting to crawl: {test_url}")
            
            # Simple configuration - no extraction strategy yet
            run_config = CrawlerRunConfig(
                wait_for="body",
                page_timeout=30000,
                cache_mode=CacheMode.BYPASS
            )
            
            result = await crawler.arun(url=test_url, config=run_config)
            
            if result.success:
                print("✓ Successfully crawled the page!")
                print(f"Content length: {len(result.markdown)}")
                print(f"Content preview (first 500 chars):\n{result.markdown[:500]}...")
                
                # Save full content for inspection
                output_file = Path("debug_crawl_output.txt")
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(f"URL: {test_url}\n")
                    f.write(f"Success: {result.success}\n")
                    f.write(f"Error: {result.error_message}\n\n")
                    f.write("=== MARKDOWN CONTENT ===\n")
                    f.write(result.markdown)
                    
                print(f"✓ Full content saved to: {output_file}")
                return True
            else:
                print(f"✗ Failed to crawl: {result.error_message}")
                return False
                
        except Exception as e:
            print(f"✗ Exception during crawling: {e}")
            return False

async def test_with_ollama():
    """Test if Ollama is accessible."""
    print("\n=== Testing Ollama Connection ===")
    
    try:
        import requests
        ollama_url = "http://localhost:11434/api/version"
        response = requests.get(ollama_url, timeout=5)
        if response.status_code == 200:
            print("✓ Ollama is running and accessible")
            return True
        else:
            print(f"✗ Ollama returned status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Cannot connect to Ollama: {e}")
        print("  Make sure Ollama is running: ollama serve")
        return False

def check_file_paths():
    """Check if required files exist."""
    print("\n=== Checking Required Files ===")
    
    base_path = Path(__file__).parent
    
    files_to_check = [
        "aica_backend/job_sources.json",
        "aica_backend/scraping/prompts/job_extraction_prompt.txt",
        "aica_backend/scraping/prompts/job_extraction_schema.json"
    ]
    
    all_found = True
    for file_path in files_to_check:
        full_path = base_path / file_path
        if full_path.exists():
            print(f"✓ Found: {file_path}")
        else:
            print(f"✗ Missing: {file_path}")
            all_found = False
            
    return all_found

async def main():
    print("🔍 Crawl4AI Debug Test Suite")
    print("=" * 50)
    
    # Check file paths first
    files_ok = check_file_paths()
    if not files_ok:
        print("\n❌ Some required files are missing. Please check the paths.")
        return
    
    # Test Ollama connection
    ollama_ok = await test_with_ollama()
    
    # Test basic crawling
    crawl_ok = await test_basic_crawling()
    
    print("\n" + "=" * 50)
    print("📋 SUMMARY:")
    print(f"Files: {'✓' if files_ok else '✗'}")
    print(f"Ollama: {'✓' if ollama_ok else '✗'}")
    print(f"Crawling: {'✓' if crawl_ok else '✗'}")
    
    if all([files_ok, ollama_ok, crawl_ok]):
        print("\n🎉 All tests passed! Your setup should work.")
    else:
        print("\n⚠️  Some tests failed. Check the output above for details.")

if __name__ == "__main__":
    asyncio.run(main())