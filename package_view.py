import re

import gi
from gi.repository import Gtk

from format_package_description import format_package_description


get_description_leading_spaces = re.compile(r'^ ', re.MULTILINE)

def get_description(version):
    """
        Get the raw description of the package version ‘version’.

        This is necessary because apt.package.Version.raw_description
        erroneously returns the short description.
    """
    # FIXME: Don’t access private properties once the bug is fixed in
    # python-apt.
    records = version._translated_records
    result = records.long_desc
    # Check whether apt_pkg erroneously included the first line of the
    # ‘Description:’ field (records.short_desc) in records.long_desc
    if not result.startswith(' ') and '\n' in result:
        result = result.split('\n', maxsplit=1)[1]
    result = get_description_leading_spaces.sub('', result)
    return result


class PackageView(Gtk.ScrolledWindow):
    def __init__(self, package):
        super().__init__()

        text_view = Gtk.TextView()
        text_view.set_editable(False)
        text_view.set_wrap_mode(Gtk.WrapMode.WORD_CHAR)
        self.add(text_view)

        # TODO: Handle multiple versions.
        version = package.candidate
        text_buffer = text_view.get_buffer()
        it = text_buffer.get_start_iter()
        text_buffer.insert_markup(
            it,
            # I18N This is the format of the first line of the package
            # view.
            _('<span size="x-large" weight="bold">{name}</span>'
              '        version <span size="large">{version}</span>\n')
                .format(name=package.name, version=version.version),
            -1)
        summary = re.sub(r' --? ', ' — ', version.summary)
        text_buffer.insert_markup(it, f'<big>{summary}</big>\n', -1)

        description = get_description(version)
        description = format_package_description(description)

        text_buffer.insert_markup(it, description, -1)
        text_buffer.insert(it, "\n")
        text_buffer.insert(it,
                           _("Section: {}".format(version.section)))
