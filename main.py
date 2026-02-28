from itertools import combinations
import networkx as nx
from networkx.algorithms import bipartite
from itertools import permutations
import matplotlib.pyplot as plt
import timeit
import time
from Utilities import *
from UtilitiesExact import *
from Coloring_MWIS_heuristics import exact_MWIS, greedy_MWIS, greedy1_MWIS

from resourceWeightsUtilities import *

import random

random.seed(3)
##############################################################################################################
def getNodeListGWMINOrder(G_function):
    G_function_copy = G_function.copy()
    GWMIN_list = []
    # get the node list sorted by degrees
    for node in list(G_function_copy.nodes):
        node_degree = float(G_function_copy.degree[node])
        node_weight = float(nodes_intervals.get(node))
        GWMIN_list = GWMIN_list + [node_weight/(node_degree + 1)]
    nodes_with_GWMIN = dict(zip(list(G_function_copy.nodes), GWMIN_list))
    node_list_GWMIN_order = sorted(nodes_with_GWMIN, key=nodes_with_GWMIN.get, reverse=True) #descending
    return node_list_GWMIN_order


def getMiddleNodeForTrees(G_function):
    nodes_degree_dict = getNodesDegreeDict(G_function)
    nodes_to_remove = getKeysByValue(nodes_degree_dict, '1') + getKeysByValue(nodes_degree_dict, '0')
    nodes_after_removal = removeSublistfromList(list(G_function.nodes), nodes_to_remove)
    #print("-----nodes_after_removal: {0}".format(nodes_after_removal))
    if len(nodes_after_removal) == 0:
        middle_node = getNodesInDegreeOrder(G_function)[0]
        #print("-----middle_node: {0}".format(middle_node))
        return middle_node
    elif len(nodes_after_removal) <= 2:
        middle_node = nodes_after_removal[0]
        return middle_node
    else:
        subgraph_after_removal = subgraphWithNodesInList(G_copy, nodes_after_removal)
        middle_node = getMiddleNodeForTrees(subgraph_after_removal)
        return middle_node


def removingNodesForLimitedPathRemoveNodeMaxDegree(G_function, node_list=[]):
    # using this function for reducing path length
    node_to_remove = getMiddleNodeForTrees(G_function)
    # print("-----node_to_remove: {0}".format(node_to_remove))
    G_function_copy = G_function.copy()
    G_function.remove_node(node_to_remove)
    subgraph_node_sets = [subgraph for subgraph in sorted(nx.connected_components(G_function), key=len, reverse=False)]
    # print(removing_node_list)
    # print(subgraph_node_sets)
    # print('-------------------subgraph_node_sets-----------------------------')
    subgraphs_dict.update({str(node_to_remove): subgraph_node_sets})
    # print(subgraphs_dict)
    # print('----------------------subgraphs_dict---------------------------------')

    for subgraph_node_set in subgraph_node_sets:
        subgraph = subgraphWithNodesInList(G_function, list(subgraph_node_set))
        # print(subgraph.node)
        # neighbors_of_removal_node = neighborsCheck(G_function_copy, [node_to_remove])
        # subgraph_GWMIN_removal = neighbors_of_removal_node + [node_to_remove]
        # print("-----subgraph_GWMIN_removal: {0}".format(subgraph_GWMIN_removal))
        # subgraph_GWMIN = subgraphWithoutNodesInList(G_function_copy, subgraph_GWMIN_removal)
        # print(subgraph_GWMIN.node)
        # print('------------------subgraph_GWMIN---------------------------')
        # print(bipartite.is_bipartite(subgraph))
        neighbors_of_removal_node = neighborsCheck(G_function_copy, [node_to_remove])
        # print("-----neighbors_of_removal_node: {0}".format(neighbors_of_removal_node))
        neighbors_of_neighbors_of_removal_node = neighborsCheck(G_function_copy, neighbors_of_removal_node)
        # print("-----neighbors_of_neighbors_of_removal_node: {0}".format(neighbors_of_neighbors_of_removal_node))
        subgraph_GWMIN_removal = neighbors_of_removal_node + neighbors_of_neighbors_of_removal_node + [node_to_remove]
        # print("-----subgraph_GWMIN_removal: {0}".format(subgraph_GWMIN_removal))
        subgraph_GWMIN_removal = removeDuplicate(subgraph_GWMIN_removal)
        subgraph_GWMIN = subgraphWithoutNodesInList(G_function_copy, subgraph_GWMIN_removal)
        # print("-----nodes in subgraph_GWMIN: {0}".format(subgraph_GWMIN.node))
        # diameter_of_graph = getDiameterOfGraph(subgraph)
        # print("-----diameter_of_graph: {0}".format(diameter_of_graph))
        # all_cycles = find_all_cycles(subgraph)
        all_cycles = cycle_basis(subgraph)
        if all_cycles != []:
            node_list_GWMIN_order = getNodeListGWMINOrder(subgraph_GWMIN)
            # print(node_list_odd_basis_order)
            node_list_odd_basis_order = GetCurrentCycleBasisOrder(G_function, node_list_GWMIN_order)
            reordered_nodes_in_subgraph = keepSublistfromList(node_list_odd_basis_order, (list(subgraph_node_set)))
            # print(reordered_nodes_in_subgraph) #['2', '9', '10', '11']
            # print('------------reordered_nodes_in_subgraph----------------')
            getSubgraphsDisctionaryOCBOGWMINwithLP(subgraph, reordered_nodes_in_subgraph)

        elif getDiameterOfGraph(subgraph) >= 3:
            # print('------in the function removingNodesForLimitedPathRemoveNodeMaxDegreegraph diameter >= 3------')

            # node_list_GWMIN_order = getNodeListGWMINOrder(subgraph_GWMIN)
            # node_list_degree_order = getNodesInDegreeOrder(subgraph_GWMIN)
            # print("-----node_list_degree_order: {0}".format(node_list_degree_order))
            # reordered_nodes_in_subgraph = keepSublistfromList(node_list_degree_order, (list(subgraph_node_set)))

            # print("-----reordered_nodes_in_subgraph: {0}".format(reordered_nodes_in_subgraph))
            removingNodesForLimitedPathRemoveNodeMaxDegree(subgraph)
    return subgraphs_dict


def TEMPremovingNodesForLimitedPathRemoveNodeMaxDegree(G_function, node_list=[]):
    # using this function for reducing path length

    if node_list == []:
        input_list_degree_order = getNodesInDegreeOrder(G_function)
    else:
        input_list_degree_order = node_list
    # print(input_list_degree_order)
    # print('------input_list_degree_order------')
    '''
    end_node_of_path = input_list_degree_order[-1]
    print(end_node_of_path)
    print('------end_node_of_path------')
    #nodelist_half_length = []
    for node in input_list_degree_order:
        all_paths_between_nodeAndend = nx.all_simple_paths(G_function, node, end_node_of_path, cutoff=None)
        max_length = [max([len(path) for path in all_paths_between_nodeAndend] + [0])]
        print(max_length)
        print('------max_length------')
        #path_length_max = [max([len(path) for path in all_paths_between_nodeAndend] + [0])]
        #print(path_length_max)
        #print('------path_length_max------')
        #if path_length_max == 2:
            #nodelist_half_length = nodelist_half_length + [node]
    #print(nodelist_half_length)
    #print('------nodelist_half_length------')
    '''

    node_to_remove = input_list_degree_order[0]
    # print(Q) #['0', '3', '2', '4', '5']
    # print('-------------------------------------------------------')
    G_function_copy = G_function.copy()
    G_function.remove_node(node_to_remove)
    subgraph_node_sets = [subgraph for subgraph in sorted(nx.connected_components(G_function), key=len, reverse=False)]
    # print(removing_node_list)
    # print(subgraph_node_sets)
    # print('-------------------subgraph_node_sets-----------------------------')
    subgraphs_dict.update({input_list_degree_order[0]: subgraph_node_sets})
    # print(subgraphs_dict)
    # print('----------------------subgraphs_dict---------------------------------')

    for subgraph_node_set in subgraph_node_sets:
        subgraph = subgraphWithNodesInList(G_function, list(subgraph_node_set))
        # print(subgraph.node)
        # neighbors_of_removal_node = neighborsCheck(G_function_copy, [node_to_remove])
        # subgraph_GWMIN_removal = neighbors_of_removal_node + [node_to_remove]
        # print("-----subgraph_GWMIN_removal: {0}".format(subgraph_GWMIN_removal))
        # subgraph_GWMIN = subgraphWithoutNodesInList(G_function_copy, subgraph_GWMIN_removal)
        # print(subgraph_GWMIN.node)
        # print('------------------subgraph_GWMIN---------------------------')
        # print(bipartite.is_bipartite(subgraph))
        neighbors_of_removal_node = neighborsCheck(G_function_copy, [node_to_remove])
        # print("-----neighbors_of_removal_node: {0}".format(neighbors_of_removal_node))
        neighbors_of_neighbors_of_removal_node = neighborsCheck(G_function_copy, neighbors_of_removal_node)
        # print("-----neighbors_of_neighbors_of_removal_node: {0}".format(neighbors_of_neighbors_of_removal_node))
        subgraph_GWMIN_removal = neighbors_of_removal_node + neighbors_of_neighbors_of_removal_node + [node_to_remove]
        # print("-----subgraph_GWMIN_removal: {0}".format(subgraph_GWMIN_removal))
        subgraph_GWMIN_removal = removeDuplicate(subgraph_GWMIN_removal)
        subgraph_GWMIN = subgraphWithoutNodesInList(G_function_copy, subgraph_GWMIN_removal)
        # print("-----nodes in subgraph_GWMIN: {0}".format(subgraph_GWMIN.node))
        # diameter_of_graph = getDiameterOfGraph(subgraph)
        # print("-----diameter_of_graph: {0}".format(diameter_of_graph))
        # all_cycles = find_all_cycles(subgraph)
        all_cycles = cycle_basis(subgraph)
        if all_cycles != []:
            node_list_GWMIN_order = getNodeListGWMINOrder(subgraph_GWMIN)
            # print(node_list_odd_basis_order)
            node_list_odd_basis_order = GetCurrentCycleBasisOrder(G_function, node_list_GWMIN_order)
            reordered_nodes_in_subgraph = keepSublistfromList(node_list_odd_basis_order, (list(subgraph_node_set)))
            # print(reordered_nodes_in_subgraph) #['2', '9', '10', '11']
            # print('------------reordered_nodes_in_subgraph----------------')
            getSubgraphsDisctionaryOCBOGWMINwithLP(subgraph, reordered_nodes_in_subgraph)

        elif getDiameterOfGraph(subgraph) >= 3:
            # print('------at line 485----------------')

            # node_list_GWMIN_order = getNodeListGWMINOrder(subgraph_GWMIN)
            node_list_degree_order = getNodesInDegreeOrder(subgraph_GWMIN)
            # print("-----node_list_degree_order: {0}".format(node_list_degree_order))
            reordered_nodes_in_subgraph = keepSublistfromList(node_list_degree_order, (list(subgraph_node_set)))
            # print("-----reordered_nodes_in_subgraph: {0}".format(reordered_nodes_in_subgraph))
            removingNodesForLimitedPathRemoveNodeMaxDegree(subgraph, reordered_nodes_in_subgraph)
    return subgraphs_dict


# getting the removed nodes and corresponding subgraphs list
subgraphs_dict = {}
def getSubgraphsDisctionaryOCBOGWMINwithLP(G_function, node_list):
    # print("-----input_node_list: {0}".format(node_list))

    # cycles_in_input_graph = find_all_cycles(G_function)
    cycles_in_input_graph = cycle_basis(G_function)
    if cycles_in_input_graph == []:
        if getDiameterOfGraph(G_function) >= 3:
            # print('------graph diameter >= 3------')
            removingNodesForLimitedPathRemoveNodeMaxDegree(G_function)
            return subgraphs_dict
        else:
            TEMPremovingNodesForLimitedPathRemoveNodeMaxDegree(G_function)
        return subgraphs_dict

    node_to_remove = node_list[0]
    # print("-----node_to_remove: {0}".format(node_to_remove))
    G_function_copy = G_function.copy()
    G_function.remove_node(node_to_remove)
    subgraph_node_sets = [subgraph for subgraph in sorted(nx.connected_components(G_function), key=len, reverse=False)]
    # print(removing_node_list)
    # print(subgraph_node_sets)
    # print('-------------------subgraph_node_sets-----------------------------')
    subgraphs_dict.update({node_list[0]: subgraph_node_sets})
    # print(subgraphs_dict)
    # print('----------------------subgraphs_dict---------------------------------')
    for subgraph_node_set in subgraph_node_sets:
        # print("-----list(subgraph_node_set): {0}".format(list(subgraph_node_set)))
        subgraph = subgraphWithNodesInList(G_function, list(subgraph_node_set))
        # print("-----subgraph.node: {0}".format(subgraph.node))
        subgraph_GWMIN_removal = neighborsCheck(G_function_copy, [node_to_remove]) + [node_to_remove]
        # print(subgraph_GWMIN_removal)
        # print('------------------subgraph_GWMIN_removal-----------------------------')
        subgraph_GWMIN = subgraphWithoutNodesInList(G_function_copy, subgraph_GWMIN_removal)
        # print(subgraph_GWMIN.node)
        # print('------------------subgraph_GWMIN.node-------------------------')
        # print(bipartite.is_bipartite(subgraph))
        # diameter_of_graph = getDiameterOfGraph(subgraph)
        # all_cycles = find_all_cycles(subgraph)
        # print("-----all_cycles: {0}".format(all_cycles))
        all_cycles = cycle_basis(subgraph)
        if all_cycles != []:
            node_list_GWMIN_order = getNodeListGWMINOrder(subgraph_GWMIN)
            # print(node_list_GWMIN_order)
            # print('------node_list_GWMIN_order------')
            later_part = removeSublistfromList(list(subgraph_node_set), node_list_GWMIN_order)
            remaining_nodes_degree_order = getNodesInDegreeOrder(subgraph)
            # print(remaining_nodes_degree_order)
            # print('------remaining_nodes_degree_order------')
            reordered_later_part = keepSublistfromList(remaining_nodes_degree_order, later_part)
            all_node_GWMIN_order = node_list_GWMIN_order + reordered_later_part
            # print(all_node_GWMIN_order)
            # print('------all_node_GWMIN_order------')
            # print(subgraph.node)
            # print('------subgraph.node------')
            node_list_odd_basis_order = GetCurrentCycleBasisOrder(subgraph, all_node_GWMIN_order)
            # print("-----node_list_odd_basis_order: {0}".format(node_list_odd_basis_order))
            reordered_nodes_in_subgraph = keepSublistfromList(node_list_odd_basis_order, (list(subgraph_node_set)))
            # print(reordered_nodes_in_subgraph) #['2', '9', '10', '11']
            # print('------------reordered_nodes_in_subgraph----------------')
            getSubgraphsDisctionaryOCBOGWMINwithLP(subgraph, reordered_nodes_in_subgraph)

        elif getDiameterOfGraph(subgraph) >= 3:
            reordered_nodes_in_subgraph = list(subgraph_node_set)
            # print(reordered_nodes_in_subgraph) #['3', '5', '9', '10', '11']
            # print('------------reordered_nodes_in_subgraph----------------')
            removingNodesForLimitedPathRemoveNodeMaxDegree(subgraph)
    return subgraphs_dict


def avgDegree(vertices_list):
    total_degree = 0
    for vertex in vertices_list:
        total_degree = total_degree + float(len(neighborhood(G, vertex, 1)))
    avgDegree = total_degree/len(vertices_list)
    return avgDegree



def getNodesFromBipartiteSubgraph(G_function):
    G_copy = G_function.copy()
    Queue = []
    # print(G.node)
    # print('------G.node------')
    isolated_nodes = list(nx.isolates(G_copy))

    for node in isolated_nodes:
        G_copy.remove_node(node)

    if list(G_copy.nodes) == []:
        Queue = Queue + isolated_nodes
        # print(Queue) #['4', '5', '6']
        # print('--------------------------------------')
    else:
        if bipartite.is_bipartite(G_copy) == True:
            Components = list(nx.connected_components(G_copy))
            for each_component in Components:
                Current_Subgraph = subgraphWithNodesInList(G_copy, list(each_component))
                X, Y = bipartite.sets(Current_Subgraph)
                if sum(getValuesByKeysAslist(nodes_intervals, list(X))) > sum(
                        getValuesByKeysAslist(nodes_intervals, list(Y))):
                    Queue = Queue + list(X) + isolated_nodes
                elif sum(getValuesByKeysAslist(nodes_intervals, list(X))) == sum(
                        getValuesByKeysAslist(nodes_intervals, list(Y))):
                    if avgDegree(list(X)) >= avgDegree(list(Y)):
                        Queue = Queue + list(X) + isolated_nodes
                    else:
                        Queue = Queue + list(Y) + isolated_nodes
                else:
                    Queue = Queue + list(Y) + isolated_nodes
        else:
            Queue = Queue
    # print(Queue)
    return Queue


def checkingBipartiteAndGetList(G_graph):
    ColorX_node_list = []
    # checking bipartite
    G_graph_copy = G_graph.copy()
    if bipartite.is_bipartite(G_graph_copy) == True:
        #print("the subgraph is bipartite")
        single_bipartite_graphs = list(connected_component_subgraphs(G_graph_copy))
        for subgraph in single_bipartite_graphs:
            nodes_list = getNodesFromBipartiteSubgraph(subgraph)
            ColorX_node_list = ColorX_node_list + nodes_list
    #else:
        #break
        #print("the subgraph is non-bipartite")
    return ColorX_node_list


def functionRemovingNodesForLimitedPathRemoveNodeMaxDegree(G_function, subgraphs_dict, node_list=[]):
    # using this function for reducing path length
    node_to_remove = getMiddleNodeForTrees(G_function)
    # print("-----node_to_remove: {0}".format(node_to_remove))

    G_function_copy = G_function.copy()
    G_function.remove_node(node_to_remove)
    subgraph_node_sets = [subgraph for subgraph in sorted(nx.connected_components(G_function), key=len, reverse=False)]
    # print(removing_node_list)
    # print(subgraph_node_sets)
    # print('-------------------subgraph_node_sets-----------------------------')
    subgraphs_dict.update({str(node_to_remove): subgraph_node_sets})
    # print("-----Current subgraphs_dict: {0}".format(subgraphs_dict))

    for subgraph_node_set in subgraph_node_sets:
        subgraph = subgraphWithNodesInList(G_function, list(subgraph_node_set))
        # print(subgraph.node)
        neighbors_of_removal_node = neighborsCheck(G_function_copy, [node_to_remove])
        # print("-----neighbors_of_removal_node: {0}".format(neighbors_of_removal_node))
        neighbors_of_neighbors_of_removal_node = neighborsCheck(G_function_copy, neighbors_of_removal_node)
        # print("-----neighbors_of_neighbors_of_removal_node: {0}".format(neighbors_of_neighbors_of_removal_node))
        subgraph_GWMIN_removal = neighbors_of_removal_node + neighbors_of_neighbors_of_removal_node + [node_to_remove]
        # print("-----subgraph_GWMIN_removal: {0}".format(subgraph_GWMIN_removal))
        subgraph_GWMIN_removal = removeDuplicate(subgraph_GWMIN_removal)
        subgraph_GWMIN = subgraphWithoutNodesInList(G_function_copy, subgraph_GWMIN_removal)
        # print("-----nodes in subgraph_GWMIN: {0}".format(subgraph_GWMIN.node))
        # diameter_of_graph = getDiameterOfGraph(subgraph)
        # all_cycles = find_all_cycles(subgraph)
        all_cycles = cycle_basis(subgraph)
        if all_cycles != []:
            node_list_GWMIN_order = getNodeListGWMINOrder(subgraph_GWMIN)
            # print(node_list_odd_basis_order)
            node_list_odd_basis_order = GetCurrentCycleBasisOrder(G_function, node_list_GWMIN_order)
            reordered_nodes_in_subgraph = keepSublistfromList(node_list_odd_basis_order, (list(subgraph_node_set)))
            # print("-----reordered_nodes_in_subgraph: {0}".format(reordered_nodes_in_subgraph))
            functionGetSubgraphsDisctionaryOCBOGWMINwithLP(subgraph, reordered_nodes_in_subgraph, subgraphs_dict)

        elif getDiameterOfGraph(subgraph) >= 3:
            # node_list_degree_order = getNodesInDegreeOrder(subgraph_GWMIN)
            # print("-----node_list_degree_order: {0}".format(node_list_degree_order))
            # reordered_nodes_in_subgraph = keepSublistfromList(node_list_degree_order, (list(subgraph_node_set)))
            functionRemovingNodesForLimitedPathRemoveNodeMaxDegree(subgraph, subgraphs_dict)
    return subgraphs_dict


def functionGetSubgraphsDisctionaryOCBOGWMINwithLP(G_function, node_list, subgraphs_dict):
    # print("-----Nodes in inputting G: {0}".format(G_function.node))
    # print("-----node_list_inputting: {0}".format(node_list))
    # cycles_in_input_graph = find_all_cycles(G_function)
    cycles_in_input_graph = cycle_basis(G_function)
    if cycles_in_input_graph == []:
        # print("-----cycles_in_input_graph: {0}".format(cycles_in_input_graph))
        # nodes_in_graph = list(G_function.node)
        # print("-----nodes_in_graph: {0}".format(nodes_in_graph))
        # removingNodesForLimitedPathRemoveNodeMaxDegree(G_function)
        functionRemovingNodesForLimitedPathRemoveNodeMaxDegree(G_function, subgraphs_dict)
        return subgraphs_dict

    node_to_remove = node_list[0]
    # print("-----node_to_remove: {0}".format(node_to_remove))
    G_function_copy = G_function.copy()
    G_function.remove_node(node_to_remove)
    subgraph_node_sets = [subgraph for subgraph in sorted(nx.connected_components(G_function), key=len, reverse=False)]
    # print(removing_node_list)
    # print(subgraph_node_sets)
    # print('-------------------subgraph_node_sets-----------------------------')
    subgraphs_dict.update({node_list[0]: subgraph_node_sets})
    # print(subgraphs_dict)
    # print('----------------------subgraphs_dict---------------------------------')

    for subgraph_node_set in subgraph_node_sets:
        subgraph = subgraphWithNodesInList(G_function, list(subgraph_node_set))
        # print(subgraph.node)
        # print('------subgraph.node------')
        subgraph_GWMIN_removal = neighborsCheck(G_function_copy, [node_to_remove]) + [node_to_remove]
        # print(subgraph_GWMIN_removal)
        # print('------------------subgraph_GWMIN_removal-----------------------------')
        subgraph_GWMIN = subgraphWithoutNodesInList(G_function_copy, subgraph_GWMIN_removal)
        # print(subgraph_GWMIN.node)
        # print('------------------subgraph_GWMIN.node-------------------------')
        # print(bipartite.is_bipartite(subgraph))
        # diameter_of_graph = getDiameterOfGraph(subgraph)
        # all_cycles = find_all_cycles(subgraph)
        # print("-----all_cycles: {0}".format(all_cycles))
        all_cycles = cycle_basis(subgraph)
        if all_cycles != []:
            node_list_GWMIN_order = getNodeListGWMINOrder(subgraph_GWMIN)
            # print(node_list_GWMIN_order)
            # print('------node_list_GWMIN_order------')
            later_part = removeSublistfromList(list(subgraph_node_set), node_list_GWMIN_order)
            remaining_nodes_degree_order = getNodesInDegreeOrder(subgraph)
            # print(remaining_nodes_degree_order)
            # print('------remaining_nodes_degree_order------')
            reordered_later_part = keepSublistfromList(remaining_nodes_degree_order, later_part)
            all_node_GWMIN_order = node_list_GWMIN_order + reordered_later_part
            # print(all_node_GWMIN_order)
            # print('------all_node_GWMIN_order------')
            # print(subgraph.node)
            # print('------subgraph.node------')
            node_list_odd_basis_order = GetCurrentCycleBasisOrder(subgraph, all_node_GWMIN_order)
            # print(node_list_odd_basis_order)
            # print('------node_list_odd_basis_order------')
            reordered_nodes_in_subgraph = keepSublistfromList(node_list_odd_basis_order, (list(subgraph_node_set)))
            # print(reordered_nodes_in_subgraph) #['2', '9', '10', '11']
            # print('------------reordered_nodes_in_subgraph----------------')
            functionGetSubgraphsDisctionaryOCBOGWMINwithLP(subgraph, reordered_nodes_in_subgraph, subgraphs_dict)

        elif getDiameterOfGraph(subgraph) >= 3:
            reordered_nodes_in_subgraph = list(subgraph_node_set)
            # print(reordered_nodes_in_subgraph) #['3', '5', '9', '10', '11']
            # print('------------reordered_nodes_in_subgraph----------------')
            functionRemovingNodesForLimitedPathRemoveNodeMaxDegree(subgraph, subgraphs_dict)
    return subgraphs_dict


def getNodeListforCompareGWMIN(LevelAndMWIS_dict, LevelAndNodes_dict, dictionary, key_index_dict, current_node_list):
    nodes_in_level = []
    # print("-----key_index_dict: {0}".format(key_index_dict))
    values_list_of_key = dictionary.get(key_index_dict)  # get values by the keys
    # print(values_list_of_key)
    # print('-----values_list_of_key------')
    # sys.exit("Error message")
    for item in values_list_of_key:
        nodes_in_level = nodes_in_level + list(item)
    nodes_in_level = nodes_in_level + [key_index_dict]  # merge all nodes together

    reordered_nodes_list = keepSublistfromList(current_node_list, nodes_in_level)
    # print("-----reordered_nodes_list: {0}".format(reordered_nodes_list))
    subgraph = subgraphWithNodesInList(G, reordered_nodes_list)

    neighbors_of_key = neighborsCheck(subgraph, [key_index_dict])
    removal_list = [key_index_dict] + neighbors_of_key
    # print(removal_list)
    # print('------removal_list------')
    graph_for_compare_list = subgraphWithoutNodesInList(subgraph, removal_list)
    # print("-----graph_for_compare_list.node: {0}".format(graph_for_compare_list.node))

    # start = timeit.default_timer()
    # diameter_of_graph = getDiameterOfGraph(graph_for_compare_list)
    # stop = timeit.default_timer()
    # print('Run Time for diameter_of_graph: ', stop - start)

    # all_cycles = find_all_cycles(graph_for_compare_list)
    all_cycles = cycle_basis(graph_for_compare_list)
    # sys.exit("Error message")
    if all_cycles != []:
        remaining_nodes_GWMIN_order = getNodeListGWMINOrder(graph_for_compare_list)
        node_list_odd_basis_order = GetCurrentCycleBasisOrder(graph_for_compare_list, remaining_nodes_GWMIN_order)
        reordered_remaining_nodes = keepSublistfromList(node_list_odd_basis_order, remaining_nodes_GWMIN_order)
        # print(reordered_remaining_nodes) #['3', '11', '1', '5', '6', '7', '8', '9', '10']
        # print('------reordered_remaining_nodes------')
        dict_subgraphs = {}
        dict_subgraphs = functionGetSubgraphsDisctionaryOCBOGWMINwithLP(graph_for_compare_list,
                                                                        reordered_remaining_nodes, dict_subgraphs)
        dict_subgraphs_reference = dict_subgraphs
        # print("-----with cycles dict_subgraphs-----: {0}".format(dict_subgraphs))
        # sys.exit("Error message")
        node_to_add = NEWgetColorXQueueGWMIN_with_GWMIN_adding(LevelAndMWIS_dict, LevelAndNodes_dict,
                                                               graph_for_compare_list, dict_subgraphs,
                                                               dict_subgraphs_reference, reordered_remaining_nodes)
        # sys.exit("Error message")
        nodes_to_compare = [key_index_dict] + node_to_add
        # print(nodes_to_compare) #['3', '5', '6', '7', '8', '9', '10']
        nodes_to_compare = removeDuplicate(nodes_to_compare)
    elif getDiameterOfGraph(graph_for_compare_list) >= 3:
        # print('---getting here, need to revise------')
        reordered_remaining_nodes = list(graph_for_compare_list.nodes)
        dict_subgraphs = {}
        dict_subgraphs = functionGetSubgraphsDisctionaryOCBOGWMINwithLP(graph_for_compare_list,
                                                                        reordered_remaining_nodes, dict_subgraphs)
        dict_subgraphs_reference = dict_subgraphs
        # print("-----without Cycles dict_subgraphs-----: {0}".format(dict_subgraphs))
        node_to_add = NEWgetColorXQueueGWMIN_with_GWMIN_adding(LevelAndMWIS_dict, LevelAndNodes_dict,
                                                               graph_for_compare_list, dict_subgraphs,
                                                               dict_subgraphs_reference, reordered_remaining_nodes)
        nodes_to_compare = [key_index_dict] + node_to_add
        # print(nodes_to_compare)
        nodes_to_compare = removeDuplicate(nodes_to_compare)
    else:
        node_to_add = checkingBipartiteAndGetList(graph_for_compare_list)
        nodes_to_compare = [key_index_dict] + node_to_add
        # print(nodes_to_compare)
        nodes_to_compare = removeDuplicate(nodes_to_compare)
    return nodes_to_compare


def getQueueInLevelNEW(LevelAndMWIS_dict,LevelAndNodes_dict,subgraphs_dictionary,Queue_previous_level,nodes_checking_list):
    #print("3557-----Queue_previous_level: {0}".format(Queue_previous_level))
    preliminary_set = []
    subgraphs_nodes_in_level = getSubgraphsByLastKey(subgraphs_dictionary)
    #print("3560-----subgraphs_nodes_in_level.node: {0}".format(subgraphs_nodes_in_level))

    for subgraph_nodes in subgraphs_nodes_in_level:
        #print("3579------subgraph_nodes : {0}".format(subgraph_nodes))
        #subgraph_nodes_examing = keepSublistfromList(node_list_degree_order,subgraph_nodes)
        #print("------subgraph_nodes_examing : {0}".format(subgraph_nodes_examing))
        if list(subgraph_nodes)[0] in nodes_checking_list:
            #print(subgraph_nodes)
            preliminary_set = preliminary_set + Queue_previous_level
            preliminary_set = removeDuplicate(preliminary_set)
            subgraph_nodes = []
        #print("3587------preliminary_set : {0}".format(preliminary_set))
        #subgraph = subgraphWithNodesInList(G_copy, subgraph_nodes)
        #part_of_G_in_level = subgraphWithNodesInList(G_copy, subgraph_nodes)
        #print("-----part_of_G_in_level-----: {0}".format(list(part_of_G_in_level.node)))
        #nodes_part_of_G = getNodesFromBipartiteSubgraph(part_of_G_in_level)
        #print("3592-----nodes_part_of_G: {0}".format(nodes_part_of_G))
        if subgraph_nodes != []:
            #print("3594------get to this line")
            part_of_G_in_level = subgraphWithNodesInList(G_copy, subgraph_nodes)
            nodes_part_of_G = getNodesFromBipartiteSubgraph(part_of_G_in_level)
            preliminary_set = nodes_part_of_G + preliminary_set
            preliminary_set = removeDuplicate(preliminary_set)
        else:
            #print("3598------get to this line")
            preliminary_set = preliminary_set + Queue_previous_level
            preliminary_set = removeDuplicate(preliminary_set)
    preliminary_set = preliminary_set + preliminary_set
    preliminary_set = removeDuplicate(preliminary_set)
    return preliminary_set


def compareToGetResult(nodes_found, node_to_compare):
    if sum(getValuesByKeysAslist(nodes_intervals, nodes_found)) > sum(getValuesByKeysAslist(nodes_intervals, node_to_compare)):
        final_queue = list(nodes_found)
    elif sum(getValuesByKeysAslist(nodes_intervals, nodes_found)) == sum(getValuesByKeysAslist(nodes_intervals, node_to_compare)):
        if avgDegree(nodes_found) >= avgDegree(node_to_compare):
            final_queue = list(nodes_found)
        else:
            final_queue = node_to_compare
    else:
        final_queue = node_to_compare
    return final_queue


def getQueueForLevelGWMIN(LevelAndMWIS_dict, LevelAndNodes_dict, overall_dict_subgraphs, current_dict_subgraphs, initial_list, current_node_list, nodes_previous_levels):
    key_index = getKeyOfLastElement(current_dict_subgraphs)
    compare_set = getNodeListforCompareGWMIN(LevelAndMWIS_dict, LevelAndNodes_dict, overall_dict_subgraphs, key_index, current_node_list)
    #print("3554-----compare_set: {0}".format(compare_set))
    preliminary_set = getQueueInLevelNEW(LevelAndMWIS_dict, LevelAndNodes_dict, current_dict_subgraphs, initial_list,nodes_previous_levels)
    #print("3627-----preliminary_set: {0}".format(preliminary_set))
    Queue = compareToGetResult(compare_set, preliminary_set)
    #sys.exit("Error message")
    #print("-----Final Queue-----: {0}".format(Queue))
    return Queue


def NEWgetColorXQueueGWMIN_with_GWMIN_adding(LevelAndMWIS_dict, LevelAndNodes_dict, G_function, overall_dict_subgraphs,
                                             current_subgraphs_reference, current_node_list):
    index = len(overall_dict_subgraphs)
    # print("3637------number of nodes removed: {0}".format(index))
    Queue = []
    i = 1

    while i <= index:  # set as the number of levels
        # print("------current_subgraphs_reference: {0}".format(current_subgraphs_reference))
        # key_index = getKeyOfLastElement(current_dict_subgraphs)
        removal_node = getKeyOfLastElement(current_subgraphs_reference)
        # print("3645------node removed: {0}".format(removal_node))
        nodes_in_level = []
        values_list_of_key = current_subgraphs_reference.get(removal_node)  # get values by the keys
        # print("------values_list_of_key------: {0}".format(values_list_of_key))
        for item in values_list_of_key:
            nodes_in_level = nodes_in_level + list(item)
        nodes_in_level = nodes_in_level + [removal_node]  # merge all nodes together
        nodes_current_level = keepSublistfromList(node_list_degree_order, nodes_in_level)  # make nodes in degree order
        # print("------nodes_current_level: {0}".format(nodes_current_level))
        # print("3656------current_MWIS_dict: {0}".format(LevelAndMWIS_dict))
        LevelAndNodes_dict.update({removal_node: nodes_current_level})
        # print("3658------LevelAndNodes_dict: {0}".format(LevelAndNodes_dict))
        level_nodes = []
        for element in values_list_of_key:
            element_list = keepSublistfromList(node_list_degree_order, list(element))
            nodes_found = getKeyByValueListNEW(LevelAndNodes_dict, element_list)
            if len(nodes_found) > 1:
                nodes_found = [nodes_found[0]]
            level_nodes = level_nodes + nodes_found
            # print("------element: {0}".format(element))
        # print("3667------level_nodes: {0}".format(level_nodes))

        initial_queue = []
        Checking_All_nodes = []
        if level_nodes == []:
            Queue = getQueueForLevelGWMIN(LevelAndMWIS_dict, LevelAndNodes_dict, overall_dict_subgraphs,
                                          current_subgraphs_reference, initial_queue, node_list_degree_order,
                                          Checking_All_nodes)
        else:
            for node in level_nodes:
                initial_queue = initial_queue + LevelAndMWIS_dict.get(node)
                Checking_All_nodes = Checking_All_nodes + LevelAndNodes_dict.get(node)
            # print("3678------initial_queue: {0}".format(initial_queue))
            Queue = getQueueForLevelGWMIN(LevelAndMWIS_dict, LevelAndNodes_dict, overall_dict_subgraphs,
                                          current_subgraphs_reference, initial_queue, node_list_degree_order,
                                          Checking_All_nodes)
            # sys.exit("Error message")
            # level_node = getKeysByValue(LevelAndNodes_dict, element_list))[0] #['13']  ['24']
            # print(level_node)
            # initial_queue = LevelAndMWIS_dict.get('10')
            # print(initial_queue)

        # Queue = getQueueForLevelGWMIN(overall_dict_subgraphs, current_subgraphs_reference, Queue, node_list_degree_order)
        Queue_reorder = keepSublistfromList(node_list_degree_order, Queue)
        LevelAndMWIS_dict.update({removal_node: Queue_reorder})
        # print("------current_MWIS_dict: {0}".format(LevelAndMWIS_dict))
        # print("------Queue_of_removal_node: {0}".format(Queue_reorder))

        # remove last element in the reference dict
        current_subgraphs_reference = removeLastElementinDict(current_subgraphs_reference)  # delete the last element
        i += 1

    # print("------current_MWIS_dict: {0}".format(LevelAndMWIS_dict))
    # compare the Queue with the
    # subgraph_after_removal = subgraphWithoutNodesInList(G_function2, all_removal_nodes)
    # preliminary_set = Queue #the subgraph is bipartite

    # print(preliminary_set)
    # print('------preliminary_set------')
    # print(subgraph_GWMIN.node)
    # print('------subgraph_GWMIN.node------')
    # compare_list = checkingBipartiteAndGetList(subgraph_GWMIN)
    # print(compare_list)
    # print('------compare_list------')
    # Final_Queue = compareToGetResult(compare_list, preliminary_set)
    # print(Final_Queue)
    # print('------Final_Queue-----')

    # Final_Queue = preliminary_set
    # print("650------Fianl_Final_Queue: {0}".format(Queue))
    return Queue


def SpecialgetNodesFromBipartiteSubgraph(G_function):
    G_copy = G_function.copy()
    # print("2412-----nodes in G_copy: {0}".format(G_copy.node))
    Queue = []
    # print(G.node)
    # print('------G.node------')
    isolated_nodes = list(nx.isolates(G_copy))

    for node in isolated_nodes:
        G_copy.remove_node(node)

    if list(G_copy.nodes) == []:
        Queue = Queue + isolated_nodes
        # print(Queue) #['4', '5', '6']
        # print('--------------------------------------')
    else:
        Components = list(nx.connected_components(G_copy))
        # print("2427-----connected components in G_copy: {0}".format(list(Components)))
        for each_component in Components:
            # print("2429-----each_component: {0}".format(each_component))
            Current_Subgraph = subgraphWithNodesInList(G_copy, list(each_component))
            X, Y = bipartite.sets(Current_Subgraph)
            # print("2432-----X: {0}".format(list(X)))
            if sum(getValuesByKeysAslist(nodes_intervals, list(X))) > sum(
                    getValuesByKeysAslist(nodes_intervals, list(Y))):
                Queue = Queue + list(X)
            elif sum(getValuesByKeysAslist(nodes_intervals, list(X))) == sum(
                    getValuesByKeysAslist(nodes_intervals, list(Y))):
                if avgDegree(list(X)) >= avgDegree(list(Y)):
                    Queue = Queue + list(X)
                else:
                    Queue = Queue + list(Y)
            else:
                Queue = Queue + list(Y)
        Queue = Queue + isolated_nodes
    Queue = removeDuplicate(Queue)
    # print("2442-----Queue: {0}".format(Queue))
    return Queue


def getMiddleNodeForTrees(G_function):
    nodes_degree_dict = getNodesDegreeDict(G_function)
    nodes_to_remove = getKeysByValue(nodes_degree_dict, '1') + getKeysByValue(nodes_degree_dict, '0')
    nodes_after_removal = removeSublistfromList(list(G_function.nodes), nodes_to_remove)
    #print("-----nodes_after_removal: {0}".format(nodes_after_removal))
    if len(nodes_after_removal) == 0:
        middle_node = getNodesInDegreeOrder(G_function)[0]
        #print("-----middle_node: {0}".format(middle_node))
        return middle_node
    elif len(nodes_after_removal) <= 2:
        middle_node = nodes_after_removal[0]
        return middle_node
    else:
        subgraph_after_removal = subgraphWithNodesInList(G_copy, nodes_after_removal)
        middle_node = getMiddleNodeForTrees(subgraph_after_removal)
        return middle_node


def AllMaximalIndependentSets(G_function, node_list_for_ordering, initial_list=[], subgraphs_dict={}):
    G_function_copy = G_function.copy()
    G_function_copy2 = G_function.copy()
    if bipartite.is_bipartite(G_function_copy) == True and getDiameterOfGraph(G_function_copy) < 2:
        Color0_list = SpecialgetNodesFromBipartiteSubgraph(G_function_copy)
        # print("2521-----Color0_list: {0}".format(Color0_list))

    else:
        # start_get_subgraphs_dict = timeit.default_timer()
        # get the dict for Bipartite subgraphs
        # bipartite_subgraphs = getSubgraphsDisctionaryOCBOGWMINwithLP(G_copy2, node_list_odd_basis_order)
        subgraphs_dict = {}
        bipartite_subgraphs = getSubgraphsDisctionaryOCBOGWMINwithLP(G_function_copy, node_list_for_ordering)
        # stop_get_subgraphs_dict = timeit.default_timer()
        # print('Run Time for get_subgraphs_dict: ', stop_get_subgraphs_dict - start_get_subgraphs_dict)
        # print("1845-----bipartite_subgraphs: {0}".format(bipartite_subgraphs))
        # print("1842-----number_of_nodes_removed: {0}".format(len(bipartite_subgraphs)))
        bipartite_subgraphs_reference = bipartite_subgraphs  # create a reference subgraph dictionary
        # sys.exit("Error message")

        # get color "0" list
        initial_list = []
        subgraphs_dict = {}  # initialize the dict
        LevelAndMWIS_dict = {}
        LevelAndNodes_dict = {}
        # start_get_color0 = timeit.default_timer()
        # start_get_color0 = time.process_time()
        Color0_list = NEWgetColorXQueueGWMIN_with_GWMIN_adding(LevelAndMWIS_dict, LevelAndNodes_dict, G_function_copy2,
                                                               bipartite_subgraphs, bipartite_subgraphs_reference,
                                                               node_list_for_ordering)
        # stop_get_color0 = timeit.default_timer()
        # stop_get_color0 = time.process_time()
        # print('Run Time for the first set: ', stop_get_color0 - start_get_color0)
    # print("2527-----Color0_list: {0}".format(Color0_list))
    # print("2635-----Number of lists: {0}".format(len(Color0_list)))
    # sys.exit("Error message")
    return Color0_list


#################################################################################################
# A3 functions

def A3getGWMINRemovalDisctionary(G_function, node_list, subgraphs_dict):
    # print("2808------node_list : {0}".format(node_list))
    if node_list == []:
        return subgraphs_dict

    node_to_remove = node_list[0]

    G_function_copy = G_function.copy()
    # G_function.remove_node(node_to_remove)
    nodes_GWMIN_removal = neighborsCheck(G_function_copy, [node_to_remove]) + [node_to_remove]
    # print(nodes_GWMIN_removal)
    # print('------nodes_GWMIN_removal------')
    remaining_nodes = removeSublistfromList(node_list, nodes_GWMIN_removal)
    # print(remaining_nodes)
    # print('------remaining_nodes------')

    # print('-------------------subgraph_node_sets-----------------------------')
    subgraphs_dict.update({node_list[0]: remaining_nodes})
    # print(subgraphs_dict)
    # print('----------------------subgraphs_dict---------------------------------')
    # sys.exit("Error message")
    if remaining_nodes != []:
        remaining_subgraph = subgraphWithNodesInList(G_function_copy, remaining_nodes)
        # print(remaining_subgraph.node)
        # print('------remaining_subgraph.node------')
        current_nodes_GWMIN_order = getNodeListGWMINOrder(remaining_subgraph)
        A3getGWMINRemovalDisctionary(remaining_subgraph, current_nodes_GWMIN_order, subgraphs_dict)
        # sys.exit("Error message")
    return subgraphs_dict

def A3getListInColoringOrder(G_function):
    # get the dict for Bipartite subgraphs
    subgraphs_dict = {}  # initial the dict space
    nodes_GWMIN_order = getNodeListGWMINOrder(G_function)
    GWMIN_Removal_dict = A3getGWMINRemovalDisctionary(G_function, nodes_GWMIN_order, subgraphs_dict)
    # print(GWMIN_Removal_dict)
    # print('----------GWMIN_Removal_dict for the whole graph-----------------')
    removal_nodes = list(GWMIN_Removal_dict.keys())
    # print(removal_nodes)
    # print('-----removal_nodes-----')
    return removal_nodes





###############################################################################################################
#Case#1
# set the weight for non-candidate nodes
NC_value = 0.0000001 # 6 0s
#NC_value = -1 this has problem
print("20-----weight of non-candidate nodes: {0}".format(NC_value))

# set the adjustment factor for multioption-tasks
AD_value = 0.00001 # 4 0s
print("24-----adjustment factor for multioption-tasks: {0}".format(AD_value))

#changed line 204 Q >= 2 (was Q >= 3)
LW_value = 1 #Case_1 = 17
#LW_value = 10 #Case_2 = 17 #make this value as 4*(average length of all jobs)
#LW_value = 0.001 #Case_3 = 17
print("30-----weight of length in same job: {0}".format(LW_value))

# load all the tasks
#Input_File = 'input_T111_TS10_D3.txt'
#Input_File = 'input_T111_TS10_liteF3.txt'
# Input_File = 'input_Week1_lite.txt'
# Input_File = 'input_Week1.txt' # about 0.6s
Input_File = 'input_Week2.txt'   # about 15s
# print("35-----The Input_File: {0}".format(Input_File))

# load all the tasks
Tasks = open(Input_File)
#resources_order = ['R1', 'R2', 'R3', 'R4'] #T100 #T110
resources_order = ['R1', 'R2', 'R3', 'R4', 'R5', 'R6', 'R7', 'R8', 'R9', 'R10', 'R11', 'R12', 'E'] # for T25D
#resources_order = ['M1', 'M2','M3','M4',
#                   'T1','T2','T3','T5','T6','T7','T8','T9','T10','T11','T12']
jobs_order = ['C1', 'C2', 'C3', 'P1', 'P2', 'OR'] #T101 #T101 #T104
#jobs_order = ['J1','J2','J3','J4'] ##T105 #T109 #T110 #T111
#jobs_order = ['J1','J2','J3','J4','J5'] #T106 #T108
Tasks_dict = eval(Tasks.read())
#print("2444-----Input Tasks_dict------: {0}".format(Tasks_dict))

Pre_AllNodesCondition = AllNodesConditions(Tasks_dict, resources_order)
print("839-----Pre_AllNodesCondition: {0}".format(Pre_AllNodesCondition))

AllNodesCondition = ADDIndexToAllNodesCondition(Pre_AllNodesCondition)
print("842-----original AllNodesCondition: {0}".format(AllNodesCondition))

AllNodesCondition_copy9 = AllNodesCondition.copy()
# resource_mapping = {
#     'R1': 10,
#     'R2': 20,
#     'R3': 30,
#     'R4': 40,
#     'R5': 50,
#     'R6': 60,
#     'R7': 70,
#     'R8': 30,
#     'R9': 40,
#     'R10': 50,
#     'R11': 60,
#     'R12': 70,
#     'E':  0
# }
# AvailWieghtsPerNode = append_assigned_numbers(AllNodesCondition_copy9, resource_mapping)
# print("849-----AvailWieghtsPerNode: {0}".format(AvailWieghtsPerNode))


excel_path = "WeightDataTemplate.csv"

resource_mapping = load_resource_mapping_from_excel(
    excel_path,
    resource_column='Resource',
    weight_column='Weight'
)

AvailWieghtsPerNode = append_number_from_resource_mapping(
    AllNodesCondition_copy9,
    resource_mapping
)
print("878-----AvailWieghtsPerNode: {0}".format(AvailWieghtsPerNode))


AllNodesCondition_copy = AllNodesCondition.copy()
AllNodesCondition_copy2 = AllNodesCondition.copy()
AllNodesCondition_copy3 = AllNodesCondition.copy()
AllNodesCondition_copy4 = AllNodesCondition.copy()
AllNodesCondition_copy5 = AllNodesCondition.copy()
AllNodesCondition_copy99 = AllNodesCondition.copy()
#print("2595-----original AllNodesCondition: {0}".format(AllNodesCondition))
#print("1262-----length testing: {0}".format(len(Pre_AllNodesCondition)))
Edges_List = FunctionEdgesList(AllNodesCondition)
print("64-----Edges_List: {0}".format(Edges_List))
print("65-----Number of Edges: {0}".format(len(Edges_List)))

G = nx.Graph()
for eachEdge in Edges_List:
    G.add_edge(str(eachEdge[0]), str(eachEdge[1]))  # ['1', '39']

task_nodes = InternalGenerateNodes(AllNodesCondition)
print("71-----number of nodes: {0}".format(len(task_nodes)))

#print("73-----G.nodes: {0}".format(G.nodes))

# the isolated nodes may cause problem
# we add back those isolated nodes to make sure of this potential situation
isolated_nodes = removeSublistfromList(task_nodes, G.nodes)

for node in isolated_nodes:
    G.add_node(node)

print("82-----G.nodes: {0}".format(G.nodes))
G_copy = G.copy()
G_copy2 = G.copy()
G_copy3 = G.copy()

# Timing Start
start_get_color0 = time.process_time()

TaskAndNode_list = functionTaskAndNodeDict(AllNodesCondition_copy)
# print("881----TaskAndNode_list : {0}".format(TaskAndNode_list))


TaskAndNode_dict_WM = functionWithMergingTaskAndNodeDict(AllNodesCondition_copy)
# print("2930----TaskAndNode_dict_WM : {0}".format(TaskAndNode_dict_WM))
# print("1430----TaskAndNode_dict : {0}".format(len(TaskAndNode_dict_WM)))


# Node_WeightsSum_dict = LenthWeightGetWeightsSumDict(TaskAndNode_dict_WM, LW_value, weight_SUM_dict={})
# the following update will make sure the shortest task is selected when multiple tasks have equal weights
Node_WeightsSum_dict = NEWLenthWeightGetWeightsSumDict(TaskAndNode_dict_WM, LW_value, AD_value, Edges_List, weight_SUM_dict={})
# print("3409------Node_WeightsSum_dict : {0}".format(Node_WeightsSum_dict))


NodesANDWeights_dict = GetNodesANDWeights_dict(Node_WeightsSum_dict, TaskAndNode_dict_WM)
# print("2939------NodesANDWeights_dict : {0}".format(NodesANDWeights_dict))


final_required_nodes = GetRequiredNodes(jobs_order, TaskAndNode_list)
# print("2639----final_required_nodes : {0}".format(final_required_nodes))


Final_NodesANDWeights_dict = FinalWeightsForColoring(NodesANDWeights_dict, final_required_nodes, NC_value)
# print("2947-----Final_NodesANDWeights_dict : {0}".format(Final_NodesANDWeights_dict))


# getting nodes and associated intervals internal
nodes_intervals = Final_NodesANDWeights_dict
print("926-----nodes_intervals: {0}".format(nodes_intervals))

new_node_intervals = add_assigned_number_to_node_weights(
    records=AvailWieghtsPerNode,      # your list of records ending with [node_id, assigned]
    node_intervals=nodes_intervals,   # your existing dict
    in_place=False,                   # keep original dict unchanged
    strict=True                       # error if any node id is missing
)
print("934-----new_node_intervals : {0}".format(new_node_intervals ))

nodes_intervals = new_node_intervals

node_list_interval_order = getIntervalOrder(nodes_intervals)
# print("861-----node_list_interval_order: {0}".format(node_list_interval_order))
node_list_GWMIN_order = getNodeListGWMINOrder(G_copy)
# print("2586-----node_list_GWMIN_order: {0}".format(node_list_GWMIN_order))


# node_list_OCBGWMIN_order
# start_cycle_order = timeit.default_timer()
node_list_odd_basis_order = GetCurrentCycleBasisOrder(G_copy, node_list_GWMIN_order)
# stop_cycle_order = timeit.default_timer()
# print("Run Time for cycle order list: {0}".format(stop_cycle_order - start_cycle_order))
# print("1445-----node_list_odd_basis_order: {0}".format(node_list_odd_basis_order))


node_list_degree_order = getNodesInDegreeOrder(G_copy)
# print("2730-----node_list_degree_order: {0}".format(len(node_list_degree_order)))


start_get_subgraphs_dict = timeit.default_timer()
# get the dict for Bipartite subgraphs
# bipartite_subgraphs = getSubgraphsDisctionaryOCBOGWMINwithLP(G_copy2, node_list_odd_basis_order)
bipartite_subgraphs = getSubgraphsDisctionaryOCBOGWMINwithLP(G_copy, node_list_odd_basis_order)
stop_get_subgraphs_dict = timeit.default_timer()
print('Run Time for getting subgraphs_dict: ', stop_get_subgraphs_dict - start_get_subgraphs_dict)
# print("1845-----bipartite_subgraphs: {0}".format(bipartite_subgraphs))
# print("1842-----number_of_nodes_removed: {0}".format(len(bipartite_subgraphs)))
bipartite_subgraphs_reference = bipartite_subgraphs  # create a reference subgraph dictionary
# sys.exit("Error message")


# get color "0" list
initial_list = []
subgraphs_dict = {} # initialize the dict
LevelAndMWIS_dict = {}
LevelAndNodes_dict = {}
#start_get_color0 = timeit.default_timer()
#start_get_color0 = time.process_time()

#--------------------------------------------
# A3 GWMIN


Color0_list = A3getListInColoringOrder(G_copy2)




# Color0_list = NEWgetColorXQueueGWMIN_with_GWMIN_adding(LevelAndMWIS_dict, LevelAndNodes_dict, G_copy2, bipartite_subgraphs, bipartite_subgraphs_reference, node_list_degree_order)

#------------
# testing 02172026
#
# Original_Color0_list = NEWgetColorXQueueGWMIN_with_GWMIN_adding(LevelAndMWIS_dict, LevelAndNodes_dict, G_copy2, bipartite_subgraphs, bipartite_subgraphs_reference, node_list_degree_order)
# Original_Color0_list_weight_sum = sum(getValuesByKeysAslist(nodes_intervals, Original_Color0_list))
# print("903-----Original_Color0_list: {0}".format(Original_Color0_list))
# print("904------Original_Color0_list weight sum: {0}".format(Original_Color0_list_weight_sum ))



# exact_Color0_list, ColGen_TotalWeight = exact_MWIS(G_copy2, nodes_intervals, b_score=0)
# print("909-----ColGen_TotalWeight: {0}".format(exact_ColGen_TotalWeight))
#
# EPS = 1e-9
# threshold = 1.0 + EPS
#
# # need to include the following at each step, the "nodes_intervals" is updating regularly
# n_shuffle = len(nodes_intervals)
#
# result = next(greedy_MWIS(G_copy2, nodes_intervals, threshold, n_shuffle, all_solutions=False))
# Color0_list, greedy_TotalWeight = result

# Color0_list, greedy_TotalWeight = greedy_MWIS(G_copy2, nodes_intervals, threshold, n_shuffle, all_solutions=False)

#--------------
#stop_get_color0 = timeit.default_timer()
#stop_get_color0 = time.process_time()
#print('Run Time for the first set: ', stop_get_color0 - start_get_color0)
# print("916-----Color0_list: {0}".format(Color0_list))
#print("2758-----Number of lists: {0}".format(len(Color0_list)))
#sys.exit("Error message")
required_nodes = final_required_nodes
#print("2675-----required_nodes: {0}".format(required_nodes))


nodes_assigned = keepSublistfromList(required_nodes, Color0_list)
# print("2688------nodes_assigned: {0}".format(nodes_assigned))


Task_Scheduled_list = GetTasksScheduled(nodes_assigned, AllNodesCondition_copy)
print("729------Task_Scheduled_list: {0}".format(Task_Scheduled_list))

Scheduled_Task_Name_List = FindTasksNamesScheduled(Task_Scheduled_list)
# print("2653------Scheduled_Task_Name_List: {0}".format(Scheduled_Task_Name_List))

Other_Nodes_To_Remove = NodesToRemoveForMultiOptions(Task_Scheduled_list, TaskAndNode_list)
# print("2948------Other_Nodes to remove: {0}".format(Other_Nodes_To_Remove))

Scheduled_Task_nodes = FindAllScheduledTaskNodes(Scheduled_Task_Name_List, TaskAndNode_list)
# print("2782------All Scheduled Task Nodes: {0}".format(Scheduled_Task_nodes))

All_Nodes_To_Remove = Scheduled_Task_nodes + Other_Nodes_To_Remove
# All_Nodes_To_Remove = removeDuplicate(All_Nodes_To_Remove)

InfoList_PreSelectedNodes = FindPreSelectedNodes(Task_Scheduled_list, AllNodesCondition_copy)
# print("2785------InfoList_PreSelectedNodes: {0}".format(InfoList_PreSelectedNodes))


PreSelectedNodes = GetNodeIndex(InfoList_PreSelectedNodes)
# print("2688------PreSelectedNodes: {0}".format(PreSelectedNodes))


G_step2 = subgraphWithoutNodesInList(G_copy3, All_Nodes_To_Remove)
# print("2856------nodes in G_step2: {0}".format(G_step2.node))



# for step2
# update the weight dict
UpdatedAllNodesConditions = UpdateAllNodesConditions(AllNodesCondition_copy4, Scheduled_Task_Name_List)
# print("2958------UpdatedAllNodesConditions: {0}".format(UpdatedAllNodesConditions))
UpdatedAllNodesConditions_copy = UpdatedAllNodesConditions.copy()

TaskAndNode_list = functionTaskAndNodeDict(UpdatedAllNodesConditions_copy)
# print("2697----TaskAndNode_list : {0}".format(TaskAndNode_list))


TaskAndNode_dict_WM = functionWithMergingTaskAndNodeDict(UpdatedAllNodesConditions_copy, TaskAndNode_dict_WM={})
# print("2930----TaskAndNode_dict_WM : {0}".format(TaskAndNode_dict_WM))
# print("2702----length TaskAndNode_dict_WM : {0}".format(len(TaskAndNode_dict_WM)))


# Node_WeightsSum_dict = LenthWeightGetWeightsSumDict(TaskAndNode_dict_WM, LW_value, weight_SUM_dict={})
# the following update will make sure the shortest task is selected when multiple tasks have equal weights
Node_WeightsSum_dict = NEWLenthWeightGetWeightsSumDict(TaskAndNode_dict_WM, LW_value, AD_value, Edges_List, weight_SUM_dict={})
# print("3409------Node_WeightsSum_dict : {0}".format(Node_WeightsSum_dict))


NodesANDWeights_dict = GetNodesANDWeights_dict(Node_WeightsSum_dict, TaskAndNode_dict_WM, NodesANDWeights_dict={})
# print("2717------NodesANDWeights_dict : {0}".format(NodesANDWeights_dict))


final_required_nodes = GetRequiredNodes(jobs_order, TaskAndNode_list)
# print("2493----final_required_nodes : {0}".format(final_required_nodes))


Final_NodesANDWeights_dict = FinalWeightsForColoring(NodesANDWeights_dict, final_required_nodes, NC_value)
# print("2987-----Final_NodesANDWeights_dict : {0}".format(Final_NodesANDWeights_dict))


neighbors_of_preSelectedNodes = neighborsCheck(G_step2, PreSelectedNodes)
# print("2774-----neighbors_of_preSelectedNodes: {0}".format(neighbors_of_Node1))
removal_list = PreSelectedNodes + neighbors_of_preSelectedNodes
removal_list = removeDuplicate(removal_list)
# print("3053-----removal_list: {0}".format(removal_list))


final_G_step2 = removeNodesInList(G_step2, removal_list)
# getting nodes and associated intervals internal
nodes_intervals = Final_NodesANDWeights_dict
node_list_interval_order = getIntervalOrder(nodes_intervals)
# print("2990-----node_list_interval_order: {0}".format(node_list_interval_order))
node_list_GWMIN_order = getNodeListGWMINOrder(final_G_step2)
# print("2992-----node_list_GWMIN_order: {0}".format(node_list_GWMIN_order))


# node_list_OCBGWMIN_order
# start_cycle_order = timeit.default_timer()
node_list_odd_basis_order = GetCurrentCycleBasisOrder(final_G_step2, node_list_GWMIN_order)
# stop_cycle_order = timeit.default_timer()
# print("Run Time for cycle order list: {0}".format(stop_cycle_order - start_cycle_order))
# print("1445-----node_list_odd_basis_order: {0}".format(node_list_odd_basis_order))

node_list_degree_order = getNodesInDegreeOrder(final_G_step2)
# print("2477-----node_list_degree_order: {0}".format(node_list_degree_order))
#

Color1_list = A3getListInColoringOrder(final_G_step2)

# Original_Color1_list = AllMaximalIndependentSets(final_G_step2, node_list_odd_basis_order)
# print("1014-----Original_Color1_list: {0}".format(Original_Color1_list))
#
# Original_Color1_list_weight_sum = sum(getValuesByKeysAslist(nodes_intervals, Original_Color1_list))
# print("1017------Original_Color1_list weight sum: {0}".format(Original_Color1_list_weight_sum ))

# Color1_list, Color1_ColGen_TotalWeight = exact_MWIS(final_G_step2, nodes_intervals, b_score=0)
# print("1021-----Color1_list: {0}".format(Color1_list))
# print("1020-----Color1_ColGen_TotalWeight: {0}".format(Color1_ColGen_TotalWeight))


# # need to include the following at each step, the "nodes_intervals" is updating regularly
# n_shuffle = len(nodes_intervals)
#
# result = next(greedy_MWIS(final_G_step2, nodes_intervals, threshold, n_shuffle, all_solutions=False))
# Color1_list, greedy_TotalWeight = result

required_nodes = final_required_nodes
# print("2780-----required_nodes: {0}".format(required_nodes))

feasible_sets = Color1_list
# print("3097-----counting feasible_sets: {0}".format(feasible_sets))
# print("3097-----counting feasible_sets: {0}".format(len(feasible_sets)))
if feasible_sets == []:
    # print("3099-----counting feasible_sets: {0}".format(len(feasible_sets)))
    Task_Scheduled_list = InfoList_PreSelectedNodes
    print("2788------Task_Scheduled_list: {0}".format(Task_Scheduled_list))
else:
    Node_list_output = feasible_sets
    # print("2812------Node_list_output: {0}".format(Node_list_output))

    nodes_assigned = keepSublistfromList(required_nodes, Node_list_output)
    # print("2815------nodes_assigned: {0}".format(nodes_assigned))

    Task_Scheduled_list = GetTasksScheduled(nodes_assigned, AllNodesCondition_copy) + InfoList_PreSelectedNodes
    print("2859------Task_Scheduled_list: {0}".format(Task_Scheduled_list))

Scheduled_Task_Name_List = FindTasksNamesScheduled(Task_Scheduled_list)
# print("3030------Scheduled_Task_Name_List: {0}".format(Scheduled_Task_Name_List))

Other_Nodes_To_Remove = NodesToRemoveForMultiOptions(Task_Scheduled_list, TaskAndNode_list)
# print("2948------Other_Nodes to remove: {0}".format(Other_Nodes_To_Remove))


Scheduled_Task_nodes = FindAllScheduledTaskNodes(Scheduled_Task_Name_List, TaskAndNode_list)
# print("2893------All Scheduled Task Nodes: {0}".format(Scheduled_Task_nodes))
All_Nodes_To_Remove = Scheduled_Task_nodes + Other_Nodes_To_Remove
# print("2895------All_Nodes_To_Remove: {0}".format(All_Nodes_To_Remove))

G_step3 = subgraphWithoutNodesInList(G_step2, All_Nodes_To_Remove)
# print("2897------nodes in G_step3: {0}".format(G_step3.node))

InfoList_PreSelectedNodes = FindPreSelectedNodes(Task_Scheduled_list, UpdatedAllNodesConditions)
# print("2877------InfoList_PreSelectedNodes: {0}".format(InfoList_PreSelectedNodes))
PreSelectedNodes = GetNodeIndex(InfoList_PreSelectedNodes)
# print("3054------PreSelectedNodes: {0}".format(PreSelectedNodes))


# for step3-11
# update the weight dict
Step_Number = 3
while list(G_step3.nodes) != []:
    print("2891------Step_Number: {0}".format(Step_Number))
    Step_Number = Step_Number + 1

    UpdatedAllNodesConditions = UpdateAllNodesConditions(UpdatedAllNodesConditions, Scheduled_Task_Name_List)
    # print("2958------UpdatedAllNodesConditions: {0}".format(UpdatedAllNodesConditions))
    UpdatedAllNodesConditions_copy = UpdatedAllNodesConditions.copy()

    TaskAndNode_list = functionTaskAndNodeDict(UpdatedAllNodesConditions_copy)
    # print("2924----TaskAndNode_list : {0}".format(TaskAndNode_list))

    TaskAndNode_dict_WM = functionWithMergingTaskAndNodeDict(UpdatedAllNodesConditions_copy, TaskAndNode_dict_WM={})
    # print("2930----TaskAndNode_dict_WM : {0}".format(TaskAndNode_dict_WM))
    # print("2702----length TaskAndNode_dict_WM : {0}".format(len(TaskAndNode_dict_WM)))

    # Node_WeightsSum_dict = LenthWeightGetWeightsSumDict(TaskAndNode_dict_WM, LW_value, weight_SUM_dict={})
    # the following update will make sure the shortest task is selected when multiple tasks have equal weights
    Node_WeightsSum_dict = NEWLenthWeightGetWeightsSumDict(TaskAndNode_dict_WM, LW_value, AD_value,Edges_List, weight_SUM_dict={})
    # print("3409------Node_WeightsSum_dict : {0}".format(Node_WeightsSum_dict))

    NodesANDWeights_dict = GetNodesANDWeights_dict(Node_WeightsSum_dict, TaskAndNode_dict_WM, NodesANDWeights_dict={})
    # print("2942------NodesANDWeights_dict : {0}".format(NodesANDWeights_dict))

    final_required_nodes = GetRequiredNodes(jobs_order, TaskAndNode_list)
    # print("2493----final_required_nodes : {0}".format(final_required_nodes))

    Final_NodesANDWeights_dict = FinalWeightsForColoring(NodesANDWeights_dict, final_required_nodes, NC_value)
    # print("3248-----Final_NodesANDWeights_dict : {0}".format(Final_NodesANDWeights_dict))

    neighbors_of_preSelectedNodes = neighborsCheck(G_step3, PreSelectedNodes)
    # print("2774-----neighbors_of_preSelectedNodes: {0}".format(neighbors_of_Node1))
    removal_list = PreSelectedNodes + neighbors_of_preSelectedNodes
    removal_list = removeDuplicate(removal_list)
    # print("3138-----removal_list: {0}".format(removal_list))

    final_G_step3 = removeNodesInList(G_step3, removal_list)
    # print("3267-----final_G_step3: {0}".format(final_G_step3.node))
    # print("3268-----final_G_step3: {0}".format(len(final_G_step3.node)))
    # getting nodes and associated intervals internal
    nodes_intervals = Final_NodesANDWeights_dict
    node_list_interval_order = getIntervalOrder(nodes_intervals)
    # print("2990-----node_list_interval_order: {0}".format(node_list_interval_order))
    node_list_GWMIN_order = NEWgetNodeListGWMINOrder(final_G_step3, nodes_intervals)
    # print("2992-----node_list_GWMIN_order: {0}".format(node_list_GWMIN_order))

    # node_list_OCBGWMIN_order
    # start_cycle_order = timeit.default_timer()
    node_list_odd_basis_order = GetCurrentCycleBasisOrder(final_G_step3, node_list_GWMIN_order)
    # stop_cycle_order = timeit.default_timer()
    # print("Run Time for cycle order list: {0}".format(stop_cycle_order - start_cycle_order))
    # print("1445-----node_list_odd_basis_order: {0}".format(node_list_odd_basis_order))

    node_list_degree_order = getNodesInDegreeOrder(final_G_step3)
    # print("2477-----node_list_degree_order: {0}".format(node_list_degree_order))

    Color2_list = A3getListInColoringOrder(final_G_step3)

    # Color2_list = AllMaximalIndependentSets(final_G_step3, node_list_odd_basis_order)
    # # print("2989-----Color2_list: {0}".format(Color2_list))
    #
    # Original_Color2_list = AllMaximalIndependentSets(final_G_step3, node_list_odd_basis_order)
    # print("1127-----Original_Color2_list: {0}".format(Original_Color2_list))
    #
    # Original_Color2_list_weight_sum = sum(getValuesByKeysAslist(nodes_intervals, Original_Color2_list))
    # print("1130------Original_Color2_list weight sum: {0}".format(Original_Color2_list_weight_sum))

    # Color2_list, Color2_ColGen_TotalWeight = exact_MWIS(final_G_step3, nodes_intervals, b_score=0)
    # # print("1133-----Color2_list: {0}".format(Color2_list))
    # # print("1134-----Color2_ColGen_TotalWeight: {0}".format(Color2_ColGen_TotalWeight))

    # need to include the following at each step, the "nodes_intervals" is updating regularly
    # print(final_G_step3.nodes)
    # n_shuffle = len(nodes_intervals)
    #
    # result3 = next(greedy_MWIS(final_G_step3, nodes_intervals, threshold, n_shuffle, all_solutions=False))
    # Color2_list, greedy_TotalWeight = result3







    required_nodes = final_required_nodes
    # print("2992-----required_nodes: {0}".format(required_nodes))

    feasible_sets = Color2_list
    # print("1172-----feasible_sets: {0}".format(feasible_sets))
    # print("1173-----counting feasible_sets: {0}".format(len(feasible_sets)))
    if feasible_sets == []:
        # print("3099-----counting feasible_sets: {0}".format(len(feasible_sets)))
        Task_Scheduled_list = InfoList_PreSelectedNodes
        print("2917------Task_Scheduled_list: {0}".format(Task_Scheduled_list))

    else:
        Node_list_output = feasible_sets
        # print("2997------Node_list_output: {0}".format(Node_list_output))

        nodes_assigned = keepSublistfromList(required_nodes, Node_list_output)
        # print("3000------nodes_assigned: {0}".format(nodes_assigned))

        Task_Scheduled_list = GetTasksScheduled(nodes_assigned, AllNodesCondition_copy) + InfoList_PreSelectedNodes
        print("2926------Task_Scheduled_list: {0}".format(Task_Scheduled_list))

    Scheduled_Task_Name_List = FindTasksNamesScheduled(Task_Scheduled_list)
    # print("3003------Scheduled_Task_Name_List: {0}".format(Scheduled_Task_Name_List))

    Other_Nodes_To_Remove = NodesToRemoveForMultiOptions(Task_Scheduled_list, TaskAndNode_list)
    # print("2948------Other_Nodes to remove: {0}".format(Other_Nodes_To_Remove))

    Scheduled_Task_nodes = FindAllScheduledTaskNodes(Scheduled_Task_Name_List, TaskAndNode_list)
    # print("3011------All Scheduled Task Nodes: {0}".format(Scheduled_Task_nodes))
    All_Nodes_To_Remove = Scheduled_Task_nodes + Other_Nodes_To_Remove

    G_step3 = subgraphWithoutNodesInList(G_step3, All_Nodes_To_Remove)
    # print("1167------G_step3: {0}".format(G_step3))
    # print("1168------nodes in G_step3: {0}".format(G_step3.nodes))

    InfoList_PreSelectedNodes = FindPreSelectedNodes(Task_Scheduled_list, UpdatedAllNodesConditions)
    # print("3858------InfoList_PreSelectedNodes: {0}".format(InfoList_PreSelectedNodes))
    PreSelectedNodes = GetNodeIndex(InfoList_PreSelectedNodes)

# timing Stop
stop_get_color0 = time.process_time()
print('Run Time for all: ', stop_get_color0 - start_get_color0)