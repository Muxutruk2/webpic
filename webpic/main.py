import click
from playwright.sync_api import sync_playwright
from os import path, makedirs
import base64
import logging
from concurrent.futures import ThreadPoolExecutor

def save_screenshot(hostname, url, folder, browser, viewport, delay, screenshot_format, auth, user_agent, retries):
    savepath = path.join(folder, f"{url.replace('/', '-')}.{screenshot_format}")
    page = browser.new_page(viewport={'width': viewport[0], 'height': viewport[1]}, user_agent=user_agent)
    
    # Set basic HTTP authentication if provided
    if auth:
        page.set_extra_http_headers({"Authorization": f"Basic {base64.b64encode(f'{auth[0]}:{auth[1]}'.encode()).decode()}"})
    
    # Ensure the hostname ends with a slash
    if not hostname.endswith("/"):
        hostname += "/"
    
    # Ensure the URL does not start with a slash
    if url.startswith("/"):
        url = url[1:]
    
    # Retry mechanism
    for attempt in range(retries):
        try:
            page.goto(f"{hostname}{url}")
            page.wait_for_timeout(delay * 1000)  # delay in milliseconds
            page.screenshot(full_page=True, path=savepath, type=screenshot_format)
            logging.info(f"Saved screenshot for {url} at {savepath}")
            break
        except Exception as e:
            if attempt < retries - 1:
                logging.warning(f"Failed to capture {url}, retrying... ({attempt + 1}/{retries})")
            else:
                logging.error(f"Failed to capture {url} after {retries} attempts: {e}")
        finally:
            page.close()

@click.command()
@click.argument('hostname')
@click.argument('savepath')
@click.argument('urls', nargs=-1, required=False)
@click.option('--file', '-f', type=click.Path(exists=True), help="File containing URLs separated by newlines.")
@click.option('--browser', '-b', type=click.Choice(['chromium', 'firefox', 'webkit'], case_sensitive=False), default='chromium', help="Choose the browser engine to use.")
@click.option('--viewport', '-v', type=(int, int), default=(1280, 720), help="Specify the viewport size as WIDTH HEIGHT.")
@click.option('--delay', '-d', type=int, default=0, help="Time to wait before taking a screenshot, in seconds.")
@click.option('--format', '-fmt', type=click.Choice(['png', 'jpeg'], case_sensitive=False), default='png', help="Screenshot format.")
@click.option('--auth', '-a', type=(str, str), help="Provide basic HTTP authentication as USERNAME PASSWORD.")
@click.option('--headless/--headful', default=True, help="Run browser in headless mode.")
@click.option('--user-agent', '-ua', type=str, help="Specify a custom User-Agent string.")
@click.option('--retries', '-r', type=int, default=3, help="Number of retry attempts if a screenshot fails.")
@click.option('--concurrent', '-c', type=int, default=1, help="Number of concurrent screenshots to capture.")
@click.option('--verbose', '-v', count=True, help="Increase verbosity of output.")
def main(hostname, savepath, urls, file, browser, viewport, delay, format, auth, headless, user_agent, retries, concurrent, verbose):
    """A CLI tool to take automated screenshots of webpages."""
    
    # Set up logging
    log_level = logging.WARNING - (10 * verbose)  # Adjust log level based on verbosity
    logging.basicConfig(level=max(logging.DEBUG, log_level), format='%(levelname)s: %(message)s')

    # Create the directory if it does not exist
    if not path.exists(savepath):
        makedirs(savepath)
    
    with sync_playwright() as p:
        browser_instance = getattr(p, browser).launch(headless=headless)
        
        # Read URLs from file if provided
        if file:
            with open(file, 'r') as f:
                urls = [line.strip() for line in f if line.strip()]
        
        # Capture screenshots concurrently
        with ThreadPoolExecutor(max_workers=concurrent) as executor:
            for url in urls:
                executor.submit(save_screenshot, hostname, url, savepath, browser_instance, viewport, delay, format, auth, user_agent, retries)
        
        browser_instance.close()

if __name__ == '__main__':
    main()
