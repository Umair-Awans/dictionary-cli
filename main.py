import requests


def fetch_word_data(word):
    """Fetch word data from the DictionaryAPI."""
    BASE_URL = "https://api.dictionaryapi.dev/api/v2/entries/en/"
    try:
        response = requests.get(BASE_URL + word)
        response.raise_for_status()  # Will raise an error for bad responses (non-200 status)
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.ConnectionError:
        print("Connection error. Please check your internet connection.")
    except Exception as err:
        print(f"An error occurred: {err}")
    return None


def display_meanings(word: str, data):
    """Display meaning(s) of the word."""
    print(f"\n<>-<>-<>---( {word.title()} )---<>-<>-<>\n")
    phonetics = data[0].get("phonetics", [])
    if phonetics:
        text = phonetics[0].get("text")
        if text:
            print(f"\nPhonetic: {text}")
    meanings = data[0].get("meanings", [])
    if not meanings:
        print("\nNo meanings found.")
        return
    for meaning in meanings:
        part_of_speech = meaning["partOfSpeech"]
        print(f"\n------( {part_of_speech} )------")
        for i, d in enumerate(meaning["definitions"], start=1):
            print(f"\n------( Definition {i} )------\n\n{d['definition']}")
            if d.get("example"):
                print("\n------( Example )------\n\n")
                print(f"{d['example']}")
            if d.get("synonyms"):
                print("\n------( Synonyms )------\n\n")
                print(", ".join(d["synonyms"]))
            if d.get("antonyms"):
                print("\n------( Antonyms )------\n\n")
                print(", ".join(d["antonyms"]))


def main():
    while True:
        print("\n<--<--<---( Dictionary )--->-->-->\n")
        word = input("\nEnter the word: ").lower()        
        
        # Fetch data for the copied or entered word
        data = fetch_word_data(word)
        if not data:
            print(f"\n{word} not found! Please enter another word.\n")
            continue  # Retry on error or invalid word
        
        display_meanings(word, data)        
        
        # Option to quit
        choice = input("\nAnother word? (Y/N): ").strip().lower()
        if choice in ["n", "no", "exit", "q"]:
            print("\nHave a nice day!\n")
            break


if __name__ == "__main__":
    main()
