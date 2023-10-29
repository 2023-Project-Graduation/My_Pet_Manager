exec(open("./DogDetection/DogDetection.py").read())

from BreedClassification import BreedClassification
from CalculatePetFood import CalculatePetFood
# from DogDetection import DogDetection

breed = BreedClassification.main()

solution = CalculatePetFood.main(breed)
