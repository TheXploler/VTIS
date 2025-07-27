import tkinter as tk
import tkinter.ttk as ttk

class ProgressWindow:
    def __init__(self, parent, title="Processing"):
        self.window = tk.Toplevel(parent)
        self.window.title(title)
        self.window.resizable(False, False)
        self.window.grab_set()
        self.window.iconbitmap("data/logo.ico")

        # Status Label
        self.status_label = ttk.Label(self.window, text="Processing",
                                      font=('Helvetica', 10))
        self.status_label.pack(pady=(20, 10))

        # Progress Bar
        self.progress_bar = ttk.Progressbar(self.window, mode='determinate', length=350)
        self.progress_bar.pack(pady=10, padx=20)

        # Cancel Button
        self.cancel_button = ttk.Button(self.window, text="Cancel", command=self.cancel_processing)
        self.cancel_button.pack(pady=10)

        # Processing var
        self.is_processing = True
        self.process = None

    def update_progress(self, current, total):
        # Calc percentage
        percentage = int((current / total) * 100)

        # Update progress n status
        self.progress_bar['value'] = percentage
        self.status_label.config(text=f"Processing frame {current} of {total}")
        self.window.update()

    def cancel_processing(self):
        self.is_processing = False

        # Terminate
        if self.process:
            try:
                self.process.terminate()
            except:
                pass

        self.window.destroy()

    def close(self):
        self.window.destroy()
