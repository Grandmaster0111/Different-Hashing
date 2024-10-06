import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Function to hash an integer into a bitmap
def bitmap_hash(value, bitmap_size):
    # Hashing function - Using modulo operator to constrain hash within bitmap size
    hash_value = value % bitmap_size
    return hash_value

# Function to create a bitmap
def create_bitmap(values, bitmap_size):
    # Initialize an empty bitmap
    bitmap = np.zeros(bitmap_size, dtype=int)
    
    # Hash each value and set corresponding bit
    for value in values:
        hash_value = bitmap_hash(value, bitmap_size)
        bitmap[hash_value] = 1  # Set the bit at the hashed index to 1
    
    return bitmap

# Function to remove index from bitmap
def remove_from_bitmap(bitmap, index_to_remove):
    if 0 <= index_to_remove < len(bitmap):
        bitmap[index_to_remove] = 0  # Set the bit at the specified index to 0
    return bitmap

# Visualization function to display bitmap
def visualize_bitmap(bitmap):
    fig, ax = plt.subplots(figsize=(10, 2))
    ax.imshow(bitmap[np.newaxis, :], cmap='Greens', aspect='auto')
    ax.set_xticks(np.arange(bitmap.size))
    ax.set_yticks([])
    plt.title('Bitmap Visualization')
    st.pyplot(fig)

# Streamlit interface
st.title("Bitmap Hashing")

# Input fields
input_values = st.text_input("Enter a list of integer values (comma separated)", "1, 15, 23, 7, 50, 92")
bitmap_size = st.slider("Select the size of the bitmap", min_value=10, max_value=100, value=50)

# Convert input values into a list of integers
values = list(map(int, input_values.split(',')))

# Create bitmap
bitmap = create_bitmap(values, bitmap_size)

# Option to delete an index
index_to_remove = st.number_input("Enter the index to delete (0 to bitmap size - 1)", min_value=0, max_value=bitmap_size-1, value=0)
if st.button("Remove Index"):
    bitmap = remove_from_bitmap(bitmap, index_to_remove)

# Show the updated bitmap
st.write(f"Bitmap (Size {bitmap_size}):")
st.write(bitmap)

# Visualize the updated bitmap
visualize_bitmap(bitmap)