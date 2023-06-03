import math

class NNclassifier:
    def train(self, dataset: list, object: list, index: int):   # train(whole dataset, single point, index of this point)
        object_to_classify = list(map(float, object))           # Single point/row to classify
        object_len = len(object)
        
        nearest_distance = math.inf
        nearest_label = 0
        
        for k, train_object in enumerate(dataset):
            temp_sum = 0
            if k != index:
                for m in range(1, object_len):                  # ignore the first column - label
                                                                # Euclidean Distance
                    temp_sum += pow(object_to_classify[m] - float(train_object[m]), 2)
                if temp_sum < nearest_distance:
                    nearest_distance = temp_sum
                    nearest_label = train_object[0]
        return nearest_label
    
    def test(self, toTest, classify):                           # test(function train(), the signle point you want to test)
        return True if toTest == classify else False
    
    def classifier(self, dataset: list, object: list, index: int):
        return self.test(self.train(dataset, object, index), object[0])