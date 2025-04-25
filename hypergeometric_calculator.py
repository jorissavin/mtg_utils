import tkinter as tk
import math

def recursive_probability(remaining_cards,categories_list):
    total = 0
    #categories_list est une liste de catégories contenant le minimum requis le maximum requis et le total de la catégorie
    if len(categories_list) > 1:
        nom, nb_total, minimum, maximum = categories_list[0]
        for i in range(0, remaining_cards + 1):
            if i >= minimum and i <= maximum:
                total += recursive_probability(remaining_cards-i, categories_list[1:] ) * math.comb(nb_total,i)
        return total
    else :
        nom, nb_total, minimum, maximum = categories_list[0]
        if remaining_cards >= minimum and remaining_cards <= maximum:
            return math.comb(nb_total, remaining_cards)
        else :
            return 0
        
def hypergeometric(n,N, categories_list):
    return math.comb(N,n)**(-1) * recursive_probability(n,categories_list)

class MyApp :

    def __init__(self):
        self.window = tk.Tk()
        self.window.title("My App")
        self.window.geometry("720x480")
        self.window.minsize(480, 360)
        
        self.frame_1 = tk.Frame(self.window, bg = "red")
        self.frame_2 = tk.Frame(self.window, bg = "green")
        self.frame_3 = tk.Frame(self.window, bg = "blue")
        self.frame_4 = tk.Frame(self.window, bg = "yellow")


        self.decksize = 0
        self.categories = []

        self.create_widgets()

        self.frame_1.pack()
        self.frame_2.pack() #gets deck size
        self.frame_3.pack() #gets the categories
    
    def create_widgets(self):
        self.create_title()
        self.create_decksize()
        self.create_categories()
    def create_title(self):
        label_title = tk.Label(self.frame_1, text = "Welcome to my hypergeometric calculator !")
        label_title.pack()
        button_validate_categories_decksize = tk.Button(self.frame_1, text = "Validate parameters", command = self.go_to_math)
        button_validate_categories_decksize.pack()
    
    def create_decksize(self):
        self.decksize = 0
        for widget in self.frame_2.winfo_children():
            widget.destroy()
        
        label_decksize = tk.Label(self.frame_2, text = "Please enter your deck size")
        label_decksize.pack()
        self.entry_decksize = tk.Entry(self.frame_2, textvariable="Deck size")
        self.entry_decksize.pack()

        button_validate_decksize = tk.Button(self.frame_2, text = "Validate", command = self.validate_decksize)
        button_validate_decksize.pack()
    
    def validate_decksize(self):
        self.decksize = int(self.entry_decksize.get())
        for widget in self.frame_2.winfo_children():
            widget.destroy()

        label_decksize = tk.Label(self.frame_2, text = "Deck size : " + str(self.decksize))
        label_decksize.pack()
        button_change_decksize = tk.Button(self.frame_2, text = "Change deck size", command = self.create_decksize)
        button_change_decksize.pack()

    def create_categories(self):
        for widget in self.frame_3.winfo_children():
            widget.destroy()
        label_category_1 = tk.Label(self.frame_3, text = "Please enter a card category.\n Category_name :")
        label_category_1.pack()
        self.entry_category_name = tk.Entry(self.frame_3, textvariable="category name")
        self.entry_category_name.pack()
        label_category_2 = tk.Label(self.frame_3, text = "number of cards :")
        label_category_2.pack()
        self.entry_category_count = tk.Entry(self.frame_3, textvariable="number of cards")
        self.entry_category_count.pack()

        button_validate_categories = tk.Button(self.frame_3, text = "Validate", command = self.validate_categories)
        button_validate_categories.pack()
    
    def validate_categories(self):
        self.categories.append([self.entry_category_name.get(), int(self.entry_category_count.get())])

        for widget in self.frame_3.winfo_children():
            widget.destroy()

        label_categories = tk.Label(self.frame_3, text = "Categories : " + str(self.categories))
        label_categories.pack()
        button_change_categories = tk.Button(self.frame_3, text = "add another category", command = self.create_categories)
        button_change_categories.pack()
        button_reset_categories = tk.Button(self.frame_3, text = "reset categories", command = self.reset_categories)
        button_reset_categories.pack()
    def reset_categories(self):
        self.categories = []
        self.create_categories()

    def go_to_math(self):
        if self.decksize == 0 or self.categories == []:
            return None
        self.categories.append(["Rest", int(self.decksize) - sum([x[1] for x in self.categories])])
        self.frame_1.pack_forget()
        self.frame_2.pack_forget()
        self.frame_3.pack_forget()
        self.frame_4.pack()
        label_recap = tk.Label(self.frame_4, text = "Parameters :\n Deck size : " + str(self.decksize) + "\n Categories : " + str(self.categories))
        label_recap.pack()
        label_howmuch = tk.Label(self.frame_4, text = "How much do you want of each in your starting hand ?")
        label_howmuch.pack()

        self.entries = []
        self.entries_validated = []
        for i, element in enumerate(self.categories):
            # Créer une Frame pour chaque paire minimum-maximum
            frame = tk.Frame(self.frame_4)
            frame.pack(pady=5)

            # Étiquette pour afficher l'élément
            label_element = tk.Label(frame, text=f"{element[0]} :")
            label_element.grid(row=0, column=0, padx=5)

            # Entrée pour le minimum
            entry_min = tk.Entry(frame)
            entry_min.grid(row=0, column=1, padx=5)

            # Entrée pour le maximum
            entry_max = tk.Entry(frame)
            entry_max.grid(row=0, column=2, padx=5)

            # Stocker les entrées dans une liste pour référence ultérieure si nécessaire
            self.entries.append((entry_min, entry_max))
        frame = tk.Frame(self.frame_4)
        frame.pack(pady=5)
        label_handsize = tk.Label(frame, text = "hand size :")
        label_handsize.pack()
        self.entry_handsize = tk.Entry(self.frame_4, textvariable="hand size")
        self.entry_handsize.pack()
        # Créer une Frame pour le bouton de validation
        frame = tk.Frame(self.frame_4)
        frame.pack(pady=5)

        # Bouton de validation
        button_validate = tk.Button(frame, text="Validate", command=lambda: self.validate_math(self.entries))
        button_validate.pack()

    def validate_math(self, entries):
        if self.entry_handsize.get() == "":
            self.handsize = 7
        else:
            self.handsize = int(self.entry_handsize.get())
        for i, element in enumerate(entries):
            if element[0].get() == "":
                min = 0 
            else :
                min = int(element[0].get())
            if element[1].get() == "":
                max = self.categories[i][1]
            else:
                max = int(element[1].get())
            self.entries_validated.append([self.categories[i][0], self.categories[i][1], min, max])
        for k in self.entries_validated:
            frame = tk.Frame(self.frame_4)
            frame.pack(pady=5)
            label_element = tk.Label(frame, text=f"Category {k[0]}, containing {k[1]} cards : minimum {k[2]}, maximum {k[3]}")
            label_element.pack()
        frame = tk.Frame(self.frame_4)
        frame.pack(pady=5)
        print(self.handsize, self.decksize, self.entries_validated)
        probability = hypergeometric(self.handsize, self.decksize, self.entries_validated)
        print(probability)
        label_mathematics = tk.Label(frame, text = "Probability of a hand with the following characteristics :\n" + str(probability))
        label_mathematics.pack()
        for i, element in enumerate(self.entries_validated):
            label_element = tk.Label(frame, text=f"Catégory {element[0]}, containing {element[1]} cards, minimum {element[2]}, maximum {element[3]}")
app = MyApp()
app.window.mainloop()
