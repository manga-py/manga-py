
# Manga-PY lifecycle

## Base

1) Check manga-py version
1) Operation mode switching (download / search / database)
1) Show help, if mode has error

---

## Download mode

1) Parsing attributes
    1) If find multiple urls, run for loop on
    `manga_py.cli._update_all`
1) For each url:
    1) Search provider by url
    `manga_py.providers.get_provider`
    1) Run provider methods


### Provider methods cycle
 <a href="https://drive.google.com/file/d/1nDThJJo2x6n7kpWfH3pYPaJ_fH1h9Zt4/view?usp=sharing">See schema here</a>


---


## Search mode

1) Run search for each provider (see <a href="https://github.com/yuru-yuri/manga-dl/issues/121">issue#121</a>)
1) Soon...
