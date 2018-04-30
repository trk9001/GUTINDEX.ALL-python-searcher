"""Script to search the GUTINDEX file by e-text number, title or author.

Usage:
------

> From the command line, run:
`python search.py {mode: etext/title/author} {search parameter}`


Known bugs:
-----------

> If there are less than 2 spaces before the e-text number, the search fails.
This is in relation to the fact that some entries in the file end with a
number (eg. "... Vol. 2"), and there is no other (known) way to
differentiate an e-text number from that one.

> When searching by author, if the author's full name breaks into a new line,
or it is not the first name in a list of authors' names, the search fails.

> When searching by title, if the title spans more than one line, the search
fails.

"""

import re  # For regex
import sys  # For parsing command line arguments


def search_by_etext_no(file_to_search, eno):
    """Search using the e-text number"""

    eno_ex = re.compile('^((.)*)(\s){{2,}}\\b{}\\b$'.format(eno))
    reg = re.compile(r'^(.)*(\s){2,}\b(\d)+(C)?\b$')

    with open(file_to_search) as f:
        for line in f:
            match = eno_ex.match(line)

            if match:
                data = [match.group(1).strip() + '\n']

                line = f.readline()
                while line not in ['', '\n'] and not reg.match(line):
                    data.append(line)
                    line = f.readline()

                return ''.join(data)

    return None


def search_by_title(file_to_search, title):
    """Search using the title"""

    reg = re.compile(r'(.)*(\s){2,}\b(\d)+(C)?\b$')

    with open(file_to_search) as f:
        for line in f:
            match = reg.match(line)

            if match and title in line:
                data = [line]

                line = f.readline()
                while line not in ['', '\n'] and not reg.match(line):
                    data.append(line)
                    line = f.readline()

                return ''.join(data)

    return None


def search_by_author(file_to_search, author):
    """Search using the author's full name"""

    reg = re.compile(r'(.)*(\s){2,}\b(\d)+(C)?\b$')

    by_list = list()
    for s in [' by ', ' mennessä ', ' par ', ' di ']:
        by_list.append(s + author)

    data = list()

    with open(file_to_search) as f:
        line = f.readline()

        while line != '':
            match = reg.match(line)

            if match:
                place = f.tell()
                first_line = line

                for s in by_list:
                    if s in line:
                        found = True
                        break
                else:
                    found = False

                if not found:
                    line = f.readline()
                    while line != '' and not reg.match(line):
                        for s in by_list:
                            if s in line:
                                found = True
                                break

                        if found:
                            break
                        else:
                            line = f.readline()

                if found:
                    f.seek(place)
                    data.append(first_line)
                    line = f.readline()
                    while line != '' and not reg.match(line):
                        data.append(line)
                        line = f.readline()

                else:
                    pass

            else:
                line = f.readline()

    if len(data):
        return ''.join(data)
    else:
        return None


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Invalid number of arguments; expected two or more.\n')

    else:
        file = 'GUTINDEX.ALL'
        mode = sys.argv[1].lower()

        if mode in ['etext', 'e-text', 'etextno', 'etext_no', 'e-text_no']:
            info = search_by_etext_no(file, sys.argv[2])
            if info:
                print(info)
            else:
                print('Not found.\n')

        elif mode == 'title':
            book_title = ' '.join(sys.argv[2:])
            info = search_by_title(file, book_title)
            if info:
                print(info)
            else:
                print('Not found.\n')

        elif mode == 'author':
            author_name = ' '.join(sys.argv[2:])
            info = search_by_author(file, author_name)
            if info:
                print(info)
            else:
                print('Not found.\n')

        else:
            print('Invalid mode.\n')
