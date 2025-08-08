#!/usr/bin/env python

import asyncio
import aiohttp

from mcp.server.fastmcp import FastMCP
from bs4 import BeautifulSoup


mcp = FastMCP("sample_server", host="127.0.0.1",
              port=8001, log_level="DEBUG", debug=True)


@mcp.tool()
async def greet(name: str) -> dict:
  """Greet a user by name."""
  return {"message": f"Hello, {name}! Welcome to MCP....!"}


@mcp.tool()
async def add_numbers(a: float, b: float) -> dict:
  """Add two numbers and return the result."""
  result = a + b
  return {"a": a, "b": b, "sum": result}


@mcp.tool()
async def create_content(url: str) -> dict:
  """Create content at the specified URL."""
  # Simulate content creation

  async with aiohttp.ClientSession() as session:
    async with session.get(url) as response:
      if response.status == 200:
        html = await response.text()
        soup = BeautifulSoup(html, 'html.parser')

        title = soup.title.string if soup.title else "No title found"

        # Try to get description from meta tags
        description = "No description found"
        meta_desc = soup.find('meta', attrs={'name': 'description'}) or \
            soup.find('meta', attrs={'property': 'og:description'})
        if meta_desc and meta_desc.get('content'):
          description = meta_desc.get('content')

        return {
            "url": url,
            "title": title,
            "description": description
        }
      else:
        return {
            "url": url,
            "error": f"Failed to fetch URL: HTTP {response.status}"
        }

if __name__ == "__main__":
  mcp.run(transport="streamable-http")
