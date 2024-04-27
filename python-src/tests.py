import json 
import pytest
import networkx as nx

from set_ordering import generate_timeset_graph


@pytest.fixture
def top_200_data():

    with open("/Users/matthewteelucksingh/Repos/TimeSets/data/infovis-citation-data.json", "r") as f:
        articles: list[dict] = json.loads(f.read())

    def get_num_citations(article):
        return len(article['citations'])

    # Counting the number of citations for each article:
    articles.sort(key=get_num_citations, reverse=True)
    top_200_articles =  articles[0:200] 
    articles_dict = {article['articleId']: article for article in top_200_articles}
    
    return articles_dict

def test_set_aggregation(top_200_data: dict):

    # Manually determining which articles are within the first two sets:
    nested_concepts = [article['concepts'] for article in top_200_data.values()]
    concepts = []
    for nested_concept in nested_concepts:
        for concept in nested_concept:
            concepts.append(concept)
    
    concepts = set(concepts)

    # All of the articles associated with each concept:
    concept_mapped = {}
    for concept in concepts:
        concept_mapped[concept] = [
            article['articleId'] for article in top_200_data.values()
            if concept in article['concepts']
        ]

    concept_1_articles = set(concept_mapped['evaluation'])
    concept_2_articles = set(concept_mapped['interaction'])

    article_concept_intersected = concept_1_articles & concept_2_articles

    graph: nx.Graph = generate_timeset_graph(
        groups=concepts,
        events=top_200_data,
        group_key='concepts',
        event_id_key='articleId'
    )

    num_articles_intersected_reference = len(article_concept_intersected)
    num_articles_intersected_calculated = graph.get_edge_data('evaluation', 'interaction')['weight']

    assert num_articles_intersected_reference == num_articles_intersected_calculated

