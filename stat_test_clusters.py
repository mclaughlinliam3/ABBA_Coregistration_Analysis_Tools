# Necessary modules. Please install missing ones with pip:
import pandas as pd
from scipy.stats import ttest_ind
import math
import statistics
from scipy.stats import ranksums
import numpy as np


# Methods section:
def list_logs(input_list):
    """Transform a list of floats into their logs, for comparing multiplicative scaled data"""
    output_list = [0] * len(input_list)

    for i, item in enumerate(input_list):
        output_list[i] = math.log(
            (item + 0.1 if item + 0.1 != 0 else item + 0.1001))  # 0.1 is added to the input values to enable comparison of values of 0... since log(0) does not exist. This 0.1 factor can be changes as needed.
        # Note the if statement is here to handle incidents where 0.1+data = 0 whose log would again not exist, although this is unlikely to be encountered.
    return output_list


def read_excel_to_lists(file_path, sheet_name=0):
    """Convert a pd dataframe to lists"""
    # Read the Excel file into a DataFrame without headers
    df = pd.read_excel(file_path, header=None, sheet_name=sheet_name)

    # Initialize an empty list to store the lists of values
    data_lists = []

    # Iterate over each row in the DataFrame
    for index, row in df.iterrows():
        # Convert the row values to a list and append to the data_lists
        data_lists.append(row.tolist())

    return data_lists


def welch_t_test(sample1, sample2):
    """Perform Welch's t-test"""
    t_statistic, p_value = ttest_ind(sample1, sample2, equal_var=False)
    return t_statistic, p_value


def student_t_test(sample1, sample2):
    """Perform Student's t-test"""
    t_statistic, p_value = ttest_ind(sample1, sample2, equal_var=True)
    return t_statistic, p_value


def compare_distributions(sample1, sample2):
    """
    Compare the distributions of two samples using the Wilcoxon Rank Sum Test (Mann-Whitney U).

    Args:
    - sample1 (list of floats): First sample
    - sample2 (list of floats): Second sample

    Returns:
    - test_statistic (float): Test statistic of the Wilcoxon Rank Sum Test
    - p_value (float): p-value indicating the significance of the test
    """

    # Perform Wilcoxon Rank Sum Test
    test_statistic, p_value = ranksums(sample1, sample2)

    return test_statistic, p_value


def save_list_to_csv(data_list, output_file):
    """
    Save a list as a single column in a CSV file using pandas.

    Parameters:
        data_list (list): The list to be saved.
        output_file (str): The path to the output CSV file.
    """
    df = pd.DataFrame(data_list, columns=['Column'])
    df.to_csv(output_file, index=False)


# Main code body:

print(f"This program can be used to do a few significance tests between groups for the data created in this pipeline.\nPlease note this version 'stat_test_clusters' is meant for only the Cluster% statistic, since it compares the distributions' logarithm\nsince Cluster% is on a multiplicative scale. If your data is on an additive scale (such as 'cell counts')\nPlease use 'stat_test' instead\nThe output of this file will be a single column. A value of 1 indicates Group1 is significantly greater for that row (region). \nA value of -1 indicates Group2 is significantly greater.\nA value of 0 indicates no significance\n")


# Get intended stat test from user:
while True:
    stat_test = input(
        "Please select intended stat test. Type 'st' for a student's two sample t test. Type 'wt' for welch's two sample t test. Type 'mw' for a Mann-Whitney U test: ")
    if stat_test == 'st' or stat_test == 'wt' or stat_test == 'mw':
        break

# Get group data from user
p7 = input("Group 1 excel file?: ")
p30 = input("Group 2 excel file?: ")
a = float(input("Alpha value?: "))

# Convert pd df to list
p7_lists = read_excel_to_lists(p7)
p30_lists = read_excel_to_lists(p30)

sig_list = []  # Running list of significances to be saved in the future

# loop through data to do significance test on each region:
for i, p7 in enumerate(p7_lists):

    p30 = p30_lists[i]  # Get current region information


    #The following several lines handle empty excel cells, if they exist for whatever reason. For example, a region may have not had a density...
    p7 = [x for x in p7 if not np.isnan(x)]
    p30 = [x for x in p30 if not np.isnan(x)]

    if not p7 or not p30:
        sig_list.append(0) #In any instance of a totally empty row, siginficance is assumed to be none...
        print(f"Empty data at {i}. Significance assumed to be none for this region.")
        continue

    # Convert to log for multiplicatively scaled data
    p7_log = list_logs(p7)  
    p30_log = list_logs(p30)

    # Perform stat test the user wants
    if stat_test == 'mw':
        t_statistic, p_value = compare_distributions(p7_log, p30_log)
    elif stat_test == 'wt':
        t_statistic, p_value = welch_t_test(p7_log, p30_log)
    elif stat_test == 'st':
        t_statistic, p_value = student_t_test(p7_log, p30_log)

    # This block is to determine which group has greater significance, if at all.
    if p_value >= a:
        sig_list.append(0)

    elif statistics.mean(p7) >= statistics.mean(p30) and p_value < a:
        sig_list.append(1)

    elif statistics.mean(p30) > statistics.mean(p7) and p_value < a:

        sig_list.append(-1)

# Save significance test results as a csv
save_list_to_csv(sig_list, "stat_output.csv")
print("Data has been saved to 'stat_output.csv'")