import matplotlib.pyplot as plt
import numpy as np


class plot():
    def __init__(self, dataset: list, dataTitle: str) -> None:
        self.dataset = dataset.copy()
        self.dataTitle = dataTitle
    
    def plotData(self):
        x = int(input("What's the first feature you want to plot? "))
        y = int(input("What's the second feature you want to plot? "))
        
        x_data = np.array(self.dataset[:,x])
        y_data = np.array(self.dataset[:,y])
        print(x_data.shape)
        
        col = []
        for i in range(len(self.dataset)):
            if self.dataset[i][0] == 2.0 :
                col.append('b')
            else:
                col.append('r')
            
        for i in range(len(x_data)):
            plt.scatter(x_data[i], y_data[i], c = col[i], s = 10,
                        linewidth = 0)
        #plt.plot(x_data, y_data, color = col, marker = '.')
        plt.xlabel("Feature: " + str(x))
        plt.ylabel("Feature: " + str(y))
        plt.title(self.dataTitle)
        plt.show()
        
        