import streamlit as st
import pandas as pd

st.title("Linear Hashing with Pictorial Bucket Representation")

# Linear Hashing functions

def initialize_buckets(level):
    """Initialize buckets for the current level."""
    buckets = {}
    for i in range(2 ** level):
        key = f'{i:b}'.zfill(level)
        buckets[key] = {'values': [], 'local_depth': level}
    return buckets

def hash_function(value, level):
    """Compute the hash function for the given value at the current level."""
    return value % (2 ** level)

def get_bucket_key(hash_value, level):
    """Generate a bucket key by formatting the hash value based on the current level."""
    return f'{hash_value:b}'.zfill(level)

def split_bucket(buckets, split_pointer, level):
    """Split the bucket that has overflowed and distribute the items."""
    new_bucket_key = get_bucket_key(split_pointer + (2 ** level), level + 1)
    old_bucket_key = get_bucket_key(split_pointer, level)

    # Update old bucket key to reflect new depth level
    old_bucket_new_key = get_bucket_key(split_pointer, level + 1)

    print(f'Splitting bucket: {old_bucket_key} -> {old_bucket_new_key}')  # Debug output
    new_bucket = []
    old_bucket = buckets.pop(old_bucket_key)['values']  # Pop removes the old bucket

    # Move items into the new bucket based on their new hash
    for value in old_bucket[:]:
        new_hash = hash_function(value, level + 1)
        if new_hash != split_pointer:
            new_bucket.append(value)
            old_bucket.remove(value)

    # Add the new bucket and update the old bucket key with new depth
    buckets[old_bucket_new_key] = {'values': old_bucket, 'local_depth': level + 1}
    buckets[new_bucket_key] = {'values': new_bucket, 'local_depth': level + 1}

    print(f'New Bucket Created: {new_bucket_key}, Values: {new_bucket}')  # Debug output
    print(f'Old Bucket Updated: {old_bucket_new_key}, Values: {old_bucket}')  # Debug output

    return buckets

def insert_into_buckets(buckets, value, level, split_pointer, bucket_size):
    """Insert value into the appropriate bucket."""
    try:
        hash_value = hash_function(value, level)
        hash_key = get_bucket_key(hash_value, level)
        
    except:
        hash_value = hash_function(value, level+1)
        hash_key = get_bucket_key(hash_value, level+1)

    # Handle case where the hash_key may have been renamed due to splitting
    if hash_key not in buckets:
        # We need to check the previous depth level
        hash_key = get_bucket_key(hash_value, level + 1)
        if hash_key not in buckets:
            raise KeyError(f"Bucket with key {hash_key} not found.")

    print(f'Inserting Value: {value}, Hash Key: {hash_key}')  # Debug output

    if len(buckets[hash_key]['values']) >= bucket_size:
        # Implement chaining for overflow handling before splitting
        return True, buckets  # Indicates overflow
    else:
        buckets[hash_key]['values'].append(value)
        print(f'Value {value} added to Bucket {hash_key}')  # Debug output
        return False, buckets  # Indicates no overflow

def linear_hashing(numbers, bucket_size, load_factor=0.7):
    """Main Linear Hashing algorithm."""
    level = 1
    split_pointer = 0
    num_records = 0
    buckets = initialize_buckets(level)

    for num in numbers:
        num_records += 1
        load = num_records / (len(buckets) * bucket_size)

        # Insert the element into buckets
        flag, buckets = insert_into_buckets(buckets, num, level, split_pointer, bucket_size)

        # Check if we need to split the bucket based on load factor or overflow
        if load > load_factor or flag:
            buckets = split_bucket(buckets, split_pointer, level)
            split_pointer += 1

            # If all buckets at the current level are split, increase the level
            if split_pointer == 2 ** level:
                split_pointer = 0
                level += 1

    return buckets, level

# Streamlit app

bucket_size = st.number_input('Enter your bucket size: ', min_value=1)
load_factor = st.number_input('Enter load factor: ', min_value=0.1, max_value=1.0, value=0.7)

if bucket_size != 0:

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
        # Execute linear hashing
        current_buckets, global_depth = linear_hashing(list(st.session_state.my_set), bucket_size, load_factor)

        # Display current buckets in a pictorial table format
        st.write(f"Global Depth: {global_depth}")
        st.write("Buckets:")

        for bucket_key, bucket_info in current_buckets.items():
            st.subheader(f"Bucket {bucket_key}:")

            # Create a DataFrame for each bucket to visualize it as a table
            bucket_df = pd.DataFrame({
                "Bucket ID": [bucket_key],
                "Values in Bucket": [", ".join(map(str, bucket_info['values']))],
                "Local Depth": [bucket_info['local_depth']]
            })

            # Display the table for each bucket
            st.table(bucket_df)

        # Display the current set and its bucket state
        st.write("Current Set:", st.session_state.my_set)