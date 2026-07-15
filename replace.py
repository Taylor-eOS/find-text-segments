import os
import sys

"""
Searches and replaces a string in all files in a folder.
"""

def replace_in_files():
    folder = input("Folder path: ").strip()
    if not os.path.isdir(folder):
        print(f"Directory not found: {folder}", file=sys.stderr)
        return
    while True:
        search_term = input("Search term (Enter to quit): ")
        if not search_term:
            break
        replacement_term = input("Replacement term: ")
        modified_files_count = 0
        for root, _, files in os.walk(folder):
            for filename in files:
                item_path = os.path.join(root, filename)
                try:
                    with open(item_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                except (UnicodeDecodeError, OSError) as e:
                    print(f"Warning: could not read {item_path}. Error: {e}", file=sys.stderr)
                    continue
                if search_term in content:
                    new_content = content.replace(search_term, replacement_term)
                    try:
                        with open(item_path, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                        modified_files_count += 1
                    except OSError as e:
                        print(f"Warning: could not write to {item_path}. Error: {e}", file=sys.stderr)
        print(f"Completed replacement in {modified_files_count} files.")

if __name__ == '__main__':
    replace_in_files()
