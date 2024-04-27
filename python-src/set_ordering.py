
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

            G.add_edge(primary_group, comparison_group, weight=len(event_intersection))

    return G


