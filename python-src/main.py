import json
import networkx as nx
import matplotlib.pyplot as plt 
from set_ordering import generate_timeset_graph, get_longest_path_graph

if __name__ == '__main__':
    with open("/Users/matthewteelucksingh/Repos/TimeSets/data/infovis-citation-data.json", "r") as f:
        articles: list[dict] = json.loads(f.read())

    def get_num_citations(article):
        return len(article['citations'])

    # Counting the number of citations for each article:
    articles.sort(key=get_num_citations, reverse=True)
    top_200_articles =  articles[0:200] 
    articles_dict = {article['articleId']: article for article in top_200_articles}

    nested_concepts = [article['concepts'] for article in articles_dict.values()]

    concepts = []
    for nested_concept in nested_concepts:
        for concept in nested_concept:
            concepts.append(concept)
    
    #concepts = set(concepts)
    concepts = ['network', 'clustering', 'overview', 'graph', 'navigation', 'interaction', 'evaluation', 'hierarchy']

    # All of the articles associated with each concept:
    concept_mapped = {}
    for concept in concepts:
        concept_mapped[concept] = [
            article['articleId'] for article in articles_dict.values()
            if concept in article['concepts']
        ]

    graph: nx.Graph = generate_timeset_graph(
        groups=concepts,
        events=articles_dict,
        group_key='concepts',
        event_id_key='articleId'
    )

    set_order, set_order_weight = get_longest_path_graph(graph, concepts)

    print(set_order, set_order_weight)