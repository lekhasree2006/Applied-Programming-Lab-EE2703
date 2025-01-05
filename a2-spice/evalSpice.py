import numpy as np


def evalSpice(filename):
    if not filename:
        raise FileNotFoundError('Please give the name of a valid SPICE file as input')

    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
    except FileNotFoundError:
        raise FileNotFoundError('Please give the name of a valid SPICE file as input')

    circuit_start = None
    circuit_end = None

    for i, line in enumerate(lines):
        if line.strip().startswith('.circuit'):
            circuit_start = i
        if line.strip().endswith('.end'):
            circuit_end = i

    if circuit_start is None or circuit_end is None or circuit_start >= circuit_end:
        raise ValueError('Malformed circuit file')

    d_main = {}
    nodes = set()
    voltage_sources = []

    for line in lines[circuit_start + 1:circuit_end]:
        words = line.split()

        if len(words) > 1:
            component = words[0]
            node1 = words[1]
            node2 = words[2]
            if component.startswith('V') or component.startswith('I'):
                value = float(words[4])
            else:
                value = float(words[3])

            if component.startswith('R'):
                d_main[component] = {'type': 'resistor', 'node_1': node1, 'node_2': node2, 'value': value}
            elif component.startswith('I'):
                d_main[component] = {'type': 'current_source', 'node_1': node1, 'node_2': node2, 'value': value}
            elif component.startswith('V'):
                d_main[component] = {'type': 'voltage_source', 'node_1': node1, 'node_2': node2, 'value': value}
                voltage_sources.append(component)
            else:
                raise ValueError('Only V, I, R elements are permitted')

            if node1 != 'GND':
                nodes.add(node1)
            if node2 != 'GND':
                nodes.add(node2)

    nodes = list(set(nodes))
    number_of_nodes = len(nodes)
    dim_g_matrix = number_of_nodes + len(voltage_sources)

    G = np.zeros((dim_g_matrix, dim_g_matrix))
    I = np.zeros(dim_g_matrix)

    node_map = {node: i for i, node in enumerate(nodes)}
    voltage_map = {voltage: i for i, voltage in enumerate(voltage_sources)}

    for component, properties in d_main.items():
        node1 = properties['node_1']
        node2 = properties['node_2']

        if properties['type'] == 'resistor':
            value = properties['value']
            if node1 != 'GND':
                G[node_map[node1], node_map[node1]] += 1 / value
            if node2 != 'GND':
                G[node_map[node2], node_map[node2]] += 1 / value
            if node1 != 'GND' and node2 != 'GND':
                G[node_map[node1], node_map[node2]] -= 1 / value
                G[node_map[node2], node_map[node1]] -= 1 / value

        elif properties['type'] == 'voltage_source':
            if node1 != 'GND':
                G[node_map[node1], number_of_nodes + voltage_map[component]] -= 1
                G[number_of_nodes + voltage_map[component], node_map[node1]] += 1
            if node2 != 'GND':
                G[node_map[node2], number_of_nodes + voltage_map[component]] += 1
                G[number_of_nodes + voltage_map[component], node_map[node2]] -= 1
            I[number_of_nodes + voltage_map[component]] = properties['value']

        elif properties['type'] == 'current_source':
            value = properties['value']
            if node1 != 'GND':
                I[node_map[node1]] -= value
            if node2 != 'GND':
                I[node_map[node2]] += value

    if np.linalg.det(G) == 0:
        raise ValueError('Circuit error: no solution')

    V = np.linalg.solve(G, I)

    node_voltages = {'GND': 0.0}  # Start with the ground node voltage
    for node, index in node_map.items():
        node_voltages[node] = float(V[index])

    voltage_source_currents = {}
    for voltage, index in voltage_map.items():
        voltage_source_currents[voltage] = float(-1 * V[number_of_nodes + index])

    return node_voltages, voltage_source_currents
