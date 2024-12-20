import unittest
import tempfile
import os
import toml
from visualizer import (
    parse_config,
    parse_pom,
    build_dependency_graph,
    generate_dot,
    visualize_graph,
)
from unittest.mock import patch

class TestVisualizer(unittest.TestCase):

    def setUp(self):

        self.config_data = {
            "paths": {
                "graphviz": "/usr/bin/dot",
                "package": "test_pom.xml",
                "output": "output/graph.png"
            },
            "max_depth": 2
        }
        self.tmp_config = tempfile.NamedTemporaryFile(delete=False, suffix=".toml")
        with open(self.tmp_config.name, "w") as f:
            toml.dump(self.config_data, f)


        self.pom_content = """
        <project xmlns="http://maven.apache.org/POM/4.0.0">
            <modelVersion>4.0.0</modelVersion>
            <dependencies>
                <dependency>
                    <groupId>org.example</groupId>
                    <artifactId>example-lib</artifactId>
                    <version>1.0</version>
                </dependency>
            </dependencies>
        </project>
        """
        self.tmp_pom = tempfile.NamedTemporaryFile(delete=False, suffix=".xml")
        with open(self.tmp_pom.name, "w") as f:
            f.write(self.pom_content)

    def tearDown(self):

        os.unlink(self.tmp_config.name)
        os.unlink(self.tmp_pom.name)

    def test_parse_config(self):
        config = parse_config(self.tmp_config.name)
        self.assertEqual(config["paths"]["graphviz"], "/usr/bin/dot")
        self.assertEqual(config["paths"]["package"], "test_pom.xml")
        self.assertEqual(config["paths"]["output"], "output/graph.png")
        self.assertEqual(config["max_depth"], 2)

    def test_parse_pom(self):
        dependencies = parse_pom(self.tmp_pom.name)
        self.assertEqual(dependencies, ["org.example:example-lib:1.0"])

    def test_build_dependency_graph(self):
        graph = build_dependency_graph(self.tmp_pom.name, 1)
        expected_graph = {
            os.path.basename(self.tmp_pom.name): ["org.example:example-lib:1.0"]
        }
        self.assertEqual(dict(graph), expected_graph)

    def test_generate_dot(self):
        graph = {
            "test_pom.xml": ["org.example:example-lib:1.0"]
        }
        with tempfile.NamedTemporaryFile(delete=False, suffix=".dot") as tmp_dot:
            generate_dot(graph, tmp_dot.name)
            with open(tmp_dot.name, "r") as f:
                content = f.read()
                expected_content = (
                    'digraph deps {\n'
                    '    "test_pom.xml" -> "org.example:example-lib:1.0";\n'
                    '}\n'
                )
                self.assertEqual(content, expected_content)
            os.unlink(tmp_dot.name)

    @patch("subprocess.run")
    def test_visualize_graph(self, mock_run):

        dot_path = "test.dot"
        output_image_path = "output.png"
        graphviz_path = "/usr/bin/dot"

        visualize_graph(dot_path, output_image_path, graphviz_path)
        mock_run.assert_called_with(
            [graphviz_path, "-Tpng", dot_path, "-o", output_image_path],
            check=True
        )

if __name__ == "__main__":
    unittest.main()
