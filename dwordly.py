import json

# Wczytanie słownika z pliku JSON
with open("dictionary.json", "r", encoding="utf-8") as file:
    words = json.load(file)

# Przygotowanie słownika z zestawami słów dla każdej długości słowa
words_by_length = {length: set() for length in range(1, max(len(word) for word in words) + 1)}

for word in words:
    word = word.strip().upper()
    words_by_length[len(word)].add(word)

# Funkcja sprawdzająca, czy słowo jest ważne
def is_valid_word_optimized(word):
    return word.upper() in words_by_length[len(word)]

def get_neighbors(word):
    """Generate all possible words by removing one letter or changing exactly one letter."""
    neighbors = set()
    
    # Generate words by removing one letter
    for i in range(len(word)):
        neighbors.add(word[:i] + word[i+1:])
        
    # Generate words by changing exactly one letter
    for i in range(len(word)):
        for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            if letter != word[i]:
                neighbors.add(word[:i] + letter + word[i+1:])
                
    return neighbors

def generate_valid_neighbors_optimized(word):
    return [neighbor for neighbor in get_neighbors(word) if is_valid_word_optimized(neighbor)]

def find_path_to_one_letter_word(start_word):
    from collections import deque
    queue = deque([(start_word, [start_word])])
    visited = set([start_word])
    
    while queue:
        current_word, path = queue.popleft()
        if len(current_word) == 1 and current_word in ['A', 'I']:
            return path 
        
        for neighbor in generate_valid_neighbors_optimized(current_word):
            if neighbor not in visited:
                visited.add(neighbor)
                new_path = path + [neighbor]
                
                # Check if the new path is valid (to avoid wrong shortcuts)
                if len(neighbor) == 1 and neighbor in ['A', 'I']:
                    return new_path
                
                queue.append((neighbor, new_path))
    
    return None

# Testowanie funkcji na przykładowym słowie
example_word = "REELER"
path_optimized = find_path_to_one_letter_word(example_word)
print(path_optimized)
