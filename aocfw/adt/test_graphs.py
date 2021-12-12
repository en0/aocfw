from unittest import TestCase, skip
from .graphs import AdjacencyList


class AdjacencyListTests(TestCase):

    def test_add_vertex(self):
        graph = AdjacencyList[int]()
        graph.add_vertex(1)
        self.assertIn(1, graph)

    def test_add_vertex_raises_value_error(self):
        graph = AdjacencyList[int]()
        graph.add_vertex(1)
        with self.assertRaises(ValueError):
            graph.add_vertex(1)

    def test_contains_vertex_not_in(self):
        graph = AdjacencyList[int]()
        graph.add_vertex(1)
        self.assertNotIn(2, graph)

    def test_add_vertex_with_value(self):
        graph = AdjacencyList[int]()
        graph[1] = 1
        self.assertEqual(graph[1], 1)

    def test_get_value_raises_key_error(self):
        graph = AdjacencyList[int]()
        self.assertRaises(KeyError, lambda: graph[1])

    def test_iterator(self):
        graph = AdjacencyList[int]()
        graph.add_vertex(1)
        graph.add_vertex(2)
        graph.add_vertex(3)
        self.assertListEqual(list(graph), [1,2,3])

    def test_add_directed_edge(self):
        graph = AdjacencyList[int]()
        graph.add_vertex(1)
        graph.add_vertex(2)
        graph.add_edge(1, 2)
        self.assertTrue(graph.adjacent(1, 2))
        self.assertFalse(graph.adjacent(2, 1))

    def test_add_edge_raises_value_error(self):
        graph = AdjacencyList[int]()
        graph.add_vertex(1)
        graph.add_vertex(2)
        graph.add_edge(1, 2)
        with self.assertRaises(ValueError):
            graph.add_edge(1, 2)

    def test_add_edge_raises_key_error(self):
        graph = AdjacencyList[int]()
        with self.assertRaises(KeyError):
            graph.add_edge(1, 2)
        graph.add_vertex(1)
        with self.assertRaises(KeyError):
            graph.add_edge(1, 2)
        graph = AdjacencyList[int]()
        graph.add_vertex(2)
        with self.assertRaises(KeyError):
            graph.add_edge(1, 2)

    def test_adjacent_raises(self):
        graph = AdjacencyList[int]()
        with self.assertRaises(KeyError):
            self.assertTrue(graph.adjacent(1, 2))

        graph.add_vertex(1)
        with self.assertRaises(KeyError):
            self.assertFalse(graph.adjacent(2, 1))

        with self.assertRaises(KeyError):
            self.assertFalse(graph.adjacent(1, 2))

    def test_cannot_add_edge_between_non_existing_vertices(self):
        graph = AdjacencyList[int]()
        with self.assertRaises(KeyError):
            graph.add_edge(1, 2)

        graph.add_vertex(1)
        with self.assertRaises(KeyError):
            graph.add_edge(1, 2)

    def test_get_neighbors(self):
        graph = AdjacencyList[int]()
        graph.add_vertex(1)
        graph.add_vertex(2)
        graph.add_edge(1, 2)
        self.assertListEqual(list(graph.neighbors(1)), [2])
        self.assertListEqual(list(graph.neighbors(2)), [])

        graph.add_edge(2, 1)
        self.assertListEqual(list(graph.neighbors(1)), [2])
        self.assertListEqual(list(graph.neighbors(2)), [1])

        with self.assertRaises(KeyError):
            graph.neighbors(3)

    def test_remove_edge(self):
        graph = AdjacencyList[int]()
        graph.add_vertex(1)
        graph.add_vertex(2)
        graph.add_edge(1, 2)
        self.assertTrue(graph.adjacent(1, 2))

        graph.remove_edge(1, 2)
        self.assertTrue(1 in graph)
        self.assertTrue(2 in graph)
        self.assertFalse(graph.adjacent(1, 2))

    def test_remove_edge_raises_key_error(self):
        graph = AdjacencyList[int]()
        with self.assertRaises(KeyError):
            graph.remove_edge(1, 2)

        graph.add_vertex(1)
        with self.assertRaises(KeyError):
            graph.remove_edge(1, 2)

        graph.add_vertex(2)
        with self.assertRaises(KeyError):
            graph.remove_edge(1, 2)

    def test_add_weight(self):
        graph = AdjacencyList[int]()
        graph.add_vertex(1)
        graph.add_vertex(2)
        graph.add_edge(1, 2)
        self.assertIsNone(graph.get_weight(1, 2))

        graph.set_weight(1, 2, 10)
        self.assertEqual(graph.get_weight(1, 2), 10)

        graph.set_weight(1, 2, 12)
        self.assertEqual(graph.get_weight(1, 2), 12)

        with self.assertRaises(KeyError):
            graph.get_weight(1, 10)

        with self.assertRaises(KeyError):
            graph.get_weight(10, 1)

        with self.assertRaises(KeyError):
            graph.get_weight(10, 10)

    def test_set_weight_raises_key_error(self):
        graph = AdjacencyList[int]()
        with self.assertRaises(KeyError):
            graph.set_weight(1, 2, 10)
        graph.add_vertex(1)
        with self.assertRaises(KeyError):
            graph.set_weight(1, 2, 10)

    def test_remove_vertex(self):
        graph = AdjacencyList[int]()
        graph.add_vertex(1)
        self.assertIn(1, graph)
        graph.remove_vertex(1)
        self.assertNotIn(1, graph)

    def test_remove_vertex_raises_key_error(self):
        graph = AdjacencyList[int]()
        with self.assertRaises(KeyError):
            graph.remove_vertex(1)

    def test_remove_vertex_removes_weight(self):
        graph = AdjacencyList[int]()
        graph.add_vertex(1)
        graph.add_vertex(2)
        graph.add_edge(1, 2)
        graph.set_weight(1, 2, 10)
        self.assertEqual(graph.get_weight(1, 2), 10)
        graph.remove_vertex(1)

        graph.add_vertex(1)
        self.assertIsNone(graph.get_weight(1, 2))

    def test_remove_vertex_removes_references(self):
        graph = AdjacencyList[int]()
        graph.add_vertex(1)
        graph.add_vertex(2)
        graph.add_edge(1, 2)
        graph.set_weight(1, 2, 10)
        self.assertEqual(graph.get_weight(1, 2), 10)
        graph.remove_vertex(2)

        graph.add_vertex(2)
        self.assertIsNone(graph.get_weight(1, 2))

    def test_graph(self):
        graph = AdjacencyList[str]()

        # And Vertices
        graph.add_vertex('start')
        graph.add_vertex('end')
        graph.add_vertex('c')
        graph.add_vertex('A')
        graph.add_vertex('b')
        graph.add_vertex('d')

        # start -> *
        graph.add_edge("start", "A")
        graph.add_edge("start", "b")

        # A -> *
        graph.add_edge("A", "start")
        graph.add_edge("A", "c")
        graph.add_edge("A", "end")
        graph.add_edge("A", "b")

        # b -> *
        graph.add_edge("b", "start")
        graph.add_edge("b", "A")
        graph.add_edge("b", "end")
        graph.add_edge("b", "d")

        # end -> *
        graph.add_edge("end", "A")
        graph.add_edge("end", "b")

        # c -> *
        graph.add_edge("c", "A")

        # d -> *
        graph.add_edge("d", "b")

        # start -> [A, b]
        self.assertTrue(graph.adjacent("start", "A"))
        self.assertTrue(graph.adjacent("start", "b"))
        self.assertFalse(graph.adjacent("start", "end"))
        self.assertFalse(graph.adjacent("start", "c"))
        self.assertFalse(graph.adjacent("start", "d"))
        self.assertListEqual(sorted(graph.neighbors("start")), ["A", "b"])

        # A -> [start, c, end, b]
        self.assertTrue(graph.adjacent("A", "start"))
        self.assertTrue(graph.adjacent("A", "c"))
        self.assertTrue(graph.adjacent("A", "end"))
        self.assertTrue(graph.adjacent("A", "b"))
        self.assertFalse(graph.adjacent("A", "d"))
        self.assertListEqual(sorted(graph.neighbors("A")), ["b", "c", "end", "start"])

        # b -> [start, A, end, d]
        self.assertTrue(graph.adjacent("b", "start"))
        self.assertTrue(graph.adjacent("b", "A"))
        self.assertTrue(graph.adjacent("b", "end"))
        self.assertTrue(graph.adjacent("b", "d"))
        self.assertFalse(graph.adjacent("b", "c"))
        self.assertListEqual(sorted(graph.neighbors("b")), ["A", "d", "end", "start"])

        # c -> [A]
        self.assertTrue(graph.adjacent("c", "A"))
        self.assertFalse(graph.adjacent("c", "start"))
        self.assertFalse(graph.adjacent("c", "end"))
        self.assertFalse(graph.adjacent("c", "b"))
        self.assertFalse(graph.adjacent("c", "d"))
        self.assertListEqual(sorted(graph.neighbors("c")), ["A"])

        # d -> [b]
        self.assertTrue(graph.adjacent("d", "b"))
        self.assertFalse(graph.adjacent("d", "start"))
        self.assertFalse(graph.adjacent("d", "end"))
        self.assertFalse(graph.adjacent("d", "A"))
        self.assertFalse(graph.adjacent("d", "c"))
        self.assertListEqual(sorted(graph.neighbors("d")), ["b"])

        # end -> [A, b]
        self.assertTrue(graph.adjacent("end", "A"))
        self.assertTrue(graph.adjacent("end", "b"))
        self.assertFalse(graph.adjacent("end", "start"))
        self.assertFalse(graph.adjacent("end", "c"))
        self.assertFalse(graph.adjacent("end", "d"))
        self.assertListEqual(sorted(graph.neighbors("end")), ["A", "b"])

