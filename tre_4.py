import nltk
from nltk import CFG, ChartParser
import tkinter as tk
from tkinter import simpledialog, messagebox
from nltk.draw.util import CanvasFrame
from nltk.draw import TreeWidget

# Initialize grammar with basic rules
grammar_rules = """
    S -> NP VP
    VP -> V NP | V NP PP | V | V ADVP
    NP -> D N | N | ADJP N | N PP
    PP -> P NP
    ADVP -> A
    ADJP -> J
    N -> 'umuntu' | 'ukudla' | 'imoto' | 'inja' | 'ikati'
    V -> 'udla' | 'ubona' | 'uhamba'
    D -> 'owesifazane' | 'owesilisa'
    A -> 'ngokushesha'
    J -> 'hle'
    P -> 'ngaphansi' | 'ngaphezulu'
"""

grammar = nltk.CFG.fromstring(grammar_rules)
parser = ChartParser(grammar)

def update_grammar(word, category):
    global grammar, parser
    productions = list(grammar.productions())
    production_str = f"{category} -> '{word}'"
    new_production = nltk.CFG.fromstring(production_str).productions()[0]
    productions.append(new_production)
    grammar = nltk.CFG(grammar.start(), productions)
    parser = ChartParser(grammar)

def parse_sentence(sentence):
    tokens = nltk.word_tokenize(sentence)
    return list(parser.parse(tokens))

def generate_tree():
    sentence = entry.get().strip()
    if not sentence:
        messagebox.showerror("Error", "Sicela ufake umusho.")
        return
    
    tokens = nltk.word_tokenize(sentence)
    for token in tokens:
        if not any(token in str(prod.rhs()) for prod in grammar.productions()):
            tag = simpledialog.askstring("Tag Word", f"Enter POS tag for '{token}': (N, V, D, A, J, P)", parent=root)
            if tag in ['N', 'V', 'D', 'A', 'J', 'P']:
                update_grammar(token, tag)
            else:
                messagebox.showerror("Invalid Tag", "Please use valid tags: N, V, D, A, J, or P.")
                return

    trees = parse_sentence(sentence)
    if trees:
        show_trees(trees)
    else:
        messagebox.showinfo("Result", "No syntactic trees could be generated for the input.")

def show_trees(trees):
    tree_window = tk.Toplevel(root)
    tree_window.title("Uhlelo Lomusho")
    tree_window.configure(bg='black')

    cf = CanvasFrame(tree_window)
    cf.pack(fill="both", expand=True)

    for tree in trees:
        tc = TreeWidget(cf.canvas(), tree)
        cf.add_widget(tc, 10, 10)  # arbitrary position

    cf.print_to_file('tree.ps')
    cf.mainloop()

# Setup GUI
root = tk.Tk()
root.geometry("600x400")
root.title('Uhlelo lohlelomisho')
root.configure(bg='black')

label = tk.Label(root, text='Uhlelo lohlelomisho', bg='black', fg='white', font=("Helvetica", 16))
label.pack(anchor='nw', padx=10, pady=10)

tk.Label(root, text='Faka umusho:', bg='black', fg='white').pack(pady=10)
entry = tk.Entry(root, width=50, bg='white', fg='black')
entry.pack()

tk.Button(root, text="Loba uhlelo lomusho", command=generate_tree, bg='grey', fg='white').pack(pady=20)

root.mainloop()
