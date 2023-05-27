import json
from sympy import symbols, Eq, solve

# Feed percent
dog_sizes = {
    'small_breed': [[0.26, 0.25, 0.26], [0.11, 0.11, 0.16], [0.9, 0.6, 0.5], [0.1, 1.1, 0.9]],
    'medium_breed': [[0.14, 0.28, 0.26], [0.5, 0.15, 0.12], [0.6, 0.4, 0.8], [0.8, 1.1, 0.7]],
    'large_breed': [[0.14, 0.28, 0.26], [0.5, 0.15, 0.12], [0.6, 0.4, 0.8], [0.8, 1.1, 0.7]]
}

def calculate_pet_food(size):
    feed_provide = 0

    # Get feed percent
    ratios = dog_sizes.get(size)

    protein_ratios = ratios[0]
    fat_ratios = ratios[1]
    calcium_ratios = ratios[2]
    phosphorus_ratios = ratios[3]

    # check breeds size
    if size == 'small_breed':
        feed_provide = 70
    elif size == 'medium_breed':
        feed_provide = 250
    else:
        feed_provide = 400

    x, y, z = symbols('x y z')
    # Equations
    protein_total_ratio = Eq((protein_ratios[0]*x + protein_ratios[1]*y + protein_ratios[2]*z), 0.26*feed_provide)
    fat_total_ratio = Eq((fat_ratios[0]*x + fat_ratios[1]*y + fat_ratios[2]*z), 0.13*(x + y + z))
    calcium_per_phosphorus = Eq((calcium_ratios[0]*x + calcium_ratios[1]*y + calcium_ratios[2]*z) / (phosphorus_ratios[0]*x + phosphorus_ratios[1]*y + phosphorus_ratios[2]*z), 1)

    # Solve the equations
    solution = solve((protein_total_ratio, fat_total_ratio, calcium_per_phosphorus), (x, y, z))

    return solution

def calculate_protein_ratio(size, solution):
    x, y, z = symbols('x y z')
    feed_a_amount = solution[x]
    feed_b_amount = solution[y]
    feed_c_amount = solution[z]

    # Total amount
    total_amount = feed_a_amount + feed_b_amount + feed_c_amount

    # Protein ratio of each feed
    protein_ratios = dog_sizes[size][0]
    feed_a_protein_ratio = (protein_ratios[0] * feed_a_amount) / total_amount
    feed_b_protein_ratio = (protein_ratios[1] * feed_b_amount) / total_amount
    feed_c_protein_ratio = (protein_ratios[2] * feed_c_amount) / total_amount

    # Total protein ratio
    total_protein_ratio = feed_a_protein_ratio + feed_b_protein_ratio + feed_c_protein_ratio

    return total_protein_ratio

def calculate_fat_ratio(size, solution):
    x, y, z = symbols('x y z')
    feed_a_amount = solution[x]
    feed_b_amount = solution[y]
    feed_c_amount = solution[z]

    # Total amount
    total_amount = feed_a_amount + feed_b_amount + feed_c_amount

    # Fat ratio of each feed
    fat_ratios = dog_sizes[size][1]
    feed_a_fat_ratio = (fat_ratios[0] * feed_a_amount) / total_amount
    feed_b_fat_ratio = (fat_ratios[1] * feed_b_amount) / total_amount
    feed_c_fat_ratio = (fat_ratios[2] * feed_c_amount) / total_amount

    # Total fat ratio
    total_fat_ratio = feed_a_fat_ratio + feed_b_fat_ratio + feed_c_fat_ratio

    return total_fat_ratio

def calculate_calories(size, solution):
    x, y, z = symbols('x y z')
    feed_a_amount = solution[x]
    feed_b_amount = solution[y]
    feed_c_amount = solution[z]

    # Calculate calories
    protein_ratios = dog_sizes[size][0]
    fat_ratios = dog_sizes[size][1]
    calories = 4 * (protein_ratios[0]*feed_a_amount + protein_ratios[1]*feed_b_amount + protein_ratios[2]*feed_c_amount) + 9 * (fat_ratios[0]*feed_a_amount + fat_ratios[1]*feed_b_amount + fat_ratios[2]*feed_c_amount)

    return calories

def get_breed_list(breed):
    with open('CalculatePetFood/Breed.json', 'r') as file:
        data = json.load(file)
        
    breed_size = None
    
    for size, breed_list in data['Dog_Breed_List'].items():
        if breed in breed_list:
            breed_size = size
            break
    
    return breed_size

def main(breed):
    breed_size = get_breed_list(breed)
    x, y, z = symbols('x y z')

    if breed_size:
        solution = calculate_pet_food(breed_size)
        if solution:
            total_protein_ratio = calculate_protein_ratio(breed_size, solution)
            total_fat_ratio = calculate_fat_ratio(breed_size, solution)
            total_calories = calculate_calories(breed_size, solution)

            print("Breed:", breed)
            # print("Size:", breed_size)
            print("Feed A amount:", round(solution[x]), "g")
            print("Feed B amount:", round(solution[y]), "g")
            print("Feed C amount:", round(solution[z]), "g")
            print("Total Feed amount:", round(solution[x] + solution[y] + solution[z]), "g")
            print("Total Protein ratio: {:.2f}%".format(total_protein_ratio * 100))
            print("Total Fat ratio: {:.2f}%".format(total_fat_ratio * 100))
            print("Total Calories:", round(total_calories), "kcal")
          
    else:
        print("Breed not found.")

if __name__ == "__main__":
    main()