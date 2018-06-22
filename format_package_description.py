import re

import gi
from gi.repository import GLib


# TODO: Disable ‘o’ in locales where it is a word.
# ‘-’ must come first or last so this can be used within ‘[]’ in a regular
# expression.
bullets = '-*+.o'

def format_package_description(description):
    description = GLib.markup_escape_text(description)
    if description_needs_strict_mode(description):
        return strict_format_description(description)
    return loose_format_description(description)

def description_needs_strict_mode(description):
    """
        Decide whether the package description needs to be formatted with
        strict_format_description instead of format_description.  This means
        that we cannot guess which lines are bullet points.
    """
    for bullet in bullets:
        indent_strings = re.findall(
            r'^ +{} '.format(re.escape(bullet)), description, re.MULTILINE)
        if not all(len(i) == len(indent_strings[0]) for i in indent_strings):
            return True
        if len(indent_strings) == 1:
            return True
        if len(indent_strings) > 0:
            if len(indent_strings[0]) > 16:
                return True
            # Check for the bullet in the same position with non-blanks before
            # it
            indent = len(indent_strings[0]) - 3
            if indent > 0:
                for line in description.splitlines():
                    if (
                        line[indent:indent+3] == ' {} '.format(bullet)
                        and not line[:indent].isspace()
                    ):
                        return True
    return False

def strict_format_description(description):
    """Format a package description strictly according to the Debian policy."""
    # List of strings to be joined to rebuild ‘description’
    desc_list = []
    # TODO: Even this one is kind of messy, and it really has a lot in common
    # with loose_format_description.  Maybe we should combine them?
    prev_blank = True
    for line in description.splitlines():
        if line.startswith('.'):
            prev_blank = True
            if len(line) > 1:
                # Extended syntax — ignore
                continue
            # Paragraph end
            desc_list.append('\n<span size="xx-small">\n</span>')
            continue
        if line.startswith(' '):
            # Preformatted line
            if not prev_blank:
                # Start a new line
                desc_list.append('\n')
            desc_list.append('<tt>{}</tt>'.format(line[1:]))
        else:
            # Normal line
            if not prev_blank:
                desc_list.append(' ')
            desc_list.append(line)
        prev_blank = False
    return ''.join(desc_list)

def loose_format_description(description):
    """
        Format a package description, trying to identify bullet points and
        then combining them onto one logical line with a nice bullet character.
    """
    # List of strings to be joined to rebuild ‘description’
    desc_list = []
    # TODO: Messy and still doesn’t work
    bullet_depth = []
    prev_blank = True
    for line in description.splitlines():
        if line.startswith('.'):
            prev_blank = True
            if len(line) > 1:
                # Extended syntax — ignore
                continue
            # Paragraph end
            desc_list.append('\n<span size="xx-small">\n</span>')
            continue
        # Indentation level
        indent = re.search(r'^ *', line).end()
        while len(bullet_depth) > 0 and indent < bullet_depth[-1]:
            bullet_depth.pop()
        # Check for bullet point
        match = re.match(fr' *[{bullets}] (.*)', line)
        if match:
            # Found bullet point
            # ‘indent + 2’ is the indentation level of the bullet point’s
            # text
            bullet_depth.append(indent + 2)
            if not prev_blank:
                # Start a new line
                desc_list.append('\n')
            # Output tabs for indentation
            desc_list.append('\t' * indent)
            # Output bullet point
            desc_list.append('•\t')
            # Output first line of text
            desc_list.append(match.group(1))
        elif (
            indent == 0
            or len(bullet_depth) > 0 and indent == bullet_depth[-1]
        ):
            if not prev_blank:
                # Continuation line
                desc_list.append(' ')
            desc_list.append(line.lstrip())
        else:
            # Preformatted line
            if not prev_blank:
                # Start a new line
                desc_list.append('\n')
            desc_list.append('<tt>{}</tt>'.format(line[1:]))
        prev_blank = False
    return ''.join(desc_list)
