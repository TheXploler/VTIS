import tkinter as tk
import tkinter.ttk as ttk
import tkinter.filedialog as filedialog
import tkinter.messagebox as messagebox
import os
import json
import sys
import subprocess
import threading
import VTISui as baseui # Main UI
from PBUI import ProgressWindow # Progress Bar UI

class ConfigManager:
    def __init__(self, config_file='vtis_config.json'):
        if getattr(sys, 'frozen', False):
            script_dir = os.path.dirname(sys.executable)
        else:
            script_dir = os.path.dirname(os.path.abspath(__file__))
        
        self.config_file = os.path.join(script_dir, config_file)
        self.config = self.load_config()

    def load_config(self):
        # Load config
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    return json.load(f)
        except (json.JSONDecodeError, IOError):
            pass
        
        # Return default config if no config
        return {
            'last_output_directory': '',
            'last_video_path': '',
            'preferred_format': 'PNG'
        }

    def save_config(self, config):
        try:
            with open(self.config_file, 'w') as f:
                json.dump(config, f, indent=4)
        except IOError:
            messagebox.showwarning("Config Save Error", 
                "Could not save configuration, some settings may not persist")

    def get(self, key, default=''):
        return self.config.get(key, default)

    def update(self, key, value):
        self.config[key] = value
        self.save_config(self.config)

class Main(baseui.MainUI):
    def __init__(self, master=None):
        self.config_manager = ConfigManager()
        super().__init__(master)
        
        # Get config
        last_output_dir = self.config_manager.get('last_output_directory')
        last_video_path = self.config_manager.get('last_video_path')
        preferred_format = self.config_manager.get('preferred_format')
        
        # Set out dir
        if last_output_dir and os.path.isdir(last_output_dir):
            self.OutputDirEntry.delete(0, tk.END)
            self.OutputDirEntry.insert(0, last_output_dir)
        
        # Set last video 
        if last_video_path and os.path.isfile(last_video_path):
            self.VideoEntry.delete(0, tk.END)
            self.VideoEntry.insert(0, last_video_path)
        
        # Set format
        if preferred_format:
            self.FormatCombobox.set(preferred_format)

    def OV(self): # Open Vid
        video_file = filedialog.askopenfilename(
            title="Select Video File",
            filetypes=[
                ("Video Files", "*.mp4 *.avi *.mkv *.mov *.wmv"),
                ("All Files", "*.*")
            ]
        )
        
        # Update video entry
        if video_file:
            # Clear n insert
            self.VideoEntry.delete(0, tk.END)
            self.VideoEntry.insert(0, video_file)
            
            # Save to config
            self.config_manager.update('last_video_path', video_file)

    def OD(self): # Open Output Dir
        # Use last output dir
        initial_dir = self.config_manager.get('last_output_directory', '')
        
        output_dir = filedialog.askdirectory(
            title="Select Output Directory",
            initialdir=initial_dir if os.path.isdir(initial_dir) else None
        )
        
        # Update output dir
        if output_dir:
            # Clear n insert
            self.OutputDirEntry.delete(0, tk.END)
            self.OutputDirEntry.insert(0, output_dir)
            
            # Save to config
            self.config_manager.update('last_output_directory', output_dir)

    def extract_frames(self, video_path, output_dir, output_format):
        # Check outdir
        os.makedirs(output_dir, exist_ok=True)

        # Get video duration n fps
        try:
            probe_cmd = [
                'ffprobe', 
                '-v', 'error', 
                '-select_streams', 'v:0', 
                '-count_packets', 
                '-show_entries', 'stream=nb_read_packets', 
                '-of', 'csv=p=0', 
                video_path
            ]
            total_frames = int(subprocess.check_output(probe_cmd).decode().strip())
        except (subprocess.CalledProcessError, ValueError):
            messagebox.showerror("Error", "Could not determine video frame count")
            return False

        # Create progress window
        progress_window = ProgressWindow(self.mainwindow, "Extracting Frames")

        def run_extraction():
            try:
                # FFmpeg command to extract frames reminder %05d is for recursivewhatever
                cmd = [
                    'ffmpeg', 
                    '-i', video_path, 
                    '-start_number', '0', 
                    os.path.join(output_dir, f'frame_%05d.{output_format.lower()}')
                ]

                # Subprocess
                progress_window.process = subprocess.Popen(
                    cmd, 
                    stdout=subprocess.PIPE, 
                    stderr=subprocess.PIPE,
                    universal_newlines=True
                )

                # Track progress
                current_frame = 0
                for line in progress_window.process.stderr:
                    if not progress_window.is_processing:
                        break

                    # Update progress/10f so that doesn't explode
                    if current_frame % 10 == 0:
                        progress_window.update_progress(current_frame, total_frames)
                    
                    current_frame += 1

                # Wait n close
                progress_window.process.wait()
                progress_window.close()

                # Complete msg
                messagebox.showinfo("Success", f"Extracted {total_frames} frames to {output_dir}")

            except Exception as e:
                messagebox.showerror("Extraction Error", str(e))
                progress_window.close()

        # Run extraction in a separate thread
        threading.Thread(target=run_extraction, daemon=True).start()

    def SP(self): # Start Processing
        video_path = self.VideoEntry.get().strip()
        
        # Get outdir
        output_dir = self.OutputDirEntry.get().strip()
        
        # Get out format
        output_format = self.FormatCombobox.get()
        
        # Validate inputs
        if not video_path:
            messagebox.showerror("Error", "Please select a video file.")
            return
        
        if not output_dir:
            messagebox.showerror("Error", "Please select an output directory.")
            return
        
        if not output_format:
            messagebox.showerror("Error", "Please select an output format.")
            return
        
        # Validate file exists
        if not os.path.exists(video_path):
            messagebox.showerror("Error", "Selected video file does not exist.")
            return
        
        # Validate output directory
        if not os.path.isdir(output_dir):
            messagebox.showerror("Error", "Selected output directory is invalid.")
            return
        
        # Save2conf
        self.config_manager.update('preferred_format', output_format)
        
        # Start convert
        self.extract_frames(video_path, output_dir, output_format)

if __name__ == "__main__":
    app = Main()
    app.run()
