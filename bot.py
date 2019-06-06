'''
Bot-related code
'''
import telegram
from telegram.ext import Updater, CommandHandler, Filters, MessageHandler

import constants as c
from graph import Graph


# Global variables
graph = None
usercoords = None


# Decorator so start has to be the first function
def start_first(func):
    def wrapper(bot, update, args=None):
        if not graph:
            bot.send_message(
                chat_id=update.message.chat_id,
                text=c.NOT_STARTED
            )
            return
        if args:
            func(bot, update, args)
        else:
            func(bot, update)
    return wrapper


# Bot functions
def start(bot, update):
    '''
    Writes a Hello message
    '''
    global graph
    global usercoords

    graph = Graph()
    usercoords = None
    bot.send_message(chat_id=update.message.chat_id, text=c.HELLO_TEXT)


@start_first
def bot_help(bot, update):
    '''
    Writes help about the bot
    '''
    bot.send_message(
        chat_id=update.message.chat_id,
        text=c.HELP_TEXT,
        parse_mode=telegram.ParseMode.MARKDOWN
    )


@start_first
def author(bot, update):
    '''
    Writes info about the author
    '''
    bot.send_message(
        chat_id=update.message.chat_id,
        text=c.AUTHOR_INFO,
        parse_mode=telegram.ParseMode.MARKDOWN
    )


@start_first
def change_graph(bot, update, args):
    '''
    Creates a new graph with arg[0] as max_dist and arg[1] as
    min_pop
    '''
    global graph

    if not args:
        bot.send_message(
            chat_id=update.message.chat_id,
            text=c.WRONG_ARGS
        )
        return

    if len(args) != 2:
        bot.send_message(chat_id=update.message.chat_id, text=c.WRONG_ARGS)
        return

    try:
        distance = float(args[0])
        population = float(args[1])

        if distance > c.MAX_USER_DISTANCE:
            bot.send_message(chat_id=update.message.chat_id, text=c.TOO_LARGE_DISTANCE)
            return

        if population < c.MIN_USER_POPULATION:
            bot.send_message(chat_id=update.message.chat_id, text=c.TOO_LOW_POPULATION)
            return

        graph = Graph(int(args[0]), int(args[1]))
        bot.send_message(chat_id=update.message.chat_id, text=c.OK_TEXT)

    except ValueError:
        bot.send_message(chat_id=update.message.chat_id, text=c.WRONG_ARGS)
        return


@start_first
def nodes(bot, update):
    '''
    Writes the number of nodes of the current graph
    '''
    bot.send_message(
        chat_id=update.message.chat_id,
        text=str(graph.get_number_nodes())
    )


@start_first
def edges(bot, update):
    '''
    Writes the number of edges of the current graph
    '''
    bot.send_message(
        chat_id=update.message.chat_id,
        text=str(graph.get_number_edges())
    )


@start_first
def components(bot, update):
    '''
    Writes the number of connected components of the graph
    '''
    bot.send_message(
        chat_id=update.message.chat_id,
        text=str(graph.get_number_components())
    )


@start_first
def where(bot, update, user_data=None):
    '''
    Receives the location of the user
    '''
    global usercoords

    lat, lon = update.message.location.latitude, update.message.location.longitude
    print(lat, lon)
    usercoords = (lat, lon)

    bot.send_message(chat_id=update.message.chat_id, text=c.OK_TEXT)


def checkcoords(lat, lon):
    '''
    Checks if given coords are valid
    '''
    lat_ok = (lat <= 90) and (lat >= -90)
    lon_ok = (lon <= 180) and (lon >= -180)

    return lat_ok and lon_ok


def parse_plot_args(bot, update, args):
    '''
    Parses args of functions plotgraph and plotpop
    '''
    if len(args) == 1:
        if not args[0].isdigit():
            bot.send_message(
                chat_id=update.message.chat_id,
                text=c.WRONG_ARGS
            )
            return
        if usercoords:
            return int(args[0]), usercoords[0], usercoords[1]
        else:
            bot.send_message(
                chat_id=update.message.chat_id,
                text=c.NOT_SPECIFIED_CHOORDS
            )
            return

    if len(args) != 3:
        bot.send_message(
            chat_id=update.message.chat_id,
            text=c.WRONG_ARGS
        )
        return

    try:
        dist = int(args[0])
        lat = float(args[1])
        lon = float(args[2])

        if checkcoords(lat, lon):
            return dist, lat, lon

        else:
            bot.send_message(
                chat_id=update.message.chat_id,
                text=c.INVALID_COORDS
            )
            return

    except ValueError:
        bot.send_message(
            chat_id=update.message.chat_id,
            text=c.WRONG_ARGS
        )


@start_first
def plotpop(bot, update, args):
    '''
    Plots a map with all the cities with distance <= args[0] from point
    args[1], and size proportional to their population
    '''
    parsed_args = parse_plot_args(bot, update, args)

    if not parsed_args:
        return

    dist, lat, lon = parsed_args

    image = graph.plotpop(lat, lon, dist)
    if not image:
        bot.send_message(chat_id=update.message.chat_id, text=c.NO_IMAGE)
    bot.send_photo(chat_id=update.message.chat_id, photo=image)


@start_first
def plotgraph(bot, update, args):
    '''
    Plots a map with all the cities with distance <= args[0] from point
    args[1], and the edges between them
    '''
    parsed_args = parse_plot_args(bot, update, args)

    if not parsed_args:
        return

    dist, lat, lon = parsed_args

    image = graph.plotgraph(lat, lon, dist)
    if not image:
        bot.send_message(chat_id=update.message.chat_id, text=c.NO_IMAGE)
    bot.send_photo(chat_id=update.message.chat_id, photo=image)


def parse_route_args(bot, update, args):
    '''
    Parses args of function route
    '''
    joint = ' '.join(args)
    cities = joint.split('"')

    if len(cities) != 5:
        return

    return cities[1], cities[3]


@start_first
def route(bot, update, args):
    '''
    Plots the shortest route between args[0] and args[1]
    '''
    parsed_args = parse_route_args(bot, update, args)

    if not parsed_args:
        bot.send_message(
            chat_id=update.message.chat_id,
            text=c.WRONG_ARGS
        )
        return

    image = graph.route(parsed_args[0], parsed_args[1])
    if image == c.SOURCE_FAIL:
        bot.send_message(
            chat_id=update.message.chat_id,
            text=c.NO_CITY.format(city=parsed_args[0])
        )
    elif image == c.DEST_FAIL:
        bot.send_message(
            chat_id=update.message.chat_id,
            text=c.NO_CITY.format(city=parsed_args[1])
        )
    elif image == c.PATH_FAIL:
        bot.send_message(
            chat_id=update.message.chat_id,
            text=c.NO_ROUTE
        )
    else:
        bot.send_photo(chat_id=update.message.chat_id, photo=image)


def main():
    '''
    Main function
    '''
    TOKEN = open('token.txt').read().strip()

    updater = Updater(token=TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('help', bot_help))
    dispatcher.add_handler(CommandHandler('author', author))
    dispatcher.add_handler(CommandHandler('graph', change_graph, pass_args=True))
    dispatcher.add_handler(CommandHandler('nodes', nodes))
    dispatcher.add_handler(CommandHandler('edges', edges))
    dispatcher.add_handler(CommandHandler('components', components))
    dispatcher.add_handler(MessageHandler(Filters.location, where))
    dispatcher.add_handler(CommandHandler('plotpop', plotpop, pass_args=True))
    dispatcher.add_handler(CommandHandler('plotgraph', plotgraph, pass_args=True))
    dispatcher.add_handler(CommandHandler('route', route, pass_args=True))

    updater.start_polling()


if __name__ == '__main__':
    main()
