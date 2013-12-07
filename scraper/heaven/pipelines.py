# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from heaven.items import TermItem, PageItem, TermValueItem
from scrapy.exceptions import DropItem
from  hvnrhell.models import  TermValue
import math

class TrainingPipeline(object):
    def normalize(self,vec):
        absValue=math.sqrt(sum([val**2 for val in vec]))
        if absValue==0:
            return vec
        else:
            for val in vec:
                val/=absValue
        return vec
    def __init__(self):
        self.pages = [page.url for page in PageItem.django_model.objects.all()]
        self.terms = [term for term in TermItem.django_model.objects.all()]
        self.termVocab = [word.term for word in self.terms]
    
    def process_item(self, item, spider):
        #Drop the item if the page is already in the database
        if item['url'] in self.pages:
            raise DropItem
        else:
            page = item.save()
            self.pages.append(item['url'])

        startIndex = len(self.terms)
        
        tokens = item['tokens']
        vocab = []
        term_freq = []
        for token in tokens:
            if token not in vocab:
                vocab.append(token)
                term_freq.append(float(1))
            else:
                term_freq[vocab.index(token)]+=1
        term_freq=self.normalize(term_freq)
        termValues = []

        #Add all of the term pages for the page to the database
        
        for i in range(0,len(vocab)):
            if vocab[i] in self.termVocab:
                t = self.terms[self.termVocab.index(vocab[i])]
                self.terms.append(t)
                termval = TermValue(value=term_freq[i],term=t,page=page)
                termValues.append(termval)
                #termval = TermValueItem()
                #termval['value'] = term_freq[i]
                #termval['term'] = t
                #termval['page'] = page
                #termval.save()
            
            else:
                term = TermItem()
                term['term']=vocab[i]
                term['index']=i+startIndex
                t = term.save()
                
                self.terms.append(t)
                self.termVocab.append(vocab[i])
                
                termval = TermValue(value=term_freq[i],term=t,page=page)
                termValues.append(termval)
                #termval['value'] = term_freq[i]
                #termval['term'] = t
                #termval['page'] = page
                #termval.save()
        TermValue.objects.bulk_create(termValues)
        return item

