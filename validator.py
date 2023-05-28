from NNclassifier import NNclassifier

class validator:
    def validation(self, dataset: list):
        number_correctly_classified = 0
        data_len = len(dataset)
        classifier = NNclassifier()
        
        for i in range(data_len):
            if classifier.classifier(dataset, dataset[i], i): number_correctly_classified +=1

        return number_correctly_classified / data_len