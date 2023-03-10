from bs4 import BeautifulSoup
import requests


def read_page(page_url):
    options_links = []
    options_text = []
    context = []

    # Hacer una solicitud GET a la página web
    url = page_url
    response = requests.get(url)

    # Parsear el contenido HTML con BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    main_content = soup.find('div', {'id': 'main-content'})
    page_title = main_content.find('div', {'id': 'page-title'}).text.strip("\n").strip(" ")
    page_content = main_content.find('div', {'id': 'page-content'})
    # image = page_content.find('img')['src']
    p_elements = page_content.find_all('p')
    print(page_title)
    for p in p_elements:
        a = p.find('a')
        if a and 'href' in a.attrs:
            options_links.append(a['href'])
            options_text.append(a.text.strip())
        else:
            context.append(p.text.strip())

    for sentence in context:
        print(sentence)

    i = 0
    for option in options_text:
        print(str(i + 1) + option)
        i += 1

    if len(options_links) == 1:
        selected_option = 1
    else:
        while True:
            try:
                selected_option = int(input("Por favor, elige tu opción: "))
                if selected_option == 'exit' or selected_option == 'salir':
                    exit(0)
                if selected_option < 1 or selected_option > len(options_links):
                    raise ValueError
                break
            except ValueError:
                print(f"Opción inválida. Por favor introduce un número entre 1 y {len(options_links)}.")

    return "http://elvertederodeelinventor.wikidot.com" + options_links[selected_option - 1]


def main():
    current_page = "http://elvertederodeelinventor.wikidot.com/moirai-inicio"
    while True:
        next_page = read_page(current_page)
        if next_page == "final":
            break
        else:
            current_page = next_page


if __name__ == '__main__':
    main()