import sys
import re
import os


def get_lines(path):
    with open(path, "r") as f:
        lines = f.readlines()
    return lines


def get_abbreviations(line):
    matches = re.finditer(r" ([A-Z-]{2,}) ", line)
    return [match.group(1) for match in matches] if matches is not None else []


def get_link(line):
    link_pattern = re.compile(r"\\(include||input){(.+)}")
    return link_pattern.match(line)


data = {}
abbreviations = []

def _print(*text, level=0):
    return None
    tabs = "".join(["\t"] * level)
    print(tabs, *text)

def find_all_links(root_dir, path, data, level):

    
    _print("path", path, level=level)
    #directory = "/".join(path.split("/")[:-1])

    for line_number, line in enumerate(get_lines(path)):

        line_abbreviations = get_abbreviations(line)
        if len(line_abbreviations) > 0:
            _print("\t", f"[{line_number}]", line_abbreviations, level=level)
            data = [*data, *line_abbreviations]

        link = get_link(line)
        if link is not None:
            key = link.group(2)
            _print("\t", f"[{line_number}]", "link", key, level=level)
            fn = key
            if ".tex" not in key:
                fn += ".tex"

            child_path = os.path.join(root_dir, fn)
            _print("\t", f"[{line_number}]", "child_path", child_path, os.path.exists(child_path), level=level)
            if os.path.exists(child_path):
                data = find_all_links(root_dir, child_path, data, level + 1)

    return data

root_file = sys.argv[1]
root_dir = "/".join(root_file.split("/")[:-1])
print("root_file", root_file)

data = find_all_links(root_dir, root_file, abbreviations, 0)

for i, abbr in enumerate(sorted(set(data))):
    print("\\nomenclature{" + abbr + "}{}")

