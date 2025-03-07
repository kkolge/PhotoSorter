# Copyright (c) 2025 Ketan Kolge
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import ImageTk
from logger import get_logger

logger = get_logger(__name__)

class PhotoManagerUI:
    def __init__(self, root, file_manager, progress_manager, image_processor, reports_manager):
        self.root = root
        self.file_manager = file_manager
        self.progress_manager = progress_manager
        self.image_processor = image_processor
        self.reports_manager = reports_manager
        self.photo = None

        self.root.title("Photo Manager")
        self.canvas = tk.Canvas(root, bg='black')
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.setup_ui()

        # Bind the close event
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def setup_ui(self):
        try:
            menu = tk.Menu(self.root)
            file_menu = tk.Menu(menu, tearoff=0)
            file_menu.add_command(label="Browse Folder", command=self.select_folder)
            file_menu.add_command(label="Pause", command=self.pause)
            file_menu.add_command(label="Resume", command=self.resume)
            file_menu.add_command(label="Start Over", command=self.start_over)
            file_menu.add_command(label="Generate Report", command=self.generate_report)
            file_menu.add_separator()
            file_menu.add_command(label="Exit", command=self.exit_application)
            menu.add_cascade(label="File", menu=file_menu)
            self.root.config(menu=menu)

            control_frame = tk.Frame(self.root)
            control_frame.pack(side=tk.BOTTOM, pady=10)

            tk.Button(control_frame, text="Back", command=self.show_previous).pack(side="left", padx=5)
            tk.Button(control_frame, text="Next", command=self.show_next).pack(side="left", padx=5)
            tk.Button(control_frame, text="Delete", command=self.delete_image).pack(side="left", padx=5)
        except Exception as e:
            logger.error(f"Error setting up UI: {e}")

    def select_folder(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            try:
                self.file_manager.load_images(folder_selected)
                self.progress_manager.load_progress()
                self.show_image()
            except Exception as e:
                logger.error(f"Error selecting folder: {e}")
                messagebox.showerror("Error", f"Failed to load images: {e}")

    def show_image(self):
        try:
            self.canvas.delete("all")
            image_path = self.file_manager.get_current_image()
            if image_path:
                img = self.image_processor.process_image(image_path)
                if img: 
                    self.photo = ImageTk.PhotoImage(img)
                    self.canvas.create_image(
                        self.canvas.winfo_width() // 2,
                        self.canvas.winfo_height() // 2,
                        anchor="center",
                        image=self.photo
                    )
                    self.progress_manager.update_progress(self.file_manager.index, len(self.file_manager.images))
                    logger.info(f"Displayed image: {image_path}")
                else:
                    logger.error(f"Failed to load image: {image_path}")
            else:
                self.canvas.delete("all")
                messagebox.showinfo("Done", "No more images to display.")
        except Exception as e:
            logger.error(f"Error displaying image: {e}")
            messagebox.showerror("Error", f"Failed to display image: {e}")

    def delete_image(self):
        try:
            self.file_manager.delete_image()
            self.show_image()
        except Exception as e:
            logger.error(f"Error deleting image: {e}")
            messagebox.showerror("Error", f"Failed to delete image: {e}")

    def show_next(self):
        try:
            self.file_manager.next_image()
            self.show_image()
        except Exception as e:
            logger.error(f"Error showing next image: {e}")
            messagebox.showerror("Error", f"Failed to show next image: {e}")

    def show_previous(self):
        try:
            self.file_manager.previous_image()
            self.show_image()
        except Exception as e:
            logger.error(f"Error showing previous image: {e}")
            messagebox.showerror("Error", f"Failed to show previous image: {e}")

    def pause(self):
        logger.info("Paused")
        messagebox.showinfo("Paused", "Processing paused.")

    def resume(self):
        logger.info("Resumed")
        messagebox.showinfo("Resumed", "Processing resumed.")

    def start_over(self):
        if messagebox.askyesno("Confirm", "Are you sure you want to start over?"):
            try:
                self.file_manager.reset()
                self.progress_manager.reset()
                self.show_image()
                logger.info("Session restarted from the beginning.")
            except Exception as e:
                logger.error(f"Error starting over: {e}")
                messagebox.showerror("Error", f"Failed to start over: {e}")

    def generate_report(self):
        try:
            self.reports_manager.generate_report()
            messagebox.showinfo("Report", "Report generated successfully.")
        except Exception as e:
            logger.error(f"Error generating report: {e}")
            messagebox.showerror("Error", f"Failed to generate report: {e}")

    def exit_application(self):
        if messagebox.askokcancel("Exit", "Do you really want to quit?"):
            logger.info("Application exited by user.")
            self.root.quit()

    def on_close(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            logger.info("Application is closing.")
            try:
                self.reports_manager.generate_report()
            except Exception as e:
                logger.error(f"Error generating final report on close: {e}")
            self.root.destroy()