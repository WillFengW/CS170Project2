import math
import numpy as np
import threading

from queue import Queue

class NNclassifier:

                                                                # train_by_part(whole dataset, single point, index of this point, label of thread, queue)
    def train_by_part(self, dataset: list, object: list, index: int, part: int, q):   
        object_to_classify = object                             # Single point/row to classify
        object_len = len(object_to_classify)
        part_len = int(len(dataset)/4)                          # Size of array that each thread need to check
        start = part_len * part                                 # Starting index for dataset
        end = start + part_len                                  # Ending index for dataset
        if part == 3:
            end = int(len(dataset))
        
        nearest_distance = math.inf
        nearest_label = 0
        k = start
        
        for train_object in dataset[start:end]:
            temp_sum = 0
            if k != index:
                for m in range(1, object_len):                  # ignore the first column - label
                                                                # Euclidean Distance
                    temp_sum += pow(object_to_classify[m] - train_object[m], 2)
                if temp_sum < nearest_distance:
                    nearest_distance = temp_sum
                    nearest_label = train_object[0]
            k = k+1
        q.put([nearest_label, nearest_distance])                # Save the result
    
    def multithreading(self, dataset: list, object: list, index: int):
        number_of_threads = 4                                   # Number of threads you want
        q = Queue()                                             # Queue for saving multithreading result
        threads = []

        for i in range(number_of_threads):                      # Create threads
            t = threading.Thread(target=self.train_by_part, args=(dataset, object, index, i, q))
            t.start()
            threads.append(t)

        for thread in threads:                                  # Wait for all threads done
            thread.join()

        temp = []
        for _ in range(number_of_threads):
            temp.append(q.get())
        temp.sort(key=lambda x:x[1])                            # Find the nearest label and return it
        nearest_label = temp[0][0]
        return nearest_label

    def train(self, dataset: list, object: list, index: int):   # train(whole dataset, single point, index of this point)
        object_to_classify = object                             # Single point/row to classify
        object_len = len(object_to_classify)
        
        nearest_distance = math.inf
        nearest_label = 0
        
        for k, train_object in enumerate(dataset):
            temp_sum = 0
            if k != index:
                for m in range(1, object_len):                  # ignore the first column - label
                                                                # Euclidean Distance
                    temp_sum += pow(object_to_classify[m] - train_object[m], 2)
                temp_sum = math.sqrt(temp_sum)
                if temp_sum < nearest_distance:
                    nearest_distance = temp_sum
                    nearest_label = train_object[0]
        return nearest_label
    
    def test(self, toTest, classify):                           # test(function train(), the signle point you want to test)
        return True if toTest == classify else False
    
    def classifier(self, dataset: list, object: list, index: int):
                                                                # Normal classifier
        return self.test(self.train(dataset, object, index), object[0])    
                                                                # Multithreading classifier    
        #return self.test(self.multithreading(dataset, object, index), object[0])
    
    
        