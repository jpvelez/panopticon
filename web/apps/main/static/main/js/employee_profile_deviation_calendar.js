// Initialize calendar and day rectangle dimensions.
var width = 905,
    height = 125,
    cellSize = 17; // cell size

// Create helper functions that return a date's day-of-the-week and week-of-the-year numbers.
var day = d3.time.format("%w"),
    week = d3.time.format("%U"),
    percent = d3.format(".1%"),
    format = d3.time.format("%Y-%m-%d");

var category_list = [
  'Vacation', 
  'Holiday', 
  'Sick',
  'F.M.L.A.', 
  'Out for a while',
  'Accident/Incident',
  'Injured On Duty', 
  'Missed', 
  'Referred to Mgr', 
  'Suspension',
  'Training', 
  'Trade', 
  ]

// Map deviation groups to day colors.
var color = d3.scale.ordinal()
    .domain(category_list)
    .range(d3.range(12).map(function(i) { return "q" + i + "-12"; }));

// Draw calendar.
var svg = d3.select("#deviation-cal").selectAll("svg")
    .data([2012])
  .enter().append("svg")
    .attr("width", width)
    .attr("height", height)
    .attr("class", "deviation-colors")
  .append("g")
    .attr("transform", "translate(" + ((width - cellSize * 53) / 2) + "," + (height - cellSize * 7 - 1) + ")");

// Draw day rectangles.
var rect = svg.selectAll(".day")
    .data(function(d) { return d3.time.days(new Date(d, 0, 1), new Date(d + 1, 0, 1)); })
  .enter().append("rect")
    .attr("class", "day")
    .attr("width", cellSize)
    .attr("height", cellSize)
    .attr("x", function(d) { return week(d) * cellSize; })
    .attr("y", function(d) { return day(d) * cellSize; })
    .datum(format);

// Draw month path around day rectangles using monthPath() function.
svg.selectAll(".month")
    .data(function(d) { return d3.time.months(new Date(d, 0, 1), new Date(d + 1, 0, 1)); })
  .enter().append("path")
    .attr("class", "month")
    .attr("d", monthPath);

// Define algorithm that draws month path.
function monthPath(t0) {
  var t1 = new Date(t0.getFullYear(), t0.getMonth() + 1, 0),
      d0 = +day(t0), w0 = +week(t0),
      d1 = +day(t1), w1 = +week(t1);
  return "M" + (w0 + 1) * cellSize + "," + d0 * cellSize
      + "H" + w0 * cellSize + "V" + 7 * cellSize
      + "H" + w1 * cellSize + "V" + (d1 + 1) * cellSize
      + "H" + (w1 + 1) * cellSize + "V" + 0
      + "H" + (w0 + 1) * cellSize + "Z";
}

// Select only day rectangles that have deviation data.
var deviation_rect = rect.filter(function(d) { return d in calendar_deviations; })

// Color deviation rectangles according to their group using the color()function. 

// If deviation's group is in the category group list, fetch group's
// css color class name and add it to the day rectangle. Otherwise, default to
// the "gray" css color class.
deviation_rect.attr("class", function(d) { 
    if (category_list.indexOf(calendar_deviations[d][0]) > -1) {
      return "day " + color(calendar_deviations[d][0]); 
    }
    else {
      // return "day " + color(calendar_deviations[d]); 
      return "day gray"
    }
    })
  .select("title")
    .text(function(d) { return d + ": " + calendar_deviations[d][1]; 
  });

// Generate tooltip for day rectangles.
rect.on("mouseover", function (d){
      var title_text = "<p>" + d + ": " + calendar_deviations[d][1] + "</p>";
      var pos = $(this).offset();
       $("#tooltip").html(title_text)
          .css({top: pos.top + 20, left: pos.left + 40})
          .show();
      })
  .on("mouseout", function (d){
      $("#tooltip").hide();
      });
