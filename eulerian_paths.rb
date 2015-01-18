require 'pry'

graph = [
  [:a, :e], [:a, :b], [:a, :c],
  [:e, :f], [:c, :f], [:f, :d],
  [:d, :c], [:b, :c], [:b, :d],
  [:d, :b]
]

graph2 = [
  [:d, :c], [:a, :c], [:b, :d],
  [:d, :b], [:b, :c], [:c, :f],
  [:e, :f], [:a, :b], [:a, :e],
  [:f, :d]
] 

graph_with_circuit = [
  [:a, :f], [:a, :e], [:a, :e], [:a, :b],
  [:f, :d], [:f, :e], [:f, :d], [:b, :c],
  [:e, :c], [:e, :b], [:e, :d], [:b, :c],
  [:d, :c]
]

def dfs(graph, start_node, visited_nodes = [])
  if not visited_nodes.include?(start_node)
    visited_nodes.push(start_node)
    neighbors = graph.select { |edge|
      edge.include?(start_node)
    }.flatten.reject { |edge|
      edge == start_node
    }
    neighbors.each { |neighbor|
      dfs(graph, neighbor, visited_nodes)
    }
  end
  visited_nodes
end

def find_bridges(graph)
  all_nodes = graph.flatten.uniq
  return graph if graph.size == 1
  graph.reject { |edge|
    clone = graph.clone
    clone = clone.reject { |e| e == edge }
    found_nodes = dfs(clone, clone[0][0])
    found_nodes.size == all_nodes.size
  }
end

def vertices_with_odd_degrees(graph)
  vertices_with_degrees = Hash.new(0)
  vertices = graph.flatten.uniq
  vertices.each { |vertex|
    degrees = graph.select { |edge| edge.include?(vertex) }.count
    vertices_with_degrees[vertex] = degrees
  }
  vertices_with_degrees.select { |vertex, degrees| degrees.odd? }
end

def has_eulerian_path?(graph)
  vertices_with_odd_degrees(graph).count == 2
end

def has_eulerian_circuit?(graph)
  vertices_with_odd_degrees(graph).count == 0
end

def eulerian_path(graph)
  if has_eulerian_path?(graph) || has_eulerian_circuit?(graph)
    path = []
    start_node = vertices_with_odd_degrees(graph).keys[0] || graph[0][0]
    current_edge = graph.detect { |edge| edge.include?(start_node) }
    next_node = nil
    until graph.empty? do
      if next_node
        current_node = next_node
        next_node = current_edge.reject { |n| n == next_node }[0]
      else
        current_node = start_node
        next_node = current_edge.reject { |n| n == start_node }[0]
      end
      path.push(current_node)
      graph = graph.tap { |g| g.delete_at(g.index(current_edge)) }
      next_edge_candidates = graph.select { |edge| edge.include?(next_node) }
      bridges = find_bridges(graph)
      non_bridges = next_edge_candidates.reject { |edge| bridges.include?(edge) }
      if non_bridges.any?
        next_edge = non_bridges[0]
      else
        next_edge = next_edge_candidates[0]
      end
      current_edge = next_edge
    end
    path.push(next_node)
    path
  else
    []
  end
end

p eulerian_path(graph_with_circuit)
