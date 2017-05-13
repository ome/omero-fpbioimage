// First, should do some checking of paths: if last character in string is / then remove it!
if (pathToImages.slice(-1) === "/"){
  pathToImages = pathToImages.slice(0,-1);
}
if (pathToFPBioimage.slice(-1) === "/"){
  pathToFPBioimage = pathToFPBioimage.slice(0,-1);
}

// Now, set memory size for the webpage based on the number of pixels.
var memorySize = 536870912;  // Half a gigabyte as the default size.

function nextPow2( aSize ){
  return Math.pow( 2, Math.ceil( Math.log( aSize ) / Math.log( 2 ) ) );
}

firstImage = pathToFPBioimage + "/../" + pathToImages + "/" + imagePrefix + numberingFormat + ".png";

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

  // Create the global variable "Module"
  Module = {
  TOTAL_MEMORY: memorySize,
  errorhandler: null,
  compatibilitycheck: null,
  dataUrl: pathToFPBioimage + "/FPBioimage.data",
  codeUrl: pathToFPBioimage + "/FPBioimage.js",
  memUrl: pathToFPBioimage + "/FPBioimage.mem",
  };

  // Start the viewer by inserting the UnitLoader javascript into the webpage:
  var s = document.createElement("script");
      s.type = "text/javascript";
      s.src = pathToFPBioimage + "/UnityLoader.js";
      s.innerHTML = null;
      document.getElementById("scriptLoader").innerHTML = "";
      document.getElementById("scriptLoader").appendChild(s);
}

img.src = firstImage;
