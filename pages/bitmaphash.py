import streamlit as st
import numpy as np
import pandas as pd

st.title("Bitmap Hashing with Pictorial Representation")

# Bitmap Hashing Functions

def initialize_bitmap(bitmap_size):
    """Initialize the bitmap with zeros."""
    bitmap = np.zeros(bitmap_size, dtype=int)
    return bitmap

def hash_function(value, bitmap_size):
    """Compute the hash function for the given value."""
    return value % bitmap_size

def insert_into_bitmap(bitmap, value, bitmap_size):
    """Insert a value into the bitmap."""
    hash_value = hash_function(value, bitmap_size)
    
    # Set the bit at the hashed index to 1
    bitmap[hash_value] = 1
    return bitmap

def bitmap_hashing(numbers, bitmap_size):
    """Main Bitmap Hashing algorithm."""
    bitmap = initialize_bitmap(bitmap_size)

    for num in numbers:
        # Insert the element into the bitmap
        bitmap = insert_into_bitmap(bitmap, num, bitmap_size)

    return bitmap

# Streamlit app

bitmap_size = st.number_input('Enter your bitmap size: ', min_value=1)

if bitmap_size != 0:

    st.write('Select which operation you want to perform:')
    st.write('1. Insertion')
    st.write('2. Deletion')

    if 'my_set' not in st.session_state:
        st.session_state.my_set = set()

    # Input for adding a value
    inpu = st.number_input("Enter a number to add:", min_value=0)
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

    if len(st.session_state.my_set) > 0:
        # Execute bitmap hashing
        current_bitmap = bitmap_hashing(list(st.session_state.my_set), bitmap_size)

        # Display current bitmap in a pictorial table format
        st.write("Bitmap:")

        # Create a DataFrame to visualize bitmap as a table
        bitmap_df = pd.DataFrame({
            "Index": list(range(bitmap_size)),
            "Bitmap Value": current_bitmap
        })

        # Display the table for the bitmap
        st.table(bitmap_df)

        # Display the current set and its bitmap state
        st.write("Current Set:", st.session_state.my_set)
