# GUTINDEX Searcher with Python

Simple script to search the accompanying `GUTINDEX.ALL` file by e-text number, title or author. This file is a publicly available, plain text compilation of e-books served by *Project Gutenberg*.

## Known bugs

- If there are less than 2 spaces before the e-text number, the search fails. This is in relation to the fact that some entries in the file end with a number (eg. "... Vol. 2"), and there is no other (known) way to differentiate an e-text number from that one.

- When searching by title, if the title spans more than one line, the search fails.

- When searching by author, if the author's full name breaks into a new line, or it is not the first name in a list of authors' names, the search fails.

