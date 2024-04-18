import numpy as np
import tifffile

def reslice_tiff(file_path, factor):
    # Load the TIFF file into a numpy array
    with tifffile.TiffFile(file_path) as tif:
        data = tif.asarray()
    
    # Validate the Z dimension is compatible with the reslice factor
    z_dim = data.shape[0]  # Assuming the first dimension is Z
    if z_dim % factor != 0:
        print("Warning: Z dimension is not perfectly divisible by the factor. Some slices may be omitted.")
    
    # Reslice the array by selecting every 'factor'th slice in Z
    resliced_data = data[::factor]
    
    # Save the resliced array as a new TIFF file
    tifffile.imwrite('reslice_output.tif', resliced_data)
    print(f"Resliced TIFF saved as 'reslice_output.tif'. Dimensions: {resliced_data.shape}")

if __name__ == "__main__":
    # Prompt the user for the file location
    file_location = input("Enter the location of the TIFF file: ")
    
    # Specify the reslice factor here
    reslice_factor = int(input("Reslice factor?: "))
    
    # Call the function with the user's file and the specified factor
    reslice_tiff(file_location, reslice_factor)