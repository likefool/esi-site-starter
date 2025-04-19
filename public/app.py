from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from utils.esi_handler import render_with_esi
import os

app = FastAPI()

# Serve static HTML files from the fragments directory
FRAGMENTS_DIR = os.path.join(os.path.dirname(__file__), "fragments")
app.mount("/fragments", StaticFiles(directory=FRAGMENTS_DIR, html=True), name="fragments")

# Serve static assets (CSS, JS, images) from the assets directory
ASSETS_DIR = os.path.join(os.path.dirname(__file__), "assets")
app.mount("/assets", StaticFiles(directory=ASSETS_DIR), name="assets")

# Serve static HTML files from the content directory
CONTENT_DIR = os.path.join(os.path.dirname(__file__), "content")
app.mount("/content", StaticFiles(directory=CONTENT_DIR, html=True), name="content")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    # Render the template with ESI processing
    return await render_with_esi("templates/index.html", {"title": "Home Page"})

@app.get("/post/{file_path:path}", response_class=HTMLResponse)
async def display_post(file_path: str):
    """
    Render the post.html template with the file_path parameter.
    """
    # Check if the file exists in the content directory
    file_path_with_extension = os.path.join(CONTENT_DIR, file_path + ".html")
    if not os.path.exists(file_path_with_extension):
        raise HTTPException(status_code=404, detail="File not found")

    # Render the post.html template with the file_path parameter
    return await render_with_esi("templates/post.html", {"filename": file_path})

# Run the app using `uvicorn` if this script is executed directly
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)