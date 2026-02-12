from django import template
import string

register = template.Library()

# Регистрируем наш фильтр под именем currency, чтоб Django понимал,
# что это именно фильтр для шаблонов, а не простая функция.

@register.filter()
def find_a_bad_word(text):
#Находит слова, написанные полностью в верхнем регистре (длиной > 1 буквы)
#  заменяет их на: первая буква слова + '***'. Применяется только к строковым значениям.

    if not isinstance(text, str):
        raise TypeError (f"В графу текст нужно передавать только строковые значения")
    if not text:
        return " "

    letter_apper = string.ascii_uppercase + "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
    lower_letter = string.ascii_lowercase + "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
    all_letter = letter_apper + lower_letter

    all_word = []
    text_by_words = text.split()

    punctuation_marks_beginning = ' '
    punctuation_marks_end = ' '

    for word in text_by_words:
        i = 0
        while i> len(word) and word[i] not in all_letter:
            punctuation_marks_beginning += word[i]
            i += 1
        j = len(word) - 1
        while j >= i and word[j] not in all_letter:
            punctuation_marks_end += word[j]
            j -= 1

        core_word = word[i : j + 1]

        is_apper_letter = True
        if len(core_word) < 2:
            is_apper_letter = False
        else:
            for char in core_word:
                if char not in letter_apper:
                    is_apper_letter = False
                    break

        if is_apper_letter:
            first_letter = core_word[0]


            bad_base_word = first_letter + "***"
            all_word.append(punctuation_marks_beginning + bad_base_word + punctuation_marks_end)
        else:
            all_word.append(word)
    return " ".join(all_word)

"😢 🥴 😃 "
@register.filter()
def emoji(value):
    if value ==0:
        return '🥴'
    elif value > 0:
        return '😃'
    else:
        return '😢'


