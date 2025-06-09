import networkx as nx # type: ignore
import matplotlib.pyplot as plt # type: ignore
from .concept_extraction import extract_key_concepts, prioritize_side_headings  # Import concept extraction methods

def create_mind_map_from_text(text, max_words=25):
    """
    Generates a mind map based on the extracted concepts from the provided text.
    
    Args:
        text (str): The text content for generating the mind map.
        max_words (int): The maximum number of key concepts to extract.
    
    Returns:
        None: Displays the mind map visualization.
    """
    # Step 1: Extract key concepts
    extracted_concepts = extract_key_concepts(text, max_words)

    # Step 2: Prioritize headings if present in the text
    prioritized_concepts = prioritize_side_headings(text, extracted_concepts)

    # Step 3: Create and visualize the mind map
    create_mind_map(prioritized_concepts)

def create_mind_map(concepts):
    """
    Visualizes a more organized mind map (graph) of the extracted concepts.
    
    Args:
        concepts (list): List of concepts to include in the mind map.
    
    Returns:
        None: Displays the mind map visualization.
    """
    G = nx.Graph()

    # Add nodes for each concept
    G.add_nodes_from(concepts)

    # Connect related concepts (for simplicity, link adjacent concepts)
    for i in range(len(concepts) - 1):
        G.add_edge(concepts[i], concepts[i + 1])

    # Adjust layout for less clutter
    plt.figure(figsize=(12, 10))
    pos = nx.spring_layout(G, k=0.75, iterations=100)  # Adjust 'k' for node spacing
    node_sizes = [2000 + 500 * (i + 1) for i in range(len(concepts))]  # Vary node size
    nx.draw(
        G, 
        pos, 
        with_labels=True, 
        node_color="lightgreen", 
        node_size=node_sizes, 
        font_size=10, 
        font_weight="bold", 
        edge_color="black"
    )
    plt.title("Mind Map", fontsize=16)
    plt.show()

# ------------------------- Module testing code starts
if __name__ == "__main__":
    # Sample text for testing the mind map generation
    sample_text = """
    MACHINE LEARNING OVERVIEW
    Machine learning involves algorithms that allow computers to learn patterns from data. 
    Applications include healthcare, finance, and more.
    """

    # Generate and display the mind map
    print("Generating mind map for the provided text...")
    create_mind_map_from_text(sample_text, max_words=10)

# ------------------------- Module testing code ends
# Status: Done Successful
