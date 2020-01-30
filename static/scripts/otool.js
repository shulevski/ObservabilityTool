var targetsArray;
var targetNames;
var ra;
var dec;

async function populateCoordinates(objectName, callback){
    //url = 'http://cdsweb.u-strasbg.fr/cgi-bin/nph-sesame/-oxp/~NSVA?' + objectName;
    url = 'https://support.astron.nl/cdsweb/cgi-bin/nph-sesame/-oxp/~NSVA?' + objectName; // proxied on the proxy server
    //url = 'http://vizier.cfa.harvard.edu/viz-bin/nph-sesame/-oxp/~N?' + objectName;
    await getCoordinates(url, function(response){
        try{
            if(window.DOMParser){
                parser = new DOMParser();
                xml = parser.parseFromString(response, "text/xml");
                callback(xml.getElementsByTagName("jpos")[0].childNodes[0].nodeValue.split(" "));
            }
        } catch (error){
            callback("ERROR");
        }

    });
}

function getCoordinates(url, callback){
        var xmlHttp = new XMLHttpRequest();
        xmlHttp.onreadystatechange = function() {
            if (xmlHttp.readyState == 4 && xmlHttp.status == 200)
                callback(xmlHttp.responseText);
        }
        xmlHttp.open("GET", url, true); // true for asynchronous 
        xmlHttp.send(null);
}

function submitTargets(){
    console.log("About to submit...................................");
    console.log(document.getElementById("targetList").value);
    var targets = document.getElementById("targetList").value;
    targetsArray = [];
    targetNames = [];
    ra = [];
    dec = [];

    targetsArray = targets.split('\n');
    console.log(targetsArray);
    for(var i = 0; i < targetsArray.length;i++){
        if(targetsArray[i].split(" ").length == 2){
            targetNames.push(i);
            ra.push(targetsArray[i].split(" ")[0]);
            dec.push(targetsArray[i].split(" ")[1]);
            document.getElementById("targets").submit();
        }
        else{
            targetNames.push(targetsArray[i].split(" ")[0]);
            populateCoordinates(targetsArray[i].split(" ")[0], function(coords){
                try{
                    populateTargets(coords);
                    document.getElementById("targets").submit();
                }
                catch(e){
                    $('#malformed').show();
                    $('#malformed').value = e.message;
                }
            });
        }
    }
}

function populateTargets(coords){
    if(coords == "ERROR"){
        throw "Target list malformed.";
    }
    else{
        console.log("Populating coords.");
        console.log("RA before: ", ra);
        ra.push(coords[0]);
        console.log("RA after: ", ra);
        dec.push(coords[1]);
        console.log("Targets array: ", targetsArray);
        console.log("Coords array: ", ra, dec);
        console.log("Target names: ", targetNames);
        document.getElementById("ra").value = ra;
        document.getElementById("dec").value = dec;
        document.getElementById("names").value = targetNames;
        console.log("Ra: ", document.getElementById("ra").value);
    }
}

function validate(){
    if (document.getElementById("elevation").value === '' || document.getElementById("date").value === '' || document.getElementById("targetList").value === ''){
        $('#alert').show();
        return false;
    }
    else{
        return true;
    }
}
