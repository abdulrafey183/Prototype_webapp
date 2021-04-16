
let tabs = ["buyers", "plots", "CAs", "ETs"];


function clicked(name){
	//Turning on the cliked button and div
	document.getElementById(name+"-div").style.display = 'block';
	document.getElementById(name+"-button").className  = 'btn btn-info';

	//Turning off the resst of buttons and divs
	for(let tab of tabs){
		if(tab != name){
			document.getElementById(tab+"-div").style.display = 'none';
			document.getElementById(tab+"-button").className  = 'btn btn-outline-info';
		}
	}
}

function makePlotCard(plot){
			console.log(plot.deal);
			let str = "<p>" +
						"Plot ID: "     	+ plot.id 		+ "</br>" +
						"Plot Type: " 		+ plot.type 		+ "</br>" +
						"Plot Address: "	+ plot.address 	+ "</br>" +
						"Plot Status: " 	+ plot.status 	+ "</br>";

			if(!plot.price)
				str += "Plot Price: <span style='color: red;''>Not Set</span></br>";

			str += "Plot Size: " 		+ plot.size 		+ "</br>" +
				   "Plot Comments: " 	+ plot.comments 	+ "</br>";

			if(plot.deal){
				str += "Plot's Deal: " + 
				"<a href='" + "/dealinfo/" + plot.deal.id + "''>" + 
					plot.deal.id + 
				"</a></br>";
			}

			return str + "</p>\n";
		}

$(document).ready(function(){
	$("#filter-btn").on('click', function(){
		console.log($("#status").val());
		$.post('/rest/filterplot/'+$("#status").val(), function(plots) {
		  let str = '';
		  for(let plot of plots.json_list){
		  	str += makePlotCard(plot);
		  }
		  $("#plots-info").html(str);
		  
		});
	});
});