import math

class NNclassifier:
    def train(self, dataset: list, object: list, index: int):
        object_to_classify = object
        label_object_to_classify = object[0]
        object_len = len(object)
        
        nearest_distance = math.inf
        nearest_location = math.inf
        nearest_label = 0
        
        for k, train_object in enumerate(dataset):
            temp_sum = 0
            if k != index:
                for m in range(1, object_len):
                    temp_sum += pow(float(object_to_classify[m]) - float(train_object[m]), 2)
                distance = math.sqrt(temp_sum)
                if distance < nearest_distance:
                    nearest_distance = distance
                    nearest_location = k
                    nearest_label = train_object[0]
        print("Object ", index+1, " is class: ", int(float(label_object_to_classify)))
        print("Its nearest_neighbor is ", nearest_location+1, " which is in class ", int(float(nearest_label)))
        
        return nearest_label
    
    def test(self, toTest, classify):
        return True if toTest == classify else False
    
    def classifier(self, dataset: list, object: list, index: int):
        return self.test(self.train(dataset, object, index), object[0])