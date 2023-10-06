def diff_words(first, second):
    if first == second:
        return []
    
    common_length = min(len(first), len(second))
    
    # jeśli słowa są różnej długości
    if len(first) != len(second):
        for i in range(common_length + 1):
            if first[i:] == second[i + 1:]:
                return ["remove", i, second[i]]
            elif first[i + 1:] == second[i:]:
                return ["remove", i, first[i]]
    
    # jeśli słowa mają taką samą długość
    for i, (f_char, s_char) in enumerate(zip(first, second)):
        if f_char != s_char:
            return ["change", i, s_char]
    
    return []