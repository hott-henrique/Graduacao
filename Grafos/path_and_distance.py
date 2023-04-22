import argparse

import networkx as nx
import numpy as np

def main(network_path: str):
    try:
        G: nx.Graph = nx.read_gml(network_path, label='id')

        V = G.number_of_nodes()

        adj_matrix = np.full(shape=( V, V ), fill_value=np.inf)

        for v in G:
            for adj in G[v]:
                adj_matrix[v - 1][adj - 1] = 1
                adj_matrix[adj - 1][v - 1] = 1

        # Floyd Warshall
        for v0 in range(V):
            for vi in range(V):
                for vj in range(V):
                    dist = adj_matrix[vi][v0] + adj_matrix[v0][vj]

                    if dist < adj_matrix[vi][vj]:
                        adj_matrix[vi][vj] = dist

        np.fill_diagonal(adj_matrix, 0)

        eccentricities: np.ndarray = np.max(adj_matrix, axis=0)

        diameter = np.max(eccentricities)
        radius = np.min(eccentricities)

        mean_dist_per_vertex = np.mean(adj_matrix, axis=0)
        centroid_dist = mean_dist_per_vertex.min()

        print(G)

        print(
            f"Eccentricities: {eccentricities.tolist()}",
            f"Diameter: {diameter}",
            f"Radius: {radius}",
            f"Vertices in Center: {np.argwhere(eccentricities == radius).flatten() + 1}",
            f"Centroids: {np.argwhere(mean_dist_per_vertex <= centroid_dist).flatten() + 1}",
            f"Vertices in Periphery: {np.argwhere(eccentricities == diameter).flatten() + 1}",
            sep='\n'
        )

    except Exception as e:
        print(f"[EXCEPTION]: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--network-path", type=str, required=True)

    args = parser.parse_args()

    main(args.network_path)
