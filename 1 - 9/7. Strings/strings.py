# -----------------------------
# STRING CREATION
# -----------------------------
print("STRING CREATION:")
text1: str = "Hello"
text2: str = 'World'
text3: str = """This is
a multi-line
string."""
print(text1)
print(text2)
print(text3)
print()

# -----------------------------
# CONCATENATION AND REPETITION
# -----------------------------
print("CONCATENATION AND REPETITION:")
greeting: str = text1 + " " + text2  # joining strings
print(greeting)

echo: str = "Hi! " * 3  # repetition
print(echo)
print()

# -----------------------------
# STRING INDEXING AND SLICING
# -----------------------------
print("INDEXING AND SLICING:")
word: str = "Python"
print("word =", word)
print("First character:", word[0])
print("Last character:", word[-1])
print("Substring [0:4]:", word[0:4])  # Pyto
print("Substring [2:]:", word[2:])   # thon
print("Substring [:3]:", word[:3])   # Pyt
print("Every second letter:", word[::2])  # Pto
print("Reversed string:", word[::-1])
print()

# -----------------------------
# STRING ITERATION
# -----------------------------
print("ITERATING OVER STRING:")
for char in word:
    print(char, end=" ")
print("\n")

# -----------------------------
# STRING METHODS
# -----------------------------
print("STRING METHODS:")
message: str = "  Python is FUN!  "
print("Original:", repr(message))
print("Lowercase:", message.lower())
print("Uppercase:", message.upper())
print("Title case:", message.title())
print("Swap case:", message.swapcase())
print("Strip spaces:", message.strip())
print("Replace:", message.replace("FUN", "powerful"))
print("Starts with 'Py':", message.startswith("Py"))
print("Ends with '!':", message.endswith("!"))
print("Count of 'n':", message.count("n"))
print("Find 'is':", message.find("is"))
print()

# -----------------------------
# STRING SPLITTING AND JOINING
# -----------------------------
print("SPLIT AND JOIN:")
sentence: str = "Python is easy to learn"
words: list[str] = sentence.split()  # split by spaces
print("Words list:", words)
joined: str = "-".join(words)
print("Joined with '-':", joined)
print()

# -----------------------------
# ESCAPE CHARACTERS
# -----------------------------
print("ESCAPE CHARACTERS:")
print("Line1\nLine2\nLine3")  # new line
print("Tabbed\ttext")
print("He said: \"Python is great!\"")
print("Backslash: \\")
print()

# -----------------------------
# STRING FORMATTING
# -----------------------------
print("STRING FORMATTING:")
name: str = "Alice"
age: int = 25
score: float = 93.4567

# Using f-string
print(f"Name: {name}, Age: {age}, Score: {score:.2f}")

# Using format()
print("Name: {}, Age: {}, Score: {:.2f}".format(name, age, score))

# Using concatenation
print("Name: " + name + ", Age: " + str(age))
print()

# -----------------------------
# CHECKING CONTENT (IS METHODS)
# -----------------------------
print("CHECKING CONTENT:")
sample: str = "Python3"
print("Is alphabetic?", sample.isalpha())  # False (because of '3')
print("Is alphanumeric?", sample.isalnum())  # True
print("Is digit?", sample.isdigit())
print("Is lowercase?", sample.islower())
print("Is uppercase?", sample.isupper())
print("Is space only?", "   ".isspace())
print()

# -----------------------------
# STRING LENGTH
# -----------------------------
print("STRING LENGTH:")
print("Length of 'Python' =", len("Python"))
print()

# -----------------------------
# STRING COMPARISON
# -----------------------------
print("STRING COMPARISON:")
a: str = "apple"
b: str = "banana"
print("a == b:", a == b)
print("a != b:", a != b)
print("a < b:", a < b)   # alphabetically before
print("a > b:", a > b)
print()

# -----------------------------
# MULTILINE STRINGS AND RAW STRINGS
# -----------------------------
print("MULTILINE AND RAW STRINGS:")
multiline: str = """Line one
Line two
Line three"""
print(multiline)

# Raw string keeps escape characters as-is
path: str = r"C:\Users\Alice\Documents\Python"
print("Raw string example:", path)
print()

# -----------------------------
# PRACTICAL EXAMPLES
# -----------------------------
print("PRACTICAL EXAMPLES:")

# Count vowels in a string
text: str = input("Enter a word to count vowels: ").lower()
vowels: str = "aeiou"
count: int = 0
for ch in text:
    if ch in vowels:
        count += 1
print(f"Number of vowels in '{text}' = {count}")
print()

# Palindrome check
word = input("Enter a word to check palindrome: ").lower()
if word == word[::-1]:
    print(f"'{word}' is a palindrome.")
else:
    print(f"'{word}' is not a palindrome.")
print()
