import time
from validator import validator
import numpy as np
from plot import plot

def normalization(data: np.ndarray):
    normal_data = data
    for i in range(1, normal_data.shape[1]):
        temp = normal_data[:, i]
        normal_data[:, i] = (temp - np.average(temp)) / np.std(temp)
    return normal_data
        

def forward_selection(dataset, num_of_features):
    valid = validator()
    allData = np.array(dataset).astype(float)                   # ndarray easy for slicing
    normal_allData = normalization(allData)
    currentSet = [0]
    decreasingCount = 0                                         # use to stop searching when accuracy decreases
    highestAccuracy = 0
    '''
    class1_count = 0
    for i in range(len(dataset)):
        if float(dataset[i][0]) == float(1):
            class1_count += 1
    class2_count = len(dataset) - class1_count
    if class1_count >= class2_count:
        highestAccuracy = class1_count / len(dataset)
    else:
        highestAccuracy = class2_count / len(dataset)
    '''
    
    print("Using no features, the default rate is ", highestAccuracy, "\n")
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
                currData = normal_allData.copy()[:, slicedCol]           # slicing the data
                accuracy = valid.validation(currData.tolist())  # make sure to have tolist()
                
                # output stuff
                temp = " ".join(str(s) for s in slicedCol)
                print("        Using feature(s) {", temp[2:], "} accuracy is", accuracy)
                
                # get the local highest
                if accuracy > bsf_accuracy:
                    bsf_accuracy = accuracy
                    outputFeatures = temp
                    colToKeep = slicedCol
        currentSet = colToKeep.copy()
        print("\nFeature set {", outputFeatures[2:], "} was best, accuracy is", bsf_accuracy)
        
        if bsf_accuracy <= highestAccuracy:
            print("(Warning, Accuracy has decreased!)\n")
            decreasingCount += 1
            if decreasingCount >= num_of_features / 4:          # allows accuracy to decrease 25% of num_of_features times
                break
        else:
            highestAccuracy = bsf_accuracy                      # get the global highest
            bestFeatures = outputFeatures
    print("Finished search!! The best feature subset is {", bestFeatures[2:], "} which has an accuracy of", highestAccuracy)
    
    return bestFeatures

def backward_elimination(dataset, num_of_features):
    valid = validator()
    allData = np.array(dataset).astype(float)                   # ndarray easy for slicing
    normal_allData = normalization(allData)
    currentSet = list(range(num_of_features))                 
    decreasingCount = 0
    highestAccuracy = valid.validation(normal_allData.tolist())
    print("Using all", num_of_features-1, "features, I get an accuracy of", highestAccuracy)
    print("Beginning search.\n")
    output_features = ""
    bestFeatures = ""

    while True:
        bsf_accuracy = 0                                        
        colToKeep = []
        for i in range(1, num_of_features):
            if i in currentSet:
                slicedCol = currentSet.copy()
                if len(slicedCol) == 2:
                    break
                slicedCol.remove(i)                             # removing instead of extending
                slicedCol.sort() 
                currData = normal_allData.copy()[:, slicedCol]
                accuracy = valid.validation(currData.tolist())
                
                # output stuff
                temp = " ".join(str(s) for s in slicedCol)
                print("        Using feature(s) {", temp[2:], "} accuracy is", accuracy)
                
                if accuracy > bsf_accuracy:
                    bsf_accuracy = accuracy
                    output_features = temp
                    colToKeep = slicedCol
        currentSet = colToKeep.copy()
        print("\nFeature set {", output_features[2:], "} was best, accuracy is", bsf_accuracy)
        
        if bsf_accuracy <= highestAccuracy:
            print("(Warning, Accuracy has decreased!)\n")
            decreasingCount += 1
            if decreasingCount >= num_of_features / 4:
                break
        else:
            highestAccuracy = bsf_accuracy
            bestFeatures = output_features
    print("Finished search!! The best feature subset is {", bestFeatures[2:], "} which has an accuracy of", highestAccuracy)
    return bestFeatures


'''
The logic of this algorithm is to find the "weight" of each features (individual 
accuracy). And, using the weight ranking to eliminate the least important feature 
like the backward elimination. This algorithm significantly reduce the run time comparing
to normal backward elimination when dataset is huge. Also, since run time is reduced,
we can try using the time to run more test (increase the acceptability of having 
more reduce accuracy situations)
'''
def special_algorithm(dataset,num_of_features):
    valid = validator()
    allData = np.array(dataset).astype(float)  # ndarray easy for slicing
    normal_allData = normalization(allData)
    currentSet = [0]
    decreasingCount = 0  # use to stop searching when accuracy decreases
    highestAccuracy = 0
    output_features = ""
    bestFeatures = ""
    acc_list = np.zeros((num_of_features-1,2))
    acc_list[:, 0] = np.arange(1,num_of_features)

    for i in range(1, num_of_features):
        slicedCol = currentSet.copy()
        slicedCol.extend([i])
        slicedCol.sort()
        currData = normal_allData[:, slicedCol]
        accuracy = valid.validation(currData.tolist())
        acc_list[i-1][1] = accuracy
        
    sorted_list = np.argsort(acc_list[:,1])
    ranking = acc_list[sorted_list]
    print("\nWeight of each feature(low to high):")
    print("\nFeature   Accuracy")
    for row in ranking:
        print("{:<10} {:<10}".format(int(row[0]), row[1]))
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
        currData = normal_allData[:, slicedCol]
        accuracy = valid.validation(currData.tolist())

        temp = " ".join(str(s) for s in slicedCol)
        print("\n\nNew feature set after removing", col_remove, " {", temp[2:], "} accuracy is", accuracy)

        if accuracy > bsf_accuracy:
            bsf_accuracy = accuracy
            output_features = temp
            colToKeep = slicedCol
        currentSet = colToKeep.copy()
        print("\nPreviously, feature set {", bestFeatures[2:], "} was best, accuracy is", highestAccuracy, "\n")

        if bsf_accuracy <= highestAccuracy:
            print("(Warning, Accuracy has decreased!)\n")
            decreasingCount += 1
            if decreasingCount >= num_of_features / 2:
                break
        else:
            highestAccuracy = bsf_accuracy
            bestFeatures = output_features
    print("\nFinished search!! The best feature subset is {", bestFeatures[2:], "} which has an accuracy of", highestAccuracy)
    return bestFeatures


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
    print("5. plot")
    choice = int(input("Type the number of the algorithm you want to run: "))
    with open(data_chosen, "r") as file:
        data = []
        for row in file.readlines():  # get each line
            data.append(row.split())  # split the line and get each column value then add to data_set
    number_of_features = len(data[0])
    if choice == 1:
        start_time = time.time()
        bestFeatures = forward_selection(data, number_of_features)
        print("--- %s seconds ---" % round((time.time() - start_time), 6))
    elif choice == 2:
        start_time = time.time()
        bestFeatures = backward_elimination(data, number_of_features)
        print("--- %s seconds ---" % round((time.time() - start_time), 6))
    elif choice == 3:
        start_time = time.time()
        bestFeatures = special_algorithm(data, number_of_features)
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
    elif choice == 5:
        allData = np.array(data).astype(float)
        normal_allData = normalization(allData)
        plt = plot(normal_allData,data_chosen)
        plt.plotData()