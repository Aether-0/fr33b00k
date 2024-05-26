import requests
import random
import string
from urllib.parse import quote
from colorama import Fore, Style, init

def get_book():
    # Initialize colorama
    init()

    # Generate random user ID (numeric) and token (alphanumeric)
    user_id = ''.join(random.choices(string.digits, k=2))
    token = ''.join(random.choices(string.ascii_letters + string.digits, k=6))

    # User input for the book ID
    book_id = input("Enter the book ID: ")

    # API endpoint and parameters
    url = f"https://willpoweraudiobooks.com/app/api/get_chapters.php"
    params = {
        "user_id": user_id,
        "token": token,
        "book": book_id
    }

    # Making the request
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise HTTPError for bad responses
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            print("Book not found.")
        else:
            print("Please wait.")
        return
    except requests.exceptions.RequestException as e:
        print(f"Request error occurred: {e}")
        return

    # Checking if the request was successful
    if response.status_code == 200:
        try:
            data = response.json()

            # Define color for keys and values
            key_color = Fore.BLUE
            value_color = Fore.YELLOW
            reset = Style.RESET_ALL

            def colored_print(key, value):
                print(f"{key_color}{key}{reset}: {value_color}{value}{reset}")

            # Print formatted response
            print(f"{key_color}Status{reset}: {value_color}{data.get('status', 'Unknown')}{reset}")

            if 'book_size' in data:
                print(f"{key_color}Book Size{reset}: {value_color}{data['book_size']}{reset}")
            else:
                print(f"{key_color}Book Size{reset}: {value_color}Not available{reset}")

            print(f"\n{key_color}Book Info{reset}")

            # Check if 'book' key exists before accessing nested keys
            if 'book' in data:
                colored_print("ID", data['book'].get('id', 'Not available'))
                colored_print("Paid Status", data['book'].get('paid_status', 'Not available'))
                colored_print("Num Listens", data['book'].get('num_listens', 'Not available'))
            else:
                print(f"{key_color}Book Info{reset}: {value_color}Not available{reset}")

            print(f"\n{key_color}Chapters{reset}")
            for chapter in data.get('chapters', []):
                print(
                    f"\n{key_color}Chapter Number{reset}: {value_color}{chapter.get('chapter_number', 'Unknown')}{reset}")
                colored_print("ID", chapter.get('id', 'Not available'))
                colored_print("Book ID", chapter.get('book_id', 'Not available'))
                colored_print("Chapter Title", chapter.get('chapter_title', 'Not available'))

                # URL encode the audio URL
                encoded_audio_url = quote(chapter.get('audio_url', ''), safe='/:')
                colored_print("Audio URL", encoded_audio_url)

                colored_print("Status", chapter.get('status', 'Not available'))
                colored_print("Num Listens", chapter.get('num_listens', 'Not available'))

        except ValueError as e:
            print(f"Error parsing JSON: {e}")
    else:
        print(f"Error: {response.status_code} - {response.reason}")


def search_book():
    # Initialize colorama
    init()

    # Prompt the user for category input
    category = input("Enter the category ID: ")

    # Define the URL with the user-provided category
    url = f'https://willpoweraudiobooks.com/app/api/get_playbooks.php?user_id=&token=&category={category}'

    # Make the HTTP request
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Ensure the response is correctly decoded as UTF-8
        response.encoding = 'utf-8'

        # Parse the JSON response
        data = response.json()

        # Function to print book details with colors
        def print_book_details(book):
            print(f"{Fore.BLUE}Category Title:{Style.RESET_ALL} {book.get('category_title')}")
            print(f"{Fore.GREEN}Book ID:{Style.RESET_ALL} {book.get('id')}")
            print(f"{Fore.CYAN}Minutes:{Style.RESET_ALL} {book.get('minutes_text')}")
            print(f"{Fore.RED}Listened Number:{Style.RESET_ALL} {book.get('num_listens')}")
            print(f"{Fore.MAGENTA}Author:{Style.RESET_ALL} {book.get('short_description')}")
            print(f"{Fore.YELLOW}Cover Photo:{Style.RESET_ALL} {book.get('thumb_url')}")
            print(f"{Fore.LIGHTYELLOW_EX}Book's Title:{Style.RESET_ALL} {book.get('title')}")
            print(f"{Fore.LIGHTRED_EX}Status:{Style.RESET_ALL} {book.get('paid_status')}")
            print("\n" + "=" * 40 + "\n")

        # Print the custom formatted JSON data for playbooks
        print("Playbooks:")
        print("=" * 40)
        for playbook in data.get('playbooks', []):
            print_book_details(playbook)

        # Print the custom formatted JSON data for top books
        print("Top Books:")
        print("=" * 40)
        for top_book in data.get('top_books', []):
            print_book_details(top_book)
    else:
        print(f"Failed to retrieve data. HTTP Status code: {response.status_code}")


def create_banner():

    # Define colors
    yellow = Fore.YELLOW
    cyan = Fore.CYAN
    reset = Style.RESET_ALL
    bold = Style.BRIGHT
    banner = """
 ______   ______     ______     ______     ______     ______     ______     __  __    
/\  ___\ /\  == \   /\  ___\   /\  ___\   /\  == \   /\  __ \   /\  __ \   /\ \/ /    
\ \  __\ \ \  __<   \ \  __\   \ \  __\   \ \  __<   \ \ \/\ \  \ \ \/\ \  \ \  _"-.  
 \ \_\    \ \_\ \_\  \ \_____\  \ \_____\  \ \_____\  \ \_____\  \ \_____\  \ \_\ \_\ 
  \/_/     \/_/ /_/   \/_____/   \/_____/   \/_____/   \/_____/   \/_____/   \/_/\/_/ 

    """
    print(Fore.RED, banner, Fore.RESET)

    # Print the banner lines directly with formatting
    print(yellow + "***********************************************" + reset)
    print(
        yellow + "*" + "                   " + bold + "Powered by" + reset + "                " + yellow + "*" + reset)
    print(yellow + "*" + "             " + cyan + "thewillpowermyanmar.com" + "         " + yellow + "*" + reset)
    print(yellow + "*" + "                                             " + yellow + "*" + reset)
    print(yellow + "*" + "           " + cyan + "Brought To You By RED-SHADOW" + "      " + yellow + "*" + reset)
    print(yellow + "***********************************************" + reset)


# Call the function to create and display the banner
create_banner()
while True:
    print("Choose an option:")
    print(Fore.CYAN + "1. Search Books")
    print(Fore.YELLOW + "2. Get Book")
    print(Fore.RED + "3. Exit")

    choice = input(Style.BRIGHT + "Enter your choice [1/2/3]: " + Style.RESET_ALL)

    if choice == '1':
        search_book()
    elif choice == '2':
        get_book()
    elif choice == '3':
        print(Fore.RED + "Exiting program." + Style.RESET_ALL)
        break
    else:
        print(Fore.RED + "(-)Invalid choice. Please enter 1, 2, or 3." + Style.RESET_ALL)