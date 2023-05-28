import math
import random


def forward_selection(dataset, num_of_features):
    currentSet = []
    decreasingCount = 0  # use to stop searching when accuracy decreases
    highestAccuracy = 0
    print("Using no features and \"random\" evaluation, I get an accuracy of ", highestAccuracy, "%\n")
    print("Beginning search.\n")
    outputFeatures = ""  # use to output current features set, may delete in part II
    bestFeatures = ""  # use to output current features set, may delete in part II
    for i in range(num_of_features):
        add_feature_on_level = 0
        bsf_accuracy = 0
        for k in range(1, num_of_features + 1):
            temp = ""  # use to trace output only, may delete in part II
            if k not in currentSet:
                accuracy = leaveOutCrossValidation(dataset, currentSet, k)
                temp = str(k)
                for j in range(len(currentSet)):
                    temp = temp + "," + str(currentSet[j])
                print("        Using feature(s) {", temp, "} accuracy is", accuracy, "%")
                if accuracy > bsf_accuracy:
                    bsf_accuracy = accuracy
                    add_feature_on_level = k
                    outputFeatures = temp
        currentSet.insert(0, add_feature_on_level)
        str(add_feature_on_level) + "," + outputFeatures
        print("\nFeature set {", outputFeatures, "} was best, accuracy is", bsf_accuracy, "%\n")
        if bsf_accuracy <= highestAccuracy:
            print("(Warning, Accuracy has decreased!)\n")
            decreasingCount += 1
            if decreasingCount >= num_of_features / 4:  # allows accuracy to decrease 25% of num_of_features times
                break
        else:
            highestAccuracy = bsf_accuracy
            bestFeatures = outputFeatures
    print("Finished search!! The best feature subset is {", bestFeatures, "} which has an accuracy of", highestAccuracy,
          "%")


def backward_elimination(dataset, num_of_features):
    decreasingCount = 0
    current_set = list(range(1, num_of_features + 1))
    highest_accuracy = leaveOutCrossValidation(dataset, current_set, 1)
    print("Using all", num_of_features, "features, I get an accuracy of", highest_accuracy, "%\n")
    print("Beginning search.\n")
    output_features = ", ".join(str(feature) for feature in current_set)
    for i in range(num_of_features - 1, 0, -1):
        remove_feature_on_level = 0
        bsf_accuracy = 0
        temp = ""
        for k in current_set:
            current_set_copy = current_set.copy()
            current_set_copy.remove(k)
            accuracy = leaveOutCrossValidation(dataset, current_set_copy, k)
            temp = ", ".join(str(feature) for feature in current_set_copy)
            print("        Feature set after removing", k, " {", temp, "} accuracy is", accuracy, "%")
            if accuracy > bsf_accuracy:
                bsf_accuracy = accuracy
                remove_feature_on_level = k
                output_features = temp
        current_set.remove(remove_feature_on_level)
        print("\nFeature set {", output_features, "} was best, accuracy is", bsf_accuracy, "%\n")
        if bsf_accuracy <= highest_accuracy:
            print("(Warning, Accuracy has decreased!)\n")
            decreasingCount += 1
            if decreasingCount >= num_of_features / 4:  # allows accuracy to decrease 1/4 of num_of_features times
                break
        else:
            highest_accuracy = bsf_accuracy
            best_features = output_features

    print("Finished search!! The best feature subset is {", best_features, "} which has an accuracy of",
          highest_accuracy, "%")


def special_algorithm(dataset):
    return


def leaveOutCrossValidation(dataset, current_set, feature_to_add):
    return round(random.uniform(0, 100), 1)


def nearest_neighbor_classifier(dataset):
    number_correctly_classified = 0

    for i in range(len(dataset)):                   # len(dataset) = number of rows
        object_to_classify = dataset[i][0:]         # the object means the whole row in dataset
        label_object_to_classify = dataset[i][0]
        nearest_distance = math.inf
        nearest_location = math.inf
        nearest_label = 0

        for k in range(len(dataset)):
            temp_sum = 0
            if k != i:
                for m in range(1, len(object_to_classify)):         # not include comparison with class label
                    #sum up (each feature (index: m) in classify object minus the kth object)^2
                    temp_sum += pow(float(object_to_classify[m]) - float(dataset[k][m]), 2)
                distance = math.sqrt(temp_sum)
                if distance < nearest_distance:
                    nearest_distance = distance
                    nearest_location = k
                    nearest_label = dataset[k][0]
        print("Object ", i+1, " is class ", int(float(label_object_to_classify)))
        print("Its nearest_neighbor is ", nearest_location+1, " which is in class ", int(float(nearest_label)))

        if label_object_to_classify == nearest_label:
            number_correctly_classified += 1

    accuracy = number_correctly_classified / len(dataset)
    return accuracy


# Main
print("Welcome to Team 22's Feature Selection Algorithm.")
print("1. Forward Selection")
print("2. Backward Elimination")
print("3. Team 22’s Special Algorithm")
print("4. Check Nearest-Neighbor Accuracy")
choice = int(input("Type the number of the algorithm you want to run: "))
correct_count = 0
with open("small-test-dataset.txt", "r") as file:
    data = []
    for row in file.readlines():  # get each line
        data.append(row.split())  # split the line and get each column value then add to data_set
number_of_features = len(data[0]) - 1
if choice == 1:
    forward_selection(data, number_of_features)
elif choice == 2:
    backward_elimination(data, number_of_features)
elif choice == 3:
    special_algorithm(data)
elif choice == 4:
    with open("small-test-dataset.txt", "r") as file:
        data_set = []
        for row in file.readlines():            # get each line
            column = row.split()
            column_to_add = [column[0], column[3], column[5], column[7]]
            data_set.append(column_to_add)        # split the line and get each column value then add to data_set
    print("Accuracy for the small dataset is ", round(nearest_neighbor_classifier(data_set), 3))
    with open("large-test-dataset.txt", "r") as file:
        data_set = []
        for row in file.readlines():            # get each line
            column = row.split()
            column_to_add = [column[0], column[1], column[15], column[27]]
            data_set.append(column_to_add)        # split the line and get each column value then add to data_set
    print("Accuracy for the large dataset is ", round(nearest_neighbor_classifier(data_set), 3))
