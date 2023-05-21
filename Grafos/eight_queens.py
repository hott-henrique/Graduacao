import numpy as np
import networkx as nx
from scipy.sparse import csr_matrix


def heuristic(mat_adj: csr_matrix):
    selection_list: list = np.argsort(mat_adj.sum(axis=1))[::-1].tolist()

    s0 = np.random.choice(selection_list)

    selection_list.remove(s0)

    s = [ s0 ]

    i = 0
    while len(s) < 8:
        for elem in selection_list:
            s.append(elem)

            if not validate(mat_adj, s):
                s.pop()
            else:
                selection_list.remove(elem)

        if len(s) == 8:
            break

        print(f"{i + 1}: {s}")

        elem = np.random.choice(s)

        s.remove(elem)

        selection_list.append(elem)

        i = i + 1

    return s

def validate(mat_adj: csr_matrix, solution: list):
    n = len(solution)

    for i in range(n):
        for j in range(i + 1, n):
            vi = solution[i]
            vj = solution[j]

            if mat_adj[vi, vj] == 1 or vi == vj:
                return False

    return True

def main():
    G: nx.DiGraph = nx.read_gml("data/eight_queens.gml")

    mat_adj: csr_matrix = nx.adjacency_matrix(G)

    print(f"Final Solution: {heuristic(mat_adj)}")

if __name__ == "__main__":
    main()
