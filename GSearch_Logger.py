#----------------------------GSearch Logger----------------------------#
#! - Simple Application that Scrapes URLs Using Google's Search Engine.
#! - EST. 1/14/21
#! - G-Logger v1.0-Beta

#TODO:
#* Add option to turn on/off url logging.
#? ~~~Maybe use Checkbox widget?~~~
#* Implement easier way to open urls in browser.
#* Add options to configure chunk sizes (number of urls per load)
#* Add options to configure max amount of urls to return (total urls to load)
#* Add options to configured rate limits (time between loads)

import secrets
from webbrowser import open as url_open

import PySimpleGUI as sg
from googlesearch import search as gSearch


def googleURLs(query: str, logURLs: bool) -> None:
    """
    Performs a google search for the query entered, and scrapes resulting URLs in 5 "chunks" of 3 urls every 1 second.
    
    - If desired, you can log the URLs returned by the search engine by checking the "Log URLs" field.
    - Saves each URL in a separate file located in the logs directory:
        - './GSearch_URL_WebScraper/logs/**.txt'
    - BE WARNED:
        - Use sparingly; otherwise Google may *BLOCK YOUR IP*, temporarily disallowing any and all future experimentation/google searches entirely.
    """
    search_query = query
    enable_logging = logURLs
    file_uid = secrets.token_urlsafe(5)

    #! If logging is enabled, URLs will be saved in the logs directory.
    if enable_logging == True:
        with open(fr'./GSearch-Logger/logs/logFile_{file_uid}.txt', 'x') as fh:
            fh.write('Search Query: %s:\n\n' % search_query)
            print('\nSearch Query: %s\n\n' % search_query)
            for url in gSearch(search_query,
                               tld="com",
                               num=3,
                               stop=15,
                               pause=1.0):
                fh.write('{}\n\n'.format(url))
                print('\n{}'.format(url))
        return print('Process Complete!\nLog saved as %s\n\n' % fh)
    #! If logging is disabled, URLs are only displayed through output.
    elif enable_logging == False:
        for url in gSearch(search_query, tld="com", num=3, stop=15, pause=1.0):
            print('\n{}'.format(url))
        return print('Process Complete!')


def openUrl(url: str) -> bool:
    """
    Opens URL within user's default browser.
    
    """
    searchQuery = url
    return url_open(searchQuery, 2)


#? Color Scheme of window:
sg.theme('DarkBlue')

#? Window Element Design/Layout:
mainLayout = [
    # Row 1 - Text/Log URLs Option
    [
        sg.Text('Enter a Search Query Below'),
        sg.Checkbox('Log URLs?', k='-URL Logging-')
    ],
    # End Row 1
    [  # Row 2 - Input/Search
        sg.InputText(do_not_clear=False,
                     size=(70, 1),
                     tooltip='Enter a search query to look up on Google.',
                     k='-User Search Query-'),
        sg.ReadButton('Search',
                      tooltip='Click to confirm search query.',
                      k='-Submit-')
    ],  # End Row 2
    [  # Row 3 - Output
        sg.Output(k='-Output Element-',
                  background_color='DarkGrey',
                  text_color='Black',
                  echo_stdout_stderr=True,
                  size=(81, 15))
    ],  # End Row 3
    # Row 4 - Text
    [sg.Text('Copy/Paste URL to Open in Browser')],
    # End Row 4
    [  # Row 5 - URL Input/Browse
        sg.InputText(
            size=(70, 1),
            do_not_clear=False,
            k='-Browse URL-',
            tooltip=
            'Copy/Paste or simply enter a URL and click "Open URL" to view the web-page in your browser.'
        ),
        sg.ReadButton('Open URL',
                      tooltip='Opens the entered URL in a web browser.',
                      k='-Open-')
    ],  # End Row 5
    # Row 6 - Exit
    [sg.Exit(tooltip='Click to Exit Application.')]
]  # End Row 6

#? Main Application Window Build:
mainWindow = sg.Window(
    'Google Search URL Scraper',
    mainLayout,
    auto_size_text=True,
    auto_size_buttons=False,
    text_justification='Center',
    margins=(5, 5),  # pixels
    element_padding=(3, 3),  # pixels
)

#! Process Window Events:
while True:
    event, values = mainWindow.read(
    )  #? Passes button press events and corresponding input values to the "event/values" variables.
    #print(event, values)  #? Displays events and input values in console. (Good for debugging.)

    #! Closes window upon exit button, or clicking the x.
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    if event == '-Submit-':
        if values['-URL Logging-'] == True:
            googleURLs(values['-User Search Query-'], values['-URL Logging-'])
        else:
            googleURLs(values['-User Search Query-'], values['-URL Logging-'])
    if event == '-Open-':
        openUrl(values['-Browse URL-'])

mainWindow.close()
