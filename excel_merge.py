import os
import pandas as pd
import numpy as np
import openpyxl

def get_directory_from_user():
    """Gets directory where data is stored """
    directory_path = input("Enter the directory path to where the excel_crunch output .csv files to be merged are stored. Do not put other files in said directory: ")

    # Check if the entered path is a valid directory
    while not os.path.isdir(directory_path):
        print("Invalid directory path. Please enter a valid directory path.")
        directory_path = input("Enter the directory path: ")

    return directory_path

def load_csv_and_extract_column(csv_file_path, column_index):
    """Opens the csv inputs into df """
    # Read the CSV file into a DataFrame without header
    df = pd.read_csv(csv_file_path, header=None)

    # Extract the specified column (index) as a NumPy array
    column_array = df.iloc[:, column_index].values

    return column_array

def excel_lists(directory, file):
    """Generates lists of all columns from a given .csv file"""
    names = load_csv_and_extract_column(f"{directory}/{file}", 0)
    
    names = names[1:]

    counts = load_csv_and_extract_column(f"{directory}/{file}", 1)

    counts = counts[1:]
    
    sizes = load_csv_and_extract_column(f"{directory}/{file}", 2)

    sizes = sizes[1:]
    
    areas = load_csv_and_extract_column(f"{directory}/{file}", 3)

    areas = areas[1:]

    densities = load_csv_and_extract_column(f"{directory}/{file}", 4)

    densities = densities[1:]

    clusters = load_csv_and_extract_column(f"{directory}/{file}", 5)

    clusters = clusters[1:]

    return names, counts, sizes, areas, densities, clusters

def get_filename_row(file_names):
    """Method to find correct spot to put the name of the original excel file when moving it into the merged excel file. Note that this method is only designed for the excel_crunch output and is not flexible otherwise
    You will need to edit it and the above method for any additional columns that exist in the files to be merged beyond the raw output, assuming you have tinkered with the pipeline"""

    name_list = ['']

    for name in file_names: #Can be replaced with for loop for more flexibility. Get number of '' placeholders from the df column count instead and use that as the loop range...
        name_list.append(name)
        name_list.append('')
        name_list.append('')
        name_list.append('')
        name_list.append('')

    return name_list

def save_dict_to_csv(column_num, my_dict, output_file='merge_output.csv'):
    """Convert a dictionary to a df and save it as .csv"""
    columns = []

    for i in range(column_num):
        columns.append('Cell Count (rough)')
        columns.append('Size(mm2)')
        columns.append('Area (mm2)')
        columns.append('Density')
        columns.append('Cluster%')

    # Create a DataFrame from the dictionary
    df = pd.DataFrame.from_dict(my_dict, orient='index', columns=columns)

    # Reset the index to include 'name' in the CSV file
    df.reset_index(inplace=True)

    # Save the DataFrame to a CSV file in the current working directory
    df.to_csv(output_file, index=False)


def insert_data_to_csv(csv_file, data_list):
    """Edit the csv to add names of the files that each data came from into the excel file"""
    # Read CSV file into DataFrame
    df = pd.read_csv(csv_file)

    # Insert a new empty row at the top
    df.loc[-1] = [None] * len(df.columns)
    df.index = df.index + 1
    df = df.sort_index()

    # Insert data from the list into the new row
    df.iloc[0] = data_list

    # Write the modified DataFrame back to the CSV file
    df.to_csv(csv_file, index=False)




#Main body of code
print(f"This program is designed to merge multiple .csv files that are generated by the 'excel_crunch.py' script into a single .csv file. \nIf the pipeline thus far has created excel_crunch .csv files with differing region order or inconsistent regions,\nthis script will handle that. However, it is only meant to merge the excel_crunch raw output and should not be applied to any other .csv or .xlsx files")
print(f"\nPlease note this script is designed for pandas version 2.2.0. If you have installed a later version of pandas,\nthe script may fail. Please install pandas 2.2.0 if that occurs\nwith 'pip install pandas==2.2.0'")
# Directory path
directory = get_directory_from_user()

# Get list of files in the directory
files = os.listdir(directory)

name_list = get_filename_row(files)

master_dict = {} #Dictionary to be outputted...

# Iterate through the files 
for i, file in enumerate(files):

    names, counts, sizes, areas, densities, clusters = excel_lists(directory, file) #Get lists from columns
    

    if i == 0: #In the case of the first file, the dictionary vals have to be initialized
        for k, name in enumerate(names):
            master_dict[name] = [counts[k], sizes[k], areas[k], densities[k], clusters[k]]

    else: #Otherwise just add to the dictionary for the current file vals...
        for k, name in enumerate(names):
            if name in master_dict:
                master_dict[name].append(counts[k])
                master_dict[name].append(sizes[k])
                master_dict[name].append(areas[k])
                master_dict[name].append(densities[k])
                master_dict[name].append(clusters[k])
            else: #If a new region name has been encountered, add it to the dictionary rather than appending to a previous key
                master_dict[name] = [counts[k], sizes[k], areas[k], densities[k], clusters[k]]



save_dict_to_csv(len(files), master_dict) #Save merged dictionary as .csv
insert_data_to_csv('merge_output.csv', name_list) #Add a row with the names of the files that the data came from to the .csv file so this info is easily available.
print("Data has been merged as 'merge_output.csv'")


