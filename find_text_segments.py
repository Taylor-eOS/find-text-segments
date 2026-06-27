import os
import json

FIELD_NAME = 'writings_path'
SETTINGS_FILE = 'settings_file'

_state = {
    SETTINGS_FILE: '.script_settings.json',
    FIELD_NAME: ''
}

def _prompt_and_save_path():
    user_path = input("Settings file or entry not found. Enter default path: ").strip()
    try:
        with open(_state[SETTINGS_FILE], 'r') as f:
            settings_data = json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        settings_data = {}
    settings_data[FIELD_NAME] = user_path
    with open(_state[SETTINGS_FILE], 'w') as f:
        json.dump(settings_data, f, indent=2)
    _state[FIELD_NAME] = user_path

def load_writings_path():
    if not os.path.exists(_state[SETTINGS_FILE]):
        _prompt_and_save_path()
        return
    with open(_state[SETTINGS_FILE], 'r') as f:
        try:
            settings_data = json.load(f)
            _state[FIELD_NAME] = settings_data.get(FIELD_NAME, '')
        except json.JSONDecodeError:
            _state[FIELD_NAME] = ''
    if not _state[FIELD_NAME]:
        _prompt_and_save_path()

def get_yes_no(prompt, default=False):
    resp = input(f"{prompt} [{'Y/n' if default else 'y/N'}]: ").strip().lower()
    if not resp:
        return default
    return resp in ('y', 'yes')

def sanitize_filename(term):
    term = term.lower().strip()
    out_chars = []
    prev_underscore = False
    for c in term:
        if c.isalnum():
            out_chars.append(c)
            prev_underscore = False
        elif c in ' _-':
            if not prev_underscore:
                out_chars.append('_')
                prev_underscore = True
        else:
            continue
    name = ''.join(out_chars).strip('_')
    return name or "search"

def collect_matching_segments(main_folder=None, output_file=None):
    if main_folder is None:
        main_folder = input("Enter main folder path (default to JSON): ").strip() or _state[FIELD_NAME]
    raw_input = input("Enter AND search strings (comma-separated, spaces permitted): ").strip()
    if not raw_input:
        print("No search string given.")
        return
    search_terms = [term.strip().lower() for term in raw_input.split(',') if term.strip()]
    if not search_terms:
        print("No valid search terms found.")
        return
    include_assistant = get_yes_no("Include Assistant segments?", True)
    include_user = get_yes_no("Include User segments?", True)
    first_term = search_terms[0]
    safe_name = sanitize_filename(first_term)
    output_file = output_file or (safe_name + "_segments.txt")
    found_segments = set()
    if not os.path.isdir(main_folder):
        print(f"Main folder not found: {main_folder}")
        return
    for item in os.listdir(main_folder):
        item_path = os.path.join(main_folder, item)
        if os.path.isdir(item_path):
            for filename in os.listdir(item_path):
                if filename.lower().endswith('.txt'):
                    file_path = os.path.join(item_path, filename)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read().strip()
                    except Exception as e:
                        print(f"Warning: could not read {file_path}, skipping. Error: {e}")
                        continue
                    raw_parts = content.replace('\n\n', '\n---\n').split('---')
                    segments = [part.strip() for part in raw_parts if part.strip()]
                    for segment in segments:
                        segment_lower = segment.lower()
                        if not all(term in segment_lower for term in search_terms):
                            continue
                        stripped = segment.lstrip()
                        is_assistant = stripped.lower().startswith('assistant:')
                        is_user = stripped.lower().startswith('user:')
                        if is_assistant and not include_assistant:
                            continue
                        if is_user and not include_user:
                            continue
                        found_segments.add(segment)
    if not found_segments:
        print(f"No segments found containing all of: {', '.join(search_terms)}")
        return
    try:
        with open(output_file, 'w', encoding='utf-8') as out:
            for i, segment in enumerate(sorted(found_segments), 1):
                out.write(segment)
                if i < len(found_segments):
                    out.write('\n\n')
    except Exception as e:
        print(f"Error writing file {output_file}: {e}")
        return
    print(f"Found {len(found_segments)} unique matching segments.")
    print(f"Results written to {output_file}")

if __name__ == '__main__':
    load_writings_path()
    collect_matching_segments()

