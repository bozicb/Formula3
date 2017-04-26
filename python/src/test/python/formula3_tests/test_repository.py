import unittest
from formula3.semantic_extensions.repository import SemanticRepository
import time

class Test(unittest.TestCase):
    repo = None
    
    def setUp(self):
        self.repo = SemanticRepository()
        [self.repo.g.parse("/home/bojan/friends.rdf") for x in range(100)]
        
    def tearDown(self):
        self.repo.close()
        
    #def testLoadOntology(self):
		#self.repo.load_ontology("/home/bojan/friends.rdf", "xml") # 1,000 triples = 4.241s
		#[self.repo.load_ontology("/home/bojan/friends.rdf", "xml") for x in range(10)] # 10,000 triples = 36.588s
		#[self.repo.load_ontology("/home/bojan/friends.rdf", "xml") for x in range(20)] # 20,000 triples = 73.520s
		#[self.repo.load_ontology("/home/bojan/friends.rdf", "xml") for x in range(30)] # 30,000 triples = 101.543s
		#[self.repo.load_ontology("/home/bojan/friends.rdf", "xml") for x in range(40)] # 40,000 triples = 151.390s
		#[self.repo.load_ontology("/home/bojan/friends.rdf", "xml") for x in range(50)] # 50,000 triples = 185.954s
		#[self.repo.load_ontology("/home/bojan/friends.rdf", "xml") for x in range(60)] # 60,000 triples = 219.977s
		#[self.repo.load_ontology("/home/bojan/friends.rdf", "xml") for x in range(70)] # 70,000 triples =  253.575s
		#[self.repo.load_ontology("/home/bojan/friends.rdf", "xml") for x in range(80)] # 80,000 triples = 296.411s
		#[self.repo.load_ontology("/home/bojan/friends.rdf", "xml") for x in range(90)] # 90,000 triples = 347.253s
		#[self.repo.load_ontology("/home/bojan/friends.rdf", "xml") for x in range(100)] # 100,000 triples = 372.820s
		#print len(self.repo.g)

    #def testAddTriple(self):
	#	self.repo = SemanticRepository()
	#	for i in range(1000):
	#		self.repo.add_object_triple("stsp:bob", "foaf:name", "stsp:person")
	#		print i
		
		#[self.repo.add_data_triple("stsp:bob", "foaf:name", "Bob Smith") for x in range(1000)] # 1,000 triples: data = 4.407s, object = 4.329s
		#[self.repo.add_data_triple("stsp:bob", "foaf:name", "Bob Smith") for x in range(10000)] # 10,000 triples: data = 37.980s, object = 37.381s
		#[self.repo.add_data_triple("stsp:bob", "foaf:name", "Bob Smith") for x in range(20000)] # 20,000 triples: data = 76.238s, object = 74.735s
		#[self.repo.add_data_triple("stsp:bob", "foaf:name", "Bob Smith") for x in range(30000)] # 30,000 triples: data = 109.259s, object = 112.583s
		#[self.repo.add_data_triple("stsp:bob", "foaf:name", "Bob Smith") for x in range(40000)] # 40,000 triples: data = 153.371s, object = 151.039s
		#[self.repo.add_data_triple("stsp:bob", "foaf:name", "Bob Smith") for x in range(50000)] # 50,000 triples: data = 190.788s, object = 192.198s
		#[self.repo.add_data_triple("stsp:bob", "foaf:name", "Bob Smith") for x in range(60000)] # 60,000 triples: data = 225.573s, object = 226.372s
		#[self.repo.add_data_triple("stsp:bob", "foaf:name", "Bob Smith") for x in range(70000)] # 70,000 triples: data = 250.861s, object = 257.627s
		#[self.repo.add_data_triple("stsp:bob", "foaf:name", "Bob Smith") for x in range(80000)] # 80,000 triples: data = 291.349s, object = 263.343s
		#[self.repo.add_data_triple("stsp:bob", "foaf:name", "Bob Smith") for x in range(90000)] # 90,000 triples: data = 297.775s, object = 307.880s
		#[self.repo.add_data_triple("stsp:bob", "foaf:name", "Bob Smith") for x in range(100000)] # 100,000 triples: data = 331.760s, object = 327.784s

		#print len(self.repo.g)
#		self.repo.serialize("nt")
        
    def testGetTriples(self):
		#   1,000 triples = 0.471s
		#  10,000 triples = 0.497s
		#  20,000 triples = 0.493s
		#  30,000 triples = 0.511s
		#  40,000 triples = 0.499s
		#  50,000 triples = 0.498s
		#  60,000 triples = 0.502s
		#  70,000 triples = 0.496s
		#  80,000 triples = 0.503s
		#  90,000 triples = 0.500s
		# 100,000 triples = 0.515s
		start = time.time()
		triples = self.repo.get_triples("SELECT ?s ?p ?o WHERE {?s ?p ?o}")
		end = time.time()
		for row in triples:
			print "%s %s %s ." % row
		print len(self.repo.g)
		print end - start

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testRepository']
    unittest.main()
