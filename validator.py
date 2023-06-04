from NNclassifier import NNclassifier
import numpy as np

class validator:
    def validation(self, dataset: list):
        if not dataset: return 0                # check empty
        number_correctly_classified = 0
        data_len = len(dataset)
        classifier = NNclassifier()
        
        for i in range(data_len):               # loop through all the points
            if classifier.classifier(dataset, dataset[i], i): number_correctly_classified +=1

        return number_correctly_classified / data_len