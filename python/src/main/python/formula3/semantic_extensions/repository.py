from rdflib import plugin, Graph, Literal, URIRef, Namespace
from rdflib.store import Store

class SemanticRepository:
    g = None
    store = None
    ident = URIRef('semantic-time-series.ts')
    uri = Literal('mysql://root:toor@localhost/TripleStore')
    
    DC   = Namespace('http://purl.org/dc/terms/')
    FOAF = Namespace('http://xmlns.com/foaf/0.1/')
    RDF  = Namespace('http://www.w3.org/1999/02/22-rdf-syntax-ns#')
    RDFS = Namespace('http://www.w3.org/2000/01/rdf-schema/#')
    OWL  = Namespace('http://www.w3.org/2002/07/owl#')
    STSP = Namespace('http://semantic-time-series-processing.org/')
    XSD  = Namespace('http://www.w3.org/2001/XMLSchema#')
    
    def __init__(self):
        self.store = plugin.get('SQLAlchemy', Store)(identifier = self.ident)
        self.g = Graph(self.store, identifier = self.ident)
        self.g.open(self.uri, create = True)
        
    def close(self):
        self.g.destroy(self.uri)
        try:
            self.g.close()
        except:
            pass
    
    def load_ontology(self, input_graph, input_format):
        self.g.load(input_graph, format=input_format)
    
    def add_data_triple(self, s, p, o):
        if p.startswith('dc:'):
            self.g.add((self.STSP[s[5:]], self.DC[p[3:]], Literal(o)))
        elif p.startswith('foaf:'):
            self.g.add((self.STSP[s[5:]], self.FOAF[p[5:]], Literal(o)))
        elif p.startswith('rdf:'):
            self.g.add((self.STSP[s[5:]], self.RDF[p[4:]], Literal(o)))
        elif p.startswith('rdfs:'):
            self.g.add((self.STSP[s[5:]], self.RDFS[p[5:]], Literal(o)))
        elif p.startswith('owl:'):
            self.g.add((self.STSP[s[5:]], self.OWL[p[4:]], Literal(o)))
        elif p.startswith('stsp:'):
            self.g.add((self.STSP[s[5:]], self.STSP[p[5:]], Literal(o)))
        elif p.startswith('xsd:'):
            self.g.add((self.STSP[s[5:]], self.XSD[p[4:]], Literal(o)))
        self.g.serialize(format = 'nt')
        self.g.commit()
        
    def add_object_triple(self, s, p, o):
        #s = self.STSP[s[5:]]
        #if p.startswith('dc:'):
        #    p = self.DC[p[3:]]
        #elif p.startswith('foaf:'):
        #    p = self.FOAF[p[5:]]
        #elif p.startswith('rdf:'):
        #    p = self.RDF[p[4:]]
        #elif p.startswith('rdfs:'):
        #    p = self.RDFS[p[5:]]
        #elif p.startswith('owl:'):
        #    p = self.OWL[p[4:]]
        #elif p.startswith('stsp:'):
        #    p = self.STSP[p[5:]]
        #elif p.startswith('xsd:'):
        #    p = self.XSD[p[4:]]
        #if o.startswith('dc:'):
        #    o = self.DC[o[3:]]
        #elif o.startswith('foaf:'):
        #    o = self.FOAF[o[5:]]
        #elif o.startswith('rdf:'):
        #    o = self.RDF[o[4:]]
        #elif o.startswith('rdfs:'):
        #    o = self.RDFS[o[5:]]
        #elif o.startswith('owl:'):
        #    o = self.OWL[o[4:]]
        #elif o.startswith('stsp:'):
        #    o = self.STSP[o[5:]]
        #elif o.startswith('xsd:'):
        #    o = self.XSD[o[4:]]
        #self.g.add((s, p, o))
        self.g.add((self.STSP[s[5:]], self.DC[p[3:]], self.STSP[o[4:]]))
        
    def get_triples(self, query):
        return self.g.query(query)
