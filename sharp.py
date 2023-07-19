from tkinter import *
import os
import configparser

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__)) + "/"
CONFIG_FILE = f"{CURRENT_DIR}config.ini"

def main():

    def to_clipboard():
        text2clipboard = ''
        for i, item in enumerate(checkboxes):
            if checkboxes_var[i].get() == 1:
                text2clipboard += f"{item.cget('text')} "
        tk.clipboard_clear()
        tk.clipboard_append(text2clipboard)
        tk.update()

    def clear():
        for item in checkboxes_var:
            item.set(0)

    def edit_tags():
        os.popen(f"gnome-text-editor {CURRENT_DIR}tags.txt")

    def geometry():

        global tk, checkboxes_var, checkboxes
        
        config = configparser.ConfigParser()
        config.read(CONFIG_FILE)
        columns_number = config["Options"]["columns_number"]

        try:
            with open(f"{CURRENT_DIR}tags.txt", 'r') as f:
                tags = f.readlines()
        except FileNotFoundError:
            with open(f"{CURRENT_DIR}tags.txt", 'w') as f:
                tags = []
        
        tk = Tk()
        tk.configure(bg='grey97')

        checkboxes = []
        checkboxes_var = []

        tk.iconphoto(False, PhotoImage(file=f"{CURRENT_DIR}icon.png"))
        tk.title('sHarp Tagger')

        checkboxes = []
        checkboxes_var = []

        for count, tag in enumerate(tags):
            tag = tag.strip()
            checked_box = 0
            checkboxes_var.append(IntVar())
            if tag.endswith('+') or tag.endswith('*'):
                checkboxes_var[count].set(1)
                box_title = tag[:-1]
            else:
                box_title = tag
            checkboxes.append(Checkbutton(tk, text=box_title, variable=checkboxes_var[count], onvalue=1, offvalue=0, bg='grey97', highlightthickness=0))
            # Calculate the row and column index for each checkbox
            row = count // int(columns_number)
            col = count % int(columns_number)
            checkboxes[count].grid(row=row, column=col, sticky=W, padx=10)

        btn_copy = Button(text="COPY!", bg="azure2", fg="grey27", font=(12), command=to_clipboard, bd = 0)
        btn_copy.grid(row=len(tags)//3+1, column=0, pady=20)
        btn_edit = Button(text="Edit tags", bg="azure2", fg="grey27", font=(12), command=edit_tags, bd = 0)
        btn_edit.grid(row=len(tags)//3+2, column=0, pady=20)
        btn_clear = Button(text="Clear selection", bg="azure2", fg="salmon1", font=(12), command=clear, bd = 0)
        btn_clear.grid(row=len(tags)//3+1, column=1, pady=20)
        btn_refresh = Button(text="Refresh window", bg="azure2", fg="grey27", font=(12), command=refresh, bd = 0)
        btn_refresh.grid(row=len(tags)//3+2, column=1, pady=20)

        # Adjust row and column configurations to fit the checkboxes
        for i in range(len(tags)//3):
            tk.grid_rowconfigure(i, weight=1)
        for j in range(3):
            tk.grid_columnconfigure(j, weight=1)
        tk.mainloop()

    def refresh():
        tk.destroy()
        main()
        
    geometry()


if __name__ == '__main__':
    main()