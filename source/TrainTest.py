from . import *

class TrainTest:
    
    def __init__(self, X_train, X_test, y_train, y_test):
        '''
        *X_train*: array containing the training set
        *X_test*: array containing the test set
        *y_train*: array containing the training set's labels
        *y_test*: array containing the tests set's labels
        '''
        self.X_train = X_train
        self.X_test = X_test
        self.y_train = y_train
        self.y_test = y_test
