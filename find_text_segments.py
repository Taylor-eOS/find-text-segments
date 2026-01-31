import os
import re
from settings import WRITINGS_PATH

def collect_matching_segments(main_folder, output_file):
    raw_input = input("Enter search strings (comma-separated): ").strip()
    if not raw_input:
        print("No search string given, exiting.")
        return
    search_terms = [term.strip().lower() for term in raw_input.split(',') if term.strip()]
    if not search_terms:
        print("No valid search terms found, exiting.")
        return
    first_term = search_terms[0]
    safe_name = re.sub(r'[^a-z0-9\s_-]', '', first_term)
    safe_name = re.sub(r'[\s_-]+', '_', safe_name.strip())
    if not safe_name:
        safe_name = "search"
   
    output_file = safe_name + "_segments.txt"
    found_segments = set()
    for item in os.listdir(main_folder):
        item_path = os.path.join(main_folder, item)
        if os.path.isdir(item_path):
            for filename in os.listdir(item_path):
                if filename.lower().endswith('.txt'):
                    file_path = os.path.join(item_path, filename)
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read().strip()
                    raw_parts = content.replace('\n\n', '\n---\n').split('---')
                    segments = [part.strip() for part in raw_parts if part.strip()]
                    for segment in segments:
                        segment_lower = segment.lower()
                        if any(term in segment_lower for term in search_terms):
                            found_segments.add(segment)
    if not found_segments:
        print(f"No segments found containing any of: {', '.join(search_terms)}")
        return
    with open(output_file, 'w', encoding='utf-8') as out:
        for i, segment in enumerate(sorted(found_segments), 1):
            out.write(segment)
            if i < len(found_segments):
                out.write('\n\n')
    print(f"Found {len(found_segments)} unique matching segments.")
    print(f"Results written to {output_file}")

if __name__ == '__main__':
    main_folder = WRITINGS_PATH
    collect_matching_segments(main_folder, None)

