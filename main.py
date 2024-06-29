
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Assumptions:
# 1. Users will input valid binary sequences (only '0' and '1').
# 2. The initial number of signals to be handled by the program is set to three, but users can add more signals as needed.
# 3. The length of the binary sequences for each signal should be equal for the diagram to be generated correctly.

class TimingDiagramGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Timing Diagram Generator")

        self.signals = []
        self.create_widgets()

    def create_widgets(self):
        self.frame = ttk.Frame(self.root, padding="10")
        self.frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        ttk.Label(self.frame, text="Signal Name").grid(row=0, column=0)
        ttk.Label(self.frame, text="Binary Sequence").grid(row=0, column=1)

        self.signal_entries = []
        self.sequence_entries = []

        for i in range(3):  # Start with 3 signals
            self.add_signal_entry()

        self.add_button = ttk.Button(self.frame, text="Add Signal", command=self.add_signal_entry)
        self.add_button.grid(row=len(self.signal_entries), column=0, columnspan=2, pady=5)

        self.plot_button = ttk.Button(self.frame, text="Generate Diagram", command=self.plot_timing_diagram)
        self.plot_button.grid(row=len(self.signal_entries) + 1, column=0, columnspan=2, pady=5)

        self.canvas_frame = ttk.Frame(self.root)
        self.canvas_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    def add_signal_entry(self):
        row = len(self.signal_entries)
        signal_name_entry = ttk.Entry(self.frame)
        signal_name_entry.grid(row=row + 1, column=0, padx=5, pady=2)
        binary_sequence_entry = ttk.Entry(self.frame)
        binary_sequence_entry.grid(row=row + 1, column=1, padx=5, pady=2)

        self.signal_entries.append(signal_name_entry)
        self.sequence_entries.append(binary_sequence_entry)

    def plot_timing_diagram(self):
        self.signals = []
        for signal_entry, sequence_entry in zip(self.signal_entries, self.sequence_entries):
            signal_name = signal_entry.get()
            binary_sequence = sequence_entry.get()
            if signal_name and binary_sequence:
                self.signals.append((signal_name, binary_sequence))

        if not self.signals:
            return

        fig, ax = plt.subplots(figsize=(10, 6))
        for idx, (signal_name, binary_sequence) in enumerate(self.signals):
            time = list(range(len(binary_sequence)))
            values = [int(bit) for bit in binary_sequence]
            ax.step(time, [value + idx * 2 for value in values], where='post', label=signal_name)

        ax.set_yticks([idx * 2 for idx in range(len(self.signals))])
        ax.set_yticklabels([signal_name for signal_name, _ in self.signals])
        ax.set_xlabel("Time")
        ax.set_ylabel("Signals")
        ax.grid(True)
        ax.legend()

        for widget in self.canvas_frame.winfo_children():
            widget.destroy()

        canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=1)

if __name__ == "__main__":
    root = tk.Tk()
    app = TimingDiagramGenerator(root)
    root.mainloop()
