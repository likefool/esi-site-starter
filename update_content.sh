#!/bin/bash

# get this script's directory
SCRIPT_DIR=$(dirname "$(realpath "$0")")
# Change to the script's directory
cd "$SCRIPT_DIR" || exit 1

# Make sure git is installed
apt-get update && apt-get install -y git

# Create a temporary directory for cloning
TEMP_DIR=$(mktemp -d)

# Clone the repository
echo "Cloning repository..."
git clone https://github.com/likefool/note.git "$TEMP_DIR"

# Create content directory if it doesn't exist
mkdir -p ./content

# Copy all files from note to content directory
echo "Copying files to content directory..."
cp -r "$TEMP_DIR"/* ./content/


# Run conversion (replace this with your actual conversion command)
echo "Running conversion process..."

python convert_markdown.py /app
# Example conversion command - update this with your actual conversion logic
# python convert_md_to_html.py ./content

# Clean up
rm -rf "$TEMP_DIR"

echo "Content update complete!"