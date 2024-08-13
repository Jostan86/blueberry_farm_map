 #!/bin/bash

# Check if the correct number of arguments are provided
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 input.kmz output.kml"
    echo "For example: $0 ../data_map_2/collected_data.kmz ../data_map_2/collected_data.kml"
    exit 1
fi

# Assign input arguments to variables
input_kmz="$1"
output_kml="$2"

# Create a temporary directory to work in
temp_dir=$(mktemp -d)

# Copy the .kmz file to a .zip file
cp "$input_kmz" "$temp_dir/converted.zip"

# Unzip the .zip file in the temporary directory
unzip "$temp_dir/converted.zip" -d "$temp_dir"

# Copy the extracted doc.kml file to the desired output file name
cp "$temp_dir/doc.kml" "$output_kml"

# Clean up: remove the temporary directory and its contents
rm -rf "$temp_dir"

echo "Conversion complete: $output_kml created."
