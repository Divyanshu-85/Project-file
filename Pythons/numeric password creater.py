from itertools import product

def generate_combinations():
    try:
        user_input = input("Enter a number:- ")
        # folder_name = input("enter file name:- ")
        if not user_input.isdigit():
            print("Invalid input. Please enter digits only.")
            return

        digits = list(user_input)
        length = int(input("Enter the length of combinations: "))
        folder_name = input("enter file name:- ")
        total_combinations = len(digits) ** length
        print(f"Generating {total_combinations} combinations...")

        file_name = folder_name
        with open(file_name, "w") as file:
            for i, combination in enumerate(product(digits, repeat=length), 1):
                file.write(''.join(combination) + '\n')
                if i % (total_combinations // 10) == 0:  # Update every 10%
                    print(f"Progress: {int(i / total_combinations * 100)}%")

        print(f"Generation complete. Results saved to '{file_name}'.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    generate_combinations()
