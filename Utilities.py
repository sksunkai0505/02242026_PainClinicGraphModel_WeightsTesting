from itertools import combinations
import networkx as nx

# # inputs
# resources_order = ['R1', 'R2', 'R3', 'R4', 'R5', 'R6', 'R7','E'] # for T25D
# ###################################################################################

def getNodesDegreeDict(G_function):
    # get the node list sorted by degrees
    degree_list = []
    for vertex in list(G_function.nodes):
        node_degree = list(str(G_function.degree[vertex]))
        degree_list = degree_list + node_degree
    nodes_degree_dict = dict(zip(list(G_function.nodes), degree_list))# get the node list sorted by degrees
    return nodes_degree_dict


def getKeysByValue(dictOfElements, valueToFind):
    #Get a list of keys from dictionary which has the given value
    listOfKeys = list()
    listOfItems = dictOfElements.items()
    for item in listOfItems:
        if item[1] == valueToFind:
            listOfKeys.append(item[0])
    return  listOfKeys


def removeSublistfromList(parent_list, sublist):
    return [x for x in parent_list if x not in sublist]


def keepSublistfromList(parent_list, sublist):
    # will keep the same order
    return [x for x in parent_list if x in sublist]


def getKeyOfFirstElement(dictionary):
    key_of_first_element = list(dictionary.keys())[0]
    return key_of_first_element


def removeFirstElementInDict(dictionary):
    key_index = getKeyOfFirstElement(dictionary)
    dictionary.pop(key_index)
    return dictionary


# def reorderAllSets(list_of_lists):
#     cleaned_list = []
#     for each_list in list_of_lists:
#         each_list = keepSublistfromList(node_list_interval_order, each_list)
#         cleaned_list = cleaned_list + [each_list]
#     cleaned_list = removeDuplicate(cleaned_list)
#     return cleaned_list

def removeDuplicate(duplicate):
    final_list = []
    for num in duplicate:
        if num not in final_list:
            final_list.append(num)
    return final_list


def mergingList(list_to_merge):
    merged_list = []
    # make[{'6'}, {'7'}, {'8'}, {'5', '10', '0', '11', '2', '4', '9', '3'}]
    # to ['6', '7', '8', '5', '10', '0', '11', '2', '4', '9', '3']
    for element in list_to_merge:
        merged_list = merged_list + list(element)
    # print(merged_list)
    # print('------merged_list------')
    return merged_list

def CleanCombination(listToClean):
    output = []
    for each_element in listToClean:
        output = output + list(each_element)
    #print("1191-----cleaned resource list: {0}".format(output))
    return output


def AllNodesConditions(input_tasks_dict, resources_order, current_node_conditions=[]):
    Frist_Task_Resources = next(iter(input_tasks_dict.values()))
    #print("1190-----Frist_Task_Resources: {0}".format(Frist_Task_Resources))
    Resource_conditions = Frist_Task_Resources[5]
    #print("1192-----Resource_conditions: {0}".format(Resource_conditions))
    if Resource_conditions[-1] == 2: #check for other conditions
        p1_resource_pool = (Resource_conditions[0])[1]
        #print("1195-----part1_resource_pool: {0}".format(p1_resource_pool))
        p2_resource_pool = (Resource_conditions[1])[1]
        #print("1197-----part2_resource_pool: {0}".format(p2_resource_pool))
        p1_choose_N = int(((Resource_conditions[0])[0])[0])
        #print("1199-----part1_choose_N: {0}".format(p1_choose_N))
        p2_choose_N = int(((Resource_conditions[1])[0])[0])
        #print("1201-----part2_choose_N: {0}".format(p2_choose_N))
        del Frist_Task_Resources[-1] #delete last element in the list
        p1_comb_resource_options = CleanCombination(list(combinations(p1_resource_pool, p1_choose_N)))
        p2_comb_resource_options = CleanCombination(list(combinations(p2_resource_pool, p2_choose_N)))
        #print("1213-----part2_comb_resource_options: {0}".format(p2_comb_resource_options))
        combined_R_options = list([[x,y] for x in p1_comb_resource_options for y in p2_comb_resource_options])
        #print("1215-----combined_R_options: {0}".format(combined_R_options))
        for i in combined_R_options:
            sublist_to_add = keepSublistfromList(resources_order, list(i))
            #print("1218-----sublist_to_add: {0}".format(sublist_to_add))
            Nodes_Details = Frist_Task_Resources + [sublist_to_add]
            #print("1220-----sublist_to_add: {0}".format(sublist_to_add))
            current_node_conditions = current_node_conditions + [Nodes_Details]
        input_tasks_dict = removeFirstElementInDict(input_tasks_dict)
        #print("1223-----Acurrent_node_conditions: {0}".format(current_node_conditions))
        if input_tasks_dict == {}:
            return current_node_conditions
        else:
            current_node_conditions = AllNodesConditions(input_tasks_dict, resources_order, current_node_conditions)
    else:
        current_resource_pool = Resource_conditions[1]
        choose_N = int((Resource_conditions[0])[0])
        del Frist_Task_Resources[-1] #delete last element in the list
        comb_resource_options = list(combinations(current_resource_pool, choose_N))
        #print("1218-----comb_resource_options: {0}".format(comb_resource_options))
        for i in comb_resource_options:
            sublist_to_add = keepSublistfromList(resources_order, list(i))
            Nodes_Details = Frist_Task_Resources + [sublist_to_add]
            current_node_conditions = current_node_conditions + [Nodes_Details]
        input_tasks_dict = removeFirstElementInDict(input_tasks_dict)
        #print("1223-----Acurrent_node_conditions: {0}".format(current_node_conditions))
        if input_tasks_dict == {}:
            return current_node_conditions
        else:
            current_node_conditions = AllNodesConditions(input_tasks_dict, resources_order, current_node_conditions)
    return current_node_conditions



def ADDIndexToAllNodesCondition(AllNodesCondition):
    Length = len(AllNodesCondition)
    i = 0
    while i <= (Length-1):
        AllNodesCondition[i] = AllNodesCondition[i] + [i]
        i = i + 1
    return AllNodesCondition


def common_element(a, b):
    a_set = set(a)
    b_set = set(b)
    if (a_set & b_set):
        return True
    else:
        return False


def FunctionEdgesList(AllNodesCondition, Edges_List=[]):
    AllNodesCondition_copy = AllNodesCondition.copy()
    FirstNodeInfo = AllNodesCondition_copy[0]
    # print("1223-----First Node Info: {0}".format(FirstNodeInfo))
    # print("1224-----Node Index: {0}".format(FirstNodeInfo[-1]))
    Node_cond1_SameTask = FirstNodeInfo[0]
    # print("1227-----Node_condition1: {0}".format(Node_cond1_SameTask))
    # print("1228-----Node_condition1: {0}".format(Node_cond1_SameTask[0]))
    # print("1229-----Node_condition1: {0}".format(Node_cond1_SameTask[0][0]))
    AllNodesCondition_copy.pop(0)
    # print("1231-----Remaining Pre_AllNodesCondition: {0}".format(AllNodesCondition))

    if len(AllNodesCondition_copy) != 0:
        for each_node in AllNodesCondition_copy:
            # print("1238-----each_node: {0}".format(each_node))
            # print("1239-----((each_node[0])[0]): {0}".format(((each_node[0])[0])))
            # print("1242-----((each_node[0])[0][0]): {0}".format(((each_node[0])[0][0])))
            # print("1240-----Node_cond1_SameTask[0]: {0}".format(Node_cond1_SameTask[0]))

            if each_node[0] == Node_cond1_SameTask:
                # print("1242-----each_node[0]: {0}".format(each_node[0]))
                Edges_List = Edges_List + [[FirstNodeInfo[6]] + [each_node[-1]]]


            elif (each_node[0])[0] == Node_cond1_SameTask[0]:
                # print("1249-----FirstNodeInfo[4]: {0}".format(FirstNodeInfo[4]))
                if (each_node[0])[2] != Node_cond1_SameTask[2]:
                    Edges_List = Edges_List + [[FirstNodeInfo[6]] + [each_node[-1]]]

                elif FirstNodeInfo[5] != each_node[5]:
                    # print("1256-----nodes has egde: {0}".format(each_node))
                    Edges_List = Edges_List + [[FirstNodeInfo[6]] + [each_node[-1]]]


            elif (each_node[0])[0][0] != Node_cond1_SameTask[0][0]:
                if common_element(FirstNodeInfo[5], each_node[5]):
                    Edges_List = Edges_List + [[FirstNodeInfo[6]] + [each_node[-1]]]
    else:
        return Edges_List

    if len(AllNodesCondition_copy) != 0:
        Edges_List = FunctionEdgesList(AllNodesCondition_copy, Edges_List)

    return Edges_List


def InternalGenerateNodes(AllNodesCondition):
    AllNodesCondition_copy = AllNodesCondition.copy()

    output_str = []
    for each_NodeInfo in AllNodesCondition_copy:
        # print("626-----each_NodeInfo: {0}".format(each_NodeInfo))
        NodeIndex = [str(each_NodeInfo[6])]
        output_str = output_str + NodeIndex
    # print("629-----output_str: {0}".format(output_str))
    return output_str


def functionTaskAndNodeDict(AllNodesCondition, TaskAndNode_list=[], task_index=1):
    AllNodesCondition_copy = AllNodesCondition.copy()
    Value_list = []
    node_index = []
    count = 0
    first_node = AllNodesCondition_copy[0]
    Task_name = first_node[0]
    MultiOptionsNumber = first_node[1]
    for each_node in AllNodesCondition_copy:
        if each_node[0] == Task_name:
            node_index = node_index + [str(each_node[6])]
            count = count + 1
    Value_list = Value_list + [count] + [node_index] + MultiOptionsNumber + [task_index]
    task_index = task_index + 1

    k = 1
    while k <= count:
        AllNodesCondition_copy.pop(0)
        k = k + 1

    TaskAndNode_list = TaskAndNode_list + [[Task_name, Value_list]]

    if AllNodesCondition_copy == []:
        return TaskAndNode_list
    else:
        TaskAndNode_list = functionTaskAndNodeDict(AllNodesCondition_copy, TaskAndNode_list, task_index)
    return TaskAndNode_list


def functionWithMergingTaskAndNodeDict(AllNodesCondition, TaskAndNode_dict_WM={}, index=1):
    AllNodesCondition_copy = AllNodesCondition.copy()
    Value_list = []
    node_index = []
    count = 0
    first_node = AllNodesCondition_copy[0]
    Task_name = first_node[0]
    # print("1448----Task_name : {0}".format(Task_name))
    MultiOptionsNumber = first_node[1]
    for each_node in AllNodesCondition_copy:
        if each_node[0] == Task_name:
            node_index = node_index + [each_node[6]]
            count = count + 1
    Value_list = Value_list + [count] + [node_index] + MultiOptionsNumber + [index]
    # print("1454----Value_list : {0}".format(Value_list))
    # AllNodesCondition_copy.pop(0)
    TaskAndNode_dict_WM.update({index: [Task_name, Value_list]})
    # print("1464----TaskAndNode_dict_WM : {0}".format(len(TaskAndNode_dict_WM)))
    index = index + 1

    k = 1
    while k <= count:
        AllNodesCondition_copy.pop(0)
        k = k + 1
    # print("1459----AllNodesCondition_copy : {0}".format(len(AllNodesCondition_copy)))

    if AllNodesCondition_copy == []:
        return TaskAndNode_dict_WM
    else:
        # print("1472----TaskAndNode_dict_WM : {0}".format(TaskAndNode_dict_WM))
        TaskAndNode_dict_WM = functionWithMergingTaskAndNodeDict(AllNodesCondition_copy, TaskAndNode_dict_WM, index)
    return TaskAndNode_dict_WM


def sortedPairsInList(list1,list2):
    Output = []
    for x in list1:
        for y in list2:
            each_pair = [x,y]
            each_pair.sort()
            Output = Output + [each_pair]
    return Output

def NEWLenthWeightGetWeightsSumDict(TaskAndNode_dict, Input_LW_value, Adjustment, Edges_List, weight_SUM_dict={}):
    key_index = 0

    TaskAndNode_dict_copy = TaskAndNode_dict.copy()
    # print("2719----TaskAndNode_dict_copy : {0}".format(TaskAndNode_dict_copy))
    all_the_keys = list(TaskAndNode_dict_copy.keys())
    # print("1569----all_the_keys : {0}".format(all_the_keys))
    # print("1559----all_the_keys : {0}".format(len(all_the_keys)))

    number_of_tasks = len(TaskAndNode_dict_copy) - 1  # testing here
    # print("1562----number_of_tasks : {0}".format(number_of_tasks))

    while key_index <= number_of_tasks:
        each_key = all_the_keys[key_index]
        # print("2728----each_key : {0}".format(each_key))
        key_index = key_index + 1
        Value_of_key_index = (TaskAndNode_dict_copy.get(each_key))[1]
        # print("1540----Value_of_key_index : {0}".format(Value_of_key_index))
        Name_of_key_index = (TaskAndNode_dict_copy.get(each_key))[0]
        # print("2728----Name_of_key_index : {0}".format(Name_of_key_index))
        option_index = Name_of_key_index[2]
        # print("2730----option_index : {0}".format(option_index))
        Job_Name_key_index = (Name_of_key_index[0])[0]
        # print("2736----Job_Name_key_index: {0}".format(Job_Name_key_index))
        Task_Name_key_index = int(Name_of_key_index[0][1][0])  # as an interger
        # print("2736----Task_Name_key_index : {0}".format(Task_Name_key_index))
        Sequence_key_index = int(Name_of_key_index[1][0])
        # print("2734----Sequence_key_index : {0}".format(Sequence_key_index))
        k = 0
        connection_rate_list = []
        while k <= number_of_tasks:
            Another_Key = all_the_keys[k]
            k = k + 1

            Value_Another_Key = (TaskAndNode_dict_copy.get(Another_Key))[1]
            # print("2742----Value_Another_Key : {0}".format(Value_Another_Key))
            Name_Another_Task = (TaskAndNode_dict_copy.get(Another_Key))[0]
            # print("2750----Name_Another_Task : {0}".format(Name_Another_Task))
            option_index_another = Name_Another_Task[2]
            # print("2748----option_index_another : {0}".format(option_index_another))
            Job_Name_Another_Key = (Name_Another_Task[0])[0]
            # print("2801----Job_Name_Another_Key : {0}".format(Job_Name_Another_Key))
            Task_Name_Another_Key = int(Name_Another_Task[0][1][0])  # as an integer
            # print("2748----Task_Name_Another_Key : {0}".format(Task_Name_Another_Key))
            Sequence_Another_Key = int(Name_Another_Task[1][0])
            # print("2750----Sequence_Another_Key : {0}".format(Sequence_Another_Key))
            Divider = int(Value_of_key_index[2]) * int(Value_Another_Key[2])
            # KeyIndexTaskSequence = (Name_of_key_index[0])[0]
            # print("2747----Task Sequence Of Key Index KeyIndexTaskSequence: {0}".format(KeyIndexTaskSequence))

            if Job_Name_key_index == Job_Name_Another_Key:
                if Task_Name_Another_Key == Task_Name_key_index:
                    if Sequence_Another_Key > Sequence_key_index:
                        if option_index_another != option_index:
                            connection_rate = Input_LW_value / Divider + Adjustment
                        else:
                            connection_rate = Input_LW_value / Divider
                    else:
                        connection_rate = 0
                elif Task_Name_Another_Key < Task_Name_key_index:
                    connection_rate = 0

                else:
                    connection_rate = Input_LW_value / Divider
                    # -0.000000001
                # print("2768----connection_rate : {0}".format(connection_rate))
                # double check here, start from here.
            else:

                nodes_pairs = sortedPairsInList(Value_Another_Key[1], Value_of_key_index[1])
                # print("1563----nodes_pairs : {0}".format(nodes_pairs))

                max_possible_pairs = Value_of_key_index[0] * Value_Another_Key[0]
                # print("1565------max_possible_pairs : {0}".format(max_possible_pairs))

                count_actural_edges = 0
                for each_pair in nodes_pairs:
                    # print("1523------each_nodes_pairs : {0}".format(list(each_pair)))

                    if list(each_pair) in Edges_List:
                        count_actural_edges = count_actural_edges + 1

                # print("1576------count_actural_edges : {0}".format(count_actural_edges))

                # connection_rate = (count_actural_edges/max_possible_pairs)
                connection_rate = (count_actural_edges / max_possible_pairs) / Divider
                # print("1581------connection_rate : {0}".format(connection_rate))

            connection_rate_list = connection_rate_list + [connection_rate]
        # print("2795------connection_rate_list : {0}".format(connection_rate_list))
        # print("1585------connection_rate_list : {0}".format(len(connection_rate_list)))

        # print("1586------connection_rate_list : {0}".format(connection_rate_list))
        # print("1587------connection_rate_list : {0}".format(len(connection_rate_list)))
        weight_SUM_dict.update({each_key: sum(connection_rate_list) + 0.000000000000000000000001})
    return weight_SUM_dict

def GetNodesANDWeights_dict(NodeANDWeightsSum,TaskAndNode,NodesANDWeights_dict={}):
    NodeANDWeightsSum_copy = NodeANDWeightsSum.copy()
    TaskAndNode_copy = TaskAndNode.copy()
    KEY = 1
    number_of_tasks = len(NodeANDWeightsSum)
    while KEY <= number_of_tasks:
        #print("1697----KEY : {0}".format(KEY))
        Weight_of_KEY = (NodeANDWeightsSum_copy.get(KEY))
        #print("1699----Weight_of_KEY : {0}".format(Weight_of_KEY))
        Nodes_of_KEY = (TaskAndNode_copy.get(KEY)[1])[1]
        #print("1701----Nodes_of_KEY : {0}".format(Nodes_of_KEY))
        KEY = KEY + 1
        for each_node in Nodes_of_KEY:
            NodesANDWeights_dict.update({str(each_node): Weight_of_KEY})
    return NodesANDWeights_dict


def GetRequiredNodes(jobs_order, TaskAndNode_list):
    final_required_nodes = []
    i = 0
    while i <= len(jobs_order) - 1:

        All_J1 = []
        for each_task in TaskAndNode_list:
            Task_Full_Name = each_task[0]
            # task_info = each_task[1]
            # task_index = task_info[3]
            # print("243----task_index : {0}".format(task_index))
            job_name = (Task_Full_Name[0])[0]
            # print("246----job_index_int : {0}".format(job_index))
            if job_name == [jobs_order[i]]:
                All_J1 = All_J1 + [Task_Full_Name]

                # return something
                # print("248----task_name : {0}".format(task_name))
                # print("249----job_full_name : {0}".format(job_full_name))
        # print("253----All_J1 : {0}".format(All_J1))

        All_task_orders = []
        for each_task in All_J1:
            task_order = ((each_task[0])[1])[0]
            # print("258----task_order : {0}".format(task_order))

            All_task_orders = All_task_orders + [int(task_order)]
        # print("1404----All_task_orders : {0}".format(All_task_orders))

        if All_task_orders != []:
            MINI_task_order = min(All_task_orders)
            # print("1408----MINI_task_order : {0}".format(MINI_task_order))
        else:
            MINI_task_order = None

        All_task_duration = []
        for each_task in All_J1:
            task_order = int(((each_task[0])[1])[0])
            # print("269----task_order : {0}".format(task_order))
            task_duration = (each_task[1])[0]
            if task_order == MINI_task_order:
                All_task_duration = All_task_duration + [int(task_duration)]

        # print("274----All_task_duration : {0}".format(All_task_duration))
        if All_task_orders != []:
            MINI_task_duration = min(All_task_duration)
            # print("1408----MINI_task_order : {0}".format(MINI_task_order))
        else:
            MINI_task_duration = None

        # print("277----MINI_task_duration : {0}".format(MINI_task_duration))

        Required_tasks = []
        for each_task in All_J1:
            task_order = int(((each_task[0])[1])[0])
            # print("282----task_order : {0}".format(task_order))
            task_duration = int((each_task[1])[0])
            # print("284----task_duration : {0}".format(task_duration))
            if task_order == MINI_task_order and task_duration == MINI_task_duration:
                Required_tasks = Required_tasks + [each_task]

        # print("288----Required_tasks : {0}".format(Required_tasks))

        required_nodes = []
        for Each_Required_Tasks in Required_tasks:
            # print("292----Each_Required_Tasks : {0}".format(Each_Required_Tasks))
            for each_task in TaskAndNode_list:
                Task_Full_Name = each_task[0]
                # print("294----Task_Full_Name : {0}".format(Task_Full_Name))
                if Task_Full_Name == Each_Required_Tasks:
                    required_nodes = required_nodes + (each_task[1])[1]

        # print("297----required_nodes : {0}".format(required_nodes))
        i = i + 1
        final_required_nodes = final_required_nodes + required_nodes
    return final_required_nodes


def FinalWeightsForColoring(NodesANDWeights_dict, final_required_nodes, value=0.000001):
    all_the_nodes = list(NodesANDWeights_dict.keys())
    nodes_to_change_weights = removeSublistfromList(all_the_nodes, final_required_nodes)

    NodesANDWeights_dict_copy = NodesANDWeights_dict.copy()
    for each_node in nodes_to_change_weights:
        NodesANDWeights_dict_copy.update({each_node: value})
    return NodesANDWeights_dict_copy


def getIntervalOrder(nodes_intervals):
    sorted_nodes_intervals = sorted(nodes_intervals, key=nodes_intervals.get, reverse=True)
    #print("2570-----sorted_nodes_intervals: {0}".format(sorted_nodes_intervals))
    node_list_interval_order = sorted_nodes_intervals.copy()
    #print("2446-----node_list_interval_order: {0}".format(node_list_interval_order))
    return node_list_interval_order

# def getNodeListGWMINOrder(G_function, nodes_intervals):
#     print("472-----list(G_function.nodes): {0}".format(G_function.nodes))
#     G_function_copy = G_function.copy()
#     GWMIN_list = []
#     # get the node list sorted by degrees
#     for node in list(G_function_copy.nodes):
#         #node = str(node)
#         print("476-----node: {0}".format(type(node)))
#         print("478-----G_function_copy.degree[node]: {0}".format(G_function_copy.degree[node]))
#         print("479-----G_function_copy.degree[node]: {0}".format(type(G_function_copy.degree[node])))
#         node_degree = float(G_function_copy.degree[node])
#         print("481-----node_degree : {0}".format(node_degree))
#
#         node_weight = float(nodes_intervals.get(str(node)))
#         print("484-----node_weight: {0}".format(node_weight))
#         GWMIN_list = GWMIN_list + [node_weight/(node_degree + 1)]
#     print("487-----list(G_function_copy.nodes): {0}".format(list(G_function_copy.nodes)))
#     nodes_with_GWMIN = dict(zip(list(G_function_copy.nodes), GWMIN_list))
#     print("487-----nodes_with_GWMIN : {0}".format(nodes_with_GWMIN))
#     node_list_GWMIN_order = sorted(nodes_with_GWMIN, key=nodes_with_GWMIN.get, reverse=True) #descending
#     return node_list_GWMIN_order

# def getNodeListGWMINOrder(G_function, nodes_intervals):
#     G_function_copy = G_function.copy()
#     GWMIN_list = []
#     # get the node list sorted by degrees
#     for node in list(G_function_copy.nodes):
#         #print("1893-----node: {0}".format(type(node)))
#         #print("1894-----G_function_copy.degree[node]: {0}".format(G_function_copy.degree[node]))
#         node_degree = float(G_function_copy.degree[node])
#         #print("1896-----node: {0}".format(type(node)))
#         node_weight = float(nodes_intervals.get(node))
#         GWMIN_list = GWMIN_list + [node_weight/(node_degree + 1)]
#     nodes_with_GWMIN = dict(zip(list(G_function_copy.nodes), GWMIN_list))
#     node_list_GWMIN_order = sorted(nodes_with_GWMIN, key=nodes_with_GWMIN.get, reverse=True) #descending
#     return node_list_GWMIN_order
# #print(GWMIN_list)


def cycle_basis(G, root=None):
    #Returns a list of cycles which form a basis for cycles of G.
    gnodes = set(G.nodes())
    #print("-----gnodes in cycle_basis function: {0}".format(gnodes))
    cycles = []
    while gnodes:  # loop over connected components
        if root is None:
            #root = gnodes.pop() # this will get a random element from the set
            root = gnodes.pop()
        stack = [root]
        #print(stack)
        #print('------stack------')
        pred = {root: root}
        used = {root: set()}
        while stack:  # walk the spanning tree finding cycles
            z = stack.pop()  # use last-in so cycles easier to find
            zused = used[z]
            for nbr in G[z]:
                if nbr not in used:   # new node
                    pred[nbr] = z
                    stack.append(nbr)
                    used[nbr] = set([z])
                elif nbr == z:          # self loops
                    cycles.append([z])
                elif nbr not in zused:  # found a cycle
                    pn = used[nbr]
                    cycle = [nbr, z]
                    p = pred[z]
                    while p not in pn:
                        cycle.append(p)
                        p = pred[p]
                    cycle.append(p)
                    cycles.append(cycle)
                    used[nbr].add(z)
        gnodes -= set(pred)
        root = None
    return cycles

def mergeAllNodeInOneList(list_of_lists):
    final_list = []
    for element in list_of_lists:
        final_list = final_list + element
    return final_list


def countOccurrence(occurrence_list, nodes_list):
    node_occurrence = {} #dictionary to store the colors assigned to each node
    for node in nodes_list:
        count = occurrence_list.count(node)
        node_occurrence[node] = count
    return node_occurrence


def GetCurrentCycleBasisOrder(G_function, node_list):
    all_basis_for_cycles = cycle_basis(G_function)
    #print("565-----all_basis_for_cycles: {0}".format(all_basis_for_cycles))
    #all_cycles = find_all_cycles(G_function)
    #print("-----all_cycles_of_G: {0}".format(all_cycles))
    odd_basis = all_basis_for_cycles
    #odd_basis = removeEvenBasis(all_basis_copy)
    mergeing_list = mergeAllNodeInOneList(odd_basis)
    occurrence_dict = countOccurrence(mergeing_list, node_list)
    #print("571-----occurrence_dict: {0}".format(occurrence_dict))
    node_list_odd_basis_order = sorted(occurrence_dict, key=occurrence_dict.get, reverse=True) #descending
    return node_list_odd_basis_order


def getNodesInDegreeOrder(G_function):
    G_copy = G_function.copy()
    # get the node list sorted by degrees
    degree_list = []
    for vertex in list(G_copy.nodes):
        node_degree = [G_copy.degree[vertex]]
        #print("690-----node_degree: {0}".format(node_degree))
        degree_list = degree_list + node_degree
    #print("692-----degree_list: {0}".format(degree_list))
    nodes_with_degree = dict(zip(list(G_copy.nodes), degree_list))# get the node list sorted by degrees
    #print("694-----nodes_with_degree: {0}".format(nodes_with_degree))
    node_list_degree_order = sorted(nodes_with_degree, key=nodes_with_degree.get, reverse=True) #descending
    return node_list_degree_order


def eccentricity(G, v=None, sp=None):
    """Return the eccentricity of nodes in G."""
#    if v is None:                # none, use entire graph
#        nodes=G.nodes()
#    elif v in G:               # is v a single node
#        nodes=[v]
#    else:                      # assume v is a container of nodes
#        nodes=v
    #order = G.order()

    e = {}
    for n in G.nbunch_iter(v):
        if sp is None:
            length = dict(nx.single_source_shortest_path_length(G, n))
            value_here = max(length.values())
            if value_here >=3:
                e[n] = value_here
                return e
            #L = len(length)
        '''
        else:
            try:
                length = sp[n]
                value_here = max(length.values())
                if value_here >=3:
                    e[n] = value_here
                    return e                  
                L = len(length)
            except TypeError:
                raise nx.NetworkXError('Format of "sp" is invalid.')
        '''
        '''
        if L != order:
            if G.is_directed():
                msg = ('Found infinite path length because the digraph is not'
                       ' strongly connected')
            else:
                msg = ('Found infinite path length because the graph is not'
                       ' connected')
            raise nx.NetworkXError(msg)
        '''

        e[n] = value_here
        #e[n] = max(length.values())
    else:
        return e


def diameter(G, e=None, usebounds=False):
    """Return the diameter of the graph G"""
    if e is None:
        e = eccentricity(G)
    return max(e.values())


def getKeyOfLastElement(dict_subgraphs):
    number_of_items = len(dict_subgraphs)
    index_last_element = (number_of_items - 1)
    #print(index_last_element) #1
    key_of_last_element = list(dict_subgraphs.keys())[index_last_element]
    return key_of_last_element


def getKeyByValueListNEW(dictionary, list_to_search):
    key = []
    for level_node, nodes_in_level in dictionary.items():    # for name, age in dictionary.iteritems():  (for Python 2.x)
        #print(nodes_in_level == list_to_search)
        if nodes_in_level == list_to_search:
            key = key + [level_node]
        else:
            key = key
    return key

def getValuesByKeysAslist(mydict, key_list):
    #get values by key list, returns a list of float
    return [float(i) for i in [mydict[x] for x in key_list]]


def getSubgraphsByLastKey(dict_subgraphs):
    key_of_last_element = getKeyOfLastElement(dict_subgraphs)
    #print(key_last_element) #4
    subgraphs_of_key = dict_subgraphs[key_of_last_element]
    #print(subgraphs_of_key)
    return subgraphs_of_key


def neighborhood(G, node, n):
    #return the neighbors of a given node with a given distance
    path_lengths = nx.single_source_dijkstra_path_length(G, node)
    return [node for node, length in path_lengths.items() if length == n]


def removeLastElementinDict(current_dict_subgraphs):
    key_index = getKeyOfLastElement(current_dict_subgraphs)
    current_dict_subgraphs.pop(key_index)
    return current_dict_subgraphs

# def getDiameterOfGraph(G_function):
#     output_diameter = 0
#     individual_graphs = list(nx.connected_component_subgraphs(G_function))
#     for subgraph in individual_graphs:
#         #print(subgraph.node)
#         Q = diameter(subgraph)
#         if Q >= 2:
#             output_diameter = 3
#             return output_diameter
#     return output_diameter


# def getDiameterOfGraph(G_function):
#     output_diameter = 0
#     individual_graphs = list(G_function.subgraph(c).copy() for c in nx.connected_components(G_function))
#     for subgraph in individual_graphs:
#         #print(subgraph.node)
#         Q = diameter(subgraph)
#         if Q >= 2:
#             output_diameter = 3
#             return output_diameter
#     return output_diameter
#
#
# def subgraphWithNodesInList(G_function, node_list_keeping):
#     G_for_function = G_function.copy()
#     node_to_remove = removeSublistfromList(list(G_for_function.nodes), node_list_keeping)
#     for node in node_to_remove:
#         G_for_function.remove_node(node)
#     return G_for_function
#
#
# def neighborsCheck(G, nodes_to_check):
#     #checking for the final output list
#     neighbors_list_final = []
#     for node in nodes_to_check:
#         neighbors_list = list(G.neighbors(node))
#         neighbors_list_final = neighbors_list_final + neighbors_list
#     return neighbors_list_final
#
#
# def subgraphWithoutNodesInList(G_function, node_list_removal):
#     #print(node_list_removal)
#     G_for_function = G_function.copy()
#     for node in node_list_removal:
#         #print(node)
#         G_for_function.remove_node(node)
#     return G_for_function
#
#

#
#

#
#
# def getMiddleNodeForTrees(G_function, G_original):
#     nodes_degree_dict = getNodesDegreeDict(G_function)
#     nodes_to_remove = getKeysByValue(nodes_degree_dict, '1') + getKeysByValue(nodes_degree_dict, '0')
#     nodes_after_removal = removeSublistfromList(list(G_function.nodes), nodes_to_remove)
#     #print("-----nodes_after_removal: {0}".format(nodes_after_removal))
#     if len(nodes_after_removal) == 0:
#         middle_node = getNodesInDegreeOrder(G_function)[0]
#         #print("-----middle_node: {0}".format(middle_node))
#         return middle_node
#     elif len(nodes_after_removal) <= 2:
#         middle_node = nodes_after_removal[0]
#         return middle_node
#     else:
#         subgraph_after_removal = subgraphWithNodesInList(G_original, nodes_after_removal)
#         middle_node = getMiddleNodeForTrees(subgraph_after_removal, G_original)
#         return middle_node
#
#
# def removingNodesForLimitedPathRemoveNodeMaxDegree(G_function, G_original, node_list=[]):
#     # using this function for reducing path length
#     node_to_remove = getMiddleNodeForTrees(G_function, G_original)
#     # print("-----node_to_remove: {0}".format(node_to_remove))
#     G_function_copy = G_function.copy()
#     G_function.remove_node(node_to_remove)
#     subgraph_node_sets = [subgraph for subgraph in sorted(nx.connected_components(G_function), key=len, reverse=False)]
#     # print(removing_node_list)
#     # print(subgraph_node_sets)
#     # print('-------------------subgraph_node_sets-----------------------------')
#     subgraphs_dict.update({str(node_to_remove): subgraph_node_sets})
#     # print(subgraphs_dict)
#     # print('----------------------subgraphs_dict---------------------------------')
#
#     for subgraph_node_set in subgraph_node_sets:
#         subgraph = subgraphWithNodesInList(G_function, list(subgraph_node_set))
#         # print(subgraph.node)
#         # neighbors_of_removal_node = neighborsCheck(G_function_copy, [node_to_remove])
#         # subgraph_GWMIN_removal = neighbors_of_removal_node + [node_to_remove]
#         # print("-----subgraph_GWMIN_removal: {0}".format(subgraph_GWMIN_removal))
#         # subgraph_GWMIN = subgraphWithoutNodesInList(G_function_copy, subgraph_GWMIN_removal)
#         # print(subgraph_GWMIN.node)
#         # print('------------------subgraph_GWMIN---------------------------')
#         # print(bipartite.is_bipartite(subgraph))
#         neighbors_of_removal_node = neighborsCheck(G_function_copy, [node_to_remove])
#         # print("-----neighbors_of_removal_node: {0}".format(neighbors_of_removal_node))
#         neighbors_of_neighbors_of_removal_node = neighborsCheck(G_function_copy, neighbors_of_removal_node)
#         # print("-----neighbors_of_neighbors_of_removal_node: {0}".format(neighbors_of_neighbors_of_removal_node))
#         subgraph_GWMIN_removal = neighbors_of_removal_node + neighbors_of_neighbors_of_removal_node + [node_to_remove]
#         # print("-----subgraph_GWMIN_removal: {0}".format(subgraph_GWMIN_removal))
#         subgraph_GWMIN_removal = removeDuplicate(subgraph_GWMIN_removal)
#         subgraph_GWMIN = subgraphWithoutNodesInList(G_function_copy, subgraph_GWMIN_removal)
#         # print("-----nodes in subgraph_GWMIN: {0}".format(subgraph_GWMIN.node))
#         # diameter_of_graph = getDiameterOfGraph(subgraph)
#         # print("-----diameter_of_graph: {0}".format(diameter_of_graph))
#         # all_cycles = find_all_cycles(subgraph)
#         all_cycles = cycle_basis(subgraph)
#         if all_cycles != []:
#             node_list_GWMIN_order = getNodeListGWMINOrder(subgraph_GWMIN)
#             # print(node_list_odd_basis_order)
#             node_list_odd_basis_order = GetCurrentCycleBasisOrder(G_function, node_list_GWMIN_order)
#             reordered_nodes_in_subgraph = keepSublistfromList(node_list_odd_basis_order, (list(subgraph_node_set)))
#             # print(reordered_nodes_in_subgraph) #['2', '9', '10', '11']
#             # print('------------reordered_nodes_in_subgraph----------------')
#             getSubgraphsDisctionaryOCBOGWMINwithLP(subgraph, reordered_nodes_in_subgraph)
#
#         elif getDiameterOfGraph(subgraph) >= 3:
#             # print('------in the function removingNodesForLimitedPathRemoveNodeMaxDegreegraph diameter >= 3------')
#
#             # node_list_GWMIN_order = getNodeListGWMINOrder(subgraph_GWMIN)
#             # node_list_degree_order = getNodesInDegreeOrder(subgraph_GWMIN)
#             # print("-----node_list_degree_order: {0}".format(node_list_degree_order))
#             # reordered_nodes_in_subgraph = keepSublistfromList(node_list_degree_order, (list(subgraph_node_set)))
#
#             # print("-----reordered_nodes_in_subgraph: {0}".format(reordered_nodes_in_subgraph))
#             removingNodesForLimitedPathRemoveNodeMaxDegree(subgraph, G_original)
#     return subgraphs_dict
#
#
#
# subgraphs_dict = {}
# def getSubgraphsDisctionaryOCBOGWMINwithLP(G_function, node_list, nodes_intervals, G_original):
#     # print("-----input_node_list: {0}".format(node_list))
#
#     # cycles_in_input_graph = find_all_cycles(G_function)
#     cycles_in_input_graph = cycle_basis(G_function)
#     if cycles_in_input_graph == []:
#         if getDiameterOfGraph(G_function) >= 3:
#             # print('------graph diameter >= 3------')
#             removingNodesForLimitedPathRemoveNodeMaxDegree(G_function)
#             return subgraphs_dict
#         else:
#             TEMPremovingNodesForLimitedPathRemoveNodeMaxDegree(G_function)
#         return subgraphs_dict
#
#     node_to_remove = node_list[0]
#     # print("-----node_to_remove: {0}".format(node_to_remove))
#     G_function_copy = G_function.copy()
#     G_function.remove_node(node_to_remove)
#     subgraph_node_sets = [subgraph for subgraph in sorted(nx.connected_components(G_function), key=len, reverse=False)]
#     # print(removing_node_list)
#     # print(subgraph_node_sets)
#     # print('-------------------subgraph_node_sets-----------------------------')
#     subgraphs_dict.update({node_list[0]: subgraph_node_sets})
#     # print(subgraphs_dict)
#     # print('----------------------subgraphs_dict---------------------------------')
#     for subgraph_node_set in subgraph_node_sets:
#         # print("-----list(subgraph_node_set): {0}".format(list(subgraph_node_set)))
#         subgraph = subgraphWithNodesInList(G_function, list(subgraph_node_set))
#         # print("-----subgraph.node: {0}".format(subgraph.node))
#         subgraph_GWMIN_removal = neighborsCheck(G_function_copy, [node_to_remove]) + [node_to_remove]
#         # print(subgraph_GWMIN_removal)
#         # print('------------------subgraph_GWMIN_removal-----------------------------')
#         subgraph_GWMIN = subgraphWithoutNodesInList(G_function_copy, subgraph_GWMIN_removal)
#         # print(subgraph_GWMIN.node)
#         # print('------------------subgraph_GWMIN.node-------------------------')
#         # print(bipartite.is_bipartite(subgraph))
#         # diameter_of_graph = getDiameterOfGraph(subgraph)
#         # all_cycles = find_all_cycles(subgraph)
#         # print("-----all_cycles: {0}".format(all_cycles))
#         all_cycles = cycle_basis(subgraph)
#         if all_cycles != []:
#             node_list_GWMIN_order = getNodeListGWMINOrder(subgraph_GWMIN, nodes_intervals)
#             # print(node_list_GWMIN_order)
#             # print('------node_list_GWMIN_order------')
#             later_part = removeSublistfromList(list(subgraph_node_set), node_list_GWMIN_order)
#             remaining_nodes_degree_order = getNodesInDegreeOrder(subgraph)
#             # print(remaining_nodes_degree_order)
#             # print('------remaining_nodes_degree_order------')
#             reordered_later_part = keepSublistfromList(remaining_nodes_degree_order, later_part)
#             all_node_GWMIN_order = node_list_GWMIN_order + reordered_later_part
#             # print(all_node_GWMIN_order)
#             # print('------all_node_GWMIN_order------')
#             # print(subgraph.node)
#             # print('------subgraph.node------')
#             node_list_odd_basis_order = GetCurrentCycleBasisOrder(subgraph, all_node_GWMIN_order)
#             # print("-----node_list_odd_basis_order: {0}".format(node_list_odd_basis_order))
#             reordered_nodes_in_subgraph = keepSublistfromList(node_list_odd_basis_order, (list(subgraph_node_set)))
#             # print(reordered_nodes_in_subgraph) #['2', '9', '10', '11']
#             # print('------------reordered_nodes_in_subgraph----------------')
#             getSubgraphsDisctionaryOCBOGWMINwithLP(subgraph, reordered_nodes_in_subgraph, nodes_intervals, G_original)
#
#         elif getDiameterOfGraph(subgraph) >= 3:
#             reordered_nodes_in_subgraph = list(subgraph_node_set)
#             # print(reordered_nodes_in_subgraph) #['3', '5', '9', '10', '11']
#             # print('------------reordered_nodes_in_subgraph----------------')
#             removingNodesForLimitedPathRemoveNodeMaxDegree(subgraph, G_original)
#     return subgraphs_dict
#
#
# def getGWMINRemovalDisctionary(G_function, node_list, subgraphs_dict,nodes_intervals):
#     # print("2808------node_list : {0}".format(node_list))
#     if node_list == []:
#         return subgraphs_dict
#
#     node_to_remove = node_list[0]
#
#     G_function_copy = G_function.copy()
#     # G_function.remove_node(node_to_remove)
#     nodes_GWMIN_removal = neighborsCheck(G_function_copy, [node_to_remove]) + [node_to_remove]
#     # print(nodes_GWMIN_removal)
#     # print('------nodes_GWMIN_removal------')
#     remaining_nodes = removeSublistfromList(node_list, nodes_GWMIN_removal)
#     # print(remaining_nodes)
#     # print('------remaining_nodes------')
#
#     # print('-------------------subgraph_node_sets-----------------------------')
#     subgraphs_dict.update({node_list[0]: remaining_nodes})
#     # print(subgraphs_dict)
#     # print('----------------------subgraphs_dict---------------------------------')
#     # sys.exit("Error message")
#     if remaining_nodes != []:
#         remaining_subgraph = subgraphWithNodesInList(G_function_copy, remaining_nodes)
#         # print(remaining_subgraph.node)
#         # print('------remaining_subgraph.node------')
#         current_nodes_GWMIN_order = getNodeListGWMINOrder(remaining_subgraph, nodes_intervals)
#         getGWMINRemovalDisctionary(remaining_subgraph, current_nodes_GWMIN_order, subgraphs_dict, nodes_intervals)
#         # sys.exit("Error message")
#     return subgraphs_dict
#
#
# def getListInColoringOrder(G_function,nodes_intervals):
#     # get the dict for Bipartite subgraphs
#     subgraphs_dict = {} #initial the dict space
#     nodes_GWMIN_order = getNodeListGWMINOrder(G_function,nodes_intervals)
#     GWMIN_Removal_dict = getGWMINRemovalDisctionary(G_function, nodes_GWMIN_order, subgraphs_dict, nodes_intervals)
#     #print(GWMIN_Removal_dict)
#     #print('----------GWMIN_Removal_dict for the whole graph-----------------')
#     removal_nodes = list(GWMIN_Removal_dict.keys())
#     #print(removal_nodes)
#     #print('-----removal_nodes-----')
#     return removal_nodes
#
#
def GetTasksScheduled(nodes_assigned,AllNodesCondition):
    AllNodesCondition_copy = AllNodesCondition.copy()
    Task_Scheduled_list = []
    for Each_Node_Got in nodes_assigned:
        Got_Node_index = Each_Node_Got
        #print("2561------Got_Node_index: {0}".format(Got_Node_index))
        for each_original_node in AllNodesCondition_copy:
            NodeIndexToCheck = each_original_node[6]
            #print("2564------NodeIndexToCheck: {0}".format(NodeIndexToCheck))
            if int(Got_Node_index) == int(NodeIndexToCheck):
                Task_Scheduled = each_original_node
                Task_Scheduled_list = Task_Scheduled_list + [Task_Scheduled]
    return Task_Scheduled_list
#
#
def FindTasksNamesScheduled(Task_Scheduled_list):
    output_list = []

    for Each_Node_Scheduled in Task_Scheduled_list:
        Task_Name = Each_Node_Scheduled[0]
        output_list = output_list + [Task_Name]
    return output_list
#
#
def NodesToRemoveForMultiOptions(current_Task_Scheduled_list, current_TaskAndNode_list):
    Other_Nodes_To_Remove = []
    for each_node in current_Task_Scheduled_list:
        # print("2839------each_node in Task_Scheduled_list: {0}".format(each_node))
        if each_node[1] != ['1']:
            Task_Name = each_node[0]
            for each_node_to_check in current_TaskAndNode_list:
                if Task_Name[0] == (each_node_to_check[0])[0] and Task_Name[2] != (each_node_to_check[0])[2]:
                    Other_Nodes = (each_node_to_check[1])[1]
                    Other_Nodes_To_Remove = Other_Nodes_To_Remove + Other_Nodes
    return Other_Nodes_To_Remove
#
#
def FindAllScheduledTaskNodes(Scheduled_Task_Name_List,TaskAndNode_list):
    output_list = []
    for each_task_name in Scheduled_Task_Name_List:
        #print("2601------each_task_name: {0}".format(each_task_name))
        for each_task_info in TaskAndNode_list:
            if each_task_info[0] == each_task_name:
                output_list = output_list + (each_task_info[1])[1]
    #print("2605------AllScheduledTaskNodes: {0}".format(output_list))
    return output_list
#
#
def FindPreSelectedNodes(Task_Scheduled_list, AllNodesCondition):
    AllNodesCondition_copy = AllNodesCondition.copy()
    output = []

    for Each_Node_Scheduled in Task_Scheduled_list:
        # Task_Name = Each_Node_Scheduled[0]
        Task_Job_Order = (Each_Node_Scheduled[0])[0]
        Task_Sequence_int = int(((Each_Node_Scheduled[0])[1])[0])
        Task_Option = (Each_Node_Scheduled[0])[2]

        # print("2630------Task_Name: {0}".format(Task_Name))
        # print("2584------Task_Job_Order: {0}".format(Task_Job_Order))
        # print("2585------Task_Sequence_int: {0}".format(Task_Sequence_int))
        # print("2586------Task_Option: {0}".format(Task_Option))

        NEW_Task_Sequence = [str(Task_Sequence_int + 1)]
        # print("2636------NEW_Task_Sequence: {0}".format(NEW_Task_Sequence))

        TaskNameToSearch = [Task_Job_Order] + [NEW_Task_Sequence] + [Task_Option]
        # print("2639------TaskNameToSearch: {0}".format(TaskNameToSearch))

        for each_task_info in AllNodesCondition_copy:
            # print("2642------each_task_info: {0}".format(each_task_info[0]))

            if TaskNameToSearch == each_task_info[0]:
                Task_Resources = Each_Node_Scheduled[5]
                Task_Resources_to_check = each_task_info[5]
                if Task_Resources == Task_Resources_to_check:
                    output = output + [each_task_info]
    return output
#
#
def GetNodeIndex(PreSelectedNodesList):
    output_list = []
    for each_node in PreSelectedNodesList:
        output_list = output_list + [str(each_node[6])]
    return output_list
#
#
def RemoveSelectedElementInList(ParentList,SelectionConditions):
    ListToRemove = []
    for item in ParentList:
        Number_Of_Options = item[1]
        Task_Name = item[0]
        if Number_Of_Options != ['1']:
            if str(Task_Name) == str(SelectionConditions):
                ListToRemove = ListToRemove + [item]
            elif SelectionConditions[0] == Task_Name[0]:
                if SelectionConditions[2] != Task_Name[2]:
                    ListToRemove = ListToRemove + [item]
                    #print("2949------Task_Name: {0}".format(Task_Name[2]))
                    #print("2950------SelectionConditions: {0}".format(SelectionConditions[2]))
                    #print("2951------Number_Of_Options: {0}".format(Number_Of_Options))
        else:
            if str(Task_Name) == str(SelectionConditions):
                ListToRemove = ListToRemove + [item]
    #print("2679------ListToRemove: {0}".format(ListToRemove))
    return ListToRemove
#
#
def UpdateAllNodesConditions(Original_AllNodesCondition,Scheduled_Task_Name_List):
    AllNodesCondition_copy = Original_AllNodesCondition.copy()
    ListsToRemove = []
    for each_node_name in Scheduled_Task_Name_List:
        #print("2682------each_node_name: {0}".format(each_node_name))
        ListsToRemove = ListsToRemove + RemoveSelectedElementInList(AllNodesCondition_copy,each_node_name)
    UpdatedAllNodesConditions =  removeSublistfromList(AllNodesCondition_copy, ListsToRemove)
    return UpdatedAllNodesConditions
#
#
# def NEWsubgraphWithoutNodesInList(G_function, node_list_removal):
#     #print("338----------node_list_removal: {0}".format(node_list_removal))
#     G_for_function = G_function.copy()
#     for node in node_list_removal:
#         #print(node)
#         G_for_function.remove_node(node)
#     return G_for_function
#
#
def NEWsubgraphWithoutNodesInList(G_function, node_list_removal):
    #print("338----------node_list_removal: {0}".format(node_list_removal))
    G_for_function = G_function.copy()
    for node in node_list_removal:
        #print(node)
        G_for_function.remove_node(node)
    return G_for_function


def removeNodesInList(current_G,removal_list):
    current_G_copy = current_G.copy()
    node_index = 0
    while node_index <= len(removal_list) - 1:
        The_node = [removal_list[node_index]]
        current_G_copy = NEWsubgraphWithoutNodesInList(current_G_copy, The_node)
        node_index = node_index + 1
    return current_G_copy

def NEWgetNodeListGWMINOrder(G_function,NEW_nodes_intervals):
    G_function_copy = G_function.copy()
    GWMIN_list = []
    # get the node list sorted by degrees
    for node in list(G_function_copy.nodes):
        node_degree = float(G_function_copy.degree[node])
        node_weight = float(NEW_nodes_intervals.get(node))
        GWMIN_list = GWMIN_list + [node_weight/(node_degree + 1)]
    nodes_with_GWMIN = dict(zip(list(G_function_copy.nodes), GWMIN_list))
    node_list_GWMIN_order = sorted(nodes_with_GWMIN, key=nodes_with_GWMIN.get, reverse=True) #descending
    return node_list_GWMIN_order



#
#
# def NEWgetNodeListGWMINOrder(G_function,NEW_nodes_intervals):
#     G_function_copy = G_function.copy()
#     GWMIN_list = []
#     # get the node list sorted by degrees
#     for node in list(G_function_copy.nodes):
#         node_degree = float(G_function_copy.degree[node])
#         node_weight = float(NEW_nodes_intervals.get(node))
#         GWMIN_list = GWMIN_list + [node_weight/(node_degree + 1)]
#     nodes_with_GWMIN = dict(zip(list(G_function_copy.nodes), GWMIN_list))
#     node_list_GWMIN_order = sorted(nodes_with_GWMIN, key=nodes_with_GWMIN.get, reverse=True) #descending
#     return node_list_GWMIN_order
#
