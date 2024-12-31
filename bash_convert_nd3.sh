#!/bin/bash

# Check for correct number of arguments
if [ "$#" -ne 3 ]; then
    echo "Usage: $0 <nd3_converter_script> <source_dir> <output_dir>"
    exit 1
fi

# Arguments
ND3_CONVERTER_SCRIPT=$1
SOURCE_DIR=$2
OUTPUT_DIR=$3

# Check if the Python converter script exists
if [ ! -f "$ND3_CONVERTER_SCRIPT" ]; then
    echo "Error: ND3 converter script not found: $ND3_CONVERTER_SCRIPT"
    exit 1
fi

# Check if source directory exists
if [ ! -d "$SOURCE_DIR" ]; then
    echo "Error: Source directory not found: $SOURCE_DIR"
    exit 1
fi

# Create the output directory if it doesn't exist
mkdir -p "$OUTPUT_DIR"

# Loop through all .tar.gz files in the source directory
for TAR_FILE in "$SOURCE_DIR"/*.tar.gz; do
    # Extract the base name of the file (without extension)
    BASENAME=$(basename "$TAR_FILE" .tar.gz)
    # Set the output ND3 file path
    OUTPUT_FILE="$OUTPUT_DIR/$BASENAME.ND3"

    # Convert the .tar.gz file to .ND3
    echo "Converting $TAR_FILE to $OUTPUT_FILE..."
    python3 "$ND3_CONVERTER_SCRIPT" "$TAR_FILE" "$OUTPUT_FILE"

    # Check if conversion succeeded
    if [ $? -eq 0 ]; then
        echo "Successfully converted $TAR_FILE to $OUTPUT_FILE"
    else
        echo "Failed to convert $TAR_FILE to $OUTPUT_FILE"
    fi
done

echo "Batch conversion complete."
