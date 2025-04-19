import httpx
from jinja2 import Environment, FileSystemLoader
from fastapi.responses import HTMLResponse  # Import added here
import os

# Configure Jinja2 to load templates from the correct directory
TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), "../")
env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))

BASE_URL = "http://127.0.0.1:8000"  # Replace with your server's base URL

async def fetch_fragment(url):
    """
    Fetches an HTML fragment from a given URL asynchronously.
    """
    # Ensure the URL is absolute
    if not url.startswith("http://") and not url.startswith("https://"):
        url = f"{BASE_URL}{url}"

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=5)
            response.raise_for_status()
            return response.text
    except httpx.RequestError as e:
        # Log the error and return a fallback message
        print(f"Error fetching ESI fragment from {url}: {e}")
        return "<!-- Error loading fragment -->"

async def render_with_esi(template_name, context=None):
    """
    Renders a template and processes ESI tags asynchronously.
    """
    if context is None:
        context = {}

    # Render the base template
    template = env.get_template(template_name)
    rendered_template = template.render(**context)

    # Process ESI tags
    processed_template = await process_esi_tags(rendered_template)

    return HTMLResponse(content=processed_template, media_type="text/html")

async def process_esi_tags(html_content):
    """
    Processes ESI tags in the given HTML content asynchronously.
    """
    import re

    esi_tag_pattern = re.compile(r'<esi:include src="([^"]+)" />')

    async def replace_esi_tags():
        """
        Generator to replace ESI tags asynchronously.
        """
        cursor = 0
        result = []

        for match in esi_tag_pattern.finditer(html_content):
            # Append the content before the match
            result.append(html_content[cursor:match.start()])

            # Fetch the fragment asynchronously
            url = match.group(1)
            fragment = await fetch_fragment(url)
            result.append(fragment)

            # Move the cursor forward
            cursor = match.end()

        # Append the remaining content after the last match
        result.append(html_content[cursor:])
        return ''.join(result)

    return await replace_esi_tags()