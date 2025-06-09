import io
import re
from typing import Dict

matchers = [
    re.compile(r"(\{\\fontsize\{[0-9\.]+\}\{1\})([0-9]+\.)( +[^\}]+\})"),
    re.compile(r"(\{\\fontsize\{[0-9\.]+\}\{1\})([0-9]+\.[0-9]+\.)( +[^\}]+\})"),
    re.compile(r"(\{\\fontsize\{[0-9\.]+\}\{1\})(\([0-9]{1,2}\))( +[^\}]+\})"),
    re.compile(r"(\{\\fontsize\{[0-9\.]+\}\{1\})(\([a-z]{1}\))( +[^\}]+\})"),  # This overlaps with the Roman numerals
    re.compile(r"(\{\\fontsize\{[0-9\.]+\}\{1\})(\([ivx]+\))( +[^\}]+\})")  # Overlaps with Latin alphabet
]

MAX_LATEX_DEPTH = 3

itemization_style = {
    0: r"[label=\arabic*.]",
    1: r"[label=\arabic{enumi}.\arabic*.]",
    2: r"[label=(\arabic*)]",
    3: r"[label=(\alph*)]",
    4: r"[label=(\roman*)]" # Too deep to use LaTeX's itemized lists.
}

MAX_DEPTH = list(itemization_style.keys())[-1]

def close_current_lists(starting_depth: int, current_headings: Dict[int, bool], output_file: io.TextIOWrapper) -> None:
    for i in range(starting_depth, MAX_DEPTH + 1):
        # Close out all deeper levels of enumeration
        if (current_headings).pop(i, None) and i <= MAX_LATEX_DEPTH:
            output_file.write(r"\end{enumerate}" + "\n")

def replace_integer_enumeration(input_file: io.TextIOWrapper, output_file: io.TextIOWrapper) -> None:
    current_headings: Dict[int, bool] = {}
    for line in input_file:
        if line.strip() == r"\end{document}" and current_headings.get(0):
            close_current_lists(0, current_headings, output_file)
        line_depth = None
        for lvl in range(MAX_DEPTH, -1, -1):
            # Go in reverse so that we can match Roman numerals before Latin characters
            matcher = matchers[lvl]
            matched = matcher.match(line)
            if matched:
                line_depth = lvl
                # Close deeper levels, as they've been abandoned
                close_current_lists(lvl + 1, current_headings, output_file)
                if lvl <= MAX_LATEX_DEPTH:
                    replacement_line = f"\\item {matched.group(1)}{matched.group(3)}\n"
                else:
                    replacement_line = line
                if not current_headings.get(lvl):
                    # Begin the list
                    if lvl <= MAX_LATEX_DEPTH:
                        output_file.write(r"\begin{enumerate}" + itemization_style[lvl] + "\n")
                    current_headings[lvl] = True
                output_file.write(replacement_line)
                break  # No need to consider higher-level enumerations
        if line_depth is None:
            output_file.write(line)

def replace_lines_in_files(input_filename: str, output_filename: str) -> None:
    with io.open(input_filename, "r") as input_file:
        with io.open(output_filename, "w") as output_file:
            replace_integer_enumeration(input_file, output_file)
            output_file.flush()


if __name__ == "__main__":
    replace_lines_in_files("main.tex", "replacement.tex")
