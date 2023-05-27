#exec(open("./DogDetection/DogDetection.py").read())

from BreedClassification import BreedClassification
from CalculatePetFood import CalculatePetFood

breed = BreedClassification.main()

solution = CalculatePetFood.main(breed)
