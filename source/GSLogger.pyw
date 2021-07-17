# #? --------------------------GSLogger v1.6.0-Beta-------------------------- #
#! - Simple Application that Scrapes/Optionally Logs URLs Using Google's Search Engine.
#! - EST. 1/14/21
#! - GSLogger Version ?.?.?-Beta

#TODO ================== :TO-DO: ==================== TODO#
#* Implement easier way to open urls in browser.
#* Add options to configure chunk sizes (number of urls per read).
#* Add options to configure total desired number of results per query.
#* Add options to configured rate limits (time between reads).

#?----------------------------Modules & Libraries----------------------------#
import secrets
from os import chdir as cwd
from os.path import abspath
from os.path import dirname as folder
from webbrowser import open as url_open
import PySimpleGUI as sg
from googlesearch import search as gSearch
#! Set working directory to install location:
cwd(folder(folder(__file__)))
#?---------------------------------------------------------------------------#


def googleURLs(query: str, logURLs: bool) -> None:
    """
    Search google for the query entered, and scrape resulting URLs.

    - As of now, function returns 3 URLs every second broken up into 5 "chunks".
    - If desired, you can log the URLs returned by the search engine by checking the "Log URLs" field.
        - Saves each URL in a separate file located in the logs directory:
            - '../logs/'
    - BE WARNED:
        - Use sparingly; otherwise Google may *BLOCK YOUR IP*, temporarily disallowing any and all future experimentation/google searches entirely.
    Parameters:
        - :param query: topic to search for.
        - :param logURLs: toggle saving a text-log of retrieved URLs upon each search.
    """
    file_uid: str = secrets.token_urlsafe(5)

    #NOTE - #! If logging is enabled, URLs will be saved in the "logs" directory.
    if logURLs == True:
        #* Create URL log file:
        with open(fr'./logs/logFile_{file_uid}.log', 'x') as fh:
            #* Write URLs to log file/display URLs in output:
            fh.write(f'> Search Query: {query}\n\n')
            print(f'> Search Query: {query}\n')
            for url in gSearch(query, tld="com", num=3, stop=15, pause=1.0):
                fh.write(f'{url}\n\n')
                print(f'\n{url}')
        return print(
            f'\n\n\t\t- Process Complete! -\n- Search log saved within the "logs" directory as:\n"{abspath(f"./logs/logFile_{file_uid}.log")}"\n'
        )

    #NOTE - #! If logging is disabled, URL logs are NOT saved, and will only displayed through output.
    elif logURLs == False:
        #* Display URLs in output:
        print(f'> Search Query: {query}\n')
        for url in gSearch(query, tld="com", num=3, stop=15, pause=1.0):
            print(f'\n{url}')
        return print('\n\n>> Process Complete! <<\n')


def openUrl(url: str) -> bool:
    """
    Opens URL within user's default browser.

    - If user's browser is already open, a new tab will be created.

    Parameters
    - :param url: URL link to be opened in browser.
    - :returns: Opens website in default web-browser.
    - :rtype: (bool)

    """
    return url_open(url, 2)


#? Color Scheme of window:
sg.theme('LightGray1')

#? Window Element Design/Layout:
mainLayout = [
    #? Row 1 - Text/Log URLs Option
    [
        sg.Text('Enter a Search Query Below'),
        sg.Checkbox(
            'Log URLs',
            k='-URL Logging-',
            tooltip='Check to enable search-result logging upon each query.')
    ],
    #? End Row 1
    [  #? Row 2 - Input/Search
        sg.InputText(do_not_clear=False,
                     size=(80, 1),
                     tooltip='Enter a search query to look up on Google.',
                     k='-User Search Query-'),
        sg.ReadButton('Search',
                      tooltip='Click to confirm search query.',
                      k='-Submit Query-')
    ],  #? End Row 2
    [  #? Row 3 - Output
        sg.Output(k='-Output Element-',
                  background_color='DarkGrey',
                  text_color='Black',
                  size=(91, 15))
    ],  #? End Row 3
    #? Row 4 - Text
    [sg.Text('Copy/Paste URL to Open in Browser')],
    #? End Row 4
    [  #? Row 5 - URL Input/Browse
        sg.InputText(
            size=(80, 1),
            do_not_clear=False,
            k='-Browse URL-',
            tooltip=
            'Copy/Paste or simply enter a URL and click "Open URL" to view the web-page in your browser.'
        ),
        sg.ReadButton('Open URL',
                      tooltip='Opens the entered URL in a web browser.',
                      k='-Open-')
    ],  #? End Row 5
    #? Row 6 - Exit
    [sg.Exit(tooltip='Click to Exit Application.')]
]  #? End Row 6

#? Main Window Properties:
mainWindow = sg.Window(
    'GSLogger - v1.6.0-Beta',
    mainLayout,
    auto_size_text=True,
    auto_size_buttons=False,
    text_justification='Center',
    margins=(10, 5),  #! pixels
    element_padding=(3, 3),  #! pixels
)

#? =============== Process Window Events: =============== ?#
while True:
    #NOTE - #? Passes button press events and corresponding input values to the "event/values" variables:
    event, values = mainWindow.read()
    #print(event, values)  #NOTE - #! Enable to display window events in console (default=OFF).

    #NOTE - #! Closes window upon exit button, or clicking the x.
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    #? ===== Search Query Events ===== ?#
    if event == '-Submit Query-':
        if values['-User Search Query-'] == '':
            sg.popup_ok('\t- ERROR -',
                        'Entry cannot be blank',
                        keep_on_top=True)
        else:
            if values['-URL Logging-'] == True:
                googleURLs(values['-User Search Query-'],
                           values['-URL Logging-'])
            else:
                googleURLs(values['-User Search Query-'],
                           values['-URL Logging-'])
    #? ===== Open URL Events ===== ?#
    if event == '-Open-':
        if values['-Browse URL-'] == '':
            sg.popup_ok('\t- ERROR -',
                        '-Entry cannot be blank-',
                        keep_on_top=True)
        else:
            openUrl(values['-Browse URL-'])

mainWindow.close()
