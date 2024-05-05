
import networkx as nx

def generate_timeset_graph(groups: list[str], events: dict, group_key: str, event_id_key: str) -> nx.Graph:

    G = nx.Graph()

    # Mapping all of the events to the associated groups:
    groups_mapped: dict[str, list[str]] = {}

    for group in groups:
        groups_mapped[group] = [
            event[event_id_key] for event in events.values() if group in event[group_key]
        ]

    # Determining all of the intersections between each concept:
    groups_mapped_cpy = groups_mapped.copy()
    for primary_group, primary_events in groups_mapped.items():
        groups_mapped_cpy.pop(primary_group)

        for comparison_group, comparison_events in groups_mapped_cpy.items():

            event_intersection = list(
                set(primary_events) & set(comparison_events)
            )

            #print(f"{primary_group} -> {comparison_group} Num Weights: {len(event_intersection)}")
            #if len(event_intersection) > 0:
            G.add_edge(primary_group, comparison_group, weight=len(event_intersection))

    return G


def get_longest_path_graph(G: nx.Graph, groups: list[str] | set[str]) -> tuple[list, int]:
    """
    Generate all possible permutations of the sets in S. Since the number of sets is limited by 
    the number of colors that humans can easily distinguish, the brute force approach is feasible.

    For each permutation, calculate the total weight of the path connecting all vertices (sets) in
    the permutation. This can be done by summing the weights of the edges (connections) between adjacent 
    sets in the permutation.

    Keep track of the permutation with the maximum total weight. The permutation with the maximum total 
    weight represents the optimal set ordering, where the maximum number of events are shared by 
    neighboring sets.
    """
    def calculate_path_weight(graph, path):
        weight = 0
        for i in range(len(path) - 1):
            weight += graph[path[i]][path[i+1]]['weight']
        return weight

    weights_dict: dict[int, list[str]] = {}
    for path in nx.simple_cycles(G):
        if len(path) == len(groups):

            current_weight = calculate_path_weight(G, path)
            weights_dict[current_weight] = path

    all_weights_lst: list[int] = list(weights_dict.keys())
    all_weights_lst.sort(reverse=True)

    highest_weight_path = weights_dict[all_weights_lst[0]]

    return highest_weight_path, all_weights_lst[0]