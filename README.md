# Webpic

Webpic fixes the issue of having to open ports on development websites to show the website to your friends by automatically taking screenshots of specified pages.

## Installation

Install via pip:

```bash
pip install webpic
```

## Usage

```bash
webpic [OPTIONS] HOSTNAME SAVEPATH [URLS]...
```

### Options

- **`-f, --file PATH`**  
  File containing URLs separated by newlines.

- **`-b, --browser [chromium|firefox|webkit]`**  
  Choose the browser engine to use. Default is `chromium`.

- **`-v, --viewport WIDTH HEIGHT`**  
  Specify the viewport size as WIDTH HEIGHT. Default is `1280x720`.

- **`-d, --delay SECONDS`**  
  Time to wait before taking a screenshot, in seconds. Default is `0`.

- **`-fmt, --format [png|jpeg]`**  
  Screenshot format. Default is `png`.

- **`-a, --auth USERNAME PASSWORD`**  
  Provide basic HTTP authentication as USERNAME PASSWORD.

- **`--headless/--headful`**  
  Run browser in headless mode (default) or headful mode.

- **`-ua, --user-agent TEXT`**  
  Specify a custom User-Agent string.

- **`-r, --retries INTEGER`**  
  Number of retry attempts if a screenshot fails. Default is `3`.

- **`-c, --concurrent INTEGER`**  
  Number of concurrent screenshots to capture. Default is `1`.

- **`-v, --verbose`**  
  Increase verbosity of output. Can be used multiple times for more detailed output.

### Examples

Let's say you have a Django development server running on your local machine with URLs `/home` and `/help`, and you want to save them in the `screenshots` directory:

```bash
webpic http://127.0.0.1:8000 ./screenshots home help
```

Or, if you have a long list of URLs, put them in a file with the URLs separated by new lines and run:

```bash
webpic -f urls.txt http://127.0.0.1:8000 ./screenshots
```

