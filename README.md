# pypaper

* fetch bibtex and pdf from IEEE and ACM
* fetch infomation from Google Scholar given bibtex

# Example

Under project root, run:

```
example\google.bat
```

The google scholar records of `example/review.bib` will be stored in `temp/google.db`, and will be sorted by citation count in `temp/review.txt`.

# Dependency

This project tested on Python `2.7`, under virtualenv. Following are `pip freeze` result:

```
SQLAlchemy==0.8.1
beautifulsoup4==4.2.0
biblio-py==0.6.1
cssselect==0.8
lxml==3.0.2
nose==1.3.0
pyparsing==1.5.0
pyquery==1.2.4
pywin32==218
```

