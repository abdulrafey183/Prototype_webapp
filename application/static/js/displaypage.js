
let tabs = ["buyer", "plot", "CA", "ET", "deal"];


function clicked(name){
	
	//Turning on the cliked div
	document.getElementById(name+"-div").style.display = 'block';

	//Turning off the rest of divs
	for(let tab of tabs){
		if(tab != name){
			document.getElementById(tab+"-div").style.display = 'none';
			$('#'+name+'-info').html('');
		}
	}
}

function make_plot_card(plot){
	
	let str = "<p>" +
				"Plot ID: "     	+ plot.id 		+ "</br>" +
				"Plot Type: " 		+ plot.type 	+ "</br>" +
				"Plot Address: "	+ plot.address 	+ "</br>" +
				"Plot Status: " 	+ plot.status 	+ "</br>";

	if(!plot.price)
		str += "Plot Price: <span style='color: red;'>Not Set</span></br>";
	else
		str += "Plot Price: " + plot.price + " </br>";

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

function make_buyer_card(buyer){

	let str = "<p>" +
				"Buyer ID: "    + buyer.id    + "</br>" +
				"Buyer Name: "  + buyer.name  + "</br>" +
				"Buyer CNIC: "  + buyer.cnic  + "</br>" +
			  "</p>";

	return str;
}

function make_deal_card(deal){

	let str = "<p>" +
				"Deal ID: "    			+ deal.id    		+ "(<a href='/add/transaction/receivepayment/"+ deal.id +"'>Recieve Payment</a>)</br>" +
				"Date of Signing: " 	+ deal.signing_date + "</br>" +
				"Respective Plot ID: "  + deal.plot_id  	+ "</br>" +
				"Respective Buyer ID: " + deal.plot_id  	+ "</br>" +
			  "</p>";

	return str;

}
function make_CA_card(CA){

	let str = "<p>" +
				"Commission Agent ID: "    + CA.id + "</br>" +
				"Commission Agent Name: "  + CA.name  + "</br>" +
				"Commission Agent CNIC: "  + CA.cnic  + "</br>" +				
			  "</p>";
}

function make_ET_card(ET){

	let str = "<p>" +
				"Expenditure Type: " + ET.name +
				"(<a href='/add/transaction/expense/"+ ET.id +
				"'>Add Expense of this type</a>)</br>"

	return str
}

function inject_div(name, list){
	console.log(list)
	let str 	   = '';
	let make_card  = window['make_'+name+'_card'];
	for(let element of list){
	  	str = make_card(element);			  	
	  	$('#'+name+'-info').append(str);
	}
}

function getall(name){
	console.log("yes");
	clicked((name || "buyer"));
	$.post('/rest/'+name+'/all', function(data){
		inject_div(name, data.json_list);
	});	
}

$(document).ready(function(){
	$("#filterPlot-btn").on('click', function(){
		$.post('/rest/filterplot/'+$("#status").val(), function(plots) {
			$('#plot-info').html('');
		 	inject_div('plot', plots.json_list);		  
		});
	});
});