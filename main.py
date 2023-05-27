exec(open("DogDetection.py").read())

import BreedClassification
import CalculatePetFood

breed = BreedClassification.main()

solution = CalculatePetFood.main(breed)
