import streamlit as st
import graphviz


st.title("Binary Tree Visualization of Extensible Hashing")


def double_dict_keys(i):
    my_dict = {}

    num_keys = 2 ** i 
    for j in range(num_keys):
        key = f'{j:b}'.zfill(i)  
        my_dict[key] = []  
    return my_dict
    
def categorize_by_two_lsb(numbers,lsb_dict,c):
    
    for num in numbers:
        lsb = num & ((2**c)-1)  # Get the two least significant bits
        key = f"{lsb:0{c}b}"  # Format as a two-bit binary string
        if len(lsb_dict[key]) == bucket_size:
            return True, lsb_dict
        else:
            lsb_dict[key].append(num)
    
    return False, lsb_dict



class TreeNode:
    def __init__(self, value=None):
        self.value = value
        self.left = None
        self.right = None

def insert(root, key, value, index=0):
    """Insert the value into the binary tree based on the binary key."""
    if root is None:
        root = TreeNode()

    if index < len(key):
        if key[index] == '0':
            root.left = insert(root.left, key, value, index + 1)
        else:
            root.right = insert(root.right, key, value, index + 1)
    else:
        root.value = value

    return root

def build_tree_from_dict(data):
    """Build a binary tree from the given dictionary."""
    root = None
    for key, value in data.items():
        root = insert(root, key, value)
    return root

def visualize_tree(node, graph=None):
    """Visualize the binary tree using Graphviz."""
    if graph is None:
        graph = graphviz.Digraph(format='png')

    if node is not None:
        graph.node(str(id(node)), str(node.value) if node.value is not None else "None")
        if node.left is not None:
            graph.edge(str(id(node)), str(id(node.left)))
            visualize_tree(node.left, graph)
        if node.right is not None:
            graph.edge(str(id(node)), str(id(node.right)))
            visualize_tree(node.right, graph)

    return graph

# Streamlit app

def ins(numbers):
    flag=True
    n=1
    while flag:
        flag, lsb_dict = categorize_by_two_lsb(numbers,double_dict_keys(n),n)
        n+=1
    return lsb_dict

bucket_size=st.number_input('Enter your bucket size: ',min_value=0)

if bucket_size!=0:

    st.write('Select which operation you want to perform:')
    st.write('1. Insertion')
    st.write('2. Deletion')
    if 'my_set' not in st.session_state:
        st.session_state.my_set = set()




    # Input for adding a value
    inpu = st.number_input("Enter a number to add:",min_value=0)
    col1, col2 = st.columns(2)

    # Insert button
    with col1:
        if st.button("Insert"):
            st.session_state.my_set.add(inpu)
            st.success(f"Added {inpu} to the set.")
            
    with col2:
        # Input for removing a value
        if st.button("Delete"):
            st.session_state.my_set.discard(inpu)
            st.success(f"Removed {inpu} from the set.")

    if inpu!=0:
        root = build_tree_from_dict(ins(list(st.session_state.my_set)))
        # Visualize the binary tree
        if root:
            graph = visualize_tree(root)
            st.graphviz_chart(graph)
        else:
            st.write("No tree available.")

        current_list = ins(list(st.session_state.my_set))

        # Display the current set and its list form
        st.write("Current Set:", st.session_state.my_set)
        st.write("Current List:", current_list)
