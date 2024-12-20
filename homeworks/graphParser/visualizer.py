import os
import subprocess
import xml.etree.ElementTree as ET
import toml
from collections import defaultdict
import sys
import tempfile
import unittest

def parse_config(config_path):
    try:
        with open(config_path, "r") as f:
            config = toml.load(f)
            return config
    except Exception as e:
        print(f"Error reading config: {e}")
        sys.exit(1)

def parse_pom(pom_path):
    dependencies = []
    try:
        tree = ET.parse(pom_path)
        root = tree.getroot()
        ns = {'m': 'http://maven.apache.org/POM/4.0.0'}

        for dep in root.findall('.//m:dependency', ns):
            group_id = dep.find("m:groupId", ns).text
            artifact_id = dep.find("m:artifactId", ns).text
            version = dep.find("m:version", ns)
            version_text = version.text if version is not None else "unknown"
            dependency = f"{group_id}:{artifact_id}:{version_text}"
            dependencies.append(dependency)

        return dependencies
    except Exception as e:
        print(f"Error parsing POM file: {e}")
        sys.exit(1)

def build_dependency_graph(pom_path, max_depth):
    graph = defaultdict(list)
    visited = set()

    def recurse(current_pom, depth):
        if depth > max_depth:
            return
        if current_pom in visited:
            return
        visited.add(current_pom)

        dependencies = parse_pom(current_pom)
        for dependency in dependencies:
            graph[os.path.basename(current_pom)].append(dependency)

            dep_pom_path = os.path.join(os.path.dirname(current_pom), "deps", dependency.replace(":", "_") + ".xml")
            if os.path.exists(dep_pom_path):
                recurse(dep_pom_path, depth + 1)

    recurse(pom_path, 0)
    return graph

def generate_dot(graph, output_dot_graph):
    with open(output_dot_graph, "w") as f:
        f.write("digraph deps {\n")
        for node, edges in graph.items():
            for edge in edges:
                f.write(f'    "{node}" -> "{edge}";\n')
        f.write("}\n")

def visualize_graph(dot_path, output_image_path, graphviz_path):
    try:
        subprocess.run([graphviz_path, "-Tpng", dot_path, "-o", output_image_path], check=True)
        print(f"Graph saved to {output_image_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error during visualization: {e}")
        sys.exit(1)

def main(config_path):
    config = parse_config(config_path)
    graphviz_path = config["paths"]["graphviz"]
    pom_path = config["paths"]["package"]
    output_image_path = config["paths"]["output"]
    max_depth = config.get("max_depth", 1)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".dot") as tmp_dot:
        dot_path = tmp_dot.name
        graph = build_dependency_graph(pom_path, max_depth)
        generate_dot(graph, dot_path)
        visualize_graph(dot_path, output_image_path, graphviz_path)
        os.unlink(dot_path)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python visualizer.py <config_path>")
        sys.exit(1)
    main(sys.argv[1])
