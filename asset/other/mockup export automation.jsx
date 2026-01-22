// Define paths
var mockupFile = new File("D:\\AI SHOPPING\\RAILS (REALTIME ARTIFICIAL INTERACTIVE LIVE STREAMING) 1.0 alpha\\test1\\asset\\other\\mockup_template.psd");
var designFile = new File("D:\\Mug Shop\\Mug Series\\Mug\\MUG-Mockup-inTable\\Edited Mockup\\Asset\\Design.psb");
var imageFolder = new Folder("D:\\Mug Shop\\Mug Series\\Mug\\Series ID\\Selling\\1-50");
var outputFolder = new Folder("D:\\AI SHOPPING\\RAILS (REALTIME ARTIFICIAL INTERACTIVE LIVE STREAMING) 1.0 alpha\\test1\\asset\\mockup_image");

// Check if the image folder exists
if (!imageFolder.exists) {
    alert("Image folder does not exist at: " + imageFolder.fullName);
    exit();
}

// Get all files in the image folder (checking for common image formats)
var imageFiles = imageFolder.getFiles(/\.(jpg|jpeg|png)$/i);

if (imageFiles.length === 0) {
    alert("No image files found in: " + imageFolder.fullName);
    exit();
}

// Check if the output folder exists
if (!outputFolder.exists) {
    outputFolder.create();
}

// Open the mockup file
app.open(mockupFile);
var mockupDoc = app.activeDocument;

// Open the design file
app.open(designFile);
var designDoc = app.activeDocument;

var frameLayer = null;
for (var l = 0; l < designDoc.layers.length; l++) {
    if (designDoc.layers[l].name === "1 Frame") {
        frameLayer = designDoc.layers[l].layers[0];
        break;
    }
}

function replaceContents(newFile, theSO) {
    app.activeDocument = designDoc;
    designDoc.activeLayer = theSO;
    // =======================================================
    var idplacedLayerReplaceContents = stringIDToTypeID("placedLayerReplaceContents");
    var desc3 = new ActionDescriptor();
    var idnull = charIDToTypeID("null");
    desc3.putPath(idnull, new File(newFile));
    var idPgNm = charIDToTypeID("PgNm");
    desc3.putInteger(idPgNm, 1);
    executeAction(idplacedLayerReplaceContents, desc3, DialogModes.NO);
    return designDoc.activeLayer
};

// Iterate through each image and replace the smart object content
for (var i = 0; i < imageFiles.length; i++) {
    var fileName = imageFiles[i].name.substring(0, imageFiles[i].name.lastIndexOf("."))

    // Replace the frame's content with the current image
    replaceContents(imageFiles[i], frameLayer)

    // Save the modified design
    designDoc.save();

    app.activeDocument = mockupDoc


    // Update the mockup PSD and export each group
    var group = mockupDoc.layers[0];

    // Export to JPG
    var outputFileName = fileName + ".png";
    var outputFile = new File(outputFolder + "/" + outputFileName);

    var pngOptions = new PNGSaveOptions();
    pngOptions.compression = 9; // Maximum compression

    // Save the visible layer to the PNG file
    mockupDoc.saveAs(outputFile, pngOptions, true, Extension.LOWERCASE);
}

alert("Mockups have been exported successfully!");
