
// Create deviation badges.
var badge_box = d3.select("#deviation-badges").selectAll("div")
    .data(deviation_badge_data)
  .enter().append("div")
    .attr("class", function(d) {
        if (category_list.indexOf(d[2]) > -1) {
            var color_class = color(d[2]); 
        }
        else {
            var color_class = 'gray';
        }
        return "single-badge " + color_class;
        })

badge_box.append('div')
    .text(function(d) {return d[0]});

badge_box.append('p')
    .text(function(d) {return d[1]});



// Create on-time percentage badges.
var badge_box = d3.select("#otp-badges").selectAll("div")
    .data(otp_badge_data)
  .enter().append("div")
    .attr("class", function(d, i) {
        return "single-badge " + "q" + i + "-5" }
        );

badge_box.append('div')
    .text(function(d) {return d[1]});

badge_box.append('p')
    .text(function(d) {return d[0]});


// Create rank badges.
var badge_box = d3.select("#rank-badges").selectAll("div")
     .data(rank_badge_data)
  .enter().append("div")
    .attr("class", function(d, i) {

        // High values are good for OTP, but low values are good for rank. For
        // the color() to work on both, the color name classes are mapped to
        // color ramp rank values in the reverse order. But that means that if
        // you generate badges in the same order, you get the green ones on the
        // left and the red ones on the right, the opposite of the otp badges.
        // The following line is an absurdly hacky way to create the rank badges
        // in reverse index order, i.e. from red to green.
        reverse_index = 4 - i
        return "single-badge " + "q" + reverse_index + "-5" } 
        );

// The count and rank labels are also being reversed in the view before being
// passed to this script.
badge_box.append('div')
    .text(function(d) {return d[1]});

badge_box.append('p')
    .text(function(d) {return d[0][1]});
