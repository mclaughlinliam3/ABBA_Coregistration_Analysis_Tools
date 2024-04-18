// Prompt user for input and output directories
input = getDirectory("Select input folder: ");
output = getDirectory("Select output folder: ");

// Get a list of all TIFF files in the input directory
list = getFileList(input);

// Set batch mode to true to avoid showing intermediate images
setBatchMode(true);

// Loop through the list and process two images at a time
for (i = 0; i < list.length; i += 4) {
    // Open two consecutive images
    open(input + list[i]);
    channelName1 = getTitle();
    run("Close");
    open(input + list[i + 1]);
    channelName2 = getTitle();
    run("Close");
    open(input + list[i + 2]);
    channelName3 = getTitle();
    run("Close");
    open(input + list[i + 3]);
    channelName4 = getTitle();
    run("Close");
	
	open(input + list[i]);
	open(input + list[i + 1]);
	open(input + list[i + 2]);
	open(input + list[i + 3]);

    // Merge the two images into a two-channel image
    run("Merge Channels...", "c1=" + channelName1 + " c2=" + channelName2 + " c3=" + channelName3 + " c4=" + channelName4 + " create");

    // Save the merged image in the output directory
    saveAs("Tiff", output + "merged_" + i/4);

    // Close the opened images
    run("Close All");
}

// Set batch mode back to false
setBatchMode(false);