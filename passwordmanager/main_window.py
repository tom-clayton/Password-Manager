
from tkinter import Frame, Listbox, Scrollbar, Frame, Entry, Button, \
                    Label, RIGHT, LEFT, BOTH, END, DISABLED, NORMAL, \
                    SUNKEN, W, X

class MainWindow(object):
    """The graphical user interface for the app."""
    def __init__(self, root, master, on_command):
        """Create the main window of the user interface.
        Load the main controller object.
        """
        self.root = root
        self.on_command = on_command

        # ---- Window Setup: ---- #
        
        self.root.title("Password Manager")
        self.root.geometry("260x320+200+200")       

        # ---- UI Elements: ---- #
        # Main frame:
        
        self.mainframe = Frame(root)

        # Master password entry:

        self.master_frame = Frame(self.mainframe)
        Label(self.master_frame, text="Master password:").pack(side = LEFT)
        self.master_entry = Entry(self.master_frame,
                                  show="*",
                                  textvariable=master)
        self.master_entry.bind('<Return>', self.on_master)
        self.master_entry.pack(side = RIGHT)
        self.master_frame.pack()

        # Handle selector scroll box:
        
        self.selecter_frame = Frame(self.mainframe)
        self.box = Listbox(self.selecter_frame)
        self.box.pack(side = LEFT)
        self.scrollbar = Scrollbar(self.selecter_frame)
        self.scrollbar.pack(side = RIGHT, fill = BOTH)
        self.box.config(yscrollcommand = self.scrollbar.set) 
        self.scrollbar.config(command = self.box.yview)
        self.box.bind('<Return>', self.on_get)
        self.box.bind('<Double-Button-1>', self.on_get)
        self.selecter_frame.pack(pady=(10))

        # Action buttons:

        first_row = Frame(self.mainframe)
        self.get_button = Button(first_row,
                                 text="Get",
                                 command=self.on_get)
        self.get_button.pack(side=LEFT)      
        self.show_button = Button(first_row,
                                   text="Show",
                                   command=self.on_show)
        self.show_button.pack(side=LEFT)
        self.renew_button = Button(first_row,
                                   text="Renew",
                                   command=self.on_renew)
        self.renew_button.pack(side=LEFT)
        self.delete_button = Button(first_row,
                                    text="Delete",
                                    command=self.on_delete)
        self.delete_button.pack(side=LEFT)
        first_row.pack()

        second_row = Frame(self.mainframe)
        self.add_button = Button(second_row,
                                 text="New",
                                 command=self.on_new)
        self.add_button.pack(side=LEFT)
        self.change_button = Button(second_row,
                                   text="Change master",
                                   command=self.on_change)
        self.change_button.pack(side=LEFT)
        second_row.pack()

        # Statusbar:

        self.statusbar = Label(self.mainframe,
                          bd=1,
                          relief=SUNKEN,
                          anchor=W)
        self.statusbar.pack(fill=X, pady=(10, 0))     

        # ---- Show: ---- #
        
        self.mainframe.pack(fill=BOTH)
        self.master_entry.focus_set()
 

    def on_master(self, *args):
        self.on_command('MAS')

    def on_get(self, *args):
        self.on_command('GET')
        
    def on_show(self, *args):
        self.on_command('SHOW')

    def on_renew(self, *args):
        self.on_command('RENEW')
        
    def on_new(self, *args):
        self.on_command('NEW')
    
    def on_delete(self, *args):
        self.on_command('DEL')
 
    def on_change(self, *args):
        self.on_command('CHG')

    def fill_box(self, handles):
        """Display handles in scrollbox."""
        self.box.delete(0, END)
        if handles:
            for handle in handles:
                self.box.insert(END, handle)
            self.box.select_set(0)
            self.enable_selection_buttons()
            self.box.focus_set()

    def disable_all_buttons(self):
        """Disable all buttons."""
        self.get_button.config(state=DISABLED)
        self.show_button.config(state=DISABLED)
        self.delete_button.config(state=DISABLED)
        self.renew_button.config(state=DISABLED)
        self.add_button.config(state=DISABLED)
        self.change_button.config(state=DISABLED)  

    def enable_selection_buttons(self):
        """Enable buttons that work on a selection."""
        self.get_button.config(state=NORMAL)
        self.show_button.config(state=NORMAL)
        self.delete_button.config(state=NORMAL)
        self.renew_button.config(state=NORMAL)

    def enable_non_selection_buttons(self):
        """Enable buttons that don't need a selection."""
        self.add_button.config(state=NORMAL)
        self.change_button.config(state=NORMAL)

    def set_statusbar(self, message):
        """Write message to statusbar."""
        self.statusbar.config(text=message)
