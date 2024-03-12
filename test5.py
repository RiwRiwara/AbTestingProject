try:
    print(" *** File Processing #2 ***\n")
    file_name = input("Enter file name and word : ")
    file_name, word = file_name.split()

    with open(file_name, 'r') as file:
        lines = file.readlines()
        words = [line.split() for line in lines]
        words = [word for sublist in words for word in sublist]
        word_length = [len(word) for word in words if word == word]
        word_length = [str(length) for length in word_length]
        print()
        print(f"There are {len(word_length)} words in the file {file_name}")
        print(f"Found {words.count(word)} '{word}' words")
    
    
except FileNotFoundError:
    print("Error: Can not open file =>", file_name)
