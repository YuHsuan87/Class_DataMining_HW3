import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from numpy import array

def show(node_mat):
    for rows in node_mat:
        rows = [("%.4f" % i) for i in rows]
        print(rows)

def read_txt(file_path):
    # read file
    with open(file_path) as f:
        lines = f.readlines()
        # print(lines)
    max_val = 0
    for line in lines:
        node = line.split(',')
        node[1] = node[1].strip()
        for i in range(2):
            if int(node[i]) > max_val:
                max_val = int(node[i])
    node_sum = max_val
    node_mat = [[0 for i in range(node_sum)] for j in range(node_sum)]
    for line in lines:
        node = line.split(',')
        node[1] = node[1].strip()
        node_mat[int(node[0]) - 1][int(node[1]) - 1] = 1
    ########################################################################
    # node_set = set()
    # # get all node
    # for line in lines:
    #     node = line.split(',')
    #     node[1] = node[1].strip()
    #     for i in range(2):
    #         node_set.add(node[i])
    # node_sum = len(node_set)
    # print(node_sum)
    # node_mat = [[0 for i in range(node_sum)] for j in range(node_sum)]
    # # show(node_link)
    # for line in lines:
    #     node = line.split(',')
    #     node[1] = node[1].strip()
    #     node_mat[int(node[0]) - 1][int(node[1]) - 1] = 1
    # # show(node_link)
    ######################################################################
    
    return node_sum, node_mat

def draw(node_mat, node_sum):
    with open('./hw3dataset/graph_3.txt') as f:
        lines = f.readlines()

    G = nx.DiGraph()

    for line in lines:
        t = tuple(line.strip().split(','))
        G.add_edge(*t)

    h, a = nx.hits(G, max_iter=100)
    h = dict(sorted(h.items(), key=lambda x: x[0]))
    a = dict(sorted(a.items(), key=lambda x: x[0]))

    pr = nx.pagerank(G)
    pr = dict(sorted(pr.items(), key=lambda x: x[0]))

    sim = nx.simrank_similarity(G)
    lol = [[sim[u][v] for v in sorted(sim[u])] for u in sorted(sim)]
    sim_array = np.round(array(lol), 3)

    nx.draw(G, with_labels=True, node_size=2000, edge_color='#eb4034', width=3, font_size=16, font_weight=500, arrowsize=20, alpha=0.8)
    plt.show()  
        
    
if __name__ == '__main__':
    node_sum, node_mat = read_txt('./hw3dataset/graph_1.txt')
    draw(node_mat, node_sum)