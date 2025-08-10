#!/usr/bin/env python

import argparse
import asyncio
import sys
from email import parser

import aiohttp
from bs4 import BeautifulSoup
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("sample_server", host="127.0.0.1",
              port=8001, log_level="DEBUG", debug=True)


@mcp.tool()
async def greet(name: str) -> dict:
  """Greet a user by name."""
  return {"message": f"Hello, {name}! Welcome to MCP....!"}


@mcp.tool()
async def add_numbers(a: float, b: float) -> dict:
  """Add two numbers and return the result."""
  result = a + b + 2
  return {"a": a, "b": b, "sum": result}


@mcp.tool()
async def extract_metadata(url: str) -> dict:
  """Extract metadata from the specified URL."""
  async with aiohttp.ClientSession() as session:
    async with session.get(url) as response:
      if response.status == 200:
        html = await response.text()
        soup = BeautifulSoup(html, 'html.parser')

        title = soup.title.string.strip(
        ) if soup.title and soup.title.string else "No title found"

        description = "No description found"
        meta_desc = soup.find('meta', attrs={'name': 'description'}) or \
            soup.find('meta', attrs={'property': 'og:description'})
        if meta_desc and meta_desc.get('content'):
          description = meta_desc.get('content')

        keywords = None
        meta_keywords = soup.find('meta', attrs={'name': 'keywords'})
        if meta_keywords and meta_keywords.get('content'):
          keywords = meta_keywords.get('content').strip()

        og_data = {}
        for tag in soup.find_all('meta'):
          if tag.get('property', '').startswith('og:'):
            og_data[tag.get('property')] = tag.get('content', '').strip()

        favicon = None
        icon_link = soup.find('link', rel=lambda x: x and 'icon' in x.lower())
        if icon_link and icon_link.get('href'):
          favicon = icon_link.get('href')

        canonical = None
        canonical_link = soup.find('link', rel='canonical')
        if canonical_link and canonical_link.get('href'):
          canonical = canonical_link.get('href')

        return {
            "url": url,
            "title": title,
            "description": description,
            "keywords": keywords,
            "favicon": favicon,
            "canonical": canonical,
            "open_graph": og_data
        }
      else:
        return {
            "url": url,
            "error": f"Failed to fetch URL: HTTP {response.status}"
        }

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("--transport", help="Transport method.")
  args = parser.parse_args()
  transport = "stdio"
  if args.transport == "streamable-http":
    print(f"Options provided: {args.transport}", file=sys.stderr)
    transport = "streamable-http"

  print("Starting MCP server...", file=sys.stderr)
  mcp.run(transport=transport)
