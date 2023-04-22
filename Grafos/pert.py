import argparse

import networkx as nx


def read_activities(file_path: str) -> dict:
    with open(file_path, "r") as f:
        data = f.readlines()

    data: list[str] = data[1:] # Ignore header line.

    activities = dict()

    for line in data:
        line = line.replace('\n', '')

        name, duration = line.split(',')

        activities[name] = int(duration)

    return activities

def PERT(g: nx.DiGraph, activities_timetable: dict):
    N = len(g)

    N_Plus = { v: list() for v in range(N) }
    N_Minus = { v: list() for v in range(N) }

    for vi in range(N):
        for vj in g[vi]:
            N_Plus[vi].append(vj)
            N_Minus[vj].append(vi)

    A = nx.get_edge_attributes(g, "activity")

    t_early = { v: 0 for v in range(N) }

    for vi in range(N):
        t_early[vi] = max(
            [ t_early[vj] + activities_timetable[A[(vj, vi)]] for vj in  N_Minus[vi] ],
            default=0
        )

    t_late = { v: t_early[v] for v in range(N) }
    f = { v: 0 for v in range(N) }

    for vi in range(N - 1, 0, -1):
        t_late[vi] = min(
            [ t_late[vj] - activities_timetable[A[(vi, vj)]] for vj in N_Plus[vi] ],
            default=t_late[vi]
        )

        f[vi] = t_late[vi] - t_early[vi]

    crit = [ 0 ]

    for vi in range(1, N):
        if t_early[vi] == t_late[vi]:
            crit.append(vi)

    return t_early, t_late, f, crit

def main(timetable_file_path: str, pert_graph_file_path: str):
    activities_timetable = read_activities(timetable_file_path)

    g = nx.read_gml(pert_graph_file_path, label='id')

    t_early, t_late, f, crit = PERT(g, activities_timetable)

    print("| {:6} | {:^4} | {:^4} | {:^3} |".format("vertex", "t", "t'", "f"))
    for vi in g:
        print("| {:6} | {:^4} | {:^4} | {:^3} |".format(vi, t_early[vi], t_late[vi], f[vi]))

    print("Critical Path:\n", " -> ".join([ str(element) for element in crit ]))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--timetable", help="Path to timetable csv file.", type=str, required=True)
    parser.add_argument("--pert-graph", help="Path to pert graph gml file.", type=str, required=True)

    args = parser.parse_args()

    main(args.timetable, args.pert_graph)

