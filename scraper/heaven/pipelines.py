# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from heaven.items import TermItem, PageItem, TermValueItem
import scrapy.exceptions.DropItem
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
    
    def process_item(self, item, spider):
        #Drop the item if the page is already in the database
        pages = [page['url'] for PageItem.django_model.objects.all()]
        if item['url'] in pages:
            raise DropItem
        else:
            page = item.save()
        
        terms = TermItem.django_model.objects.all()
        termVocab = [word['term'] for word in terms]
        start_index = len(terms)
        
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
        
        for i in range(0,len(vocab)):
            if vocab[i] in termVocab:
                t = terms[termVocab.index(vocab[i])]
                
                termval = TermValueItem()
                termval['value'] = term_freq[i]
                termval['term'] = t
                termval['page'] = page
                termval.save()
            
            else:
                term = TermItem()
                term['term']=vocab[i]
                term['index']=i+index
                t = term.save()
                
                termval = TermValueItem()
                termval['value'] = term_freq[i]
                termval['term'] = t
                termval['page'] = page
                termval.save()
                
        return item

