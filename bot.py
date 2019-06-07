'''
Bot-related code
'''
import telegram
from telegram.ext import Updater, CommandHandler, Filters, MessageHandler

import constants as c
from graph import Graph


def start_first(func):
    '''
    Decorator to force that the first command is start
    '''
    def wrapper(bot, update, user_data, args=None):
        if not user_data.get('graph', None):
            bot.send_message(
                chat_id=update.message.chat_id,
                text=c.NOT_STARTED
            )
            return
        if args:
            func(bot, update, user_data, args)
        else:
            func(bot, update, user_data)
    return wrapper


# Bot functions
def start(bot, update, user_data):
    '''
    Writes a Hello message
    '''
    user_data['graph'] = Graph()
    user_data['usercoords'] = None
    bot.send_message(chat_id=update.message.chat_id, text=c.HELLO_TEXT)


@start_first
def bot_help(bot, update, user_data):
    '''
    Writes help about the bot
    '''
    bot.send_message(
        chat_id=update.message.chat_id,
        text=c.HELP_TEXT,
        parse_mode=telegram.ParseMode.MARKDOWN
    )


@start_first
def author(bot, update, user_data):
    '''
    Writes info about the author
    '''
    bot.send_message(
        chat_id=update.message.chat_id,
        text=c.AUTHOR_INFO,
        parse_mode=telegram.ParseMode.MARKDOWN
    )


@start_first
def change_graph(bot, update, user_data, args):
    '''
    Creates a new graph with arg[0] as max_dist and arg[1] as
    min_pop
    '''
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

        user_data['graph'] = Graph(int(args[0]), int(args[1]))
        bot.send_message(chat_id=update.message.chat_id, text=c.OK_TEXT)

    except ValueError:
        bot.send_message(chat_id=update.message.chat_id, text=c.WRONG_ARGS)
        return


@start_first
def nodes(bot, update, user_data):
    '''
    Writes the number of nodes of the current graph
    '''
    bot.send_message(
        chat_id=update.message.chat_id,
        text=str(user_data['graph'].get_number_nodes())
    )


@start_first
def edges(bot, update, user_data):
    '''
    Writes the number of edges of the current graph
    '''
    bot.send_message(
        chat_id=update.message.chat_id,
        text=str(user_data['graph'].get_number_edges())
    )


@start_first
def components(bot, update, user_data):
    '''
    Writes the number of connected components of the graph
    '''
    bot.send_message(
        chat_id=update.message.chat_id,
        text=str(user_data['graph'].get_number_components())
    )


@start_first
def where(bot, update, user_data):
    '''
    Receives the location of the user
    '''
    lat, lon = update.message.location.latitude, update.message.location.longitude
    user_data['usercoords'] = (lat, lon)

    bot.send_message(chat_id=update.message.chat_id, text=c.OK_TEXT)


def checkcoords(lat, lon):
    '''
    Checks if given coords are valid
    '''
    lat_ok = (lat <= 90) and (lat >= -90)
    lon_ok = (lon <= 180) and (lon >= -180)

    return lat_ok and lon_ok


def parse_plot_args(bot, update, user_data, args):
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
        if user_data.get('usercoords', None):
            print(user_data['usercoords'])
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
def plotpop(bot, update, user_data, args):
    '''
    Plots a map with all the cities with distance <= args[0] from point
    args[1], and size proportional to their population
    '''
    parsed_args = parse_plot_args(bot, update, user_data, args)

    if not parsed_args:
        return

    dist, lat, lon = parsed_args

    image = user_data['graph'].plotpop(lat, lon, dist)
    if not image:
        bot.send_message(chat_id=update.message.chat_id, text=c.NO_IMAGE)
    bot.send_photo(chat_id=update.message.chat_id, photo=image)


@start_first
def plotgraph(bot, update, user_data, args):
    '''
    Plots a map with all the cities with distance <= args[0] from point
    args[1], and the edges between them
    '''
    parsed_args = parse_plot_args(bot, update, user_data, args)

    if not parsed_args:
        return

    dist, lat, lon = parsed_args

    image = user_data['graph'].plotgraph(lat, lon, dist)
    if not image:
        bot.send_message(chat_id=update.message.chat_id, text=c.NO_IMAGE)
    bot.send_photo(chat_id=update.message.chat_id, photo=image)


def parse_route_args(bot, update, user_data, args):
    '''
    Parses args of function route
    '''
    joint = ' '.join(args)
    cities = joint.split('"')

    if len(cities) != 5:
        return

    return cities[1], cities[3]


@start_first
def route(bot, update, user_data, args):
    '''
    Plots the shortest route between args[0] and args[1]
    '''
    parsed_args = parse_route_args(bot, update, user_data, args)

    if not parsed_args:
        bot.send_message(
            chat_id=update.message.chat_id,
            text=c.WRONG_ARGS
        )
        return

    image = user_data['graph'].route(parsed_args[0], parsed_args[1])
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

    dispatcher.add_handler(CommandHandler('start', start, pass_user_data=True))
    dispatcher.add_handler(CommandHandler('help', bot_help, pass_user_data=True))
    dispatcher.add_handler(CommandHandler('author', author, pass_user_data=True))
    dispatcher.add_handler(CommandHandler('graph', change_graph, pass_user_data=True, pass_args=True))
    dispatcher.add_handler(CommandHandler('nodes', nodes, pass_user_data=True))
    dispatcher.add_handler(CommandHandler('edges', edges, pass_user_data=True))
    dispatcher.add_handler(CommandHandler('components', components, pass_user_data=True))
    dispatcher.add_handler(MessageHandler(Filters.location, where, pass_user_data=True))
    dispatcher.add_handler(CommandHandler('plotpop', plotpop, pass_user_data=True, pass_args=True))
    dispatcher.add_handler(CommandHandler('plotgraph', plotgraph, pass_user_data=True, pass_args=True))
    dispatcher.add_handler(CommandHandler('route', route, pass_user_data=True, pass_args=True))

    updater.start_polling()


if __name__ == '__main__':
    main()
