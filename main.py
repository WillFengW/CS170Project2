import time
from validator import validator
import numpy as np


def forward_selection(dataset, num_of_features):
    valid = validator()
    allData = np.array(dataset)                                 # ndarray easy for slicing
    currentSet = [0]
    decreasingCount = 0                                         # use to stop searching when accuracy decreases
    highestAccuracy = 0
    print("Using no features, I get an accuracy of ", highestAccuracy, "%\n")
    print("Beginning search.\n")
    outputFeatures = ""
    bestFeatures = ""
    
    while True:
        bsf_accuracy = 0
        colToKeep = []
        for i in range(1, num_of_features):                     # ignore the first column
            if i not in currentSet:                             # ignore itself
                slicedCol = currentSet.copy()
                slicedCol.extend([i])
                slicedCol.sort()                                # sort only for output format         
                currData = allData[:, slicedCol]                # slicing the data
                accuracy = valid.validation(currData.tolist())  # make sure to have tolist()
                
                # output stuff
                temp = str(slicedCol[1])
                if len(slicedCol) > 2:
                    for j in range(2, len(slicedCol)):
                        temp = temp + "," + str(slicedCol[j])
                print("        Using feature(s) {", temp, "} accuracy is", accuracy, "%")
                
                # get the local highest
                if accuracy > bsf_accuracy:
                    bsf_accuracy = accuracy
                    outputFeatures = temp
                    colToKeep = slicedCol
        currentSet = colToKeep.copy()
        print("\nFeature set {", outputFeatures, "} was best, accuracy is", bsf_accuracy, "%\n")
        
        if bsf_accuracy <= highestAccuracy:
            print("(Warning, Accuracy has decreased!)\n")
            decreasingCount += 1
            if decreasingCount >= num_of_features / 4:          # allows accuracy to decrease 25% of num_of_features times
                break
        else:
            highestAccuracy = bsf_accuracy                      # get the global highest
            bestFeatures = outputFeatures
    print("Finished search!! The best feature subset is {", bestFeatures, "} which has an accuracy of", highestAccuracy,
          "%")

def backward_elimination(dataset, num_of_features):
    valid = validator()
    allData = np.array(dataset)
    currentSet = list(range(num_of_features))                   
    decreasingCount = 0
    highestAccuracy = valid.validation(dataset)
    print("Using all", num_of_features-1, "features, I get an accuracy of", highestAccuracy, "%\n")
    print("Beginning search.\n")
    output_features = ""
    bestFeatures = ""

    while True:
        bsf_accuracy = 0                                        
        colToKeep = []
        for i in range(1, num_of_features):
            if i in currentSet:
                slicedCol = currentSet.copy()
                slicedCol.remove(i)                             # removing instead of extending
                slicedCol.sort() 
                currData = allData[:, slicedCol]
                accuracy = valid.validation(currData.tolist())
                
                temp = str(slicedCol[1])
                if len(slicedCol) > 2:
                    for j in range(2, len(slicedCol)):
                        temp = temp + "," + str(slicedCol[j])
                print("        Feature set after removing", i, " {", temp, "} accuracy is", accuracy, "%")
                
                if accuracy > bsf_accuracy:
                    bsf_accuracy = accuracy
                    output_features = temp
                    colToKeep = slicedCol
        currentSet = colToKeep.copy()
        print("\nFeature set {", output_features, "} was best, accuracy is", bsf_accuracy, "%\n")
        
        if bsf_accuracy <= highestAccuracy:
            print("(Warning, Accuracy has decreased!)\n")
            decreasingCount += 1
            if decreasingCount >= num_of_features / 4:
                break
        else:
            highestAccuracy = bsf_accuracy
            bestFeatures = output_features
    print("Finished search!! The best feature subset is {", bestFeatures, "} which has an accuracy of", highestAccuracy,
          "%")

def special_algorithm(dataset,num_of_features):
    valid = validator()
    allData = np.array(dataset)  # ndarray easy for slicing
    currentSet = [0]
    decreasingCount = 0  # use to stop searching when accuracy decreases
    highestAccuracy = 0
    outputFeatures = ""
    bestFeatures = ""
    acc_list = np.zeros((num_of_features-1,2))
    acc_list[:, 0] = np.arange(1,num_of_features)
    counter = 0
    for i in range(1, num_of_features):
        slicedCol = currentSet.copy()
        slicedCol.extend([i])
        slicedCol.sort()
        currData = allData[:, slicedCol]
        accuracy = valid.validation(currData.tolist())
        acc_list[counter][1] = accuracy
        counter += 1
    sorted_list = np.argsort(acc_list[:,1])
    ranking = acc_list[sorted_list]
    print(ranking)
    currentSet = list(range(num_of_features))
    while True:
        bsf_accuracy = 0
        colToKeep = []
        slicedCol = currentSet.copy()
        col_remove = int(ranking[0][0])
        ranking = ranking[1:]
        if len(slicedCol) == 2:
            break
        else:
            slicedCol.remove(col_remove)  # removing instead of extending
        slicedCol.sort()
        currData = allData[:, slicedCol]
        accuracy = valid.validation(currData.tolist())

        temp = str(slicedCol[1])
        if len(slicedCol) > 2:
            for j in range(2, len(slicedCol)):
                temp = temp + "," + str(slicedCol[j])
        print("\n\nNew feature set after removing", col_remove, " {", temp, "} accuracy is", accuracy, "%")

        if accuracy > bsf_accuracy:
            bsf_accuracy = accuracy
            output_features = temp
            colToKeep = slicedCol
        currentSet = colToKeep.copy()
        print("\nPreviously, feature set {", bestFeatures, "} was best, accuracy is", highestAccuracy, "%\n")

        if bsf_accuracy <= highestAccuracy:
            print("(Warning, Accuracy has decreased!)\n")
            decreasingCount += 1
            if decreasingCount >= num_of_features / 2:
                break
        else:
            highestAccuracy = bsf_accuracy
            bestFeatures = output_features
    print("Finished search!! The best feature subset is {", bestFeatures, "} which has an accuracy of", highestAccuracy,
          "%")

if __name__ == "__main__":
    print("Welcome to Team 22's Feature Selection Algorithm.")
    print("Please choose the data set: ")
    print("1, Initial Small")
    print("2, Initial Large")
    print("3, Personal Small")
    print("4, Persobal Large")
    choice = int(input("Type the number of the data set you want to run: "))
    if choice == 1:
        data_chosen = "small-test-dataset.txt"
    elif choice == 2:
        data_chosen = "large-test-dataset.txt"
    elif choice == 3:
        data_chosen = "CS170_Spring_2023_Small_data__22.txt"
    elif choice == 4:
        data_chosen = "CS170_Spring_2023_Large_data__22.txt"
    
    print("\n1. Forward Selection")
    print("2. Backward Elimination")
    print("3. Team 22's Special Algorithm")
    print("4. Check Nearest-Neighbor Accuracy (part 2)")
    choice = int(input("Type the number of the algorithm you want to run: "))
    with open(data_chosen, "r") as file:
        data = []
        for row in file.readlines():  # get each line
            data.append(row.split())  # split the line and get each column value then add to data_set
    number_of_features = len(data[0])
    if choice == 1:
        start_time = time.time()
        forward_selection(data, number_of_features)
        print("--- %s seconds ---" % round((time.time() - start_time), 6))
    elif choice == 2:
        start_time = time.time()
        backward_elimination(data, number_of_features)
        print("--- %s seconds ---" % round((time.time() - start_time), 6))
    elif choice == 3:
        start_time = time.time()
        special_algorithm(data, number_of_features)
        print("--- %s seconds ---" % round((time.time() - start_time), 6))
    elif choice == 4:
        print("\n1. Small-data-set")
        print("2. Small-data-set (only features 3,5,7)")
        print("3. large-data-set")
        print("4. large-data-set (only features 1,15,27)")
        choice = int(input("Type which data set you want to run: "))
        valid = validator()
        
        if choice == 1:
             with open("small-test-dataset.txt", "r") as file:
                data_set = []
                for row in file.readlines():
                    column = row.split()
                    data_set.append(column)
        elif choice == 2:
            with open("small-test-dataset.txt", "r") as file:
                data_set = []
                for row in file.readlines():            
                    column = row.split()
                    column_to_add = [column[0],column[3],column[5],column[7]]
                    data_set.append(column_to_add)      
        elif choice == 3:
            with open("large-test-dataset.txt", "r") as file:
                data_set = []
                for row in file.readlines():
                    column = row.split()
                    data_set.append(column)
        elif choice == 4:
            with open("large-test-dataset.txt", "r") as file:
                data_set = []
                for row in file.readlines():
                    column = row.split()
                    column_to_add = [column[0], column[1], column[15], column[27]]
                    data_set.append(column_to_add)
        
        start_time = time.time()
        print("Accuracy for the dataset is ", round(valid.validation(data_set), 3))
        print("--- %s seconds ---" % round((time.time() - start_time), 6))