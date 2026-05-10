from tkinter import *
from tkinter import ttk

film = ["Janur Ireng", "KKN di Desa Ayak", "Ambacong"]

jam_tayang = [
    ["10:00", "12:00"], 
    ["11:00", "13:00"], 
    ["12:00", "15:00"]
]

kursi = [
    [["A1", "A2", "A3", "B1", "B2", "B3", "C1", "C2", "C3"], ["A1", "A2", "A3", "B1", "B2", "B3", "C1", "C2", "C3"]], 
    [["A1", "A2", "A3", "B1", "B2", "B3", "C1", "C2", "C3"], ["A1", "A2", "A3", "B1", "B2", "B3", "C1", "C2", "C3"]], 
    [["A1", "A2", "A3", "B1", "B2", "B3", "C1", "C2", "C3"], ["A1", "A2", "A3", "B1", "B2", "B3", "C1", "C2", "C3"]]
]

# Kode untuk membuat GUI menggunakan Tkinter
root = Tk()
frm = ttk.Frame(root, padding=10)
frm.grid()

# Ubah kode di bawah ini sesuai dengan kebutuhan
ttk.Label(frm, text="Hello BUT!").grid(column=0, row=0)
ttk.Button(frm, text="Quit", command=root.destroy).grid(column=1, row=0)

root.mainloop()