import sys
import tkinter as tk
import main
import tkinter.messagebox as messagebox

root = tk.Tk()
root.title('Pesquisa de Casas')
root.geometry('400x400')


def get_values(number_of_pages_input, url_of_page_input, file_name_input):
    number_of_pages = int(number_of_pages_input.get())
    url_of_page = url_of_page_input.get()
    file_name = file_name_input.get()
    return number_of_pages, url_of_page, file_name


def create_labeled_input_box(root, label_text):
    label = tk.Label(root, text=label_text)
    label.pack()
    input_box = tk.Entry(root)
    input_box.pack()
    return input_box


def create_button(root, number_of_pages_input, url_of_page_input, file_name_input):
    submit_button = tk.Button(root, text='Enter',
                              command=lambda: handle_button_click(number_of_pages_input, url_of_page_input,
                                                                  file_name_input))
    submit_button.pack()


def handle_button_click(number_of_pages_input, url_of_page_input, file_name_input):
    number_of_pages, url_of_page, file_name = get_values(number_of_pages_input, url_of_page_input, file_name_input)
    messagebox.showinfo('A correr..', message="O programa vai correr\n Carrega em OK")

    print(f"Number of pages: {number_of_pages}")
    print(f"URL of page: {url_of_page}")
    print(f"File name: {file_name}")

    main.get_houses(number_of_pages, url_of_page, file_name)

    root.quit()


number_of_pages_input = create_labeled_input_box(root, "Escreve o numero de paginas: ")
url_of_page_input = create_labeled_input_box(root, "Escolhe o URL (nao fazer copy-paste de '/pagina-<i>)': ")
file_name_input = create_labeled_input_box(root, "Escreve o nome do ficheiro: ")
create_button(root, number_of_pages_input, url_of_page_input, file_name_input)

root.mainloop()
