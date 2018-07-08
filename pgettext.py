def pgettext(context, msgid):
    """
        I can’t find any evidence of a pgettext implementation in the
        Python standard library or any other library other than Web
        frameworks.  DuckDuckGo gives the gettext module documentation
        as a match for "pgettext" (Google doesn’t), but I can’t find it
        in that page.

        Thus, this function based on GNU gettext.h.
    """
    context_id = f'{context}\u0004{msgid}'
    translation = _(context_id)
    if translation == context_id:
        return msgid
    else:
        return translation
