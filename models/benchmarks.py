"""Módulo de Métricas y Benchmark de Rendimiento en Tiempo Real (Semana 3 - Día 3).
Calcula operaciones por segundo (ops/sec), consumo en memoria (bytes) y
compara la complejidad teórica Big-O (O(1) vs O(n)) con resultados empíricos reales.
"""

import sys
import time
from typing import Dict, Any, List
from .structures import Node, PriorityNode, DoublyLinkedList, Stack, PriorityQueue, CircularQueue


def get_memory_footprint() -> Dict[str, Any]:
    """Calcula el consumo de memoria en bytes de los nodos y estructuras puras."""
    sample_node = Node("EST-100")
    sample_pnode = PriorityNode("EST-100", 10.0)
    return {
        "node_bytes": sys.getsizeof(sample_node),
        "priority_node_bytes": sys.getsizeof(sample_pnode),
        "empty_list_bytes": sys.getsizeof(DoublyLinkedList()),
        "empty_stack_bytes": sys.getsizeof(Stack()),
        "empty_pqueue_bytes": sys.getsizeof(PriorityQueue()),
    }


def run_benchmark_suite(iterations: int = 5000) -> List[Dict[str, Any]]:
    """Ejecuta una batería de micro-benchmarks midiendo ops/seg y latencia promedio."""
    results: List[Dict[str, Any]] = []

    def _benchmark(name: str, complexity: str, struct_name: str, op_callable, count: int):
        t0 = time.perf_counter()
        op_callable()
        elapsed = max(time.perf_counter() - t0, 1e-9)
        ops_per_sec = count / elapsed
        avg_us = (elapsed / count) * 1_000_000
        results.append({
            "operacion": name,
            "estructura": struct_name,
            "complejidad": complexity,
            "operaciones": count,
            "tiempo_total_ms": round(elapsed * 1000, 2),
            "ops_segundo": int(ops_per_sec),
            "tiempo_por_op_us": round(avg_us, 3),
        })

    # 1. DoublyLinkedList.append -> O(1)
    dll = DoublyLinkedList()
    def op_append():
        for i in range(iterations):
            dll.append(i)
    _benchmark("append() [final]", "O(1)", "DoublyLinkedList", op_append, iterations)

    # 2. DoublyLinkedList.prepend -> O(1)
    dll_prep = DoublyLinkedList()
    def op_prepend():
        for i in range(iterations):
            dll_prep.prepend(i)
    _benchmark("prepend() [inicio]", "O(1)", "DoublyLinkedList", op_prepend, iterations)

    # 3. Stack.push y pop -> O(1)
    stack = Stack()
    def op_stack():
        for i in range(iterations):
            stack.push(i)
        for _ in range(iterations):
            stack.pop()
    _benchmark("push() / pop()", "O(1)", "Stack (LIFO)", op_stack, iterations * 2)

    # 4. CircularQueue.step -> O(1)
    cq = CircularQueue()
    for i in range(100):
        cq.enqueue(i)
    def op_cstep():
        for _ in range(iterations):
            cq.step()
    _benchmark("step() [turno]", "O(1)", "CircularDoublyList", op_cstep, iterations)

    # 5. DoublyLinkedList.search -> O(n)
    target = iterations // 2
    def op_search():
        for _ in range(500):
            dll.search(target)
    _benchmark("search() [lineal]", "O(n)", "DoublyLinkedList", op_search, 500)

    # 6. PriorityQueue.enqueue -> O(n)
    pq = PriorityQueue()
    def op_pq():
        for i in range(1000):
            pq.enqueue(f"id_{i}", (i * 37) % 100)
    _benchmark("enqueue() [ordenada]", "O(n)", "PriorityQueue", op_pq, 1000)

    return results
