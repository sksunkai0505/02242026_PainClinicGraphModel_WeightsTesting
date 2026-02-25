import networkx as nx
from Utilities import *
from networkx.algorithms import bipartite

def subgraphWithNodesInList(G_function, node_list_keeping):
    G_for_function = G_function.copy()
    node_to_remove = removeSublistfromList(list(G_for_function.nodes), node_list_keeping)
    for node in node_to_remove:
        G_for_function.remove_node(node)
    return G_for_function


def neighborsCheck(G, nodes_to_check):
    #checking for the final output list
    neighbors_list_final = []
    for node in nodes_to_check:
        neighbors_list = list(G.neighbors(node))
        neighbors_list_final = neighbors_list_final + neighbors_list
    return neighbors_list_final


def subgraphWithoutNodesInList(G_function, node_list_removal):
    #print(node_list_removal)
    G_for_function = G_function.copy()
    for node in node_list_removal:
        #print(node)
        G_for_function.remove_node(node)
    return G_for_function


def connected_component_subgraphs(G, copy=True):
    """Generate connected components as subgraphs.

    Parameters
    ----------
    G : NetworkX graph
       An undirected graph.

    copy: bool (default=True)
      If True make a copy of the graph attributes

    Returns
    -------
    comp : generator
      A generator of graphs, one for each connected component of G.

    Examples
    --------
    >>> G = nx.path_graph(4)
    >>> G.add_edge(5,6)
    >>> graphs = list(nx.connected_component_subgraphs(G))

    See Also
    --------
    connected_components

    Notes
    -----
    For undirected graphs only.
    Graph, node, and edge attributes are copied to the subgraphs by default.
    """
    for c in nx.connected_components(G):
        if copy:
            yield G.subgraph(c).copy()
        else:
            yield G.subgraph(c)


def getDiameterOfGraph(G_function):
    output_diameter = 0
    individual_graphs = list(connected_component_subgraphs(G_function))
    for subgraph in individual_graphs:
        #print(subgraph.node)
        Q = diameter(subgraph)
        if Q >= 2:
            output_diameter = 3
            return output_diameter
    return output_diameter







# def getKeyOfLastElement(dict_subgraphs):
#     number_of_items = len(dict_subgraphs)
#     index_last_element = (number_of_items - 1)
#     # print(index_last_element) #1
#     key_of_last_element = list(dict_subgraphs.keys())[index_last_element]
#     return key_of_last_element
#
# def getKeyByValueListNEW(dictionary, list_to_search):
#     key = []
#     for level_node, nodes_in_level in dictionary.items():    # for name, age in dictionary.iteritems():  (for Python 2.x)
#         #print(nodes_in_level == list_to_search)
#         if nodes_in_level == list_to_search:
#             key = key + [level_node]
#         else:
#             key = key
#     return key
#

#
#
# def getSubgraphsByLastKey(dict_subgraphs):
#     key_of_last_element = getKeyOfLastElement(dict_subgraphs)
#     #print(key_last_element) #4
#     subgraphs_of_key = dict_subgraphs[key_of_last_element]
#     #print(subgraphs_of_key)
#     return subgraphs_of_key
#
#
# def getValuesByKeysAslist(mydict, key_list):
#     #get values by key list, returns a list of float
#     return [float(i) for i in [mydict[x] for x in key_list]]
#
#
# def neighborhood(G, node, n):
#     #return the neighbors of a given node with a given distance
#     path_lengths = nx.single_source_dijkstra_path_length(G, node)
#     return [node for node, length in path_lengths.items() if length == n]
#
#
# def removeLastElementinDict(current_dict_subgraphs):
#     key_index = getKeyOfLastElement(current_dict_subgraphs)
#     current_dict_subgraphs.pop(key_index)
#     return current_dict_subgraphs
#
#
#
#
# # def getKeyOfLastElement(dict_subgraphs):
# #     number_of_items = len(dict_subgraphs)
# #     index_last_element = (number_of_items - 1)
# #     #print(index_last_element) #1
# #     key_of_last_element = list(dict_subgraphs.keys())[index_last_element]
# #     return key_of_last_element
# #
# #
# # def getKeyByValueListNEW(dictionary, list_to_search):
# #     key = []
# #     for level_node, nodes_in_level in dictionary.items():    # for name, age in dictionary.iteritems():  (for Python 2.x)
# #         #print(nodes_in_level == list_to_search)
# #         if nodes_in_level == list_to_search:
# #             key = key + [level_node]
# #         else:
# #             key = key
# #     return key
# #
# #
# # def neighborhood(G, node, n):
# #     #return the neighbors of a given node with a given distance
# #     path_lengths = nx.single_source_dijkstra_path_length(G, node)
# #     return [node for node, length in path_lengths.items() if length == n]
# #
# #
# #
# # def avgDegree(G_original, vertices_list):
# #     G_originalCopy = G_original.copy()
# #     total_degree = 0
# #     for vertex in vertices_list:
# #         total_degree = total_degree + float(len(neighborhood(G_originalCopy, vertex, 1)))
# #     avgDegree = total_degree/len(vertices_list)
# #     return avgDegree
# #
# #
# # def getNodesFromBipartiteSubgraph(G_function, nodes_intervals, G_original):
# #     G_copy = G_function.copy()
# #     Queue = []
# #     # print(G.node)
# #     # print('------G.node------')
# #     isolated_nodes = list(nx.isolates(G_function))
# #
# #     for node in isolated_nodes:
# #         G_copy.remove_node(node)
# #
# #     if list(G_copy.nodes) == []:
# #         Queue = Queue + isolated_nodes
# #         # print(Queue) #['4', '5', '6']
# #         # print('--------------------------------------')
# #     else:
# #         if bipartite.is_bipartite(G_copy) == True:
# #             Components = list(nx.connected_components(G_copy))
# #             for each_component in Components:
# #                 Current_Subgraph = subgraphWithNodesInList(G_copy, list(each_component))
# #                 X, Y = bipartite.sets(Current_Subgraph)
# #                 if sum(getValuesByKeysAslist(nodes_intervals, list(X))) > sum(
# #                         getValuesByKeysAslist(nodes_intervals, list(Y))):
# #                     Queue = Queue + list(X) + isolated_nodes
# #                 elif sum(getValuesByKeysAslist(nodes_intervals, list(X))) == sum(
# #                         getValuesByKeysAslist(nodes_intervals, list(Y))):
# #                     if avgDegree(G_original, list(X)) >= avgDegree(G_original,list(Y)):
# #                         Queue = Queue + list(X) + isolated_nodes
# #                     else:
# #                         Queue = Queue + list(Y) + isolated_nodes
# #                 else:
# #                     Queue = Queue + list(Y) + isolated_nodes
# #         else:
# #             Queue = Queue
# #     # print(Queue)
# #     return Queue
# #
#
# #
# # def checkingBipartiteAndGetList(G_graph, nodes_intervals,G_original):
# #     ColorX_node_list = []
# #     # checking bipartite
# #     G_graph_copy = G_graph.copy()
# #     if bipartite.is_bipartite(G_graph_copy) == True:
# #         #print("the subgraph is bipartite")
# #         # single_bipartite_graphs = [subgraph for subgraph in
# #         #                       sorted(nx.connected_components(G_graph_copy), key=len, reverse=False)]
# #         single_bipartite_graphs = list(connected_component_subgraphs(G_graph_copy))
# #         # subgraph_node_sets = [subgraph for subgraph in
# #         #                       sorted(nx.connected_components(G_function), key=len, reverse=False)]
# #         for subgraph in single_bipartite_graphs:
# #             nodes_list = getNodesFromBipartiteSubgraph(subgraph, nodes_intervals,G_original)
# #             ColorX_node_list = ColorX_node_list + nodes_list
# #     #else:
# #         #break
# #         #print("the subgraph is non-bipartite")
# #     return ColorX_node_list
# #
# #
# #
# # def ApproximationGetNodeListforCompareGWMIN(LevelAndMWIS_dict, LevelAndNodes_dict, dictionary, key_index_dict,
# #                                             current_node_list, G_original, nodes_intervals):
# #     nodes_in_level = []
# #     # print("-----key_index_dict: {0}".format(key_index_dict))
# #     values_list_of_key = dictionary.get(key_index_dict)  # get values by the keys
# #     # print(values_list_of_key)
# #     # print('-----values_list_of_key------')
# #     # sys.exit("Error message")
# #     for item in values_list_of_key:
# #         nodes_in_level = nodes_in_level + list(item)
# #     nodes_in_level = nodes_in_level + [key_index_dict]  # merge all nodes together
# #
# #     reordered_nodes_list = keepSublistfromList(current_node_list, nodes_in_level)
# #     # print("-----reordered_nodes_list: {0}".format(reordered_nodes_list))
# #     subgraph = subgraphWithNodesInList(G_original, reordered_nodes_list)
# #     print("151-----when having cycles nodes_to_compare: {0}".format(subgraph))
# #
# #     neighbors_of_key = neighborsCheck(subgraph, [key_index_dict])
# #     removal_list = [key_index_dict] + neighbors_of_key
# #     # print(removal_list)
# #     # print('------removal_list------')
# #     graph_for_compare_list = subgraphWithoutNodesInList(subgraph, removal_list)
# #     # print("1452-----graph_for_compare_list.node: {0}".format(graph_for_compare_list.node))
# #
# #     all_cycles = cycle_basis(graph_for_compare_list)
# #     # sys.exit("Error message")
# #     if all_cycles != []:
# #         node_to_add = getListInColoringOrder(graph_for_compare_list,nodes_intervals)
# #         # sys.exit("Error message")
# #         nodes_to_compare = [key_index_dict] + node_to_add
# #         # print("1460-----when having cycles nodes_to_compare: {0}".format(nodes_to_compare))
# #         nodes_to_compare = removeDuplicate(nodes_to_compare)
# #     elif getDiameterOfGraph(graph_for_compare_list) >= 3:
# #         # print('Cannot get result')
# #         # print("-----graph_for_compare_list.node: {0}".format(graph_for_compare_list.node))
# #         node_to_add = getListInColoringOrder(graph_for_compare_list, nodes_intervals)
# #         nodes_to_compare = [key_index_dict] + node_to_add
# #         # print(nodes_to_compare)
# #         nodes_to_compare = removeDuplicate(nodes_to_compare)
# #     else:
# #         # print('Can get results directly')
# #         node_to_add = checkingBipartiteAndGetList(graph_for_compare_list, nodes_intervals, G_original)
# #         nodes_to_compare = [key_index_dict] + node_to_add
# #         # print(nodes_to_compare)
# #         nodes_to_compare = removeDuplicate(nodes_to_compare)
# #     return nodes_to_compare
# #
# #
# # def getSubgraphsByLastKey(dict_subgraphs):
# #     key_of_last_element = getKeyOfLastElement(dict_subgraphs)
# #     #print(key_last_element) #4
# #     subgraphs_of_key = dict_subgraphs[key_of_last_element]
# #     #print(subgraphs_of_key)
# #     return subgraphs_of_key
# #
# #
# # def getQueueInLevelNEW(LevelAndMWIS_dict,LevelAndNodes_dict,subgraphs_dictionary,Queue_previous_level,nodes_checking_list, G_original, nodes_intervals):
# #     #print("3557-----Queue_previous_level: {0}".format(Queue_previous_level))
# #     preliminary_set = []
# #     subgraphs_nodes_in_level = getSubgraphsByLastKey(subgraphs_dictionary)
# #     #print("3560-----subgraphs_nodes_in_level.node: {0}".format(subgraphs_nodes_in_level))
# #
# #     for subgraph_nodes in subgraphs_nodes_in_level:
# #         #print("3579------subgraph_nodes : {0}".format(subgraph_nodes))
# #         #subgraph_nodes_examing = keepSublistfromList(node_list_degree_order,subgraph_nodes)
# #         #print("------subgraph_nodes_examing : {0}".format(subgraph_nodes_examing))
# #         if list(subgraph_nodes)[0] in nodes_checking_list:
# #             #print(subgraph_nodes)
# #             preliminary_set = preliminary_set + Queue_previous_level
# #             preliminary_set = removeDuplicate(preliminary_set)
# #             subgraph_nodes = []
# #         #print("3587------preliminary_set : {0}".format(preliminary_set))
# #         #subgraph = subgraphWithNodesInList(G_copy, subgraph_nodes)
# #         #part_of_G_in_level = subgraphWithNodesInList(G_copy, subgraph_nodes)
# #         #print("-----part_of_G_in_level-----: {0}".format(list(part_of_G_in_level.node)))
# #         #nodes_part_of_G = getNodesFromBipartiteSubgraph(part_of_G_in_level)
# #         #print("3592-----nodes_part_of_G: {0}".format(nodes_part_of_G))
# #         if subgraph_nodes != []:
# #             #print("3594------get to this line")
# #             part_of_G_in_level = subgraphWithNodesInList(G_original, subgraph_nodes)
# #             nodes_part_of_G = getNodesFromBipartiteSubgraph(part_of_G_in_level,nodes_intervals,G_original)
# #             preliminary_set = nodes_part_of_G + preliminary_set
# #             preliminary_set = removeDuplicate(preliminary_set)
# #         else:
# #             #print("3598------get to this line")
# #             preliminary_set = preliminary_set + Queue_previous_level
# #             preliminary_set = removeDuplicate(preliminary_set)
# #     preliminary_set = preliminary_set + preliminary_set
# #     preliminary_set = removeDuplicate(preliminary_set)
# #     return preliminary_set
# #
# #
# # def getValuesByKeysAslist(mydict, key_list):
# #     #get values by key list, returns a list of float
# #     return [float(i) for i in [mydict[x] for x in key_list]]
# #
# #
# # def compareToGetResult(nodes_found, node_to_compare, G_original, nodes_intervals):
# #     if sum(getValuesByKeysAslist(nodes_intervals, nodes_found)) > sum(getValuesByKeysAslist(nodes_intervals, node_to_compare)):
# #         final_queue = list(nodes_found)
# #     elif sum(getValuesByKeysAslist(nodes_intervals, nodes_found)) == sum(getValuesByKeysAslist(nodes_intervals, node_to_compare)):
# #         if avgDegree(G_original, nodes_found) >= avgDegree(G_original, node_to_compare):
# #             final_queue = list(nodes_found)
# #         else:
# #             final_queue = node_to_compare
# #     else:
# #         final_queue = node_to_compare
# #     return final_queue
# #
# #
# #
# # def getQueueForLevelGWMIN_CompareSetSubgraph(LevelAndMWIS_dict, LevelAndNodes_dict, overall_dict_subgraphs, current_dict_subgraphs, initial_list,current_node_list,Checking_All_nodes,G_original, nodes_intervals):
# #     key_index = getKeyOfLastElement(current_dict_subgraphs)
# #     #compare_set = getNodeListforCompareGWMIN(LevelAndMWIS_dict, LevelAndNodes_dict, overall_dict_subgraphs, key_index, current_node_list)
# #     compare_set = ApproximationGetNodeListforCompareGWMIN(LevelAndMWIS_dict, LevelAndNodes_dict, overall_dict_subgraphs,
# #                                                           key_index, current_node_list, G_original, nodes_intervals)
# #     #print("1561-----compare_set-----: {0}".format(compare_set))
# #     preliminary_set = getQueueInLevelNEW(LevelAndMWIS_dict, LevelAndNodes_dict, current_dict_subgraphs, initial_list,
# #                                          Checking_All_nodes, G_original, nodes_intervals)
# #     #print("-----preliminary_set-----: {0}".format(preliminary_set))
# #     Queue = compareToGetResult(compare_set, preliminary_set, G_original, nodes_intervals)
# #     #sys.exit("Error message")
# #     #print("-----Final Queue-----: {0}".format(Queue))
# #     return Queue
# #
# #
# # def removeLastElementinDict(current_dict_subgraphs):
# #     key_index = getKeyOfLastElement(current_dict_subgraphs)
# #     current_dict_subgraphs.pop(key_index)
# #     return current_dict_subgraphs
# #
# #
# # def GetMWIS_GWMIN_Merged_SubCompareSets(LevelAndMWIS_dict, LevelAndNodes_dict, G_function, overall_dict_subgraphs,
# #                                         current_subgraphs_reference, current_node_list, node_list_degree_order, G_original, nodes_intervals):
# #     index = len(overall_dict_subgraphs)
# #     # print("------number of nodes removed: {0}".format(index))
# #     Queue = []
# #     i = 1
# #
# #     while i <= index:  # set as the number of levels
# #         # print("------current_subgraphs_reference: {0}".format(current_subgraphs_reference))
# #         # key_index = getKeyOfLastElement(current_dict_subgraphs)
# #         removal_node = getKeyOfLastElement(current_subgraphs_reference)
# #         # print("------node removed: {0}".format(removal_node))
# #         nodes_in_level = []
# #         values_list_of_key = current_subgraphs_reference.get(removal_node)  # get values by the keys
# #         # print("------values_list_of_key------: {0}".format(values_list_of_key))
# #         for item in values_list_of_key:
# #             nodes_in_level = nodes_in_level + list(item)
# #         nodes_in_level = nodes_in_level + [removal_node]  # merge all nodes together
# #         nodes_current_level = keepSublistfromList(node_list_degree_order, nodes_in_level)  # make nodes in degree order
# #         # print("------nodes_current_level: {0}".format(nodes_current_level))
# #         # print("------current_MWIS_dict: {0}".format(LevelAndMWIS_dict))
# #         LevelAndNodes_dict.update({removal_node: nodes_current_level})
# #         # print("------LevelAndNodes_dict: {0}".format(LevelAndNodes_dict))
# #         level_nodes = []
# #         for element in values_list_of_key:
# #             # print("------element: {0}".format(element))
# #             element_list = keepSublistfromList(node_list_degree_order, list(element))
# #             level_nodes = level_nodes + getKeyByValueListNEW(LevelAndNodes_dict, element_list)
# #         # print("------level_nodes: {0}".format(level_nodes))
# #
# #         initial_queue = []
# #         Checking_All_nodes = []
# #         if level_nodes == []:
# #             Queue = getQueueForLevelGWMIN_CompareSetSubgraph(LevelAndMWIS_dict, LevelAndNodes_dict,
# #                                                              overall_dict_subgraphs, current_subgraphs_reference,
# #                                                              initial_queue, node_list_degree_order, Checking_All_nodes,
# #                                                              G_original, nodes_intervals)
# #         else:
# #             for node in level_nodes:
# #                 initial_queue = initial_queue + LevelAndMWIS_dict.get(node)
# #                 Checking_All_nodes = Checking_All_nodes + LevelAndNodes_dict.get(node)
# #             # print("------initial_queue: {0}".format(initial_queue))
# #             Queue = getQueueForLevelGWMIN_CompareSetSubgraph(LevelAndMWIS_dict, LevelAndNodes_dict,
# #                                                              overall_dict_subgraphs, current_subgraphs_reference,
# #                                                              initial_queue, node_list_degree_order, Checking_All_nodes,
# #                                                              G_original, nodes_intervals)
# #             # sys.exit("Error message")
# #             # level_node = getKeysByValue(LevelAndNodes_dict, element_list))[0] #['13']  ['24']
# #             # print(level_node)
# #             # initial_queue = LevelAndMWIS_dict.get('10')
# #             # print(initial_queue)
# #
# #         # Queue = getQueueForLevelGWMIN(overall_dict_subgraphs, current_subgraphs_reference, Queue, node_list_degree_order)
# #         Queue_reorder = keepSublistfromList(node_list_degree_order, Queue)
# #         LevelAndMWIS_dict.update({removal_node: Queue_reorder})
# #         # print("------current_MWIS_dict: {0}".format(LevelAndMWIS_dict))
# #         # print("------Queue_of_removal_node: {0}".format(Queue_reorder))
# #
# #         # remove last element in the reference dict
# #         current_subgraphs_reference = removeLastElementinDict(current_subgraphs_reference)  # delete the last element
# #         i += 1
# #
# #     # print("------current_MWIS_dict: {0}".format(LevelAndMWIS_dict))
# #     # compare the Queue with the
# #     # subgraph_after_removal = subgraphWithoutNodesInList(G_function2, all_removal_nodes)
# #     # preliminary_set = Queue #the subgraph is bipartite
# #
# #     # print(preliminary_set)
# #     # print('------preliminary_set------')
# #     # print(subgraph_GWMIN.node)
# #     # print('------subgraph_GWMIN.node------')
# #     # compare_list = checkingBipartiteAndGetList(subgraph_GWMIN)
# #     # print(compare_list)
# #     # print('------compare_list------')
# #     # Final_Queue = compareToGetResult(compare_list, preliminary_set)
# #     # print(Final_Queue)
# #     # print('------Final_Queue-----')
# #
# #     # Final_Queue = preliminary_set
# #     # print("------Fianl_Final_Queue: {0}".format(Final_Queue))
# #     return Queue