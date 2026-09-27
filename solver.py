def check_word(guess, result, candidate):
    """تحليل نتيجة WOTD مثل Wordle."""
    if len(guess) != len(candidate):
        return False

    # الأخضر
    for i, color in enumerate(result):
        if color == "🟩" and candidate[i] != guess[i]:
            return False

    # الأصفر
    for i, color in enumerate(result):
        if color == "🟨":
            if guess[i] not in candidate:
                return False
            if candidate[i] == guess[i]:
                return False

    # الرمادي
    for i, color in enumerate(result):
        if color == "⬛" and guess[i] in candidate:
            return False

    return True


def find_words(guess, result, words):
    return [
        word for word in words
        if check_word(guess.lower(), result, word.lower())
    ]
