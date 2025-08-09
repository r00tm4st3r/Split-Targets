import argparse
import os
from urllib.parse import urlparse
import ipaddress
import shutil
import filecmp

GREEN = '\033[92m'
CYAN = '\033[96m'
YELLOW = '\033[93m'
RED = '\033[91m'
RESET = '\033[0m'

BANNER = rf"""{CYAN}

 __       _ _ _  _____                     _
/ _\_ __ | (_) |/__   \__ _ _ __ __ _  ___| |_ ___
\ \| '_ \| | | __|/ /\/ _` | '__/ _` |/ _ \ __/ __|
_\ \ |_) | | | |_/ / | (_| | | | (_| |  __/ |_\__ \
\__/ .__/|_|_|\__\/   \__,_|_|  \__, |\___|\__|___/
   |_|                          |___/

{RESET}"""

def extract_ip(url_line):
    line = url_line.strip()
    if not line:
        return None
    try:
        ipaddress.ip_address(line)
        return line
    except ValueError:
        pass
    if '.' in line and '/' not in line and ':' not in line:
        return line
    if "://" not in line:
        line = "http://" + line
    try:
        return urlparse(line).hostname
    except:
        return None

def should_exclude_ip(ip_line, exclude_prefixes):
    ip = extract_ip(ip_line)
    if not ip:
        return False
    if any(ip.startswith(prefix) for prefix in exclude_prefixes):
        return True
    try:
        parsed_ip = ipaddress.ip_address(ip)
        if parsed_ip.is_private:
            return True
    except:
        pass
    return False

def write_deduplicated_lines(output_file, new_lines):
    seen = set()
    if os.path.exists(output_file):
        with open(output_file, 'r') as f:
            for line in f:
                seen.add(line.strip())
        mode = 'a'
    else:
        mode = 'w'
    written = 0
    with open(output_file, mode) as out:
        for line in new_lines:
            clean = line.strip()
            if clean and clean not in seen:
                out.write(clean + '\n')
                seen.add(clean)
                written += 1
    return written

def split_file(input_path, lines_per_file=10000, start_index=2, exclude_prefixes=None, dry_run=False):
    if exclude_prefixes is None:
        exclude_prefixes = ["23.", "104.", "173."]
    input_basename = os.path.basename(input_path).rsplit('.', 1)[0]
    cwd = os.getcwd()
    base_output_name = os.path.join(cwd, input_basename)
    try:
        with open(input_path, 'r') as infile:
            file_index = start_index
            line_buffer = []
            valid_total = 0
            estimated_chunks = 0
            created_files = []
            any_written = False
            for line in infile:
                line = line.strip()
                if not line or should_exclude_ip(line, exclude_prefixes):
                    continue
                line_buffer.append(line)
                valid_total += 1
                if len(line_buffer) == lines_per_file:
                    estimated_chunks += 1
                    if not dry_run:
                        output_file = f"{base_output_name}-{file_index}.txt"
                        written = write_deduplicated_lines(output_file, line_buffer)
                        print(f"{GREEN}[+]{RESET} Appended {written} new unique lines to {output_file}")
                        if written > 0:
                            any_written = True
                        created_files.append(output_file)
                    line_buffer = []
                    file_index += 1
            if line_buffer:
                estimated_chunks += 1
                if not dry_run:
                    output_file = f"{base_output_name}-{file_index}.txt"
                    written = write_deduplicated_lines(output_file, line_buffer)
                    print(f"{GREEN}[+]{RESET} Appended {written} new unique lines to {output_file}")
                    if written > 0:
                        any_written = True
                    created_files.append(output_file)
            if dry_run:
                print(f"{YELLOW}[i]{RESET} Dry run complete — {valid_total} valid lines would be split into {estimated_chunks} files.")
            else:
                print(f"{GREEN}[✓]{RESET} Done! {valid_total} valid URLs processed.")
            return created_files, base_output_name, any_written
    except FileNotFoundError:
        print(f"{RED}[!]{RESET} File not found: {input_path}")
        return [], None, False
    except Exception as e:
        print(f"{RED}[!]{RESET} An error occurred: {e}")
        return [], None, False

def ask_yes_no(prompt):
    while True:
        answer = input(prompt).strip().lower()
        if answer == 'y':
            return True
        elif answer == 'n':
            return False
        else:
            print(f"{RED}Invalid input. Please enter 'y' or 'n'.{RESET}")

def ask_copy_move(prompt):
    while True:
        answer = input(prompt).strip().lower()
        if answer == 'c':
            return 'copy'
        elif answer == 'm':
            return 'move'
        else:
            print(f"{RED}Invalid input. Please enter 'c' for copy or 'm' for move.{RESET}")

def ask_move_files(created_files, base_output_name, any_written):
    if not created_files:
        return

    if ask_yes_no("Store the files in the current directory? (y/n): "):
        print(f"{GREEN}[i]{RESET} Files kept in the current directory.")
        if not any_written:
            print(f"{YELLOW}[i]{RESET} No new lines added — files already contain all data.")
        return


    while True:
        new_dir = input("Enter the directory path where you want to store the files: ").strip()
        if new_dir:
            break
        else:
            print(f"{RED}Invalid input. Directory path cannot be empty.{RESET}")

    if not os.path.exists(new_dir):
        try:
            os.makedirs(new_dir)
            print(f"{GREEN}[i]{RESET} Created directory: {new_dir}")
        except Exception as e:
            print(f"{RED}[!]{RESET} Could not create directory: {e}")
            return

    action = ask_copy_move("Copy or move the files? (c/m): ")

    all_identical_at_dest = True
    for filepath in created_files:
        filename = os.path.basename(filepath)
        dest_path = os.path.join(new_dir, filename)
        if not os.path.exists(dest_path) or not filecmp.cmp(filepath, dest_path, shallow=False):
            all_identical_at_dest = False
            break

    for filepath in created_files:
        filename = os.path.basename(filepath)
        dest = os.path.join(new_dir, filename)
        try:
            if action == 'move':
                shutil.move(filepath, dest)
            else:
                shutil.copy2(filepath, dest)
        except Exception as e:
            print(f"{RED}[!]{RESET} Could not {action} {filename}: {e}")

    verb = "Moved" if action == 'move' else "Copied"
    print(f"{GREEN}[i]{RESET} {verb} {len(created_files)} files to {new_dir}")

    if not any_written and all_identical_at_dest:
        print(f"{YELLOW}[i]{RESET} No new lines added — destination already contained identical files.")

if __name__ == "__main__":
    print(BANNER)
    try:
        parser = argparse.ArgumentParser(
            description="Split and clean a large URL/IP target list into smaller chunk files with deduplication."
        )
        parser.add_argument("-i", "--input", required=True, help="Path to input .txt file")
        parser.add_argument("-s", "--start", type=int, default=2, help="Start index for output files (default: 2)")
        parser.add_argument("-n", "--lines", type=int, default=10000, help="Lines per file (default: 10000)")
        parser.add_argument("-x", "--exclude", help="Comma-separated IP prefixes to exclude (e.g. 23,104,173)")
        parser.add_argument("--dry-run", action="store_true", help="Show how many lines/files would be created without writing output")
        args = parser.parse_args()

        if args.exclude:
            exclude_prefixes = [
                prefix.strip() + '.' if not prefix.strip().endswith('.') else prefix.strip()
                for prefix in args.exclude.split(',')
            ]
        else:
            exclude_prefixes = ["23.", "104.", "173."]

        created_files, base_output_name, any_written = split_file(
            input_path=args.input,
            lines_per_file=args.lines,
            start_index=args.start,
            exclude_prefixes=exclude_prefixes,
            dry_run=args.dry_run
        )

        if not args.dry_run:
            ask_move_files(created_files, base_output_name, any_written)

    except KeyboardInterrupt:
        print(f"\n{YELLOW}[!]{RESET} Process interrupted by user. Exiting safely.")

