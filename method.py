from load_data import *
from tqdm import tqdm
import copy

# iter = 100

# ------------------hits-------------------------------------------------------
def hits(node_sum, node_mat, iter):
    # init
    hubs = [1 for i in range(node_sum)]
    auths = [1 for i in range(node_sum)]
    # to visual converage rate
    cr_auths = []
    cr_hubs = []

    # compute
    for i in range(iter): 
        temp_auths = [0 for i in range(node_sum)]
        temp_hubs = [0 for i in range(node_sum)]
        for node_num in range(node_sum):
            for arr_node in range(node_sum):
                # can't arrive themselve
                if node_num == arr_node:
                    continue
                else:
                    if node_mat[node_num][arr_node] == 1:
                        temp_auths[arr_node] += hubs[node_num]
                        temp_hubs[node_num] += auths[arr_node]
        total_auths = sum(temp_auths)
        temp_auths = [float(i/total_auths) for i in temp_auths]
        cr_auths.append(temp_auths)
        auths = temp_auths
        total_hubs = sum(temp_hubs)
        temp_hubs = [float(i/total_hubs) for i in temp_hubs]
        cr_hubs.append(temp_hubs)
        hubs = temp_hubs

    return auths, hubs, cr_auths, cr_hubs

# ----------------page_rank-----------------------------------------------------
def pagerank(node_sum, node_mat, iter, damping_factor):
    # init
    pr = [1/node_sum for n in range(node_sum)]
    # print(pr)
    output_link = [0 for i in range(node_sum)]
    

    # find the node_OutputLink_num
    for node_num in range(node_sum):
        output_link[node_num] = sum(node_mat[node_num])
    # print(output_link)

    # to visual converage rate
    cr_pr = []
    # compute pr
    for i in range(iter):
        temp_pr = [0 for i in range(node_sum)]
        for node_num in range(node_sum):
            for start_node in range(node_sum):
                if node_num == start_node:
                    continue
                else:
                    if node_mat[start_node][node_num] == 1:
                        # print(start_node, node_num)
                        temp_pr[node_num] += float(pr[start_node]/
                                                        output_link[start_node])
            temp_pr[node_num] = damping_factor/node_sum + ((1 - damping_factor) 
                                                            * temp_pr[node_num])
        pr = temp_pr
        temp_cr_pr = copy.deepcopy(temp_pr)
        cr_pr.append(temp_cr_pr)
    

    # normalize
    pr_sum = sum(pr)
    for index in range(len(pr)):
        pr[index] = pr[index] / pr_sum

    return pr, cr_pr
    
# ------------------simrank-----------------------------------------------------
def simrank(node_sum, node_mat, iter, decay_factor):
    # init sim
    sim = []
    for i in range(node_sum):
        row = []
        for j in range(node_sum):
            if i == j:
                row.append(1)
            else:
                row.append(0)
        sim.append(row)

    # to visual converage rate
    cr_sim = []
    # calculate sim
    for i in tqdm(range(iter)):
        temp_sim = [[0 for i in range(node_sum)] for j in range(node_sum)]
        for node1 in range(node_sum):
            for node2 in range(node_sum):
                if node1 == node2:
                    temp_sim[node1][node2] = 1
                else:
                    # find node1 & node2's in_neighbor.
                    in_node1 = []
                    in_node2 = []
                    for i in range(node_sum):
                        if node_mat[i][node1] == 1:
                            in_node1.append(i)
                        if node_mat[i][node2] == 1:
                            in_node2.append(i)
                    if len(in_node1) == 0 or len(in_node2) == 0:
                        temp_sim[node1][node2] = 0
                    else:
                        temp_sum = 0
                        for in_n1 in in_node1:
                            for in_n2 in in_node2:
                                temp_sum += sim[in_n1][in_n2]
                        result = (decay_factor/(len(in_node1)*len(in_node2)))
                        result *= temp_sum 
                        temp_sim[node1][node2] = result

            # if(node1 == 6):
            #     cr_sim.append(temp_sim[node1])
        sim = temp_sim

    return sim, cr_sim
    

if __name__ == '__main__':
    file_path = './hw3dataset/graph_3.txt'
    node_sum, node_mat = read_txt(file_path)
    auths, hubs = hits(node_sum, node_mat)
    print(f'auths:{auths}')
    print(f'hubs:{hubs}')
