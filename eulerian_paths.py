"""
An Euler path (EP) is a path that uses every edge of a graph exactly once and
starts and ends at different vertices.

To have an EP, the graph must have exactly two nodes of odd degree:
an EP will visit every edge as well as exit any node the same
number of times it enters the node, except for the starting and ending nodes,
which implies that the starting and ending nodes have odd degree -- and only
these nodes.

To have a chance of explicitly following an EP, we must choose as our starting
point a node of odd degree.
"""

GRAPH1 = """
    A -> BEEF
    B -> ACE
    C -> BDEF
    D -> CEFF
    E -> AABCD
    F -> ACDD
"""

### Parsing

def parse_graph(graph):
    lines = (line for line in graph.strip().split('\n') if line)
    parsed_lines = (map(lambda s: s.strip(), line.split('->')) for line in lines)
    return {node: neighbors for node,neighbors in parsed_lines}


### Helpers

def is_connected(graph):
    connected_nodes = [node for node,neighbors in graph.iteritems() if neighbors]
    starting_node = connected_nodes[0]
    to_visit_queue = [ starting_node ]
    visited = set()

    while to_visit_queue:  # search accumulates 'visited' graph nodes
        node = to_visit_queue.pop()
        if node not in visited:
            visited.add(node)
            to_visit_queue += list(graph[node])

    return visited == set(connected_nodes)


def is_odd(n): return n % 2 == 1


def odd_nodes(graph):
    return [node for node,neighbors in graph.iteritems() if is_odd(len(neighbors))]


def edges(node, neighbors): return (node + n for n in neighbors)


def all_edges(graph):
    return (edge for node,neighbors in graph.iteritems()
            for edge in edges(node, neighbors))


def non_bridges(edges, graph):
    for edge in edges:
        start_node = edge[0]
        _, new_graph = walk_edge(graph, start_node, edge)
        if is_connected(new_graph):
            yield edge


def walk_edge(graph, start_node, edge):
    end_node = next(node for node in edge if node != start_node)
    new_graph = graph.copy()
    new_graph[start_node] = new_graph[start_node].replace(end_node, '', 1)
    new_graph[end_node]   = new_graph[end_node].replace(start_node, '', 1)
    return end_node, new_graph


def walk_non_bridges_first(graph, start_node, path=[]):
    neighbors = graph[start_node]

    if not neighbors:  # can't continue path
        return path

    available_edges = edges(start_node, neighbors)
    next_edge = next(non_bridges(available_edges, graph), next(available_edges))

    new_path = path + [next_edge]
    new_node, new_graph = walk_edge(graph, start_node, next_edge)
    return walk_non_bridges_first(new_graph, new_node, new_path)


### Top-Level

def can_find_eulerian_path(graph):
    start_node = odd_nodes(graph)[0]
    path = walk_non_bridges_first(graph, start_node)
    edges_in_path = set(frozenset(edge) for edge in path)
    all_graph_edges = set(frozenset(edge) for edge in all_edges(graph))
    return edges_in_path == all_graph_edges


def has_two_odd_nodes(graph): return len(odd_nodes(graph)) == 2


def has_eulerian_path(graph):
    assert len(graph.keys()) > 1, 'Not interesting'
    return has_two_odd_nodes(graph) and can_find_eulerian_path(graph)


def main(graph=GRAPH1):
    parsed_graph = parse_graph(graph)
    return has_eulerian_path(parsed_graph)


def tests():
    assert main()
    return 'tests pass!'


if __name__ == '__main__':
    print tests()
