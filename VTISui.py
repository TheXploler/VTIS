import ttkbootstrap as ttk
from ttkbootstrap.constants import *

class MainUI:
    def __init__(self, master=None):
        tk2 = ttk.Window(themename="vapor")
        tk2.title("VTIS - Video To Image Sequence")
        tk2.resizable(False, False)
        
        self.SelectVideo = ttk.Button(tk2, text='Open', bootstyle="primary")
        self.SelectVideo.grid(column=2, row=0, padx=5, pady=5)
        self.SelectVideo.configure(command=self.OV)

        self.VideoEntry = ttk.Entry(tk2, bootstyle="primary")
        self.VideoEntry.grid(column=1, row=0, sticky="we", padx=5, pady=5)

        self.OutputFormatLbl = ttk.Label(tk2, text='Output Format', bootstyle="inverse-primary")
        self.OutputFormatLbl.grid(
            column=0,
            columnspan=2,
            padx=10,
            pady=10,
            row=1,
            sticky="w")

        self.OutputDirEntry = ttk.Entry(tk2, bootstyle="primary")
        self.OutputDirEntry.grid(column=1, row=2, padx=5, pady=5, sticky="we")

        self.OutputDirBtn = ttk.Button(tk2, text='Open', bootstyle="primary")
        self.OutputDirBtn.grid(column=2, row=2, padx=5, pady=5)
        self.OutputDirBtn.configure(command=self.OD)

        self.ProcessBtn = ttk.Button(tk2, text='Start Processing', bootstyle="success")
        self.ProcessBtn.grid(column=0, columnspan=3, padx=10, pady=10, row=3)
        self.ProcessBtn.configure(command=self.SP)

        self.VideoInputLbl = ttk.Label(tk2, text='Video Input', bootstyle="inverse-primary")
        self.VideoInputLbl.grid(
            column=0,
            columnspan=2,
            padx=10,
            pady=10,
            row=0,
            sticky="nw")

        self.OutputDirLbl = ttk.Label(tk2, text='Output Directory', bootstyle="inverse-primary")
        self.OutputDirLbl.grid(column=0, padx=10, pady=10, row=2, sticky="w")

        self.FormatCombobox = ttk.Combobox(tk2, values=['JPG', 'PNG'], bootstyle="primary")
        self.FormatCombobox.grid(column=1, row=1, padx=5, pady=5)

        tk2.grid_columnconfigure(1, weight=1)

        self.mainwindow = tk2

    def run(self):
        self.mainwindow.mainloop()

    def OV(self):
        pass

    def OD(self):
        pass

    def SP(self):
        pass


if __name__ == "__main__":
    app = MainUI()
    app.run()
