import streamlit as st
import streamlit_bd_cytoscapejs
import pandas as pd


st.set_page_config(layout="wide")


# DataFrame for nodes
nodes_df = pd.DataFrame({
    'id': ['quantum_networks', 'node_entanglement', 'no_node_entanglement', 'quantum_memory', 'erbium', 'silicon', 'photonic_chip', 'su8', 'fiber_chip'],
    'label': ['Quantum Networks', 'Requires Node Entanglement', 'Doesn’t Require Node Entanglement', 'Quantum Memory Platform', 'Erbium Atoms', 'Silicon', 'Photonic Chip', 'SU8', 'Fiber-to-Chip Coupling']
})

# DataFrame for edges
edges_df = pd.DataFrame({
    'id': ['e1', 'e2', 'e3', 'e4', 'e5', 'e6', 'e7', 'e8'],
    'source': ['quantum_networks', 'quantum_networks', 'node_entanglement', 'quantum_memory', 'quantum_memory', 'silicon', 'photonic_chip', 'su8'],
    'target': ['node_entanglement', 'no_node_entanglement', 'quantum_memory', 'erbium', 'silicon', 'photonic_chip', 'su8', 'fiber_chip']
})

def df_to_elements(nodes_df, edges_df):
    nodes_list = nodes_df.to_dict(orient='records')
    nodes_elements = [{'data': node} for node in nodes_list]
    
    edges_list = edges_df.to_dict(orient='records')
    edges_elements = [{'data': edge} for edge in edges_list]

    return nodes_elements + edges_elements

layout = {
    'name': 'cose',
    'animate': False,
    'refresh': 1,
    'componentSpacing': 100,
    'nodeOverlap': 50,
    'nodeRepulsion': 5000,
    'edgeElasticity': 100,
    'nestingFactor': 5,
    'gravity': 80,
    'numIter': 1000,
    'initialTemp': 200,
    'coolingFactor': 0.95,
    'minTemp': 1.0
}




stylesheet = [
    {
        'selector': 'node',
        'style': {
            'background-color': '#11479e',
            'label': 'data(label)',
            'text-valign': 'center',
            'color': 'white',
            'text-outline-width': 2,
            'text-outline-color': '#11479e'
        }
    },
    {
        'selector': 'edge',
        'style': {
            'curve-style': 'bezier',
            'width': 3,
            'line-color': '#9dbaea',
            'target-arrow-color': '#9dbaea',
            'target-arrow-shape': 'triangle',
            'line-fill': 'linear-gradient'
        }
    }
]




nodes_df = st.data_editor(nodes_df, num_rows="dynamic")
edges_df = st.data_editor(edges_df, num_rows="dynamic")



elements = df_to_elements(nodes_df, edges_df)

node_id = streamlit_bd_cytoscapejs.st_bd_cytoscape(
    elements,
    layout=layout,
    stylesheet=stylesheet,
    key='quantum_networks_graph'
)
