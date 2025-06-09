import io
import re

stripping_matcher = re.compile(r"(^.*)(\{\\fontsize\{[0-9\.]+\}\{1\})([^\}]+)(\})(.*)")

def replace_font_sizing(input_file: io.TextIOWrapper, output_file: io.TextIOWrapper) -> None:
    for line in input_file:
        matched = stripping_matcher.match(line)
        if matched:
            replacement = matched.group(1) + matched.group(3) + matched.group(5) + "\n"
        else:
            replacement = line
        output_file.write(replacement)

def replace_custom_font_size_in_file(input_filename: str, output_filename: str) -> None:
    with io.open(input_filename, "r") as input_file:
        with io.open(output_filename, "w") as output_file:
            replace_font_sizing(input_file, output_file)
            output_file.flush()


if __name__ == "__main__":
    replace_custom_font_size_in_file("main.tex", "replacement.tex")
