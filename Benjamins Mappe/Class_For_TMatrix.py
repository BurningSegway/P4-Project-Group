import numpy as np

A = [[1, 0, 0, 3],
     [0, 1, 0, 3],
     [0, 0, 1, 3],
     [0, 0, 0, 1]]

class HomogeneousTransform:
  def __init__(self, Rotation, Translation, Scale):
    self.Rotation = Rotation
    self.Translation = Translation
    self.Scale = Scale
    self.HMatrix=[[self.Rotation(1,1), self.Rotation(1,2), self.Rotation(1,3), self.Translation(1,1) ],
                  [self.Rotation(2,1), self.Rotation(2,2), self.Rotation(2,3), self.Translation(2,1) ],
                  [self.Rotation(3,1), self.Rotation(3,2), self.Rotation(3,3), self.Translation(3,1) ],
                  [self.Scale(1,1),    self.Scale(1,2),    self.Scale(1,3),    self.Scale(1,4)       ]]

  def Multiply_By(a, self):
    return np.dot(a, self.HMatrix)

  def Get_Transpose(self):
    return np.linalg.inverse(self.HMatrix)
  
  def P_print(Rotation, Translation):
    return 1

    






