import json
import logging
import sys
from typing import Dict, Any
from pathlib import Path

# --- Configure Logging ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)
logger = logging.getLogger(__name__)

# --- Path Setup (KISS Principle) ---
# More robust and simpler path resolution.
# Assumes a standard project structure where `src` is the source root.
try:
    PROJECT_ROOT = Path(__file__).resolve().parent.parent
    SOURCE_ROOT = PROJECT_ROOT / "src"
    if not SOURCE_ROOT.is_dir():
        # Fallback for when the script is run from within the src directory
        PROJECT_ROOT = Path(__file__).resolve().parent
        SOURCE_ROOT = PROJECT_ROOT

    if str(SOURCE_ROOT) not in sys.path:
        sys.path.insert(0, str(SOURCE_ROOT))

    from aica_backend.scraping.providers.factory import ScrapingProviderFactory
except (ImportError, FileNotFoundError) as e:
    logger.error("---" * 20)
    logger.error("FATAL ERROR: Could not import dependencies or set up paths.", exc_info=True)
    logger.error("\nPlease ensure this script is inside the 'src' folder or its parent.")
    logger.error("And that all packages have an __init__.py file.")
    logger.error("---" * 20)
    sys.exit(1)


def load_scraping_config(site_name: str) -> Dict[str, Any]:
    """Loads and retrieves the configuration for a specific site."""
    config_path = SOURCE_ROOT / "aica_backend" / "job_sources.json"
    logger.info(f"Loading configuration from: {config_path}")
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)

        site_config = config.get("sources", {}).get(site_name)
        if not site_config:
            raise ValueError(f"No config for site '{site_name}' found in job_sources.json.")

        # Make prompt/schema paths absolute and pass them in the config
        # This keeps the provider clean of path-resolution logic (Single Responsibility).
        llm_config = site_config.get('llm_config', {})
        if llm_config:
            prompt_path = SOURCE_ROOT / 'aica_backend' / llm_config['prompt_path']
            schema_path = SOURCE_ROOT / 'aica_backend' / llm_config['schema_path']
            llm_config['prompt_path'] = str(prompt_path)
            llm_config['schema_path'] = str(schema_path)

        return site_config
    except (FileNotFoundError, json.JSONDecodeError, KeyError) as e:
        logger.error(f"FATAL: Could not load or parse config from '{config_path}': {e}", exc_info=True)
        raise


def run_scraping_test(site_name: str):
    """Runs the scraping test for a single configured site."""
    logger.info(f"--- [START] Scraping test for site: '{site_name}' ---")
    try:
        site_config = load_scraping_config(site_name)

        if not site_config.get("active", False):
            logger.warning(f"Site '{site_name}' is inactive. Skipping.")
            return

        provider = ScrapingProviderFactory.create_provider('crawl4ai', site_config)
        logger.info(f"Successfully created '{type(provider).__name__}' for '{site_name}'.")

        logger.info("Starting the scraping process... (This may take a few minutes)")
        scraped_jobs = provider.scrape_job_listings()

        if scraped_jobs:
            logger.info(f"SUCCESS: Scraped {len(scraped_jobs)} unique jobs.")
            output_file = PROJECT_ROOT / f"{site_name}_scraped_jobs.json"
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(scraped_jobs, f, indent=4, ensure_ascii=False)
            logger.info(f"Full results saved to '{output_file}'")
        else:
            logger.warning("Scraping completed, but no jobs were found or extracted.")

    except Exception as e:
        logger.error(f"An unexpected error occurred during the test for '{site_name}': {e}", exc_info=True)
    finally:
        logger.info(f"--- [END] Test for '{site_name}' finished. ---")


if __name__ == "__main__":
    TARGET_SITE_TO_TEST = "jobstreet"
    run_scraping_test(TARGET_SITE_TO_TEST)