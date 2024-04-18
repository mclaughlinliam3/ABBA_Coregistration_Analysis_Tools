// Prompt user for input and output directories
input = getDirectory("Select input folder: ");
output = getDirectory("Select output folder: ");

// Get a list of all TIFF files in the input directory
list = getFileList(input);

// Set batch mode to true to avoid showing intermediate images
setBatchMode(true);

// Loop through the list and process two images at a time
for (i = 0; i < list.length; i += 7) {
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
    open(input + list[i + 4]);
    channelName5 = getTitle();
    run("Close");
    open(input + list[i + 5]);
    channelName6 = getTitle();
    run("Close");
    open(input + list[i + 6]);
    channelName7 = getTitle();
    run("Close");
	
	open(input + list[i]);
	open(input + list[i + 1]);
	open(input + list[i + 2]);
	open(input + list[i + 3]);
	open(input + list[i + 4]);
	open(input + list[i + 5]);
	open(input + list[i + 6]);

    // Merge the two images into a two-channel image
    run("Merge Channels...", "c1=" + channelName1 + " c2=" + channelName2 + " c3=" + channelName3 + " c4=" + channelName4 + " c5=" + channelName5 + " c6=" + channelName6 + " c7=" + channelName7 + " create");

    // Save the merged image in the output directory
    saveAs("Tiff", output + "merged_" + i/7);

    // Close the opened images
    run("Close All");
}

// Set batch mode back to false
setBatchMode(false);