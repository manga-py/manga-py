
# Manga-PY lifecycle

## Base
1) Check manga-py version
2) If `--title` not empty, run search for each provider (see <a href="https://github.com/yuru-yuri/manga-dl/issues/121">issue#121</a>)
3) Parsing attributes
    1) If find multiple urls, run for loop on
    `manga_py.cli._update_all`
4) For each url:
    1) Search provider by url
    `manga_py.providers.get_provider`
    1) Run provider methods


## Provider methods cycle

1) `before_provider()`
1) `get_main_page_url()`
1) `get_content()`
1) `get_manga_name()`
1) `get_chapters()`<br>
    ***See <a href="#chapter-methods-lifecycle">chapter lifecycle</a>***
1) `after_provider()`

### Chapter methods lifecycle

1) `before_chapter()`
1) `get_chapter_name()`
1) `get_chapter_url()`
1) `get_files()`<br>
    ***See <a href="#files-methods-lifecycle">files lifecycle</a>***
1) `after_chapter()`

### Files methods lifecycle

1) `progress_next(True)`
1) `before_download()`
1) `manga_py.libs.http.Http.download()`
1) `manga_py.libs.modules.image.Image.process()`
1) `after_download()`
1) `progress_next()`
