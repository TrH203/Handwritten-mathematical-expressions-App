from pathlib import Path
import pyautogui
import subprocess
import io
import matplotlib.pyplot as plt
import tkinter as tk
import win32clipboard
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
from PIL import Image, ImageTk, ImageGrab


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = str(OUTPUT_PATH) + str(Path(r"\assets\frame0"))

class MyApp:

    def relative_to_assets(self, path: str) -> Path:
        return ASSETS_PATH / Path(path)

    def __init__(self, root):
        self.root = root
        self.root.geometry("864x540")
        self.root.configure(bg="#F1E1C7")

        self.canvas = Canvas(
            self.root,
            bg="#F1E1C7",
            height=540,
            width=864,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.place(x=0, y=0)

        self.canvas.create_rectangle(
            0.0,
            0.0,
            864.0,
            60.0,
            fill="#260D13",
            outline=""
        )

        self.canvas.create_text(
            363.0,
            12.0,
            anchor="nw",
            text="HMER",
            fill="#F1E1C7",
            font=("JustAnotherHand Regular", 32 * -1)
        )

        # Images setup
        self.image_image_1 = PhotoImage(file=self.relative_to_assets("image_1.png"))
        self.image_1 = self.canvas.create_image(217.0, 231.0, image=self.image_image_1)

        self.image_image_2 = PhotoImage(file=self.relative_to_assets("image_2.png"))
        self.image_2 = self.canvas.create_image(649.0, 231.0, image=self.image_image_2)

        # Buttons setup
        self.button_image_1 = PhotoImage(file=self.relative_to_assets("button_1.png"))
        self.button_1 = tk.Button(
            image=self.button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=self.snip_function,  # Replace with your snip function call
            relief="flat"
        )
        self.button_1.place(x=38.0, y=447.0, width=100.0, height=50.0)

        self.button_image_2 = PhotoImage(file=self.relative_to_assets("button_2.png"))
        self.button_2 = tk.Button(
            image=self.button_image_2,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_2 clicked"),
            relief="flat"
        )
        self.button_2.place(x=210.0, y=447.0, width=100.0, height=50.0)

        self.button_image_3 = PhotoImage(file=self.relative_to_assets("button_3.png"))
        self.button_3 = tk.Button(
            image=self.button_image_3,
            borderwidth=0,
            highlightthickness=0,
            command= self.update_image_2,
            relief="flat"
        )
        self.button_3.place(x=382.0, y=447.0, width=100.0, height=50.0)

        self.button_image_4 = PhotoImage(file=self.relative_to_assets("button_4.png"))
        self.button_4 = tk.Button(
            image=self.button_image_4,
            borderwidth=0,
            highlightthickness=0,
            command=self.copy_to_clipboard,
            relief="flat"
        )
        self.button_4.place(x=554.0, y=447.0, width=100.0, height=50.0)

        self.button_image_5 = PhotoImage(file=self.relative_to_assets("button_5.png"))
        self.button_5 = tk.Button(
            image=self.button_image_5,
            borderwidth=0,
            highlightthickness=0,
            command=self.copy_image_to_clipboard,
            relief="flat"
        )
        self.button_5.place(x=726.0, y=447.0, width=100.0, height=50.0)

        # Entry setup
        self.canvas.create_rectangle(120.0, 371.0, 744.0, 412.0, fill="#FFFFFF", outline="")
        self.entry_image_1 = PhotoImage(file=self.relative_to_assets("entry_1.png"))
        self.entry_bg_1 = self.canvas.create_image(432.0, 391.5, image=self.entry_image_1)
        self.entry_1 = Entry(
            bd=0,
            bg="#f2f0f0",
            fg="#000000",
            highlightthickness=0
        )
        self.entry_1.place(x=125.0, y=377.0, width=614.0, height=27.0)
#---------------------------------------------------------------------

    #region BUTTON_1:snip
    def snip_function(self):
        # Minimize the app window
        self.root.withdraw()

    #     # Capture a screenshot of the current desktop
    #     self.screenshot = pyautogui.screenshot()

    #     # Create a new fullscreen window to display the screenshot
    #     self.snip_window = tk.Toplevel(self.root)
    #     self.snip_window.attributes("-fullscreen", True)
    #     self.snip_window.attributes("-topmost", True)

    #     # Convert screenshot to a Tkinter-compatible image and display it
    #     screenshot_image = ImageTk.PhotoImage(self.screenshot)
    #     self.label = tk.Label(self.snip_window, image=screenshot_image)
    #     self.label.image = screenshot_image  # Keep a reference to prevent garbage collection
    #     self.label.pack(fill=tk.BOTH, expand=True)        

        # Capture a screenshot of the current desktop
        self.screenshot = pyautogui.screenshot()

        # Create a new fullscreen window to display the screenshot
        self.snip_window = tk.Toplevel(self.root)
        self.snip_window.attributes("-fullscreen", True)
        self.snip_window.attributes("-topmost", True)

        # Convert screenshot to a Tkinter-compatible image
        self.screenshot_image = ImageTk.PhotoImage(self.screenshot)

        # Create a canvas for drawing the screenshot and snipping rectangle
        self.rect_canvas = tk.Canvas(self.snip_window, cursor="cross")
        self.rect_canvas.place(relx=0, rely=0, relwidth=1, relheight=1)

        # Display the screenshot as a background on the canvas
        self.rect_canvas.create_image(0, 0, image=self.screenshot_image, anchor="nw")

        # Bind mouse events to initiate, draw, and complete the snipping
        self.rect_canvas.bind("<ButtonPress-1>", self.start_snip)
        self.rect_canvas.bind("<B1-Motion>", self.update_rectangle)
        self.rect_canvas.bind("<ButtonRelease-1>", self.complete_snip)

    def start_snip(self, event):
        # Capture the starting coordinates of the snip area (top-left corner)
        self.start_x = event.x
        self.start_y = event.y

        # Create a rectangle placeholder on the canvas
        self.rect = self.rect_canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline="red", width=2, fill="")

    def update_rectangle(self, event):
        # Update the rectangle's size dynamically as the mouse moves
        self.rect_canvas.coords(self.rect, self.start_x, self.start_y, event.x, event.y)

    def complete_snip(self, event):
        # Capture the ending coordinates of the snip area (bottom-right corner)
        self.end_x = event.x
        self.end_y = event.y

        # Destroy the snip window and proceed with cropping
        self.snip_window.destroy()
        self.snip()

    def snip(self):
        # Ensure we have valid coordinates
        if self.start_x and self.start_y and self.end_x and self.end_y:
            x1, y1 = min(self.start_x, self.end_x), min(self.start_y, self.end_y)
            x2, y2 = max(self.start_x, self.end_x), max(self.start_y, self.end_y)

            # Crop the screenshot to the selected region
            cropped_image = self.screenshot.crop((x1, y1, x2, y2))
            # cropped_image.show()  # Display the snipped image, or you can save it

            # Define the target size of image_1 (replace with your predefined size)
            target_width, target_height = 373, 210  # Example size (modify as needed)

            # Resize the cropped image to fit into the predefined size (maintaining aspect ratio)
            cropped_image = cropped_image.resize((target_width, target_height))

            # Convert the cropped image to a format Tkinter can use
            self.cropped_tk_image = ImageTk.PhotoImage(cropped_image)

            # Update the canvas image (self.image_1) with the new resized image
            self.canvas.itemconfig(self.image_1, image=self.cropped_tk_image)
        # Restore the main window
        self.root.deiconify()
        
    #endregion
    #-----------------------------------------------------------------

    #region BUTTON_3: convert
    def latex_to_png(self, latex_str):
    # Create a figure and turn off axis
        fig, ax = plt.subplots()
        ax.axis("off")

        # Add LaTeX string to the plot and suppress the output
        _ = ax.text(0.5, 0.5, f"${latex_str}$", size=50, ha="center", va="center")

        # Save the figure to a BytesIO buffer
        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format="png", bbox_inches="tight", pad_inches=0.1)

        # Clear the current figure to suppress interactive output
        plt.gcf().clear()

        # Seek to the beginning of the buffer before opening it as an image
        img_buffer.seek(0)
        im = Image.open(img_buffer).copy()  # Fully load the image into memory

        # Close the buffer after the image has been loaded
        img_buffer.close()

        return im
    
    def update_image_2(self):
        # # Get the text from entry_1
        latex_str = self.entry_1.get()

        # Convert the LaTeX string to a PNG image
        self.image_2_pil = self.latex_to_png(latex_str)

        # Define the target size of image_1 (replace with your predefined size)
        target_width, target_height = 373, 210  # Example size (modify as needed)

        # Resize the cropped image to fit into the predefined size (maintaining aspect ratio)
        resized_img = self.image_2_pil.resize((target_width, target_height))

        
        # Convert the image to a format Tkinter can use
        self.image_2_tk = ImageTk.PhotoImage(resized_img)

        # Update the canvas image (self.image_2) with the new image
        self.canvas.itemconfig(self.image_2, image=self.image_2_tk)
        
    #endregion
    #-----------------------------------------------------------------
    
    #region BUTTON_4: save latex to clipboard
    def copy_to_clipboard(self):
        # Get the text from entry_1
        text_to_copy = self.entry_1.get()

        # Clear the clipboard and append the new text
        self.root.clipboard_clear()
        self.root.clipboard_append(text_to_copy)

        # (Optional) Show a message that text is copied
        print(f"Copied to clipboard: {text_to_copy}")

    #endregion
    #-----------------------------------------------------------------

    #region BUTTON_5: save img to clipboard
    def copy_image_to_clipboard(self):
        # Check if there is an image currently displayed at image_2
        if hasattr(self, 'image_2_pil'):
            try:
                # Convert the PIL image to a format suitable for the clipboard (DIB format)
                output = io.BytesIO()
                self.image_2_pil.convert("RGB").save(output, "BMP")
                data = output.getvalue()[14:]  # BMP files have a 14-byte header we need to remove
                output.close()

                # Set the image to the clipboard
                win32clipboard.OpenClipboard()
                win32clipboard.EmptyClipboard()
                win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
                win32clipboard.CloseClipboard()

                print("Image copied to clipboard.")
            except Exception as e:
                print(f"Failed to copy image to clipboard: {e}")
        else:
            print("No image found in image_2.")
    #endregion
    #-----------------------------------------------------------------
# Running the app
if __name__ == "__main__":
    root = tk.Tk()
    app = MyApp(root)
    root.mainloop()
