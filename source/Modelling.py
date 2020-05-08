from . import *

class Modelling:
    
    def split_to_train_test(X, y, test_size = Params.TEST_PERC, random_state = Params.RANDOM_STATE):
        '''
        returns a TrainTest object
        *X*: pandas dataframe containing the covariates of the dataset
        *y*: pandas dataframe containing the targets of the dataset
        *random_state*: the random state used for ensuring the reproducibility of the results
        '''
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)
        return TrainTest(X_train, X_test, y_train, y_test)
    
    
    def generate_cross_val_data_without_restrictions(traintest, splits = Params.CV_SPLITS, random_state = Params.RANDOM_STATE):
        '''
        returns a list of TrainTest objects with corresponding to the different cross validation pairs
        *traintest*: a TrainTest object
        *splits*: the number of cross-validation pairs to be generated
        *random_state*: the random state used so that the results are reproducible (int)
        '''
        X = traintest.X_train
        y = traintest.y_train
        cv = KFold(n_splits=splits, shuffle=True, random_state=random_state)
        train_val_index_tuples = list(cv.split(X))
        X_trains = [X.iloc[train_index] for train_index, _ in train_val_index_tuples]
        y_trains = [y.iloc[train_index] for train_index, _ in train_val_index_tuples]
        X_vals = [X.iloc[val_index] for _, val_index in train_val_index_tuples]
        y_vals = [y.iloc[val_index] for _, val_index in train_val_index_tuples]
        zipped_datasets = list(zip(X_trains, X_vals, y_trains, y_vals))
        train_tests = list(map(lambda data: TrainTest(data[0], data[1], data[2], data[3]), zipped_datasets))
        return train_tests
    
    
    
    
    def fit_predict_and_evaluate(classification_model, traintest, get_importances):
        '''
        returns a Metrics object
        *classification_model*: sklearn initialized object corresponding to the classification technique to be applied and its hyper-parameters
        *traintest*: TrainTest object
        *get_importances*: boolean flag denoting whether the feature importances should be outputed
        '''
        X_train = traintest.X_train
        y_train = traintest.y_train
        X_val = traintest.X_test
        y_val = traintest.y_test
        classification_model.fit(X_train, y_train.values.ravel())
        y_pred = classification_model.predict(X_val)
        y_score = classification_model.predict_proba(X_val)
        #y_pred_train = classification_model.predict(X_train)
        #print("Precision on training set: {}".format(precision_score(y_pred_train, y_train)))
        #print("Recall on training set: {}".format(recall_score(y_pred_train, y_train)))
        if get_importances:
            feat_importances = pd.Series(classification_model.feature_importances_, index=X_train.columns)
            feat_importances.nlargest(20).plot(kind='barh', fontsize = 13)
        accuracy = accuracy_score(y_val,y_pred)
        precision = precision_score(y_val, y_pred)
        recall = recall_score(y_val, y_pred)
        return Metrics(accuracy, precision, recall)

    
    def apply_classification(classification_model, cv_datasets, get_importances = False):
        '''
        returns a Metrics object containing the average performance metrics of the cross-validation for a
        particular classification model
        *classification_model*: sklearn initialized object corresponding to the classification technique to be applied and its hyper-parameters
        *cv_datasets*: list of TrainTest objects
        *get_importances*: boolean flag denoting whether the feature importances should be outputed
        '''
        metrics = list(map(lambda cv_pair: Modelling.fit_predict_and_evaluate(classification_model, cv_pair,
                                                                             get_importances), cv_datasets))

        accuracies = list(map(lambda metric: metric.accuracy, metrics))
        precisions = list(map(lambda metric: metric.precision, metrics))
        recalls = list(map(lambda metric: metric.recall, metrics))

        avg_accuracy = sum(accuracies) / len(accuracies)
        avg_precision = sum(precisions) / len(precisions)
        avg_recall = sum(recalls) / len(recalls)
        return Metrics(avg_accuracy, avg_precision, avg_recall)

