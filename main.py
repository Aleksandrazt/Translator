import requests
import os.path
import sys

from bs4 import BeautifulSoup

LANGUAGES = {'1': 'arabic', '2': 'german', '3': 'english', '4': 'spanish', '5': 'french', '6': 'hebrew',
             '7': 'japanese', '8': 'dutch', '9': 'polish', '10': 'portuguese', '11': 'romanian', '12': 'russian',
             '13': 'turkish'}


def connection(url):
    user_agent = 'Mozilla/5.0'
    try:
        response = requests.get(url, headers={'User-Agent': user_agent})
    except requests.exceptions.ConnectionError:
        print('Something wrong with your internet connection')
        return False
    return response.status_code


def get_translate(url):
    user_agent = 'Mozilla/5.0'
    page = requests.get(url, headers={'User-Agent': user_agent})
    soup = BeautifulSoup(page.content, 'html.parser')
    translations = soup.find('div', {'id': 'translations-content'})
    words = []
    for word in translations.contents:
        if word != '\n':
            words.append(word.text.strip())
    if not bool(words[-1]):
        words.pop()
    translations = soup.find('section', {'id': 'examples-content'})
    examples = []
    for example in translations.contents:
        if example != '\n':
            if example.contents[1].text.strip():
                examples.append(example.contents[1].text.strip())
                examples.append(example.contents[3].text.strip())
    return words, examples


def make_url(lang_word, lang_trans, word):
    url = f'https://context.reverso.net/translation/{LANGUAGES[lang_word]}-{LANGUAGES[lang_trans]}/{word}'
    return url


def readable_output(words, examples, lang):
    if len(words) > 5:
        words = words[0: 5]
    if len(examples) > 10:
        examples = examples[0: 10]
    print()
    print(lang, 'Translations:')
    for word in words:
        print(word)
    print()
    print(lang, 'Examples:')
    for i in range(0, len(examples) - 1, 2):
        print(examples[i])
        print(examples[i + 1])
        if i + 2 != len(examples):
            print()


def readable_output_per_one(word, examples, lang):
    print()
    print()
    print(lang, 'Translations:')
    print(word)
    print()
    print(lang, 'Examples:')
    print(examples[0])
    print(examples[1])


def translate(lang_word, lang_trans, word):
    url = f'https://context.reverso.net/translation/{lang_word}-{lang_trans}/{word}'
    resp = connection(url)
    if resp:
        if resp != 200:
            print(f"Sorry, unable to find {word}")
            return False, False
    else:
        return False, False
    words, examples = get_translate(url)
    return words[0], examples[0:2]
    # readable_output(words, examples, LANGUAGES[lang_trans].capitalize())
    # file_save(word, LANGUAGES[lang_trans].capitalize(), words, examples)


def file_save(name, lang, word, examples):
    if os.path.exists(f"{name}.txt"):
        with open(f"{name}.txt", 'a', encoding='utf8') as f:
            f.write(f'\n\n\n{lang} Translations:\n')
            f.write(f'{word}\n\n')
            f.write(f'{lang} Examples:\n')
            f.write(f'{examples[0]}\n')
            f.write(f'{examples[1]}')
    else:
        with open(f"{name}.txt", 'w', encoding='utf8') as f:
            f.write(f'{lang} Translations:\n')
            f.write(f'{word}\n\n')
            f.write(f'{lang} Examples:\n')
            f.write(f'{examples[0]}\n')
            f.write(f'{examples[1]}')


def main():
    #     print("""Hello, you're welcome to the translator. Translator supports:
    # 1. Arabic
    # 2. German
    # 3. English
    # 4. Spanish
    # 5. French
    # 6. Hebrew
    # 7. Japanese
    # 8. Dutch
    # 9. Polish
    # 10. Portuguese
    # 11. Romanian
    # 12. Russian
    # 13. Turkish
    # Type the number of your language: """)
    #     lang_word = input()
    #     print("Type the number of a language you want to translate to or '0' to translate to all languages:")
    #     lang_trans = input()
    #     print('Type the word you want to translate:')
    #     word = input().lower()
    lang_word = sys.argv[1]
    lang_trans = sys.argv[2]
    word = sys.argv[3]
    if lang_word not in LANGUAGES.values():
        print(f"Sorry, the program doesn't support {lang_word}")
        return
    if lang_trans != 'all':
        if lang_trans not in LANGUAGES.values():
            print(f"Sorry, the program doesn't support {lang_trans}")
            return
        words, examples = translate(lang_word, lang_trans, word)
        if words:
            readable_output_per_one(words, examples, lang_trans.capitalize())
            file_save(word, lang_trans.capitalize(), words, examples)
        else:
            return
    else:
        for lang_trans in LANGUAGES.keys():
            if LANGUAGES[lang_trans] != lang_word:
                words, examples = translate(lang_word, LANGUAGES[lang_trans], word)
                if words:
                    readable_output_per_one(words, examples, LANGUAGES[lang_trans].capitalize())
                    file_save(word, LANGUAGES[lang_trans].capitalize(), words, examples)
                else:
                    return


if __name__ == '__main__':
    main()
