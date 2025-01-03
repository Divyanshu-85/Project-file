def split_text_file(input_file):
    try:
        # Open the input file for reading
        with open(input_file, "r") as file:
            lines = file.readlines()

        # Initialize lists for categories
        alphabets = []
        numbers = []
        combinations = []

        # Categorize lines
        for line in lines:
            content = line.strip()  # Remove extra spaces and newline characters
            if content.isalpha():
                alphabets.append(content)
            elif content.isdigit():
                numbers.append(content)
            elif any(c.isdigit() for c in content) and any(c.isalpha() for c in content):
                combinations.append(content)

        # Write to separate files
        with open("alphabets.txt", "w") as file:
            file.write("\n".join(alphabets))

        with open("numbers.txt", "w") as file:
            file.write("\n".join(numbers))

        with open("combinations.txt", "w") as file:
            file.write("\n".join(combinations))

        print("File splitting completed!")
        print("Generated files: alphabets.txt, numbers.txt, combinations.txt")
    except FileNotFoundError:
        print(f"Error: The file '{input_file}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    input_file = input("Enter the name of the text file (e.g., input.txt): ").strip()
    split_text_file(input_file)
