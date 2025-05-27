#!/bin/bash

echo "Building ELNADA Application..."

# Check if we're on Windows
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    # Run the batch file
    ./build.bat
else
    echo "This script is designed to run on Windows only."
    echo "Please run build.bat directly on Windows."
    exit 1
fi 


# ./build.sh    