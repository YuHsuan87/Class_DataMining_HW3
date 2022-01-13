from method import *
from load_data import *
import numpy as np
import matplotlib.pyplot as plt
import time

# matplot to see convergence rate
def cr_result(cr_s, iter, node_sum):
    cr_result = [[0 for i in range(iter)]for j in range(node_sum)]
    for i in range(node_sum):
        for j in range(iter):
            cr_result[i][j] = cr_s[j][i]
    x = [i for i in range(1, iter+1)]
    for i in range(node_sum):
        plt.plot(x, cr_result[i], label = x[i], marker = 'o')  
    plt.xlabel('Iter')
    plt.ylabel('Sim')
    plt.title('Sim CR result')
    plt.legend()
    plt.show()

if __name__ == '__main__':
    # load file
    # num range is the graph_'num' you want
    for num in range(1, 6):
        file_name = 'graph_' + str(num)
        file_path = './hw3dataset/' + file_name + '.txt'
        node_sum, node_mat = read_txt(file_path)

        # select the method you want to implement
        method = 'all'
        iter = 20
        # done
        if method == 'hits':
            # implement HITS
            auths, hubs, cr_auths, cr_hubs = hits(node_sum, node_mat, iter)
            print('-----------------------------------------------------------')
            print(f'{file_name}:')
            print(f'auths:{auths}')
            print(f'hubs:{hubs}')
            # cr_result(cr_auths, iter, node_sum)
            # visualize
            # x = [i for i in range(1,node_sum+1)]
            # plt.xlabel('node')
            # plt.ylabel('Authorities')
            # plt.title(f'{file_name}_Auths')
            # plt.bar(x, auths)
            # plt.show()

            # Output txt_file
            # np.savetxt(f'{file_name}_HITS_authority.txt', auths, fmt='%.08f', newline=' ')
            # np.savetxt(f'{file_name}_HITS_hubs.txt', hubs, fmt='%.08f', newline=' ')

        elif method == 'pagerank':
            damping_factors = [0.1, 0.15, 0.2, 0.3, 0.6, 0.8]
            for damping_factor in damping_factors:
                pr, cr_pr = pagerank(node_sum, node_mat, iter, damping_factor)
                print('-----------------------------------------------------------')
                print(f'{file_name}:')
                pr = [('%.5f' % i) for i in pr]
                print(f'damping_factor:{damping_factor}, PR:{pr}')

            # cr_result(cr_pr, iter, node_sum)
            # np.savetxt(f'{file_name}_PageRank.txt', pr, fmt='%.08f', newline=' ')

            # visualize
            # x = [i for i in range(1,node_sum+1)]
            # plt.xlabel('node')
            # plt.ylabel('PR')
            # plt.title(f'{file_name}_PR')
            # plt.bar(x, pr)
            # plt.show()
        
        # done
        elif method == 'simrank':
            decay_factors = [0.4, 0.7, 0.8, 0.9]
            for decay_factor in decay_factors: 
                sim, cr_sim = simrank(node_sum, node_mat, iter, decay_factor)
                print('-----------------------------------------------------------')
                print(f'{file_name}:')
                print(f'decay_factor:{decay_factor}')
                show(sim)
            # cr_result(cr_sim, iter, node_sum)
            # np.savetxt(f'{file_name}_SimRank.txt', sim, fmt='%.04f', newline='\n')
        
        else:
            # HITS
            start = time.time()
            auths, hubs, cr_auths, cr_hubs = hits(node_sum, node_mat, iter)
            end = time.time()
            print('-----------------------------------------------------------')
            print(f'{file_name}\'s HITS execution time: {end-start}')
            np.savetxt(f'./result/{file_name}_HITS_authority.txt', auths, fmt='%.07f', newline=' ')
            np.savetxt(f'./result/{file_name}_HITS_hubs.txt', hubs, fmt='%.07f', newline=' ')

            # PageRank
            start = time.time()
            pr, cr_pr = pagerank(node_sum, node_mat, iter, 0.15)
            end = time.time()
            print('-----------------------------------------------------------')
            print(f'{file_name}\'s PageRank execution time: {end-start}')
            np.savetxt(f'./result/{file_name}_PageRank.txt', pr, fmt='%.07f', newline=' ')

            # SimRank
            start = time.time()
            sim, cr_sim = simrank(node_sum, node_mat, iter, 0.9)
            end = time.time()
            print('-----------------------------------------------------------')
            print(f'{file_name}\'s SimRank execution time: {end-start}')
            np.savetxt(f'./result/{file_name}_SimRank.txt', sim, fmt='%.07f', newline='\n')



