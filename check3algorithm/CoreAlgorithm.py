from operator import itemgetter
import json
import math
import os
from stemming import porter2

#I'm using json for the purposes of this demonstration,but have set up a
#database to store web training data into a database that can be read by the
#django site much more quickly
def read_data(filename):
    try:
        with open(filename) as f:
            data=(json.load(f))
    except:
        print "Failed to read data!"
        return []
    print "The json file has been successfully read!"
    return data

class KNN(object):

    def __init__(self):
        #database for webpages
        self.mypages = []
        self.vocabulary = []
        #Store the normalized vector for each page
        self.norm_vec=[]
        
    def index_pages(self, pages):
        self.mypages = [page for page in pages]
        for page in self.mypages:
            for token in page['tokens']:
                if token not in self.vocabulary:
                    self.vocabulary.append(token)
        
        self.norm_vec=[[float(pages[i]['tokens'].count(token)) for token in self.vocabulary] for i in range(0,len(pages))]
        for vector in self.norm_vec:
            vec_size = math.sqrt(sum([i**2 for i in vector]))
            for i in vector:
                i = i/vec_size
        
    def getDistance(self, vec1,vec2):
        return math.sqrt(sum([(vec1[i]-vec2[i])**2 for i in range(0,len(vec1))]))
    

    def computeKNearestNeighbors(self, page, k):
        page_vec = [float(page['tokens'].count(token)) for token in self.vocabulary]
        nearest_neighbors = []
        vec_size = math.sqrt(sum([i**2 for i in page_vec]))
        #normalize
        for i in page_vec:
            i = i/vec_size
        #will replace with precompiled version later
        for i in range(0,len(self.mypages)):
            distance = self.getDistance(page_vec,self.norm_vec[i])
            nearest_neighbors.append((self.mypages[i],distance))
            if(len(nearest_neighbors)>k):
                nearest_neighbors.remove(max(nearest_neighbors,key=itemgetter(1)))
        # set up an initial list for the nearest neighbors
        return nearest_neighbors

    def classify(self, page, k):
        nearest_neighbors=self.computeKNearestNeighbors(page,k)
        countG=0
        countPG13=0
        countR=0
        for page in nearest_neighbors:
            if page[0]['rating']=='G':
                countG+=1
            elif page[0]['rating']=='PG-13':
                countPG13+=1
            elif page[0]['rating']=='R':
                countR+=1
        #if countR is equal to any of the other rankings play it safe and go with R as a rating
        print str(countG)+','+str(countPG13)+','+str(countR)
        if max(countG,countPG13,countR)==countR:
            return 'R'
        elif countG <= countPG13:
            return 'PG-13'
        return 'G'

if __name__ == "__main__":
    print "Test is starting"
    pages = read_data(os.path.join(os.getcwd(),'g_rated.json'))[0:1]
    pages = pages + read_data(os.path.join(os.getcwd(),'pg13_rated.json'))[0:1]
    pages = pages + read_data(os.path.join(os.getcwd(),'r_rated.json'))[0:1]
    knn = KNN()
    knn.index_pages(pages)
    print "Indexing finished"
    #the first few hundered or so should all be g rated
    print knn.classify(pages[0],0)
