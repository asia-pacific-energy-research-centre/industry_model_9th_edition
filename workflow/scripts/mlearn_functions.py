# Machine learning functions
# Set working directory to be the project folder
import os
import re

wanted_wd = 'industry_model_9th_edition'
os.chdir(re.split(wanted_wd, os.getcwd())[0] + wanted_wd)

# execute config file
config_file = './config/config_apr2023.py'
with open(config_file) as infile:
    exec(infile.read())

def save_ktss_datasets(X, y, k):
    """ Splits the time series datasets (X, y) into k folds and saves the output from 
    each fold into directories.

    Args:
        X : numpy array represents the features
        y : numpy array represents the target
        k : int value represents the number of folds to split the given datasets
    """

    # Shuffles and Split dataset into k folds. 
    splits = TimeSeriesSplit(n_splits = k)

    fold_idx = 0
    for train_index, test_index in splits.split(X, y = y, groups = None):    
       X_train, X_test = X[train_index], X[test_index]
       y_train, y_test = y[train_index], y[test_index]

       os.makedirs(f'./data/model_dev/train/{fold_idx}', exist_ok = True)
       np.savetxt(f'./data/model_dev/train/{fold_idx}/train_x.csv', X_train, delimiter = ',')
       np.savetxt(f'./data/model_dev/train/{fold_idx}/train_y.csv', y_train, delimiter = ',')

       os.makedirs(f'./data/model_dev/test/{fold_idx}', exist_ok = True)
       np.savetxt(f'./data/model_dev/test/{fold_idx}/test_x.csv', X_test, delimiter = ',')
       np.savetxt(f'./data/model_dev/test/{fold_idx}/test_y.csv', y_test, delimiter = ',')
       
       fold_idx += 1


def listGen(start, stop):
    return [[x for x in range(start, i + 1)] for i in range(start, stop + 1)]

def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)  # allows duplicate elements
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))