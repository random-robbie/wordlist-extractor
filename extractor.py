import argparse
from urllib.parse import urlparse

def extract_unique_names(urls):
    directories = set()

    for url in urls:
        path = urlparse(url).path
        directories.add(path)

    return directories

def is_valid_file(file_name):
    invalid_chars = [',','=','|','%','*','{','}']
    if any(char in file_name for char in invalid_chars):
        return False
    if file_name.endswith(('.jpg', '.jpeg', '.tif', '.woff2', '.png', '.svg', '.gif')):
        return False
    return True

def split_path(path):
    parts = [p for p in path.split("/") if p]  # Split the path and remove empty parts
    subfolders = parts[:-1]  # Get subfolders (excluding the file name or last part)
    file_name = parts[-1] if parts else ""  # Get the file name or last part
    return subfolders, file_name

def main(input_file, output_file):
    with open(input_file, 'r') as f:
        urls = f.read().splitlines()

    directories = extract_unique_names(urls)

    with open(output_file, 'w') as f:
        unique_subfolders = set()
        for directory in directories:
            subfolders, file_name = split_path(directory)
            if is_valid_file(file_name):
                unique_subfolders.update(subfolders)
                if file_name:
                    unique_subfolders.add(file_name)

        for subfolder in sorted(unique_subfolders):
            f.write(subfolder + '\n')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Extract unique directory names and file names from a list of URLs')
    parser.add_argument('input_file', help='Input file containing the list of URLs')
    parser.add_argument('output_file', help='Output file to store the unique directory and subfolder names')
    args = parser.parse_args()

    main(args.input_file, args.output_file)
