import os
import pickle
import numpy as np

path = os.path.dirname(os.path.abspath(__file__))

def load_dataset_from_file(file_name, cateogries=None):
    """
    load dataset from file to arrays needed for prediction
    :return: group_ix, tokens, features and labels from data set
    """
    with open(file_name,'rb') as f:
        tweet_ix, ix, _, tokens,  features, labels = map(np.array, pickle.load(f))
    return load_dataset(tweet_ix, ix, tokens, features, labels, cateogries)


def load_dataset(tweet_ix, ix, tokens, features, labels, categories=None):
    """
    load dataset from various part to arrays needed for prediction
    :return: group_ix, tokens, features and labels from data set
    """
    def one_hot_encode(data, ixs):
        assert(all(np.array(ixs)>=0))
        for i in ixs:
            records = np.zeros((len(data), len(categories)))
            for row_ix, elem in enumerate(data[:, i]):
                records[row_ix, np.where(categories == elem)] = 1
            data = np.concatenate((data, records), axis=1)
        return np.delete(data, ixs, axis=1).astype(float)

    features[:,1], features[:,0] = features[:,0], features[:,1].copy()
    group_ix = list(zip(tweet_ix, ix))
    assert (all(group_ix[i] >= group_ix[i - 1] for i in range(1, len(group_ix))))
    #print('#match: {}, #groups: {}, total: {}'.format(sum(labels),len(set(group_ix)), len(labels)))

    if categories is None:
        # all the POS_taggings I can find
        categories = np.array(['','!','#','$','&',',','@','A','D','E','G','L','N',
                               'O','P','R','S','T','U','V','X','Y','Z','^','~'])
    features = one_hot_encode(features,[8,9])
    features, labels = features.astype(float), labels.astype(int)
    return group_ix, tokens, features, labels


def save_model(model, file_name=path + '/model_trained'):
    """
    save model to file specified
    :param model: any model to be saved
    :param file_name: file to dump the model
    :return: None
    """
    with open(file_name,'wb') as f:
        pickle.dump(model,f)

def load_model(file_name=path + '/model_trained'):
    """
    load model from file specified
    :param file_name: file to load the model
    :return: model
    """
    with open(file_name, 'rb') as f:
        return pickle.load(f)
