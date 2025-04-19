import os
import markdown
from pathlib import Path

# Define input and output directories
INPUT_DIR = "content"
OUTPUT_DIR = "public/content"

def convert_markdown_to_html(input_dir, output_dir):
    """
    Scans all .md files in the input directory, converts them to HTML,
    and saves them in the output directory while preserving the structure.
    """
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Walk through the input directory
    for root, _, files in os.walk(input_dir):
        for file in files:
            if file.endswith(".md"):
                # Full path to the input .md file
                input_path = os.path.join(root, file)

                # Read the Markdown content
                with open(input_path, "r", encoding="utf-8") as f:
                    markdown_content = f.read()

                # Convert Markdown to HTML
                html_content = markdown.markdown(markdown_content)

                # Determine the output path
                relative_path = os.path.relpath(root, input_dir)
                output_path = os.path.join(output_dir, relative_path, file.replace(".md", ".html"))

                # Ensure the output directory exists
                os.makedirs(os.path.dirname(output_path), exist_ok=True)

                # Write the HTML content to the output file
                with open(output_path, "w", encoding="utf-8") as f:
                    f.write(html_content)

                print(f"Converted: {input_path} -> {output_path}")

if __name__ == "__main__":
    # Run the conversion
    convert_markdown_to_html(INPUT_DIR, OUTPUT_DIR)