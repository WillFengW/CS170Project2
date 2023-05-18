import random

def forward_selection(num_of_features):
    currentSet = []
    highestAccuracy = 0
    decreasingCount = 0  # use to stop searching when accuracy decreases
    accuracy = leaveOutCrossValidation(currentSet, 1)
    print("Using no features and \"random\" evaluation, I get an accuracy of ", accuracy, "%\n")
    print("Beginning search.\n")
    outputFeatures = ""   # use to output current features set, may delete in part II
    bestFeatures = ""     # use to output current features set, may delete in part II
    for i in range(num_of_features):
        add_feature_on_level = 0
        bsf_accuracy = 0
        for k in range(1, num_of_features + 1):
            temp = ""  # use to trace output only, may delete in part II
            if k not in currentSet:
                accuracy = leaveOutCrossValidation(currentSet, k)
                temp = str(k)
                for j in range(len(currentSet)):
                    temp = temp + "," + str(currentSet[j])
                print("        Using feature(s) {", temp,"} accuracy is", accuracy, "%")
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
            if decreasingCount >= num_of_features/4:  # allows accuracy to decrease 25% of num_of_features times
                break
        else:
            highestAccuracy = bsf_accuracy
            bestFeatures = outputFeatures
    print("Finished search!! The best feature subset is {", bestFeatures, "} which has an accuracy of", highestAccuracy, "%")

def backward_elimination(num_of_features):
    return

def special_algorithm(num_of_features):
    return

def leaveOutCrossValidation(currentSet, k):
    return round(random.uniform(0, 100), 1)


# Main program
print("Welcome to Team 22's Feature Selection Algorithm.")
num_of_features = int(input("Please enter the total number of features: "))
print("1. Forward Selection")
print("2. Backward Elimination")
print("3. Team 22’s Special Algorithm")
choice = int(input("Type the number of the algorithm you want to run: "))
if choice == 1:
    forward_selection(num_of_features)
elif choice == 2:
    backward_elimination(num_of_features)
elif choice == 3:
    special_algorithm(num_of_features)
