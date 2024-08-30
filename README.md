# Webshot

Webshot fixes the issue of having to open ports on develepment websites to show the website to your friends.

## Installation

Install via pip:
```bash
pip install webpic      
```

## Usage

Usage: webpic [OPTIONS] HOSTNAME SAVEPATH [URLS]...

Options:
  -f, --file PATH  File containing URLs separated by newlines.

### Examples

Let's say you have a django development server in your local machine with 2 urls: /home and /help and you want to save them in "screenshots"

```bash
webpic http://127.0.0.1:8000 ./screenshots home help
```

Or, if you have a long list of urls, put them in a file with the urls separated by new lines and run

```bash
webpic -f urls.txt http://127.0.0.1:8000 ./screenshots 
```