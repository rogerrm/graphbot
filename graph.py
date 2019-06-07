'''
Class that stores the graph and handles all its functions
'''
import csv
import logging
import gzip
import requests
import os
from io import BytesIO

import pandas as pd
import networkx as nx
from haversine import haversine
from staticmap import StaticMap, Line, CircleMarker
from fuzzywuzzy import fuzz

import constants as c
import graph_utilities as gu


class Graph:
    '''
    Class that stores the graph and handles all its functions
    '''

    def __init__(self, max_dist=c.MAX_DISTANCE, min_pop=c.MIN_POPULATION):
        '''
        Downloads the data and creates the graph
        '''

        # Download the data and process it
        if not os.path.exists(c.CSV_DIR):
            os.makedirs(c.CSV_DIR)
        if os.path.exists(c.CSV_URI):
            os.remove(c.CSV_URI)
        r = requests.get(c.URL)
        open(c.CSV_URI, 'wb').write(r.content)

        dataframe = pd.read_csv(
            c.CSV_URI,
            usecols=c.COLUMNS.keys(),
            compression='gzip'
        )
        dataframe = dataframe[dataframe['Population'] > min_pop]

        self.coordinates = dict()
        self.populations = dict()
        for row in dataframe.iterrows():
            info = row[1]
            city = info[c.COLUMNS['AccentCity']]
            country = info[c.COLUMNS['Country']]
            region = info[c.COLUMNS['Region']]
            key = '{city}, {country}; {region}'.format(
                city=city,
                country=country,
                region=region
            )
            self.coordinates[key] = (
                info[c.COLUMNS['Latitude']],
                info[c.COLUMNS['Longitude']]
            )
            self.populations[key] = info[c.COLUMNS['Population']]

        # Create the graph
        self.G = gu.build_graph(self.coordinates, max_dist)

    def get_number_nodes(self):
        '''
        Returns the number of nodes in the graph
        '''
        return len(self.G.nodes)

    def get_number_edges(self):
        '''
        Returns the number of edges in the graph
        '''
        return len(self.G.edges)

    def get_number_components(self):
        '''
        Returns the number of edges in the graph
        '''
        return len(list(nx.connected_components(self.G)))

    def is_plottable(self, edge, coords, dist):
        '''
        Returs True if the distance between each of the two points in the
        edge and the point coords is lower than dist
        '''
        dist0 = haversine(self.coordinates[edge[0]], coords)
        dist1 = haversine(self.coordinates[edge[1]], coords)
        return dist0 <= dist and dist1 <= dist

    def plotgraph(self, lat, lon, dist):
        '''
        Returns the plot of the graph of the edges between cities that
        have distance than dist from (lat, lon)
        '''
        mapa = StaticMap(400, 400)
        some = False

        for edge in self.G.edges:
            if self.is_plottable(edge, (lat, lon), dist):
                some = True
                # Staticmap needs coordinates in order (Longitude, Latitude)
                rev_coords_0 = tuple(reversed(self.coordinates[edge[0]]))
                rev_coords_1 = tuple(reversed(self.coordinates[edge[1]]))
                mapa.add_line(Line((rev_coords_0, rev_coords_1), 'blue', 3))

        if not some:
            return

        image = mapa.render()
        bio = BytesIO()
        bio.name = 'map.png'
        image.save(bio)
        bio.seek(0)
        return bio

    def plotpop(self, lat, lon, dist):
        '''
        Returns the plot of the graph of the cities that have distance
        lower than dist from (lat, lon)
        '''
        mapa = StaticMap(400, 400)
        some = False

        max_pop = 0
        for node in self.G.nodes:
            if self.is_plottable((node, node), (lat, lon), dist):
                some = True
                if max_pop < self.populations[node]:
                    max_pop = self.populations[node]

        if not some:
            return

        for node in self.G.nodes:
            if self.is_plottable((node, node), (lat, lon), dist):
                rev_coords = tuple(reversed(self.coordinates[node]))
                circle = CircleMarker(
                    rev_coords,
                    'red',
                    self.populations[node]*c.CIRCLE_SCALE/max_pop
                )
                mapa.add_marker(circle)

        image = mapa.render()
        bio = BytesIO()
        bio.name = 'map.png'
        image.save(bio)
        bio.seek(0)
        return bio

    def get_most_similar(self, name):
        '''
        Returns the most similar city name in G to name
        '''
        max_sim = -1
        argmax = None
        for city in self.G.nodes:
            ratio = fuzz.ratio(city.split(';')[0], name)
            if ratio > max_sim:
                max_sim = ratio
                argmax = city
        if max_sim > 80:
            return argmax

    def route(self, src, dst):
        '''
        Returns the plot of the shortest route between src and dst
        '''
        real_src = self.get_most_similar(src)
        real_dst = self.get_most_similar(dst)

        if real_src and real_dst:
            try:
                path = nx.algorithms.shortest_paths.generic.shortest_path(
                    self.G,
                    source=real_src,
                    target=real_dst,
                    weight='weight'
                )
            except Exception as e:
                return c.PATH_FAIL

            mapa = StaticMap(400, 400)
            for cities in zip(['']+path, path):
                rev_coords_1 = tuple(reversed(self.coordinates[cities[1]]))
                circle = CircleMarker(rev_coords_1, 'red', 4)
                mapa.add_marker(circle)
                if '' in cities:
                    continue
                rev_coords_0 = tuple(reversed(self.coordinates[cities[0]]))
                mapa.add_line(Line((rev_coords_0, rev_coords_1), 'blue', 3))

            image = mapa.render()
            bio = BytesIO()
            bio.name = 'map.png'
            image.save(bio)
            bio.seek(0)
            return bio

        if not real_src:
            return c.SOURCE_FAIL

        return c.DEST_FAIL
