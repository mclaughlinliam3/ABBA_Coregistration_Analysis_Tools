import os
import pandas as pd
import numpy as np

def get_directory_from_user():
    directory_path = input("Enter the directory path to where the cells macro output .csv files to be merged are stored. Do not put other files in said directory: ")

    # Check if the entered path is a valid directory
    while not os.path.isdir(directory_path):
        print("Invalid directory path. Please enter a valid directory path.")
        directory_path = input("Enter the directory path: ")

    return directory_path

def count_files_in_directory(directory_path):
    # Get the list of files in the directory
    files = [f for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f))]
    
    # Get the total number of files
    total_files = len(files)

    return total_files

def load_csv_and_extract_column(csv_file_path, column_index):
    # Read the CSV file into a DataFrame without header
    df = pd.read_csv(csv_file_path, header=None)

    # Extract the specified column (index) as a NumPy array
    column_array = df.iloc[:, column_index].values

    return column_array

def save_dict_to_csv(my_dict, output_file='crunch_output.csv'):
    # Create a DataFrame from the dictionary
    df = pd.DataFrame.from_dict(my_dict, orient='index', columns=['Count', 'Size', 'Area', 'Density', 'Cluster%'])
    
    # Reset the index to include 'name' in the CSV file
    df.reset_index(inplace=True)
    
    # Rename the columns
    df.columns = ['Region Name', 'Cell Count (rough)', 'Size (mm2)', 'Area (mm2)', 'Density', 'Cluster%']

    # Save the DataFrame to a CSV file in the current working directory
    df.to_csv(output_file, index=False)

print(f"This program will merge the .csv files containing the data from the cells macro into one sheet.\nIt expects the order and nature of the .csv files created by the cells macro to have NOT been altered.\nOutput data includes col 1 region names, col2 cell counts, col 3 cell area, col 4 region area, col 5 cell density, col 6 normalized clustering factor.\nSee protocol for more information")

# Replace 'your_csv_file.csv' with the actual CSV file path
directory_path = get_directory_from_user()
total_files = count_files_in_directory(directory_path)

master_counts = {}
master_counts['root'] = [0,0,0]

output_dict = {}


for i in range(total_files // 3):
    # Load CSV data
    names_csv = load_csv_and_extract_column(f"{directory_path}/names{i}.csv", 1)
    names_csv = names_csv[1:]
    counts_csv = load_csv_and_extract_column(f"{directory_path}/counts{i}.csv", 1)
    counts_csv = counts_csv[1:]
    sizes_csv = load_csv_and_extract_column(f"{directory_path}/counts{i}.csv", 2)
    sizes_csv = sizes_csv[1:]
    areas_csv = load_csv_and_extract_column(f"{directory_path}/areas{i}.csv", 1)
    areas_csv = areas_csv[1:]

    mini_dict = {}

    # Create mini dictionary
    for k, item in enumerate(names_csv):


        mini_dict[names_csv[k]] = [counts_csv[k], sizes_csv[k], areas_csv[k]]

    #Update master_counts

    for j in range(len(names_csv)):
        name = names_csv[j]
        current_value = mini_dict[name]

        if name not in master_counts:
        
        	master_counts[name] = [0, 0, 0]

        #Update values in master_counts
        master_name = master_counts[name]

       	master_counts[name] = [float(master_name[0]) + float(current_value[0]), float(master_name[1]) + float(current_value[1]), float(master_name[2]) + float(current_value[2])]


root = master_counts['root']
root = root[1]/root[2]
    
for key, value in master_counts.items():
    try:
        density = value[1]/value[2]
    except ZeroDivisionError:
        density = None #Missing data passed as nothing to excel spreadsheet
    try:
        cluster = density/root
    except TypeError:
        cluster = None

    output_dict[key] = [value[0], value[1], value[2], density, cluster]



save_dict_to_csv(output_dict)
print("Combined file saved to crunch_output.csv")