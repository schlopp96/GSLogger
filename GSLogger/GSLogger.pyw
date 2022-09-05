#!/usr/bin/env python3
#? --------------------------GSLogger------------------------------------- #
#! - Simple Application that Scrapes/Optionally Logs URLs Using Google's Search Engine.
#! - EST. 1/14/21

#TODO ================== :TO-DO: ==================== TODO#
#* Implement easier way to open urls in browser.
#* Add options to configure chunk sizes (number of urls per read).
#* Add options to configure total desired number of results per query.
#* Add options to configured rate limits (time between reads).

#?----------------------------Modules & Libraries----------------------------#

import secrets
import sys
from datetime import datetime as time
from os import chdir as cwd
from os.path import abspath
from os.path import dirname as folder
from posixpath import dirname
from webbrowser import open as url_open

import PySimpleGUI as sg
from googlesearch import search as gSearch

sys.path.insert(0, dirname(
    dirname(__file__)))  # Ensure main module can be found by Python.

#$ Set working directory to install location:
cwd(folder(folder(__file__)))

#?---------------------------------------------------------------------------#


def googleURLs(query: str, logURLs: bool) -> None:
    """Search google for the query entered, and scrape resulting URLs.

    - As of now, function returns 3 URLs every second broken up into 5 "chunks".
    - If desired, you can log the URLs returned by the search engine by checking the "Log URLs" field.
        - Saves each URL in a separate file located in the logs directory:
            - `'GSLogger/logs/'`

    ### BE WARNED:
        - Use sparingly, otherwise Google may *BLOCK YOUR IP*, temporarily disallowing any and all future experimentation/google searches entirely.

    ---

    :param query: topic to search for.
    :type query: :class:`str`
    :param logURLs: toggle saving a text-log of retrieved URLs upon each search.
    :type logURLs: :class:`bool`
    :return: URLs from user search paramaters are printed to output window.
    :rtype: `None`
    """

    if logURLs:
        file_uid: str = secrets.token_urlsafe(5)

        with open(fr'./logs/logFile_{file_uid}.log', 'x') as fh:
            fh.write(
                f'> Time of Search:\n{time.now().strftime("> %Y-%m-%d %H:%M:%S")}\n\n> Search Query:\n"{query}"\n\n'
            )
            print(
                f'> Time of Search:\n{time.now().strftime("> %Y-%m-%d %H:%M:%S")}\n\n> Search Query:\n"{query}"\n'
            )
            for url in gSearch(query, tld="com", num=3, stop=15, pause=1.0):
                fh.write(f'> {url}\n\n')
                print(f'\n> {url}')
        return print(
            f'\n\n\t\t- Process Complete! -\n- Search log saved within the "logs" directory as:\n"{abspath(f"./logs/logFile_{file_uid}.log")}"\n'
        )

    else:
        print(
            f'> Time of Search:\n{time.now().strftime("> %Y-%m-%d %H:%M:%S")}\n\n> Search Query:\n"{query}"\n'
        )

        for url in gSearch(query, tld="com", num=3, stop=15, pause=1.0):
            print(f'\n> {url}')
        return print('\n\n>> Process Complete! <<\n')


def openUrl(url: str) -> bool:
    """Opens URL within user's default browser.

    If a browser window is already open, a new tab will be created within the window.

    ---

    :param url: URL link to be opened in browser.
    :type url: :class:`str`
    :return: Opens website in default web-browser.
    :rtype: :class:`bool`
    """

    return url_open(url, 2)


#> Color Scheme of window:
sg.theme('DarkGrey')

#& Window Element Design/Layout:
mainLayout = [
    [
        sg.Text('Enter a Search Query Below'),
        sg.Checkbox(
            'Log URLs',
            k='-URL Logging-',
            tooltip='Check to enable search-result logging upon each query.')
    ],
    [
        sg.InputText(do_not_clear=False,
                     size=(80, 1),
                     tooltip='Enter a search query to look up on Google.',
                     k='-User Search Query-'),
        sg.ReadButton('Search',
                      tooltip='Click to confirm search query.',
                      k='-Submit Query-')
    ],
    [
        sg.Output(
            k='-Output Element-',
            background_color='DarkGrey',
            text_color='Black',
            size=(91, 15),
            tooltip=
            'Highlight a URL with your cursor and use Ctrl+C to copy a link, then use Ctrl+V to paste a link into the search bar.'
        )
    ], [sg.Text('Copy/Paste URL to Open in Browser')],
    [
        sg.InputText(
            size=(80, 1),
            do_not_clear=False,
            k='-Browse URL-',
            tooltip=
            'Copy & Paste a URL using Ctrl+C while highlighting a URL and click "Open URL" to view the web-page in your browser.'
        ),
        sg.ReadButton('Open URL',
                      tooltip='Opens the entered URL in a web browser.',
                      k='-Open-')
    ], [sg.Exit(tooltip='Click to Exit Application.')]
]

mainWindow = sg.Window(
    'GSLogger - v1.7.1b',
    layout=mainLayout,
    auto_size_text=True,
    auto_size_buttons=False,
    text_justification='Center',
    margins=(2, 2)  #! pixels
)

#~ =============== Process Window Events: =============== ~#
while True:
    event, values = mainWindow.read()
    #print(event, values)  #NOTE - #@ Enable to display window events in console (default=OFF).

    if event in [sg.WIN_CLOSED, 'Exit']:
        break

    if event == '-Submit Query-':
        if values['-User Search Query-'] == '':
            sg.popup_ok('\t- ERROR -',
                        'Entry cannot be blank',
                        keep_on_top=True)
        else:
            googleURLs(query=values['-User Search Query-'],
                       logURLs=values['-URL Logging-'])

    if event == '-Open-':
        if values['-Browse URL-'] == '':
            sg.popup_ok('\t- ERROR -',
                        '-Entry cannot be blank-',
                        keep_on_top=True)
        else:
            openUrl(values['-Browse URL-'])

mainWindow.close()
