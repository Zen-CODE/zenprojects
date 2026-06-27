#!/usr/bin/env python3
import os
import sys
import argparse
import re
from mutagen.easyid3 import EasyID3


def sanitize_filename(name):
    """Remove or replace characters that are invalid in filenames."""
    # Replace invalid chars with underscores
    name = re.sub(r'[\\/*?:"<>|]', '_', name)
    # Strip leading/trailing whitespace
    return name.strip()
def format_track_number(track_str):
    """Format track number to be 2-digit zero-padded if numeric."""
    if not track_str:
        return None
    # Track numbers can be like "3", "03", "3/12"
    match = re.match(r'^(\d+)', track_str)
    if match:
        num = int(match.group(1))
        return f"{num:02d}"
    return track_str
def rename_mp3_files(directory, commit=False):
    if not os.path.isdir(directory):
        print(f"Error: Directory '{directory}' does not exist.", file=sys.stderr)
        sys.exit(1)
    print(f"Scanning directory: {os.path.abspath(directory)}")
    print(f"Mode: {'COMMIT (renaming files)' if commit else 'DRY RUN (no changes will be made)'}\n")
    try:
        files = os.listdir(directory)
    except Exception as e:
        print(f"Error listing directory: {e}", file=sys.stderr)
        sys.exit(1)
    mp3_files = [f for f in files if f.lower().endswith('.mp3')]
    
    if not mp3_files:
        print("No MP3 files found in the directory.")
        return
    success_count = 0
    skipped_count = 0
    error_count = 0
    for filename in sorted(mp3_files):
        filepath = os.path.join(directory, filename)
        
        try:
            audio = EasyID3(filepath)
            
            # Extract track number and title
            track_list = audio.get('tracknumber')
            title_list = audio.get('title')
            
            track_raw = track_list[0] if track_list else None
            title_raw = title_list[0] if title_list else None
            
            if not track_raw or not title_raw:
                missing = []
                if not track_raw: missing.append("track number")
                if not title_raw: missing.append("title")
                print(f"⚠️  Skipping: '{filename}' (Missing metadata: {', '.join(missing)})")
                skipped_count += 1
                continue
            
            track_num = format_track_number(track_raw)
            title = sanitize_filename(title_raw)
            
            new_filename = f"{track_num} - {title}.mp3"
            
            if filename == new_filename:
                print(f"ℹ️  Skipping: '{filename}' (Already correctly named)")
                skipped_count += 1
                continue
                
            new_filepath = os.path.join(directory, new_filename)
            
            print(f"👉 Proposed: '{filename}' ──> '{new_filename}'")
            
            if commit:
                # Check if target file already exists to prevent overwriting
                if os.path.exists(new_filepath):
                    print(f"❌ Error: Target file '{new_filename}' already exists. Skipping to avoid overwrite.")
                    error_count += 1
                    continue
                os.rename(filepath, new_filepath)
                success_count += 1
            else:
                success_count += 1
                
        except Exception as e:
            print(f"❌ Error processing '{filename}': {str(e)}")
            error_count += 1
    print("\n" + "="*60)
    if commit:
        print(f"Summary: Successfully renamed {success_count} files. Skipped {skipped_count}. Errors: {error_count}.")
    else:
        print(f"Summary (DRY RUN): Would rename {success_count} files. Skipped {skipped_count}. Errors: {error_count}.")
        print("To apply these changes, run the script with the '--commit' flag.")
    print("="*60)


def main():
    parser = argparse.ArgumentParser(
        description="Rename MP3 files in a directory to '<track number> - <track name>.mp3' using ID3 tags."
    )
    parser.add_argument(
        "directory", 
        nargs="?", 
        default=".", 
        help="Path to the directory containing MP3 files (default: current directory)"
    )
    parser.add_argument(
        "--commit", 
        action="store_true", 
        help="Perform the actual renaming (default is dry-run mode)"
    )
    
    args = parser.parse_args()
    rename_mp3_files(args.directory, commit=args.commit)

if __name__ == "__main__":
    # main()
    rename_mp3_files("/home/richard/Downloads/The Doors - STUDIO DISCOGRAPHY/1978 - An American Prayer", commit=True)