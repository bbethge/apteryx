import io
import itertools
import re

import gi
from gi.repository import GLib


# TODO: Disable ‘o’ in locales where it is a word.
# ‘-’ must come first or last so this can be used within ‘[]’ in a regular
# expression.
bullets = '-*+.o'

def can_parse_bullets(description):
    """
        Decide whether we can detect that certain lines in ‘description’
        are meant to be bullet points and we can reformat them
        appropriately.
    """
    bullet_types = _get_bullet_types(description)
    if bullet_types == [] or _has_singleton(bullet_types):
        # An indentation level that only occurs once could be a bullet-
        # like symbol not used as a bullet.
        return False
    # Remove repeats from bullet_types.
    bullet_types = [bt for bt, _grp in itertools.groupby(bullet_types)]
    for bt in bullet_types:
        # Check for the bullet in the same position with non-blanks
        # before it.
        for line in description.splitlines():
            if (line[bt.indent-1 :].startswith(f' {bt.character} ')
                    and not line[:bt.indent].isspace()):
                return False
    return True


class _BulletType:
    __slots__ = 'indent', 'text_indent', 'character'

    def __init__(self, indent, text_indent, character):
        self.indent = indent
        self.text_indent = text_indent
        self.character = character

    def __repr__(self):
        return ('_BulletType('
                f'{self.indent}, {self.text_indent}, {self.character!r})')

    def __eq__(self, other):
        return (self.indent == other.indent
                and self.text_indent == other.text_indent
                and self.character == other.character)

    def __lt__(self, other):
        return (self.indent < other.indent
                or (self.indent == other.indent
                    and self.character < other.character))

    _detect_re = re.compile(
        fr'^(?P<indent> *)(?P<bullet>[{bullets}]) +(?P<content>.*)')

    @classmethod
    def detect(cls, string):
        match = cls._detect_re.match(string)
        if match:
            return cls(indent=len(match['indent']),
                       text_indent=match.start('content'),
                       character=match['bullet'])
        else:
            return None


def _get_bullet_types(description):
    bullet_types = [_BulletType.detect(line)
                    for line in description.splitlines()]
    return sorted(bt for bt in bullet_types if bt is not None)


def _count_iter(iter_):
    n = 0
    for i in iter_:
        n += 1
    return n


def _has_singleton(bullet_types):
    """
        Return whether there is a bullet type that only occurs once in
        bullet_types.
    """
    for _key, group in itertools.groupby(bullet_types,
                                         key = lambda bt: bt.indent):
        if _count_iter(group) == 1:
            return True
    else:
        return False


class _DescriptionFormatter:
    def __init__(self):
        self.output = io.StringIO()
        self.prev_blank = True

    def get_value(self):
        return self.output.getvalue()

    def output_paragraph_break(self):
        self.output.write('\n<span size="xx-small">\n</span>')
        self.prev_blank = True

    def _start_new_line(self):
        if not self.prev_blank:
            self.output.write('\n')

    def output_preformatted(self, text):
        self._start_new_line()
        self.output.write('<tt>')
        self.output.write(text)
        self.output.write('</tt>')
        self.prev_blank = False

    def output_bullet_line(self, indent_level, text):
        self._start_new_line()
        for _i in range(indent_level):
            self.output.write('\t')
        self.output.write('•\t')
        self.output.write(text)
        self.prev_blank = False

    def output_normal(self, text):
        if not self.prev_blank:
            self.output.write(' ')
        self.output.write(text)
        self.prev_blank = False


def format_package_description(description):
    formatter = _DescriptionFormatter()
    description = GLib.markup_escape_text(description)
    parse_bullets = can_parse_bullets(description)
    used_indent_levels = list(
        i for i, _g in itertools.groupby(bt.text_indent
                                         for bt
                                         in _get_bullet_types(description)))
    # FIXME: Messy
    indent_level = []
    for line in description.splitlines():
        if line.startswith('.'):
            if len(line) > 1:
                # Extended syntax — ignore.
                continue
            formatter.output_paragraph_break()
            continue
        if parse_bullets:
            bullet_type = _BulletType.detect(line)
            if bullet_type is not None:
                indent_level.append(bullet_type.text_indent)
                formatter.output_bullet_line(
                    used_indent_levels.index(bullet_type.text_indent) + 1,
                    line[bullet_type.text_indent:])
            else:
                indent = re.search(r'^ *', line).end()
                while len(indent_level) > 0 and indent < indent_level[-1]:
                    indent_level.pop()
                if (indent == 0
                        or len(indent_level) > 0
                           and indent == indent_level[-1]):
                    formatter.output_normal(line.lstrip())
                else:
                    formatter.output_preformatted(line[1:])
        else:
            # Don’t parse bullets
            if line.startswith(' '):
                formatter.output_preformatted(line[1:])
            else:
                formatter.output_normal(line)
    return formatter.get_value()
