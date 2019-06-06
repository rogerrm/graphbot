'''
Constants for the GraphBot project
'''

# Graph-related constants
URL = 'https://github.com/jordi-petit/lp-graphbot-2019/blob/master/dades/' + \
      'worldcitiespop.csv.gz?raw=true'

COLUMNS = {
    'Country': 0,
    'AccentCity': 1,
    'Region': 2,
    'Population': 3,
    'Latitude': 4,
    'Longitude': 5
}

MIN_POPULATION = 100000
MAX_DISTANCE = 300
CIRCLE_SCALE = 15

CSV_URI = 'data/citydata.csv.gz'

SOURCE_FAIL = 'Source Fail'
DEST_FAIL = 'Dest Fail'
PATH_FAIL = 'Paht Fail'

# Bot-related constants
NOT_STARTED = "The bot is not started! To start using it, use /start"

HELLO_TEXT = "Hello"

HELP_TEXT = """
*List of possible commands:*

- /start

    Starts the communication with the bot; no other command can be executed \
before it. It creates an initial graph with distance `{initial_dist}` \
and restricted to cities with more than `{initial_pop}` \
population.

- /help

    Shows information about all the possible commands.

- /author

    Shows information about the author of the bot.

- /graph ⟨distance⟩ ⟨population⟩

    Tells the bot to start using a new geometric graph with distance \
`⟨distance⟩` and restricted to cities with more than `⟨population⟩` \
population.

- /nodes

    Writes the number of nodes in the graph.

- /edges

    Writes the number of edges in the graph.

- /components

    Writes the number of connected components in the graph.

- /setcoords ⟨lat⟩ ⟨lon⟩

    Tells the bot to use ⟨lat⟩ ⟨lon⟩ as your current coordinates.

- /plotpop ⟨dist⟩ [[⟨lat⟩ ⟨lon⟩]]

    Plots a map of all cities in the graph whose distance with \
`⟨lat⟩,⟨lon⟩` is less than or equal to `⟨dist⟩`. The cities are \
shown with a circle of ratius proportional to their population.

Coordenates are optional: when not given, the bot will use the user's \
location (they must have been already specified with /setcoords).

- /plotpop ⟨dist⟩ [[⟨lat⟩ ⟨lon⟩]]

    Plots a map of all edges between cities in the graph whose distance with \
`⟨lat⟩,⟨lon⟩` is less than or equal to `⟨dist⟩`.

Coordenates are optional: when not given, the bot will use the user's \
location (they must have been already specified with /setcoords).

- /route ⟨src⟩ ⟨dst⟩

    Plots the shortest way to go from `⟨src⟩` to `⟨dst⟩`. Both have to \
follow the format "city, country", where country refers to the \
abbreviation (for example, Barcelona would be "Barcelona, es".
""".format(
    initial_dist=MAX_DISTANCE,
    initial_pop=MIN_POPULATION
)

AUTHOR_INFO = """
Roger Romero Morral
roger.romero.morral@est.fib.upc.edu
"""

OK_TEXT = "Ok"

NOT_SPECIFIED_CHOORDS = "If you don't want to specify the coordinates, " + \
                        "please set your current location with /setcoords"

WRONG_ARGS = "You did not pass the arguments in the right way. " + \
             "Please use /help to check the usage of this command."

NO_IMAGE = "No nodes/edges were found satisfying the given conditions."

NO_CITY = "No cities were found matching the name {city}. Pleas use " + \
           "/help to check the format in which cities must be given."

NO_ROUTE = "No route was found between the given cities."

INVALID_COORDS = "Please enter valid coordinates."

LON_LAT_REGEX = r'^\[(\-|)[0-9]*(\.|)[0-9]+ (\-|)[0-9]*(\.|)[0-9]+\]$'
