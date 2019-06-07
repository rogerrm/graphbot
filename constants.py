'''
Constants for the GraphBot project
'''

# Graph-related constants
URL = 'https://github.com/jordi-petit/lp-graphbot-2019/blob/master/dades/worldcitiespop.csv.gz?raw=true'

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

CSV_DIR = 'data/'
CSV_URI = CSV_DIR + 'citydata.csv.gz'

SOURCE_FAIL = 'Source Fail'
DEST_FAIL = 'Dest Fail'
PATH_FAIL = 'Paht Fail'

MAX_USER_DISTANCE = 1000
MIN_USER_POPULATION = 80000

EARTH_RADIUS = 6371.0

# Bot-related constants
NOT_STARTED = "You have not started a conversation with the bot! To start using it, use /start"

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

- Additionaly, you can send your location and the bot will start using it\
when needed.
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
                        "please send your current location"

WRONG_ARGS = "You did not pass the arguments in the right way. " + \
             "Please use /help to check the usage of this command."

NO_IMAGE = "No nodes/edges were found satisfying the given conditions."

NO_CITY = "No cities were found matching the name {city}. Please use " + \
           "/help to check the format in which cities must be given."

NO_ROUTE = "No route was found between the given cities."

TOO_LARGE_DISTANCE = "Please set a distance less than {}".format(MAX_USER_DISTANCE)

TOO_LOW_POPULATION = "Please set a population greater than {}".format(MIN_USER_POPULATION)

INVALID_COORDS = "Please give the coords in a valid range: lat in (-90, 90) and lon in (-180, 180)"
