import io
import re
from typing import List

stripping_matcher = re.compile(r"(^.*)(\{\\fontsize\{[0-9\.]+\}\{1\})([^\}]+)(\})(.*)")

def strip_empty_lines(input_file: io.TextIOWrapper, output_file: io.TextIOWrapper) -> None:
    batch: List[str] = []
    has_document_begun = False
    for line in input_file:
        if line.startswith("\\") or line.startswith("("):
            # Recall that there was a maximum enumeration depth
            output_file.write("\n" + "".join(batch) + ("\n" if has_document_begun else ""))
            batch.clear()
        if line.startswith(r"\newpage"):
            output_file.write(line)
            continue
        if line.startswith(r"\begin{document}"):
            has_document_begun = True
        batch.append(line.rstrip("\n"))
    output_file.write("".join(batch))

def strip_empty_lines_in_file(input_filename: str, output_filename: str) -> None:
    with io.open(input_filename, "r") as input_file:
        with io.open(output_filename, "w") as output_file:
            strip_empty_lines(input_file, output_file)
            output_file.flush()


if __name__ == "__main__":
    strip_empty_lines_in_file("main.tex", "replacement.tex")
