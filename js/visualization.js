// setup two.js
var elem = document.getElementById('draw');
var params = {width: 1600, height: 1600};
var two = new Two(params).appendTo(elem);

// global variables
var totalSeconds = 0;
var currentYear = 0;
var randomRotation = Math.random(1) * 360;

// add your csv file below
var csvfile = 'example.csv';

// load in svg file
two.load('treering.svg', function(svg)
{
    // create an invisible reference ring
    svg.center();
    svg.translation.set(two.width / 2, two.height / 2);
    svg.noFill();
    svg.noStroke();
    svg.linewidth = 0.1;
    svg.rotation = randomRotation;
    
    // open spreadsheet
    Papa.parse("../" + csvfile, 
    {
        download: true,
        header: true,
        complete: function(results)
        {
            // loop through each video
            $.each(results.data, function(key, value)
            {  
                if(value.seconds != undefined)
                {
                    // update total seconds
                    totalSeconds = totalSeconds + parseInt(value.seconds);

                    // clone svg shape to make ring
                    var newring = svg.clone();
                    newring.noStroke();
                    newring.noFill();
                    newring.stroke = '#b2830b';

                    // get video year
                    var videoDate = value.date.split('-');
                    if(videoDate[0] != currentYear)
                    {
                        // make a thicker line when a new year occurs
                        newring.linewidth = 1.5;
                        currentYear = videoDate[0];
                    } else {
                        newring.linewidth = 0.3;
                    }

                    newring.scale = totalSeconds / 5500;

                    two.update();
                } 
            });
            
            // remove scaling stroke
            $("path").attr("vector-effect", "non-scaling-stroke");
            
            // load in tree bark svg
            two.load('treebark.svg', function(treeBark)
            {
                treeBark.center();
                treeBark.translation.set(two.width / 2, two.height / 2);
                treeBark.noStroke();
                treeBark.fill = '#754d29';
                treeBark.scale = totalSeconds / 5500;
                treeBark.rotation = randomRotation;
                two.update();
            });
        }
    });
    
    two.update();
  
});