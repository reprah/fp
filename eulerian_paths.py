GRAPH1 = """
    A -> BEF
    B -> ACE
    C -> BDE
    D -> CEF
    E -> ABCDF
    F -> ADE
"""


def parse_graph(graph):
    lines = (line for line in graph.strip().split('\n') if line)
    parsed_lines = (map(lambda s: s.strip(), line.split('->')) for line in lines)
    return {node: neighbors for node,neighbors in parsed_lines}


def traverse_edge(edge, graph):
    def _update_nodes(graph):
        for node,neighbors in graph.iteritems():
            if node == from_node:
                yield node, neighbors.replace(to_node, '')
            elif node == to_node:
                yield node, neighbors.replace(from_node, '')
            else:
                yield (node, neighbors)

    from_node, to_node = edge
    assert from_node in graph[to_node] and to_node in graph[from_node]
    new_graph = {node: neighbors for node,neighbors in _update_nodes(graph)}
    return new_graph


def is_bridge(edge, graph):
    new_graph = traverse_edge(edge, graph)
    return not is_connected(new_graph)


def is_connected(graph):
    starting_node = graph.keys()[0]
    to_visit_queue = [ starting_node ]
    visited = set()

    while to_visit_queue:  # search to accumulate 'visited' graph nodes
        node = to_visit_queue.pop()
        visited.add(node)
        next_nodes = [n for n in graph[node] if n not in visited]
        to_visit_queue += next_nodes

    return visited == set(graph.keys())


def has_eulerian_path(graph):
    def _next_edge(current_node):
        if not graph[current_node]:
            return None
        default_edge = current_node + graph[current_node][0]
        candidate_edges = (current_node + next_node for next_node in graph[current_node])
        non_bridges = (e for e in candidate_edges if not is_bridge(e, graph))
        return frozenset(next(non_bridges, default_edge))

    starting_node = next(n for n,neighbors in graph.iteritems() if neighbors)

    if not starting_node:
        return len(graph.keys()) in (0, 1)

    current_node = starting_node
    to_traverse_queue = [ _next_edge(current_node) ]
    traversed = set()
    all_graph_edges = all_edges(graph)

    while to_traverse_queue:
        edge = to_traverse_queue.pop()
        graph = traverse_edge(edge, graph)
        traversed.add(edge)
        current_node = next(n for n in edge if n != current_node)
        next_edge = _next_edge(current_node)
        if next_edge:
            to_traverse_queue.append(next_edge)

    return current_node == starting_node and traversed == all_graph_edges


def all_edges(graph):  #, one_node=None):
    # graph_items = [(one_node, graph[one_node])] if one_node else graph.iteritems()
    edges = (node+node2 for node,neighbors in graph.iteritems() for node2 in neighbors)
    return set(frozenset(e) for e in edges)


def main(graph=GRAPH1):
    parsed_graph = parse_graph(graph)
    return has_eulerian_path(parsed_graph)


def tests():
    graph = """
        a -> bc
        b -> ac
        c -> abd
        d -> ce
        e -> d
    """
    g = parse_graph(graph)
    assert traverse_edge('ab', g) == {'a': 'c', 'b': 'c', 'c': 'abd', 'd': 'ce', 'e': 'd'}

    g2 = g.copy()
    g2['d'] = 'c'
    g2['e'] = ''
    assert traverse_edge('de', g) == g2
    assert is_connected(g)
    assert not is_connected(g2)

    assert is_bridge('de', g)
    assert not is_bridge('ab', g)

    assert all_edges(g) == set([frozenset(['e', 'd']), frozenset(['c', 'b']), frozenset(['a', 'c']), frozenset(['a', 'b']), frozenset(['c', 'd'])])
    assert all_edges(g2) == set([frozenset(['c', 'b']), frozenset(['a', 'c']), frozenset(['a', 'b']), frozenset(['c', 'd'])])

    assert main()

    return 'tests pass!'


if __name__ == '__main__':
    print tests()
