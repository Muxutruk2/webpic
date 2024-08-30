import click
from playwright.sync_api import sync_playwright
from os import path, makedirs

def save_screenshot(hostname, url, folder, browser):
    # Create a safe file path by replacing '/' with '-'
    savepath = path.join(folder, f"{url.replace('/', '-')}.png")
    
    page = browser.new_page()
    
    # Ensure the hostname ends with a slash
    if not hostname.endswith("/"):
        hostname += "/"
    
    # Ensure the URL does not start with a slash
    if url.startswith("/"):
        url = url[1:]
    
    # Navigate to the full URL and take a screenshot
    page.goto(f"{hostname}{url}")
    page.screenshot(full_page=True, path=savepath)

@click.command()
@click.argument('hostname')
@click.argument('savepath')
@click.argument('urls', nargs=-1, required=False)
@click.option('--file', '-f', type=click.Path(exists=True), help="File containing URLs separated by newlines.")
def main(hostname, savepath, urls, file):
    """A CLI tool to take automated screenshots of webpages"""
    
    # Create the directory if it does not exist
    if not path.exists(savepath):
        makedirs(savepath)
    
    with sync_playwright() as p:
        browser = p.chromium.launch()
        
        # Read URLs from file if provided
        if file:
            with open(file, 'r') as f:
                urls = [line.strip() for line in f if line.strip()]
        
        # Capture screenshots for each URL
        for url in urls:
            save_screenshot(hostname, url, savepath, browser)
        
        browser.close()

if __name__ == '__main__':
    main()
