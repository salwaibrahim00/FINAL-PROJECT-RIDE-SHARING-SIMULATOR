# dijkstra.py
import heapq

def find_shortest_path(graph, start_node, end_node):
    """
    Returns (path_list, total_weight) using Dijkstra over graph.adjacency_list.
    If unreachable, returns (None, float('inf')).
    """
    dist = {n: float('inf') for n in graph.adjacency_list}
    prev = {n: None for n in graph.adjacency_list}
    dist[start_node] = 0.0

    pq = [(0.0, start_node)]
    while pq:
        d, u = heapq.heappop(pq)
        if u == end_node:
            break
        if d > dist[u]:
            continue
        for v, w in graph.adjacency_list.get(u, []):
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                prev[v] = u
                heapq.heappush(pq, (nd, v))

    if dist[end_node] == float('inf'):
        return None, float('inf')

    # reconstruct
    path = []
    cur = end_node
    while cur is not None:
        path.append(cur)
        cur = prev[cur]
    path.reverse()
    return path, dist[end_node]
