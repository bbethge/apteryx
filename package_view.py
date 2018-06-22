import re

import gi
from gi.repository import Gtk

from format_package_description import format_package_description


class LowLevelPackageNotFoundError(Exception):
    pass

get_description_leading_spaces = re.compile(r'^ ', re.MULTILINE)

def get_description(package, version):
    """
        Get the raw description of the package identified by ‘package’ and
        ‘version’ (both strings).  This is necessary because, in my version
        of apt, apt.package.Version.raw_description erroneously returns the
        short description.
    """
    import apt_pkg

    # FIXME: This is kind of slow.
    ll_cache = apt_pkg.Cache()
    for ll_version in ll_cache[package].version_list:
        if ll_version.ver_str == version:
            break
    else:
        raise LowLevelPackageNotFoundError(package, version)
    records = apt_pkg.PackageRecords(ll_cache)
    # TODO: Figure out whether we need to iterate through file_list
    records.lookup(ll_version.translated_description.file_list[0])
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
        text_buffer.insert_markup(it,
            _('<span size="x-large" weight="bold">{name}</span>'
              '        version <span size="large">{version}</span>\n')
            .format(name=package.name, version=version.version),
            -1)
        summary = re.sub(r' --? ', ' — ', version.summary)
        text_buffer.insert_markup(it, '<big>{}</big>\n'.format(summary), -1)

        description = get_description(package.name, version.version)
        description = format_package_description(description)

        text_buffer.insert_markup(it, description, -1)
        text_buffer.insert(it, "\n")
        text_buffer.insert(it,
            _("Section: {}".format(version.section)))
