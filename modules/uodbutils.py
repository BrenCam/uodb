'''
Test app to find partial key matches
Builds a searchable string string from the key values
?? Modify to ignore case in searches
?? Need to  capitalize key values when entered and before search
'''
# See http://stackoverflow.com/questions/5174506/search-of-dictionary-keys-python
class DictLookupBySubstr(object):

    def __init__(self, dictionary, separator='\n'):
        self.dic = dictionary
        self.sep = separator
        self.txt = separator.join(dictionary.keys())+separator
        # Force lower case 
        #print '\n **************  DictLookupBy: __init__: %s \n' %type(self.txt)
        #self.txt = self.xtxt.lower()


    def search(self, key):
        res = []
        i = self.txt.find(key)
        #i = self.txt.find(key.lower())
        while i >= 0:
            left = self.txt.rfind(self.sep, 0, i) + 1
            right = self.txt.find(self.sep, i)
            dic_key = self.txt[left:right]
            res.append(self.dic[dic_key])
            i = self.txt.find(key, right+1)
        return res


mydict ={}

# populate dictionary with test keys
mydict['joe'] = 1
mydict['jon'] = 2
mydict['john'] = 3
mydict['jona'] = 4
mydict['jonah'] = 5

if __name__ == "__main__":

  print '>>> Start <<<'
  mydlu = DLU(mydict)
  str = mydlu.search('jon')
  print 'result: %s' %str
  print '>>> End <<<'


