import tkinter as tk
from tkinter import ttk
from algorithms import first_fit, best_fit, next_fit, fcfs, sjf, priority_scheduling

# Color scheme
BG_COLOR = "#2E3440"
FG_COLOR = "#D8DEE9"
ACCENT_COLOR = "#5E81AC"
HIGHLIGHT_COLOR = "#88C0D0"
BUTTON_COLOR = "#434C5E"
ENTRY_COLOR = "#3B4252"

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("CPU Scheduling and Memory Management Algorithms")
        self.geometry("1200x800")
        self.configure(bg=BG_COLOR)
        
        # Configure styles
        self.style = ttk.Style(self)
        self.style.theme_use('clam')
        
        # Configure colors
        self.style.configure('TFrame', background=BG_COLOR)
        self.style.configure('TLabel', background=BG_COLOR, foreground=FG_COLOR, font=('Helvetica', 10))
        self.style.configure('TButton', background=BUTTON_COLOR, foreground=FG_COLOR, 
                           font=('Helvetica', 10, 'bold'), borderwidth=1)
        self.style.map('TButton', 
                      background=[('active', ACCENT_COLOR), ('pressed', HIGHLIGHT_COLOR)])
        self.style.configure('Header.TLabel', font=('Helvetica', 14, 'bold'), foreground=ACCENT_COLOR)
        self.style.configure('Treeview', background=ENTRY_COLOR, fieldbackground=ENTRY_COLOR, 
                           foreground=FG_COLOR, font=('Helvetica', 10))
        self.style.configure('Treeview.Heading', background=ACCENT_COLOR, foreground=FG_COLOR, 
                           font=('Helvetica', 11, 'bold'))
        self.style.map('Treeview', background=[('selected', HIGHLIGHT_COLOR)])
        
        self.current_frame = None
        self.category = None
        self.algorithm = None
        self.data = {}
        self.show_category_selection()

    def show_category_selection(self):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = CategorySelectionFrame(self, self)
        self.current_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

    def show_algorithm_selection(self, category):
        self.category = category
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = AlgorithmSelectionFrame(self, self, category)
        self.current_frame.pack(fill=tk.BOTH, expand=True)

    def show_input_frame(self, algorithm):
        self.algorithm = algorithm
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = InputFrame(self, self, self.category, algorithm)
        self.current_frame.pack(fill=tk.BOTH, expand=True)

    def show_results(self, results):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = ResultsFrame(self, self, results, self.algorithm)
        self.current_frame.pack(fill=tk.BOTH, expand=True)

class CategorySelectionFrame(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, style='TFrame')
        self.controller = controller
        
        container = ttk.Frame(self, style='TFrame')
        container.pack(expand=True)
        
        label = ttk.Label(container, text="Select Category", style='Header.TLabel')
        label.pack(pady=20)
        
        btn_style = {'width': 20, 'padding': 10}
        cpu_btn = ttk.Button(container, text="CPU Scheduling", 
                           command=lambda: controller.show_algorithm_selection("cpu"), **btn_style)
        cpu_btn.pack(pady=10, ipady=5)
        
        mem_btn = ttk.Button(container, text="Memory Management", 
                            command=lambda: controller.show_algorithm_selection("memory"), **btn_style)
        mem_btn.pack(pady=10, ipady=5)

class AlgorithmSelectionFrame(ttk.Frame):
    def __init__(self, parent, controller, category):
        super().__init__(parent, style='TFrame')
        self.controller = controller
        self.category = category
        
        container = ttk.Frame(self, style='TFrame')
        container.pack(expand=True)
        
        label = ttk.Label(container, text="Select Algorithm", style='Header.TLabel')
        label.pack(pady=20)
        
        algorithms = []
        if category == "cpu":
            algorithms = [("FCFS", "fcfs"), ("SJF", "sjf"), ("Priority", "priority")]
        else:
            algorithms = [("First Fit", "first_fit"), ("Best Fit", "best_fit"), ("Next Fit", "next_fit")]
            
        btn_style = {'width': 15, 'padding': 8}
        for name, algo in algorithms:
            btn = ttk.Button(container, text=name, 
                            command=lambda a=algo: controller.show_input_frame(a), **btn_style)
            btn.pack(pady=8, ipady=4)
            
        back_btn = ttk.Button(container, text="Back", command=controller.show_category_selection, 
                             style='TButton', width=10, padding=6)
        back_btn.pack(pady=20, ipady=3)

class InputFrame(ttk.Frame):
    def __init__(self, parent, controller, category, algorithm):
        super().__init__(parent, style='TFrame')
        self.controller = controller
        self.category = category
        self.algorithm = algorithm
        self.step = 0
        self.inputs = {}
        self.widgets = []
        
        self.header = ttk.Label(self, text=self.get_header_text(), style='Header.TLabel')
        self.header.pack(pady=20)
        
        self.content_frame = ttk.Frame(self, style='TFrame')
        self.content_frame.pack(expand=True, fill=tk.BOTH)
        
        self.next_step()

    def get_header_text(self):
        algo_names = {
            'fcfs': "First Come First Served",
            'sjf': "Shortest Job First",
            'priority': "Priority Scheduling",
            'first_fit': "First Fit Memory Allocation",
            'best_fit': "Best Fit Memory Allocation",
            'next_fit': "Next Fit Memory Allocation"
        }
        return f"{algo_names[self.algorithm]} - Input Parameters"

    def next_step(self):
        for widget in self.widgets:
            widget.destroy()
        self.widgets = []
        if self.category == "memory":
            if self.step == 0:
                self.show_memory_blocks_input()
            elif self.step == 1:
                self.show_processes_input()
        else:
            if self.step == 0:
                self.show_process_count_input()
            elif self.step == 1:
                self.show_process_details_input()
        self.step += 1

    def show_memory_blocks_input(self):
        label = ttk.Label(self.content_frame, text="Enter number of memory blocks:")
        label.pack(pady=10)
        self.widgets.append(label)
        
        entry = ttk.Entry(self.content_frame, width=20, font=('Helvetica', 12), 
                         style='TEntry', justify='center')
        entry.pack(pady=10)
        self.widgets.append(entry)
        
        btn = ttk.Button(self.content_frame, text="Next", 
                        command=lambda: self.collect_blocks(entry.get()),
                        style='TButton', width=15)
        btn.pack(pady=15)
        self.widgets.append(btn)

    def collect_blocks(self, num_blocks):
        try:
            self.inputs['num_blocks'] = int(num_blocks)
            self.next_step()
        except ValueError:
            pass

    def show_processes_input(self):
        label = ttk.Label(self.content_frame, text="Enter number of processes:")
        label.pack(pady=10)
        self.widgets.append(label)
        
        entry = ttk.Entry(self.content_frame, width=20, font=('Helvetica', 12),
                         style='TEntry', justify='center')
        entry.pack(pady=10)
        self.widgets.append(entry)
        
        btn = ttk.Button(self.content_frame, text="Next", 
                        command=lambda: self.collect_processes(entry.get()),
                        style='TButton', width=15)
        btn.pack(pady=15)
        self.widgets.append(btn)

    def collect_processes(self, num_processes):
        try:
            self.inputs['num_processes'] = int(num_processes)
            self.show_block_sizes()
        except ValueError:
            pass

    def show_block_sizes(self):
        label = ttk.Label(self.content_frame, text="Enter block sizes:")
        label.pack(pady=10)
        self.widgets.append(label)
        
        self.block_entries = []
        entry_style = {'width': 10, 'font': ('Helvetica', 11), 'justify': 'center'}
        
        for i in range(self.inputs['num_blocks']):
            frame = ttk.Frame(self.content_frame, style='TFrame')
            frame.pack(pady=5)
            
            lbl = ttk.Label(frame, text=f"Block {i+1}:", style='TLabel')
            lbl.pack(side=tk.LEFT, padx=5)
            
            entry = ttk.Entry(frame, **entry_style)
            entry.pack(side=tk.LEFT, padx=5)
            self.block_entries.append(entry)
            self.widgets.append(frame)
            
        btn = ttk.Button(self.content_frame, text="Next", 
                        command=self.collect_block_sizes,
                        style='TButton', width=15)
        btn.pack(pady=20)
        self.widgets.append(btn)

    def collect_block_sizes(self):
        block_sizes = []
        for entry in self.block_entries:
            block_sizes.append(int(entry.get()))
        self.inputs['block_sizes'] = block_sizes
        self.show_process_sizes()

    def show_process_sizes(self):
        label = ttk.Label(self.content_frame, text="Enter process sizes:", style='TLabel')
        label.pack(pady=10)
        self.widgets.append(label)
        
        self.process_entries = []
        entry_style = {'width': 10, 'font': ('Helvetica', 11), 'justify': 'center'}
        
        for i in range(self.inputs['num_processes']):
            frame = ttk.Frame(self.content_frame, style='TFrame')
            frame.pack(pady=5)
            
            lbl = ttk.Label(frame, text=f"Process {i+1}:", style='TLabel')
            lbl.pack(side=tk.LEFT, padx=5)
            
            entry = ttk.Entry(frame, **entry_style)
            entry.pack(side=tk.LEFT, padx=5)
            self.process_entries.append(entry)
            self.widgets.append(frame)
            
        btn = ttk.Button(self.content_frame, text="Run Algorithm", 
                        command=self.collect_process_sizes,
                        style='TButton', width=20)
        btn.pack(pady=20)
        self.widgets.append(btn)

    def collect_process_sizes(self):
        process_sizes = []
        for entry in self.process_entries:
            process_sizes.append(int(entry.get()))
        self.inputs['process_sizes'] = process_sizes
        self.run_algorithm()

    def show_process_count_input(self):
        label = ttk.Label(self.content_frame, text="Enter number of processes:")
        label.pack(pady=10)
        self.widgets.append(label)
        
        entry = ttk.Entry(self.content_frame, width=20, font=('Helvetica', 12),
                         style='TEntry', justify='center')
        entry.pack(pady=10)
        self.widgets.append(entry)
        
        btn = ttk.Button(self.content_frame, text="Next", 
                        command=lambda: self.collect_process_count(entry.get()),
                        style='TButton', width=15)
        btn.pack(pady=15)
        self.widgets.append(btn)

    def collect_process_count(self, num_processes):
        try:
            self.inputs['num_processes'] = int(num_processes)
            self.next_step()
        except ValueError:
            pass

    def show_process_details_input(self):
        self.entries = []
        entry_style = {'width': 8, 'font': ('Helvetica', 11), 'justify': 'center'}
        
        if self.algorithm in ['fcfs', 'sjf']:
            for i in range(self.inputs['num_processes']):
                frame = ttk.Frame(self.content_frame, style='TFrame')
                frame.pack(pady=5)
                
                lbl_at = ttk.Label(frame, text=f"P{i+1} Arrival:", style='TLabel')
                lbl_at.pack(side=tk.LEFT, padx=5)
                entry_at = ttk.Entry(frame, **entry_style)
                entry_at.pack(side=tk.LEFT, padx=5)
                
                lbl_bt = ttk.Label(frame, text="Burst:", style='TLabel')
                lbl_bt.pack(side=tk.LEFT, padx=5)
                entry_bt = ttk.Entry(frame, **entry_style)
                entry_bt.pack(side=tk.LEFT, padx=5)
                
                self.entries.append((entry_at, entry_bt))
                self.widgets.append(frame)
                
        elif self.algorithm == 'priority':
            for i in range(self.inputs['num_processes']):
                frame = ttk.Frame(self.content_frame, style='TFrame')
                frame.pack(pady=5)
                
                lbl_bt = ttk.Label(frame, text=f"P{i+1} Burst:", style='TLabel')
                lbl_bt.pack(side=tk.LEFT, padx=5)
                entry_bt = ttk.Entry(frame, **entry_style)
                entry_bt.pack(side=tk.LEFT, padx=5)
                
                lbl_prio = ttk.Label(frame, text="Priority:", style='TLabel')
                lbl_prio.pack(side=tk.LEFT, padx=5)
                entry_prio = ttk.Entry(frame, **entry_style)
                entry_prio.pack(side=tk.LEFT, padx=5)
                
                self.entries.append((entry_bt, entry_prio))
                self.widgets.append(frame)
                
        btn = ttk.Button(self.content_frame, text="Run Algorithm", 
                        command=self.collect_process_details,
                        style='TButton', width=20)
        btn.pack(pady=20)
        self.widgets.append(btn)

    def collect_process_details(self):
        arrival_times = []
        burst_times = []
        priorities = []
        
        if self.algorithm in ['fcfs', 'sjf']:
            for entry_at, entry_bt in self.entries:
                arrival_times.append(int(entry_at.get()))
                burst_times.append(int(entry_bt.get()))
            self.inputs['arrival_times'] = arrival_times
            self.inputs['burst_times'] = burst_times
        elif self.algorithm == 'priority':
            for entry_bt, entry_prio in self.entries:
                burst_times.append(int(entry_bt.get()))
                priorities.append(int(entry_prio.get()))
            self.inputs['burst_times'] = burst_times
            self.inputs['priorities'] = priorities
            
        self.run_algorithm()

    def run_algorithm(self):
        if self.category == "memory":
            block_sizes = self.inputs['block_sizes']
            process_sizes = self.inputs['process_sizes']
            if self.algorithm == 'first_fit':
                result = first_fit(block_sizes, process_sizes)
            elif self.algorithm == 'best_fit':
                result = best_fit(block_sizes, process_sizes)
            elif self.algorithm == 'next_fit':
                result = next_fit(block_sizes, process_sizes)
        else:
            if self.algorithm == 'fcfs':
                result = fcfs(self.inputs['arrival_times'], self.inputs['burst_times'])
            elif self.algorithm == 'sjf':
                result = sjf(self.inputs['arrival_times'], self.inputs['burst_times'])
            elif self.algorithm == 'priority':
                result = priority_scheduling(self.inputs['burst_times'], self.inputs['priorities'])
                
        self.controller.show_results(result)

class ResultsFrame(ttk.Frame):
    def __init__(self, parent, controller, results, algorithm):
        super().__init__(parent, style='TFrame')
        self.controller = controller
        self.results = results
        self.algorithm = algorithm
        
        self.container = ttk.Frame(self, style='TFrame')
        self.container.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)
        
        self.create_widgets()

    def create_widgets(self):
        header_text = "Results - " + ("Memory Allocation" if self.algorithm in ['first_fit', 'best_fit', 'next_fit'] 
                                     else "CPU Scheduling")
        header = ttk.Label(self.container, text=header_text, style='Header.TLabel')
        header.pack(pady=15)
        
        if self.algorithm in ['first_fit', 'best_fit', 'next_fit']:
            self.show_memory_results()
        else:
            self.show_cpu_results()
            
        back_btn = ttk.Button(self.container, text="Back to Start", 
                             command=self.controller.show_category_selection,
                             style='TButton', width=15)
        back_btn.pack(pady=20)

    def show_memory_results(self):
        scroll_frame = ttk.Frame(self.container, style='TFrame')
        scroll_frame.pack(expand=True, fill=tk.BOTH)
        
        tree = ttk.Treeview(scroll_frame, columns=("Process No.", "Process Size", "Block No."), 
                          show='headings', height=10)
        
        tree.column("Process No.", width=100, anchor='center')
        tree.column("Process Size", width=150, anchor='center')
        tree.column("Block No.", width=150, anchor='center')
        
        tree.heading("Process No.", text="Process No.")
        tree.heading("Process Size", text="Process Size")
        tree.heading("Block No.", text="Block No.")
        
        for i in range(len(self.results['process_sizes'])):
            process_no = i + 1
            size = self.results['process_sizes'][i]
            block_no = self.results['allocation'][i] + 1 if self.results['allocation'][i] != -1 else "Not Allocated"
            tree.insert('', 'end', values=(process_no, size, block_no))
            
        vsb = ttk.Scrollbar(scroll_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=vsb.set)
        
        tree.grid(row=0, column=0, sticky='nsew')
        vsb.grid(row=0, column=1, sticky='ns')
        scroll_frame.grid_columnconfigure(0, weight=1)
        scroll_frame.grid_rowconfigure(0, weight=1)
        
        remaining_frame = ttk.Frame(self.container, style='TFrame')
        remaining_frame.pack(pady=15)
        
        ttk.Label(remaining_frame, text="Remaining Block Sizes:", style='TLabel').pack(side=tk.LEFT)
        ttk.Label(remaining_frame, text=str(self.results['remaining_blocks']), 
                 style='TLabel', foreground=HIGHLIGHT_COLOR).pack(side=tk.LEFT, padx=10)

    def show_cpu_results(self):
        scroll_frame = ttk.Frame(self.container, style='TFrame')
        scroll_frame.pack(expand=True, fill=tk.BOTH)
        
        columns = ("PID", "Arrival", "Burst", "Completion", "TAT", "WT")
        tree = ttk.Treeview(scroll_frame, columns=columns, show='headings', height=10)
        
        col_widths = [60, 80, 80, 100, 80, 80]
        for col, width in zip(columns, col_widths):
            tree.column(col, width=width, anchor='center')
            tree.heading(col, text=col)
            
        for process in self.results['processes']:
            values = (
                process['pid'],
                process.get('at', ''),
                process['bt'],
                process.get('ct', ''),
                process['tat'],
                process['wt']
            )
            tree.insert('', 'end', values=values)
            
        vsb = ttk.Scrollbar(scroll_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=vsb.set)
        
        tree.grid(row=0, column=0, sticky='nsew')
        vsb.grid(row=0, column=1, sticky='ns')
        scroll_frame.grid_columnconfigure(0, weight=1)
        scroll_frame.grid_rowconfigure(0, weight=1)
        
        avg_frame = ttk.Frame(self.container, style='TFrame')
        avg_frame.pack(pady=15)
        
        ttk.Label(avg_frame, text="Average Waiting Time:", style='TLabel').pack(side=tk.LEFT)
        ttk.Label(avg_frame, text=f"{self.results.get('avg_wt', 0):.2f}", 
                 style='TLabel', foreground=HIGHLIGHT_COLOR).pack(side=tk.LEFT, padx=10)
        
        ttk.Label(avg_frame, text="Average Turnaround Time:", style='TLabel').pack(side=tk.LEFT, padx=20)
        ttk.Label(avg_frame, text=f"{self.results.get('avg_tat', 0):.2f}", 
                 style='TLabel', foreground=HIGHLIGHT_COLOR).pack(side=tk.LEFT)

        if 'timeline' in self.results:
            timeline_frame = ttk.Frame(self.container, style='TFrame')
            timeline_frame.pack(pady=10)
            
            ttk.Label(timeline_frame, text="Execution Timeline:", style='TLabel').pack(side=tk.LEFT)
            ttk.Label(timeline_frame, text=str(self.results['timeline']), 
                     style='TLabel', foreground=HIGHLIGHT_COLOR).pack(side=tk.LEFT, padx=10)

if __name__ == "__main__":
    app = App()
    app.mainloop()