import networkx as nx
from itertools import combinations
import numpy as np

from app.schemas.context import Context
from app.schemas.mindmap import MindMap

fields = ['ID', 'FORM', 'LEMMA', 'CPOS', 'POS', 'FEATS', 'HEAD', 'DEPREL', 'PHEAD', 'PDEPREL']
fields_dict = { field: index for index, field in enumerate(fields) }

class DependencyGraph:
    def __init__(self, dep_data):
        self.dep_data = dep_data
        self.graph = [[] for i in range(len(dep_data[0]))]
        self.make_graph()

    def make_graph(self):
        for i, head in enumerate(self.dep_data[fields_dict['HEAD']]):
            if head != '_': self.graph[int(head) - 1].append(i)

    def search_graph(self, concept, window_size):
        res = []
        here = int(concept)
        if window_size == 1: return [here]
        else:
            res = self.search_graph(concept, window_size-1)
            for i in range(here - window_size + 1, here + 1):
                dep = [self.graph[x] for x in range(i, i + window_size)]
                dep = sum(dep, [])

                window = [x for x in range(i, i + window_size)]
                ok = True
                for word in window:
                    if word != here and word not in dep: ok = False
                if ok: res = window
            return res
        
    def make_keyword(self, keyword_index):
        keyword_index.sort()
        
        keyword = ""
        for i, value in enumerate(keyword_index):
            if self.dep_data[fields_dict['CPOS']][value] == 'PART': continue
            if i == len(keyword_index)-1 and self.dep_data[fields_dict['CPOS']][value] == 'ADP': break
            keyword = keyword + self.dep_data[fields_dict['FORM']][value]
            if i != len(keyword_index)-1 and self.dep_data[fields_dict['PDEPREL']][value] != 'SpaceAfter=No': keyword = keyword + " "
        return keyword

    def extract_keywords(self, window_size):
        concepts = [i for i, dep in enumerate(self.dep_data[fields_dict['DEPREL']]) if dep in ['nsubj', 'obj', 'iobj']]
        
        keywords = []
        for concept in concepts:
            keyword_index = self.search_graph(concept, window_size)
            keywords.append(self.make_keyword(keyword_index))
        return keywords

class MindMapController:
    def __init__(self, nlp_model, window_size: int = 5):
        self.graphs: nx.Graph = None
        self.context = {}
        self.mindmap: MindMap = MindMap()
        
        self.model = nlp_model
        self.window_size = window_size

    def transform(self, context: Context) -> nx.Graph:
        self.context["text"] = context.text
        self.context["words"] = self.preprocess(self.context["text"])

        self.context["nouns"] = self.extract_keyword_noun()
        self.context["index"] = {n: i for i, n in enumerate(self.context["nouns"])}
        self.graphs = self.make_concept_map()
        self.mindmap = self.make_concept_tree()
        return self.mindmap

    def preprocess(self, context: str) -> list:
        # apply kss code after making mst baseline
        stop_words = ["<p>", "</p>", "<h1>", "</h1>", "<h2>", "</h2>", "<h3>", "</h3>", "\\", "(", ")", "Fig.", "fig.", "Fig", "fig", "Table", "table", "mathrm"]

        for word in stop_words:
            context = context.replace(word, '')
        preprocessed_context = self.model(context).values
        return preprocessed_context
    
    def extract_keyword_noun(self) -> list:
        dg = DependencyGraph(self.context["words"])
        return list(set(dg.extract_keywords(window_size=3)))
    
    def make_concept_map(self) -> nx.Graph:
        G = nx.Graph()

        nouns = self.context["nouns"]
        context = self.context["words"]
        for i, word in enumerate(nouns):
            G.add_nodes_from([(word, {'freq': 0, 'offsets': []})])

        for i, word in enumerate(context[fields_dict['FORM']]):
            if word not in nouns: continue

            offsets = G.nodes[word]['offsets']
            offsets.append((i, i+1))
            G.add_nodes_from([word], offsets=offsets)
            G.add_nodes_from([word], freq=len(G.nodes[word]['offsets']))

        for i in range(len(context[1])-self.window_size):
            here_data = [data for data in context[1][i:i+self.window_size] if data in nouns]
            here_data_comb = list(combinations(here_data, 2))

            for first, second in here_data_comb:
                G.add_edge(first, second) 
        return G

    def make_concept_tree(self) -> MindMap:
        ret = MindMap()

        max_node = np.argmax([self.graphs.nodes[_]['freq'] for _ in self.graphs.nodes()])
        ret.root = str(max_node)
        ret.keywords = self.context["nouns"]

        max_node = self.context["nouns"][max_node]
        tree = nx.bfs_tree(self.graphs, max_node, depth_limit=3)
        
        q = [max_node]
        while len(q) != 0:
            here = q.pop(0)
            here_index = self.context["index"][here]
            if tree.neighbors(here) != None:
                ret.graph[here_index] = []

            for next in tree.neighbors(here):
                q.append(next)

                next_index = self.context["index"][next]
                ret.graph[here_index].append(next_index)
        return ret

    def clean(self):
        self.graphs = []