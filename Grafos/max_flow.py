import argparse

import networkx as nx

def create_flow_graph(G: nx.DiGraph): 
    Gf = nx.DiGraph()

    Gf.add_nodes_from(G.nodes)

    for Vi in G:
        Vi_adj_list = G[Vi]
        for Vj in Vi_adj_list:
            Gf.add_edge(Vi, Vj, flow=G[Vi][Vj]["weight"])
            Gf.add_edge(Vj, Vi, flow=0)

    return Gf

def main(graph_edgelist_file_path: str):
    G = nx.read_weighted_edgelist(graph_edgelist_file_path, delimiter=',', create_using=nx.DiGraph)

    Gf =  create_flow_graph(G)

    max_flow = 0.0

    try:
        while True:
            path = nx.shortest_path(Gf, source='S', target='T', weight="flow")

            Vidx = min(range(len(path) - 1), key=lambda i: Gf[path[i]][path[i + 1]]["flow"])

            min_flow_edge = (path[Vidx], path[Vidx + 1])

            min_flow = Gf[min_flow_edge[0]][min_flow_edge[1]]["flow"]

            for i in range(len(path) - 1):
                s, t = path[i], path[i + 1]

                Gf[s][t]["flow"] -= min_flow
                Gf[t][s]["flow"] += min_flow

                if Gf[s][t]["flow"] == 0:
                    Gf.remove_edge(s, t)

                    max_flow += min_flow
    except:
        print(f"Maximum Flow in Graph: {max_flow}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--graph-edgelist", help="Path to edgelist format graph file.", type=str, required=True)

    args = parser.parse_args()

    main(args.graph_edgelist)

