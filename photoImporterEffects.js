// ExtendScript for Adobe After Effects to import all photos from a folder into a composition with specific duration in milliseconds

// Path to the folder containing photos
var folderPath = "/Users/will/codingProjects/editMaker/downloaded_images";  // Update this to your folder path

// Desired duration for each photo in milliseconds
var photoDurationMs = 100; // 5000 milliseconds (5 seconds)

// Function to get all image files from a folder
function getPhotoPaths(folderPath) {
    var folder = new Folder(folderPath);
    var files = folder.getFiles(function(file) {
        return file instanceof File && /\.(jpg|jpeg|png|gif)$/i.test(file.name);
    });
    $.writeln("Found " + files.length + " files.");
    return files.map(function(file) {
        return file.fsName;
    });
}

// Function to import files and return the imported project items
function importFiles(filePaths) {
    var importedItems = [];
    for (var i = 0; i < filePaths.length; i++) {
        var importOptions = new ImportOptions(new File(filePaths[i]));
        if (importOptions.canImportAs(ImportAsType.FOOTAGE)) {
            importOptions.importAs = ImportAsType.FOOTAGE;
            var importedFile = app.project.importFile(importOptions);
            importedItems.push(importedFile);
        }
    }
    return importedItems;
}

// Function to create a new composition
function createNewComposition(compName, width, height, duration, frameRate) {
    var comp = app.project.items.addComp(compName, width, height, 1, duration, frameRate);
    return comp;
}

// Function to add items to the composition with specific duration in milliseconds
function addItemsToComposition(comp, items, durationMs) {
    var durationSec = durationMs / 1000; // Convert milliseconds to seconds
    for (var i = 0; i < items.length; i++) {
        var layer = comp.layers.add(items[i]);
        layer.startTime = i * durationSec;
        layer.outPoint = layer.startTime + durationSec;
    }
}

// Main function to execute the script
function main() {
    app.beginUndoGroup("Import Photos to Composition");

    var photoPaths = getPhotoPaths(folderPath);
    var importedItems = importFiles(photoPaths);
    
    // Set composition settings
    var compWidth = 1920;
    var compHeight = 1080;
    var compFrameRate = 30;
    var compDuration = (importedItems.length * photoDurationMs) / 1000; // Convert to seconds
    
    var comp = createNewComposition("Photo Composition", compWidth, compHeight, compDuration, compFrameRate);
    addItemsToComposition(comp, importedItems, photoDurationMs);

    app.endUndoGroup();
}

// Execute the main function
main();
