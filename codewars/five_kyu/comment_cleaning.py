def strip_comments(comment: str, markers: list[str]) -> str:
    comments_by_lines = comment.split("\n")
    stripped_lines: list[str] = []
    for line in comments_by_lines:
        new_line = ""
        for character in line:
            if character in markers:
                break
            new_line += character

        new_line = new_line.rstrip()
        stripped_lines.append(new_line)

    return "\n".join(stripped_lines)

def test_group():
    assert strip_comments('apples, pears # and bananas\ngrapes\nbananas !apples', ['#', '!']) == 'apples, pears\ngrapes\nbananas'
    assert strip_comments('a #b\nc\nd $e f g', ['#', '$']) == 'a\nc\nd'
    assert strip_comments(' a #b\nc\nd $e f g', ['#', '$']) == ' a\nc\nd'