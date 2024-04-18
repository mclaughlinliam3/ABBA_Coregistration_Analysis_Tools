// Prompt user for input and output directories
input = getDirectory("Select input folder: ");
output = getDirectory("Select output folder: ");

// Get a list of all TIFF files in the input directory
list = getFileList(input);

// Set batch mode to true to avoid showing intermediate images
setBatchMode(true);

// Loop through the list
for (k = 0; k < list.length; k ++) {
	open(input + list[k]);
	name = getTitle();
	run("List Elements");
	run("To ROI Manager");
	setOption("BlackBackground", true);

    // Load ROIs into the ROI Manager
    run("ROI Manager...");
    roiManager("Show All");

    // Initialize an array to hold ROI names and particle counts
    roiParticleCounts = newArray();

    // Loop through each ROI in the ROI Manager
    n = roiManager("count");
    for (i = 0; i < n; i++) {
        // Select the ROI
        roiManager("Select", i);

        // Run particle analysis
        run("Analyze Particles...", "size=0-Infinity circularity=0.00-1.00 show=Nothing summarize");

    }


    // Specify the path and file name for the CSV file to be saved
    saveAs("Results", output + "counts" + k + ".csv");
    
    run("Close", "name=Summary");
    
    for (i = 0; i < n; i++) {
	    // Select the ROI
	    roiManager("Select", i);
	
	    // Run particle analysis
	    run("Measure");
    

    }
    
    
    saveAs("Results", output + "areas" + k + ".csv");
    
    run("Close", "name=Results");

    run("ROI Manager...");
    roiManager("Show All");

    // Initialize an array to hold ROI names and particle counts
    roiParticleCounts = newArray();

    // Loop through each ROI in the ROI Manager
    n = roiManager("count");
    for (i = 0; i < n; i++) {
        // Select the ROI
        roiManager("Select", i);

        // Retrieve the particle count directly from the Results table
        z_slice = k;

        // Get the ROI name
        roiManager("Select", i);
        roiName = Roi.getName();

        // Store the ROI name and particle count in an array
        roiParticleCounts = Array.concat(roiParticleCounts, newArray(roiName, z_slice));

        // Clear the Results table for the next iteration
        run("Clear Results");
    }

    // Create a new Results window and populate it with the data
    for (j = 0; j < roiParticleCounts.length; j += 2) {
        setResult("ROI Name", j / 2, roiParticleCounts[j]);
        setResult("Z-slice", j / 2, roiParticleCounts[j + 1]);
    }

    updateResults(); // Update the Results table with the new data

    saveAs("Results", output + "names" + k + ".csv");
    
    // Close all open images
	run("Close All");

	run("Close All", "name=Summary");
	close("ROI Manager");
	close("Results");

}

setBatchMode(false);
