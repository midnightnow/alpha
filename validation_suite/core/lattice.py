import json
import numpy as np

class Lattice93:
    def __init__(self, json_path="/Users/studio/ALPHA/PMG_ROOT42_RELEASE_v1.0/CODE/engine/93_node_shell.json"):
        if not os.path.exists(json_path):
            self.nodes = self._generate_fallback()
        else:
            with open(json_path, 'r') as f:
                data = json.load(f)
                self.nodes = self._flatten_nodes(data['nodes'])
        
        self.count = len(self.nodes)

    def _flatten_nodes(self, node_data):
        flat = []
        for cat in node_data:
            for pt in node_data[cat]:
                flat.append(np.array(pt))
        return flat

    def _generate_fallback(self):
        # Fibonacci spiral on sphere for 93 nodes if JSON missing
        nodes = []
        phi = np.pi * (3. - np.sqrt(5.))  # golden angle in radians
        for i in range(93):
            y = 1 - (i / float(93 - 1)) * 2  # y goes from 1 to -1
            radius = np.sqrt(1 - y * y)  # radius at y
            theta = phi * i  # golden angle increment
            x = np.cos(theta) * radius
            z = np.sin(theta) * radius
            nodes.append(np.array([x, y, z]))
        return nodes

    def get_volume(self):
        # Normalized volume of the 93-node shell
        return 93.0 # Symbolic volume

import os
