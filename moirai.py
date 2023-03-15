from bs4 import BeautifulSoup
import requests
import colorama


# Description: This function reads from a block of HTML code to get the divs that are a collapsible element
# Argument: A block of HTML code
def read_collapsible_block(block):
    link_text = block.find('div', {'class': 'collapsible-block-folded'}).text.strip()
    content = block.find('div', {'class': 'collapsible-block-content'}).text.strip()
    return link_text, content


# Description: This function retrieves the interesting content of a webpage to parse variables
# Argument 1: page main content of webpage
# Argument 2: output value of the paragraphs of the main page content
def read_raw_paragraphs(page_content, out_context):
    # incluir cualquier texto antes del primer p
    first_p = page_content.find('p')
    if first_p.previous_sibling:
        out_context.append(first_p.previous_sibling.strip())
    return page_content.find_all(['p', 'div'], recursive=False)


# Description: Show the texts options to the output
# Argument: A list of the option values as text
def display_options(options_text):
    # print options
    i = 0
    for index, option in enumerate(options_text):
        print(f"{index + 1}> {option}")


# Description: Show the texts options to the output
# Argument 1: A list of the option values as text
# Argument 2: A list containing the context of the page
def display_context(page_title, context):
    print(colorama.Fore.RED + page_title)
    print(colorama.Fore.GREEN + "*" * 50 + colorama.Fore.YELLOW)
    for sentence in context:
        if sentence == "":
            continue
        else:
            print(sentence)


# Description: Show the texts options to the output
# Argument: A list of the option values as text
def display_fake_context(context):
    for sentence in context:
        print(sentence)


# Description: Show the content of the page of the game
# Argument 1: Name of the level
# Argument 2: List holding the context of the level
# Argument 3: List of the options for the user to select
def create_page_and_return_selected_option_link(page_name, page_context, options_text, options_links):
    display_context(page_name, page_context)
    print(colorama.Fore.GREEN + "=" * 50 + colorama.Fore.RESET + "\n")
    display_options(options_text)
    return get_next_page_link(options_links)


# Description: Show the content a fake page of the game
# Argument 1: Name of the level (edited)
# Argument 2: List holding the context of the level (edited)
# Argument 3: List of the options for the user to select (edited)
def create_page_from_scratch_and_return_selected_option_link(page_name, page_context, options_text):
    print(colorama.Fore.RESET)
    print(page_name + "\n")
    print("*" * 50)
    print(colorama.Fore.GREEN)
    display_fake_context(page_context)
    print(colorama.Fore.RESET)
    print("=" * 50 + "\n")
    print(colorama.Fore.CYAN)
    display_options(options_text)


def add_element_to_options_list(options_links_list, a):
    options_links_list.append(a['href'])


def add_element_to_text_list(options_text_list, a):
    options_text_list.append(a.text.strip())


def add_element_to_context(context, elem):
    context.append(elem.text.strip())


def add_element_to_target_list(elem, target_list):
    target_list.append(elem)


def add_element_to_fake_context(fake_context, content):
    fake_context.append(content)


def detect_fake_pages(list_of_elements, context, options_text_list, options_links_list, fake_context = [], fake_options_text_list = [], fake_options_links_list = []):
    for element in list_of_elements:
        if element.name == 'p':
            a = element.find('a')
            if a and 'href' in a.attrs:
                add_element_to_options_list(options_links_list, a)
                add_element_to_text_list(options_text_list, a)
            else:
                # Check if there is an unfolded collapsible block inside this element
                unfolded_block = element.find('div', {'class': 'collapsible-block-unfolded'})
                if unfolded_block:
                    link_text, content = read_collapsible_block(unfolded_block)

                    print("ADDING THE TEXT TO OPTIONS_TEXT:")
                    options_text_list.append(link_text + " -> ERROR")
                    options_links_list.append(unfolded_block.find('a')['href'])

                    add_element_to_fake_context(fake_context, content)
                    if not content:
                        add_element_to_context(context, content)
                else:
                    add_element_to_context(context, element)

                '''print("DEBUG!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                print("OPTIONS_TEXT_LIST = ", options_text_list)
                print("OPTIONS_LINKS_LIST = ", options_links_list)
                print("DEBUG!!!!!!!!!!!!!!!!!!!!!!!!!!!!")'''
        elif element.name == 'div':
            if element.has_attr('class') and 'collapsible-block' in element['class']:
                link_text, content = read_collapsible_block(element)
                options_text_list.append(link_text + " -> ERROR")
                options_links_list.append(element.find('a')['href'])

                add_element_to_fake_context(fake_context, content)
                if not content:
                    add_element_to_context(context, content)

                print("DEBUG!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                print("OPTIONS_TEXT_LIST = ", options_text_list)
                print("OPTIONS_LINKS_LIST = ", options_links_list)
                print("DEBUG!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            else:
                add_element_to_context(context, element)
    return context, options_text_list, options_links_list, fake_context, fake_options_text_list, fake_options_links_list


def refine_paragraphs(list_of_elements, context, options_text_list, options_links_list, fake_context = [], fake_options_text_list = [], fake_options_links_list = []):
    return detect_fake_pages(list_of_elements, context, options_text_list, options_links_list, fake_context, fake_options_text_list, fake_options_links_list)


# Description: This function gives back a request to an url of a webpage and returns the HTML content
# Arguments: url of the webpage
def get_webpage(url):
    # Hacer una solicitud GET a la página web
    url = url
    response = requests.get(url)
    return BeautifulSoup(response.content, 'html.parser')


# Description: This function retrieves the main content of the webpage
# Argument: url of a webpage to read the elements
def get_main_content(url):
    return get_webpage(url).find('div', {'id': 'main-content'})


# Description: This function retrieves the page title
# Argument: page main content of webpage
def get_main_page_title(main_content):
    return main_content.find('div', {'id': 'page-title'}).text.strip("\n").strip(" ")


# Description: This function retrieves the page main content of the webpage
# Argument: page main content of webpage
def get_main_page_content(main_content):
    return main_content.find('div', {'id': 'page-content'})


# Description: Get the user selected option page link, if it hasn't any link, return javascript error
# Argument: A list of the option values as links
def get_next_page_link(options_links):
    url_path = options_links[get_selected_option(options_links) - 1]
    if url_path == "javascript:;":
        return "javascript_error"
    else:
        return "http://elvertederodeelinventor.wikidot.com" + url_path


# Description: Get the user selected option
# Argument: A list of the option values as link
def get_selected_option(options_links):
    while True:
        try:
            if len(options_links) == 1:
                return 1
            else:
                selected_option = int(input("Por favor, elige tu opción:\t"))
            if selected_option == 0:
                exit(0)
            if selected_option < 1 or selected_option > len(options_links):
                raise ValueError
            return selected_option
        except ValueError:
            print(f"Opción inválida. Por favor introduce un número entre 1 y {len(options_links)}.")


# Description: This function retrieves the interesting content of a webpage to parse variables
# Argument: url of a webpage to read the elements
def parse_html_content(url):
    page_title = get_main_page_title(get_main_content(url))
    page_content = get_main_page_content(get_main_content(url))

    options_links = []
    options_text = []
    context = []

    fake_context = []
    fake_options_text_list = []
    fake_options_links_list = []

    context, options_text, options_links, fake_context, fake_options_text_list, fake_options_links_list = refine_paragraphs(read_raw_paragraphs(page_content, context),
                                                                           context, options_text, options_links,
                                                                           fake_context, fake_options_text_list, fake_options_links_list)
    return page_title, context, options_text, options_links, fake_context, fake_options_text_list, fake_options_links_list


def main():
    current_page = "http://elvertederodeelinventor.wikidot.com/moirai-inicio"
    print("Escribe 0 para salir del juego.")

    while True:
        page_title, page_context, page_options, page_links, fake_context, fake_options_text_list, fake_options_links_list = parse_html_content(current_page)
        next_page = create_page_and_return_selected_option_link(page_title, page_context, page_options, page_links)

        # Ask to ElInventor which is the final page
        if next_page == "final":
            break
        elif next_page == "javascript_error":
            print(colorama.Fore.RED)
            print("ERROR:###########################")

            print(colorama.Fore.CYAN)
            print("We need to take out the previous option from the list of options")

            create_page_from_scratch_and_return_selected_option_link(page_title, fake_context, page_options)

            print(colorama.Fore.RESET)
            exit(1)
        else:
            current_page = next_page


if __name__ == '__main__':
    main()
