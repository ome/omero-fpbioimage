
// COPY all of this file into the bottom of UnityLoader every re-compile

// Change pathToImages to an absolute path
var link = document.createElement("a");
link.href = pathToImages;
pathToImages = (link.protocol+"//"+link.host+link.pathname+link.search+link.hash);

// Get paths in a consistent format: if last character in string is / then remove it!
if (pathToImages.slice(-1) === "/"){
  pathToImages = pathToImages.slice(0,-1);
}
if (pathToFPBioimage.slice(-1) === "/"){
  pathToFPBioimage = pathToFPBioimage.slice(0,-1);
}

// Calculate how much memory we need to request
var memorySize = 536870912;  // Half a gigabyte as the default size.

function nextPow2( aSize ){
  return Math.pow( 2, Math.ceil( Math.log( aSize ) / Math.log( 2 ) ) );
}

firstImage = pathToImages + "/" + imagePrefix + numberingFormat + ".png";

var img = new Image();

img.onload = function(){
  var imHeight = img.height;
  var imWidth = img.width;

  // code here to use the dimensions
  var maxTexturesPerSlice = Math.ceil(numberOfImages/4.0);
  var atlasWidth = nextPow2(imWidth);
  var atlasHeight = nextPow2(imHeight * numberOfImages);

  while ((atlasHeight > 2*atlasWidth) && (atlasHeight > imHeight)){
    atlasHeight /= 2;
    atlasWidth *= 2;
  }

  // Now how much memory do we need?
  var numPixels = atlasHeight * atlasWidth * 4;
  var textureMemory = numPixels * 4;

  if (atlasWidth > 4096 && atlasHeight > 4096){
    memorySize = 1761607680; // Large textures have disproportionaly large memory requirements
  }else{
    memorySize = textureMemory + 134217728; // Add 128MB for other things
  }
  console.log("Total memory requested from browser: " + memorySize + " bytes (" + (memorySize/Math.pow(2,30)).toPrecision(4) + " GiB)");

  fpcanvas = UnityLoader.instantiate("fullBrowserWindow", pathToFPBioimage + "/FPBioimage.json", {onProgress: UnityProgress, Module: {TOTAL_MEMORY: memorySize,
      onRuntimeInitialized: function () {
      UnityProgress(fpcanvas, "complete");
      }
    }
  });

}

//Load in that image, which should start everything else!
var fpcanvas = null;
img.src = firstImage;
