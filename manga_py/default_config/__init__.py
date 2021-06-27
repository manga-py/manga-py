from pathlib import Path


CONFIG_FILE = Path.home().joinpath('manga-py.toml')


def _available_keys():
    return [
        'auto_skip_deleted', 'cbz', 'create_empty_files', 'destination', 'global_progress',
        'max_threads', 'min_free_space', 'no_progress', 'no_webp', 'not_change_files_extension',
        'override_archive_name', 'proxy', 'rename_pages', 'rewrite_exists_archives',
        'skip_incomplete_chapters', 'user_agent', 'wait_after_chapter', 'wait_after_page', 'zero_fill'
    ]


def dump_init_content():
    if CONFIG_FILE.is_file():
        return

    data = """# default manga-py config. You can change the values as you like. See the "manga-py --help" for the meaning of the keys.
[default]
#auto_skip_deleted=
#cbz=
#create_empty_files=
#destination=
#global_progress=
#max_threads=
#min_free_space=
#no_progress=
#no_webp=
#not_change_files_extension=
#override_archive_name=
#proxy=
#rename_pages=
#rewrite_exists_archives=
#skip_incomplete_chapters=
#user_agent=
#wait_after_chapter=
#wait_after_page=
#zero_fill=
"""
    with CONFIG_FILE.open('w') as w:
        w.write(data)


class DefaultConfig:
    params = None

    def __init__(self, params: dict = None):
        self.params = {k: params[k] for k in params if k in _available_keys()}

    def __getattr__(self, item):
        return (self.params or {}).get(item, None)

    def get_all(self) -> dict:
        return (self.params or {}).copy()
