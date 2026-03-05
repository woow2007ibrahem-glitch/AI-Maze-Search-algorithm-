import tkinter as tk
from tkinter import filedialog, messagebox
import random

class MazeViewer:
    def __init__(self, map_server):
        self.map = map_server
        self.cell_size = 40
        self.margin = 20

        # Initialize Main Window
        self.root = tk.Tk()
        self.root.title("Maze Viewer")

        # Create the Canvas
        self.canvas = tk.Canvas(self.root, bg="white")
        self.canvas.pack()

        # Update window size based on maze dimensions
        self.resize_window()

        # --- ADD MENU BAR TO TEST METHODS ---
        self.create_menus()

        # Initial Draw
        self.draw()

        # Start the GUI loop
        self.root.mainloop()

    def resize_window(self):
        """Calculates width/height based on rows/cols and resizes the canvas."""
        width = self.map.cols * self.cell_size + 2 * self.margin
        height = self.map.rows * self.cell_size + 2 * self.margin
        self.canvas.config(width=width, height=height)

    def create_menus(self):
        """Creates a top menu bar to test MapServer methods."""
        menubar = tk.Menu(self.root)

        # 1. File Menu (Save / Load)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Save to JSON", command=self.save_maze_action)
        file_menu.add_command(label="Load from JSON", command=self.load_maze_action)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        menubar.add_cascade(label="File", menu=file_menu)

        # 2. Test Menu (Generate / Assign)
        test_menu = tk.Menu(menubar, tearoff=0)
        test_menu.add_command(label="Generate New Maze", command=self.generate_new_action)
        # CHANGED: Pointing to the new Custom Dialog method
        test_menu.add_command(label="Assign Custom Positions...", command=self.custom_assign_action)
        menubar.add_cascade(label="Test Methods", menu=test_menu)

        self.root.config(menu=menubar)

    # ==========================================
    # DRAWING LOGIC
    # ==========================================
    def draw(self):
        self.canvas.delete("all")  # Clear screen

        self.draw_red_border()
        self.draw_grid_walls()
        self.draw_markers()

    def draw_red_border(self):
        # Draw only the Red Border (Text removed as requested)
        w = self.map.cols * self.cell_size
        h = self.map.rows * self.cell_size
        x1 = self.margin
        y1 = self.margin
        x2 = x1 + w
        y2 = y1 + h

        self.canvas.create_rectangle(x1, y1, x2, y2, outline="red", width=2)

    def draw_grid_walls(self):
        for r in range(self.map.rows):
            for c in range(self.map.cols):
                # Calculate pixel position for this cell
                x = self.margin + c * self.cell_size
                y = self.margin + r * self.cell_size
                cs = self.cell_size

                # Get cell data from MapServer
                cell = self.map.getRoom(r, c)
                walls = cell["walls"]  # [Right, Top, Left, Down]

                # Draw Walls (Black Lines)
                # Right (Index 0)
                if walls[0] == 1:
                    self.canvas.create_line(x + cs, y, x + cs, y + cs, width=2)
                # Top (Index 1)
                if walls[1] == 1:
                    self.canvas.create_line(x, y, x + cs, y, width=2)
                # Left (Index 2)
                if walls[2] == 1:
                    self.canvas.create_line(x, y, x, y + cs, width=2)
                # Down (Index 3)
                if walls[3] == 1:
                    self.canvas.create_line(x, y + cs, x + cs, y + cs, width=2)

    def draw_markers(self):
        # Draw Start (S) - Green
        self.draw_circle(self.map.start_pos, "green", "S")

        # Draw Object (O) - Blue
        self.draw_circle(self.map.object_pos, "blue", "O")

        # Draw Target (T) - Red
        self.draw_circle(self.map.target_pos, "red", "T")

    def draw_circle(self, pos, color, label):
        if pos is None: return

        r, c = pos  # unpack (row, col)

        x = self.margin + c * self.cell_size + self.cell_size / 2
        y = self.margin + r * self.cell_size + self.cell_size / 2
        radius = self.cell_size * 0.3

        self.canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill=color, outline="black")
        self.canvas.create_text(x, y, text=label, fill="white", font=("Arial", 12, "bold"))

    # ==========================================
    # EVENT HANDLERS (TESTING METHODS)
    # ==========================================
    def save_maze_action(self):
        filename = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if filename:
            self.map.save_to_file(filename)
            messagebox.showinfo("Success", f"Maze saved to {filename}")

    def load_maze_action(self):
        filename = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if filename:
            self.map.load_from_file(filename)
            self.resize_window()  # Size might change
            self.draw()  # Redraw new maze

    def generate_new_action(self):
        self.map.generate_maze()
        self.draw()

    def custom_assign_action(self):
        """Opens a popup window to manually enter coordinates."""
        dialog = tk.Toplevel(self.root)
        dialog.title("Assign Coordinates")
        dialog.geometry("300x250")

        # Helper to create label+entry rows
        entries = {}
        row_idx = 0

        labels = ["Start Row", "Start Col", "Object Row", "Object Col", "Target Row", "Target Col"]
        # Get current values to pre-fill the boxes
        current_vals = [
            self.map.start_pos[0], self.map.start_pos[1],
            self.map.object_pos[0], self.map.object_pos[1],
            self.map.target_pos[0], self.map.target_pos[1]
        ]

        for label_text, val in zip(labels, current_vals):
            tk.Label(dialog, text=label_text).grid(row=row_idx, column=0, padx=10, pady=5)
            entry = tk.Entry(dialog)
            entry.insert(0, str(val))
            entry.grid(row=row_idx, column=1, padx=10, pady=5)
            entries[label_text] = entry
            row_idx += 1

        def apply_changes():
            try:
                # Read all inputs
                sr = int(entries["Start Row"].get())
                sc = int(entries["Start Col"].get())
                or_ = int(entries["Object Row"].get())
                oc = int(entries["Object Col"].get())
                tr = int(entries["Target Row"].get())
                tc = int(entries["Target Col"].get())

                # Apply to map
                self.map.assign_objects(sr, sc, or_, oc, tr, tc)
                self.draw()  # Redraw
                dialog.destroy()  # Close popup
            except ValueError:
                messagebox.showerror("Error", "Please enter valid integers.")

        submit_btn = tk.Button(dialog, text="Apply Changes", command=apply_changes, bg="#dddddd")
        submit_btn.grid(row=row_idx, column=0, columnspan=2, pady=15)