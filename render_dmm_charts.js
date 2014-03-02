
/* render_dmm_charts.js
	render the model momentum charts to individuals files to serve up in email.
	jpb, 2/17/2014
	requires phantomjs to render 

	Note:  separate rendering is required for the dmm and cross shop reports because they are different sizes.

*/

var RenderUrlsToFile, arrayOfUrls, system;
system = require("system");
 

/*
Render given urls
@param array of URLs to render
@param callbackPerUrl Function called after finishing each URL, including the last URL
@param callbackFinal Function called after finishing everything
*/
RenderUrlsToFile = function(urls, callbackPerUrl, callbackFinal) {
    var getFilename, next, page, retrieve, urlIndex, webpage;
    urlIndex = 0;
    webpage = require("webpage");
    page = null;
    getFilename = function() {
        return "client_dmm_" + urlIndex + ".png";
    };
    next = function(status, url, file) {
        page.close();
        callbackPerUrl(status, url, file);
        return retrieve();
    };
    retrieve = function() {
        var url;
        if (urls.length > 0) {
            url = urls.shift();
            urlIndex++;
            page = webpage.create();
			
			page.clipRect = {
								top: 0,
								left: 0,
								width: 202,
								height: 140
			};
			
            page.settings.userAgent = "Phantom.js bot";
            return page.open(url, function(status) {
                var file;
                file = getFilename();
                if (status === "success") {
                    return window.setTimeout((function() {
                        page.render(file);
                        return next(status, url, file);
                    }), 200);
                } else {
                    return next(status, url, file);
                }
            });
        } else {
            return callbackFinal();
        }
    };
    return retrieve();
};




if (phantom.args.length != 1) {
    console.log('Usage: loopurls.js # , where # is the number of loops');
    phantom.exit();
} else {
    maxurls = phantom.args[0];
	console.log('max urls is: ' + maxurls);
	
	// array to hold the URLs
	var arrayOfUrls = new Array();
	// create an array of URLs for processing here
	for (var i=0; i<maxurls; i++) {
		arrayOfUrls.push("https://report-ninja-c9-muttinthehut.c9.io/client_dmm/get/"+(i+1)+"/");
	}
    
		RenderUrlsToFile(arrayOfUrls, (function(status, url, file) {
			if (status !== "success") {
				return console.log("Unable to render '" + url + "'");
			} else {
				return console.log("Rendered '" + url + "' at '" + file + "'");
			}
	}), function() {
		return phantom.exit();
	});
	
	}
	
	
	// all URLs created now.
	
	// jpb, commented out from original
	// page.viewportSize = { width: 200, height: 200 };
    // page.paperSize = { width: 1024, height: 768, border: '0px' }
	// jpb, end of comment

		
