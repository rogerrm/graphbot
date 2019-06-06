'''
Utilities to build the graph
'''
import math

import networkx as nx
from haversine import haversine

import constants as c

def spherical_to_cartesian(coords):
    '''
    Converts spherical coordinates to cartesian coordinates
    '''
    rad_lat, rad_lon = math.radians(coords[0]), math.radians(coords[1])
    
    x = c.EARTH_RADIUS*math.cos(rad_lat)*math.cos(rad_lon)
    y = c.EARTH_RADIUS*math.cos(rad_lat)*math.sin(rad_lon)
    z = c.EARTH_RADIUS*math.sin(rad_lat)
    return x, y, z


def haversine_to_euclidean(dist):
    '''
    Converts haversine dist to euclidean dist
    '''
    R = c.EARTH_RADIUS # earth radius
    gamma = math.acos((2*(R**2) - dist**2) / (2*R**2))
    return gamma * R


def build_kdtree(points, depth=0):
    '''
    Builds a 3-dimensional kdtree to store the cities
    '''
    n = len(points)

    if n <= 0:
        return None

    axis = depth%3

    sorted_points = sorted(points, key=lambda point: point['coords'][axis])

    return {
        'point': sorted_points[int(n/2)],
        'left': build_kdtree(sorted_points[:int(n/2)], depth + 1),
        'right': build_kdtree(sorted_points[int(n/2) + 1:], depth + 1)
    }


def search_neighbours(kdtree, dist, edist, point_cartesian, point_spherical, coordinates, depth=0):
    '''
    Returns a set with all the points nearest
    '''
    result = set()
    
    axis = depth%3
    
    if haversine(coordinates[kdtree['point']['city']], point_spherical) < dist:
        result.add(kdtree['point']['city'])
        
    if not kdtree['left'] is None:
        if kdtree['point']['coords'][axis] > point_cartesian[axis] - edist:
            result = result.union(search_neighbours(kdtree['left'], dist, edist, point_cartesian, point_spherical, coordinates, depth + 1))
            
    if not kdtree['right'] is None:
        if kdtree['point']['coords'][axis] < point_cartesian[axis] + edist:
            result = result.union(search_neighbours(kdtree['right'], dist, edist, point_cartesian, point_spherical, coordinates, depth + 1))
    
    return result


def build_graph(coordinates, dist):
    cartesian_points = [{'city': k, 'coords': spherical_to_cartesian(v)} for k, v in coordinates.items()]

    kdtree = build_kdtree(cartesian_points)

    G = nx.Graph()
    G.add_nodes_from(coordinates.keys())

    for node in G.nodes:
        point_spherical = coordinates[node]
        point_cartesian = spherical_to_cartesian(point_spherical)
        for neighbour in search_neighbours(
            kdtree,
            dist,
            haversine_to_euclidean(dist),
            point_cartesian,
            point_spherical,
            coordinates
        ):
            if node != neighbour:
                G.add_edge(node, neighbour, distance=haversine(coordinates[neighbour], point_spherical))

    return G
