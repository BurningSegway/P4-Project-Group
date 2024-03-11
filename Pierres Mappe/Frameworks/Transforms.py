import numpy as np

class HomogeneousTransform:
    def __init__(self, transform):
        self.Transform = transform
        print("New transform: \n" + str(self.Transform))
       
    def multiply(self, TF1, TF2):
        self.Transform = np.matmul(TF1, TF2)
        print("Multiplied transforms results in: \n" + str(self.Transform))
    
    def transpose(self, TF):
        self.Transform = np.linalg.inv(TF)
        print("The inverse: \n" + str(self.Transform))


a = np.array([[0.866, -0.5, 0, 10], [0.5, 0.866, 0, 5], [0, 0, 1, 0], [0, 0, 0, 1]])
b = np.array([[0.866, -0.5, 0, 4], [0.5, 0.866, 0 , 3], [0, 0, 1, 0], [0, 0, 0, 1]])
c = np.array([[0.933, 0.067, 0.354, 0], [0.067, 0.933, -0.354, 0], [-0.354, 0.354, 0.866, 0], [0, 0, 0, 1]])

TF1 = HomogeneousTransform(a)
TF2 = HomogeneousTransform(b)
TF3 = HomogeneousTransform(c)

TF4 = HomogeneousTransform.multiply(HomogeneousTransform(0), TF1.Transform, TF2.Transform)
TF5 = HomogeneousTransform.transpose(HomogeneousTransform(0), TF1.Transform)
