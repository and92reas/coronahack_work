from . import *

class Metrics:
    
    def __init__(self, accuracy, precision, recall):
        '''
        *accuracy*: accuracy
        *precision*: precision
        *recall*: recall
        '''
        self.accuracy = accuracy
        self.precision = precision
        self.recall = recall
        
        
    def tostring(self):
        '''
        prints the results
        '''
        print("accuracy: {:.2f}\nprecision: {:.2f}\nrecall: {:.2f}".format(
            self.accuracy, self.precision, self.recall))

