import tkinter as tk
from tkinter import ttk
import heapq

class CompactNetworkSimulation:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Route Finder: Viewport-Safe Mesh Network")
        # Optimized window dimensions to fit smaller screens perfectly
        self.root.geometry("1020x600")
        self.root.configure(bg="#f8f9fa")

        # 1. 12 Nodes Coordinates - Compressed and padded away from canvas edges
        self.locations = {
            'Kirtipur': (50, 310),    'Balkhu': (60, 200),      'Kalimati': (140, 100),
            'Ratnapark': (260, 60),   'Sanepa': (170, 270),     'Kathmandu': (280, 170),
            'Pulchowk': (280, 370),   'Lalitpur': (420, 340),   'Baneshwor': (440, 190),
            'Chabahil': (440, 70),    'Koteshwor': (560, 260),  'Thimi': (650, 190)
        }

        # 2. Optimized Cross-Connected Roads Matrix
        self.base_edges = [
            ('Kirtipur', 'Balkhu', 4),      ('Kirtipur', 'Sanepa', 6),
            ('Balkhu', 'Kalimati', 5),      ('Balkhu', 'Sanepa', 3),
            ('Kalimati', 'Ratnapark', 4),   ('Kalimati', 'Kathmandu', 3),
            ('Ratnapark', 'Chabahil', 7),   ('Ratnapark', 'Kathmandu', 2),
            ('Sanepa', 'Pulchowk', 2),      ('Sanepa', 'Kathmandu', 5),
            ('Kathmandu', 'Pulchowk', 4),   ('Kathmandu', 'Baneshwor', 4),
            ('Pulchowk', 'Lalitpur', 3),    ('Lalitpur', 'Koteshwor', 6),
            ('Baneshwor', 'Chabahil', 5),   ('Baneshwor', 'Koteshwor', 3),
            ('Chabahil', 'Koteshwor', 8),   ('Koteshwor', 'Thimi', 5)
        ]

        # Convert to standardized edge configurations lookup dictionary
        self.edge_configs = {}
        for u, v, d in self.base_edges:
            key = tuple(sorted((u, v)))
            self.edge_configs[key] = {'distance': d, 'traffic': 'Normal (1.5x)'}

        self.traffic_multipliers = {
            'Light (1.0x)': 1.0, 'Normal (1.5x)': 1.5, 'Heavy (2.0x)': 2.0, 'Severe (3.0x)': 3.0
        }

        # Dynamic Route States
        self.agent_state = 'Kirtipur'
        self.source_state = 'Kirtipur'
        self.goal_state = 'Koteshwor'
        
        self.planned_path = []
        self.full_calculated_path = []
        self.is_navigating = False
        self.animation_speed = 1000

        # UI Canvas Component Trackers
        self.node_objects = {}
        self.text_objects = {}
        self.edge_line_objects = {}
        self.edge_text_objects = {}
        self.ui_controls = {}

        self.build_layout()
        self.draw_graph()
        self.update_visuals()

    def build_layout(self):
        # Configuration Sidebar Parameters Panel
        left_panel = tk.Frame(self.root, width=330, bg="#ffffff", bd=1, relief=tk.SOLID)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
        left_panel.pack_propagate(False)

        right_panel = tk.Frame(self.root, bg="#f8f9fa")
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        tk.Label(left_panel, text="Network Road Weights", font=("Helvetica", 12, "bold"), bg="#ffffff", fg="#1e293b").pack(pady=10)

        scroll_canvas = tk.Canvas(left_panel, bg="#ffffff", highlightthickness=0)
        scrollbar = ttk.Scrollbar(left_panel, orient="vertical", command=scroll_canvas.yview)
        scroll_frame = tk.Frame(scroll_canvas, bg="#ffffff")
        scroll_frame.bind("<Configure>", lambda e: scroll_canvas.configure(scrollregion=scroll_canvas.bbox("all")))
        scroll_canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        scroll_canvas.configure(yscrollcommand=scrollbar.set)
        scroll_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        for edge in sorted(self.edge_configs.keys()):
            data = self.edge_configs[edge]
            lbl_frame = tk.LabelFrame(scroll_frame, text=f" {edge[0]} ↔ {edge[1]} ", font=("Helvetica", 8, "bold"), bg="#ffffff", fg="#475569")
            lbl_frame.pack(fill=tk.X, padx=5, pady=4)

            dist_slider = tk.Scale(
                lbl_frame, from_=1, to=20, orient=tk.HORIZONTAL, bg="#ffffff", troughcolor="#f1f5f9", highlightthickness=0, font=("Helvetica", 8),
                command=lambda val, e=edge: self.on_parameter_changed(e, 'distance', val)
            )
            dist_slider.set(data['distance'])
            dist_slider.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=4)

            traffic_combo = ttk.Combobox(lbl_frame, values=list(self.traffic_multipliers.keys()), state="readonly", font=("Helvetica", 8), width=11)
            traffic_combo.set(data['traffic'])
            traffic_combo.pack(side=tk.RIGHT, padx=4, pady=5)
            traffic_combo.bind("<<ComboboxSelected>>", lambda event, e=edge, cb=traffic_combo: self.on_parameter_changed(e, 'traffic', cb.get()))

            self.ui_controls[edge] = (dist_slider, traffic_combo)

        # Right Simulation Visualization Layout Panel
        tk.Label(right_panel, text="AI Pathfinding Simulation (Dijkstra Optimization)", font=("Helvetica", 14, "bold"), bg="#f8f9fa", fg="#1a73e8").pack(pady=5)

        control_strip = tk.Frame(right_panel, bg="#f8f9fa")
        control_strip.pack(pady=5)

        tk.Label(control_strip, text="Start Point: ", font=("Helvetica", 9, "bold"), bg="#f8f9fa").grid(row=0, column=0, padx=2)
        self.start_selector = ttk.Combobox(control_strip, values=sorted(list(self.locations.keys())), state="readonly", width=12)
        self.start_selector.set(self.agent_state)
        self.start_selector.grid(row=0, column=1, padx=5)
        self.start_selector.bind("<<ComboboxSelected>>", self.on_endpoints_changed)

        tk.Label(control_strip, text=" Destination: ", font=("Helvetica", 9, "bold"), bg="#f8f9fa").grid(row=0, column=2, padx=2)
        self.goal_selector = ttk.Combobox(control_strip, values=sorted(list(self.locations.keys())), state="readonly", width=12)
        self.goal_selector.set(self.goal_state)
        self.goal_selector.grid(row=0, column=3, padx=5)
        self.goal_selector.bind("<<ComboboxSelected>>", self.on_endpoints_changed)

        self.nav_btn = tk.Button(control_strip, text="Run Path Search", font=("Helvetica", 9, "bold"), bg="#10b981", fg="white", padx=12, command=self.start_navigation)
        self.nav_btn.grid(row=0, column=4, padx=15)

        # FIX: Removed the non-existent 'width_propagate' option to fix the TclError
        self.canvas = tk.Canvas(right_panel, width=700, bg="#ffffff", bd=1, relief=tk.SOLID)
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        legend_label = tk.Label(
            right_panel, 
            text="Legend:  🔮 Pink = Source  |  🎯 Yellow = Destination  |  🔥 Orange Edge = Remaining  |  🍏 Green Edge = Traveled",
            font=("Helvetica", 9), bg="#f8f9fa", fg="#1e293b"
        )
        legend_label.pack(pady=2)

        self.status_log = tk.Label(right_panel, text="System Ready.", font=("Helvetica", 10, "italic"), bg="#f8f9fa", fg="#475569")
        self.status_log.pack(pady=2)

    def draw_graph(self):
        self.canvas.delete("all")
        
        # Render connecting edge vector lines
        for edge in self.edge_configs:
            u, v = edge
            x1, y1 = self.locations[u]
            x2, y2 = self.locations[v]
            self.edge_line_objects[edge] = self.canvas.create_line(x1, y1, x2, y2, fill="#cbd5e1", width=2)
            self.edge_text_objects[edge] = self.canvas.create_text((x1+x2)/2, (y1+y2)/2 - 8, text="", font=("Helvetica", 7, "bold"), fill="#64748b")
            
        # Render city circle nodes
        radius = 20
        for name, (x, y) in self.locations.items():
            self.node_objects[name] = self.canvas.create_oval(x-radius, y-radius, x+radius, y+radius, fill="#f8fafc", outline="#cbd5e1", width=2)
            self.text_objects[name] = self.canvas.create_text(x, y, text=name, font=("Helvetica", 8, "bold"), fill="#334155")

    def update_visuals(self):
        """Updates graph text overlays and re-colors paths based on navigation state."""
        for edge, data in self.edge_configs.items():
            cost = data['distance'] * self.traffic_multipliers[data['traffic']]
            self.canvas.itemconfig(self.edge_text_objects[edge], text=f"{cost:.1f}")
            self.canvas.itemconfig(self.edge_line_objects[edge], fill="#cbd5e1", width=2)

        if len(self.full_calculated_path) > 1:
            remaining_segment = [self.agent_state] + self.planned_path
            for i in range(len(self.full_calculated_path) - 1):
                u = self.full_calculated_path[i]
                v = self.full_calculated_path[i+1]
                edge_sig = (u, v) if (u, v) in self.edge_line_objects else (v, u)

                if edge_sig in self.edge_line_objects:
                    if u in remaining_segment and v in remaining_segment:
                        u_idx, v_idx = remaining_segment.index(u), remaining_segment.index(v)
                        if abs(u_idx - v_idx) == 1:
                            self.canvas.itemconfig(self.edge_line_objects[edge_sig], fill="#f97316", width=5) # Orange (Upcoming)
                            continue
                    self.canvas.itemconfig(self.edge_line_objects[edge_sig], fill="#10b981", width=5) # Green (Traveled)

        for name in self.locations:
            node = self.node_objects[name]
            text = self.text_objects[name]

            if name == self.agent_state:
                self.canvas.itemconfig(node, fill="#22c55e", outline="#15803d", width=3)
                self.canvas.itemconfig(text, fill="#ffffff", text=f"🤖\n{name}")
            elif name == self.goal_state:
                self.canvas.itemconfig(node, fill="#eab308", outline="#a16207", width=3)
                self.canvas.itemconfig(text, fill="#1e293b", text=f"🎯\n{name}")
            elif name == self.source_state:
                self.canvas.itemconfig(node, fill="#f472b6", outline="#db2777", width=3)
                self.canvas.itemconfig(text, fill="#ffffff", text=f"🔮\n{name}")
            elif name in self.full_calculated_path:
                self.canvas.itemconfig(node, fill="#ffedd5", outline="#f97316", width=2)
                self.canvas.itemconfig(text, fill="#1e293b", text=name)
            else:
                self.canvas.itemconfig(node, fill="#f8fafc", outline="#cbd5e1", width=2)
                self.canvas.itemconfig(text, fill="#334155", text=name)

    def on_parameter_changed(self, edge, key, value):
        if self.is_navigating: return
        self.edge_configs[edge][key] = int(value) if key == 'distance' else value
        self.full_calculated_path = []
        self.update_visuals()

    def on_endpoints_changed(self, event):
        if self.is_navigating: return
        self.agent_state = self.start_selector.get()
        self.source_state = self.agent_state
        self.goal_state = self.goal_selector.get()
        self.full_calculated_path = []
        self.update_visuals()

    def compute_dijkstra_path(self, start, goal):
        graph = {node: [] for node in self.locations}
        for (u, v), data in self.edge_configs.items():
            cost = data['distance'] * self.traffic_multipliers[data['traffic']]
            graph[u].append((v, cost))
            graph[v].append((u, cost))

        queue = [(0.0, start, [start])]
        distances = {node: float('inf') for node in self.locations}
        distances[start] = 0.0

        while queue:
            curr_cost, current, path = heapq.heappop(queue)
            if current == goal: return path, curr_cost
            if curr_cost > distances[current]: continue

            for neighbor, weight in graph[current]:
                new_cost = curr_cost + weight
                if new_cost < distances[neighbor]:
                    distances[neighbor] = new_cost
                    heapq.heappush(queue, (new_cost, neighbor, path + [neighbor]))
        return [], float('inf')

    def toggle_ui_activation(self, active=True):
        state = "normal" if active else "disabled"
        self.start_selector.config(state="readonly" if active else "disabled")
        self.goal_selector.config(state="readonly" if active else "disabled")
        self.nav_btn.config(state=state, bg="#10b981" if active else "#94a3b8")
        for sliders, combos in self.ui_controls.values():
            sliders.config(state=state)
            combos.config(state="readonly" if active else "disabled")

    def start_navigation(self):
        if self.is_navigating: return
        if self.agent_state == self.goal_state:
            self.status_log.config(text="Error: Start and Destination cannot be identical.")
            return

        path, total_cost = self.compute_dijkstra_path(self.agent_state, self.goal_state)
        
        if path:
            self.is_navigating = True
            self.toggle_ui_activation(False)
            
            self.source_state = self.agent_state
            self.full_calculated_path = list(path)
            self.planned_path = list(path)
            self.planned_path.pop(0)
            
            self.status_log.config(text=f"Shortest path calculated via Dijkstra. Total path cost: {total_cost:.1f}")
            self.update_visuals()
            self.step_agent_along_route()
        else:
            self.status_log.config(text="Path calculation failed: Target node is unreachable.")

    def step_agent_along_route(self):
        if not self.planned_path:
            self.is_navigating = False
            self.toggle_ui_activation(True)
            self.status_log.config(text="Navigation Complete! Agent has reached its destination.")
            return

        next_state = self.planned_path.pop(0)
        self.agent_state = next_state
        self.update_visuals()
        
        self.root.after(self.animation_speed, self.step_agent_along_route)

if __name__ == "__main__":
    root = tk.Tk()
    app = CompactNetworkSimulation(root)
    root.mainloop()