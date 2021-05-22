let tabs = ['buyer', 'plot', 'CA', 'ET', 'deal',  'employee'];

function clicked(name) {
  //Turning on the cliked div
  document.getElementById(name + '-div').style.display = 'block';

  //Turning off the rest of divs
  for (let tab of tabs) {
    if (tab != name) {
      document.getElementById(tab + '-div').style.display = 'none';
      $('#' + name + '-info').html('');
    }
  }
}

function make_plot_card(plot) {
  let str =
    "<div class='accordion' id='accordionExample'><div class='card'><div class='card-header' id='headingOne'><h2 class='mb-0'><button class='btn btn-link btn-block text-left' type='button' data-toggle='collapse' data-target='#collapseBuyer" +
    plot.id +
    "' aria-expanded='true' aria-controls='collapseBuyer" +
    plot.id +
    "'>" +
    "PLOT# "+ plot.id + " - " + plot.address +
    "</button></h2></div><div id='collapseBuyer" +
    plot.id +
    "' class='collapse' aria-labelledby='headingOne' data-parent='#accordionExample'><div class='card-body'>" +
    "<section class='my-3'><div class='container'><div class='row'><div class='col-12'><table class='table mt-4'><tbody><tr class='text-dark-3'><th scope='row'>Id</th><td>" +
    plot.id +
    "</td></tr><tr class='text-dark-3'><th scope='row'>Type</th><td>" +
    plot.type +
    "</td></tr><tr class='text-dark-3'><th scope='row'>Address</th><td>" +
    plot.address +
    "</td></tr><tr class='text-dark-3'><th scope='row'>Status</th><td>" +
    plot.status +
    '</td></tr>';

  if (!plot.price)
    str += "<tr class='text-dark-3'><th scope='row'>Price</th><td><span style='color: red;'>Not Set</span></td></tr>";
  else
    str +=  "<tr class='text-dark-3'><th scope='row'>Price</th><td>" +
            plot.price +
            "</td></tr>";

  str +=    "<tr class='text-dark-3'><th scope='row'>Size</th><td>" +
            plot.size +
            "</td></tr>";

  if (plot.deal)
    str +=  "<tr class='text-dark-3'><th scope='row'>Deal</th><td><a href='/deal/" +
            plot.deal.id +
            "'>" +
            "Deal# " + plot.deal.id +
            "</a></td></tr>";
  

  str +=    "<tr class='text-dark-3'><td scope='row'>" +
            "<span><a href='/plot/" + plot.id + "''>Show Details</a></span></td><td></td>" +
            "</tr>"
             

  return (
    str + '</tbody></table></div></div></div></section></div></div></div></div>'
  );
}

function make_buyer_card(buyer) {
  
  var deal_ids = '';
  if(buyer.deals != null)
    for(var deal of buyer.deals){ deal_ids += ' <a href="/deal/' + deal.id + '">Deal#' + deal.id + '</a><br>'; }
  else
    deal_ids = 'None';

  let str =
    "<div class='accordion' id='accordionExample'><div class='card'><div class='card-header' id='headingOne'><h2 class='mb-0'><button class='btn btn-link btn-block text-left' type='button' data-toggle='collapse' data-target='#collapseBuyer" +
    buyer.id +
    "' aria-expanded='true' aria-controls='collapseBuyer" +
    buyer.id +
    "'>" +
    buyer.person.name +
    "</button></h2></div><div id='collapseBuyer" +
    buyer.id +
    "' class='collapse' aria-labelledby='headingOne' data-parent='#accordionExample'><div class='card-body'>" +
    "<section class='my-3'><div class='container'><div class='row'><div class='col-12'><table class='table mt-4'><tbody<tr class='text-dark-3'><th scope='row'>Name</th><td>" +
    "<a href='/buyer/" + buyer.id + "'>" +
    buyer.person.name +
    "</a></td></tr><tr class='text-dark-3'><th scope='row'>CNIC</th><td>" +
    buyer.person.cnic +
    '</td></tr><tr class="text-dark-3"><th scope="row">Phone</th><td>' +
    buyer.person.phone +
    '</td></tr><tr class="text-dark-3"><th scope="row">Email</th><td>' +
    buyer.person.email +
    '</td></tr>';

    if(deal_ids != 'None'){
      str += '<tr class="text-dark-3"><th scope="row">Deals</th><td>' + deal_ids + '</td></tr>';
    }
    str += '</tbody></table></div></div></div></section>' +
    '</div></div></div></div>';

  return str;
}

function make_deal_card(deal) {
  
  let str =
    "<div class='accordion' id='accordionExample'><div class='card'><div class='card-header' id='headingOne'><h2 class='mb-0'><button class='btn btn-link btn-block text-left' type='button' data-toggle='collapse' data-target='#collapseBuyer" +
    deal.id +
    "' aria-expanded='true' aria-controls='collapseBuyer" +
    deal.id +
    "'>" +
    "DEAL# " + deal.id +
    "</button></h2></div><div id='collapseBuyer" +
    deal.id +
    "' class='collapse' aria-labelledby='headingOne' data-parent='#accordionExample'><div class='card-body'>" +
    "<section class='my-3'><div class='container'><div class='row'><div class='col-12'><table class='table mt-4'><tbody><tr class='text-dark-3'><td scope='row'><a href='/add/transaction/receivepayment/" + deal.id + "'>Recieve Payment</a></td><td>" +
    "</td></tr>" +
    "<tr class='text-dark-3'><th scope='row'>Date of Signing</th><td>" +
    deal.signing_date +
    "</td></tr><tr class='text-dark-3'><th scope='row'>Respective Plot</th><td>" +
    deal.plot_id +
    "</td></tr><tr class='text-dark-3'><th scope='row'>Respective Buyer</th><td>" +
    "<a href='/buyer/" + deal.buyer_id + "'><div class='buyer-" + deal.buyer_id + "'>" +
    "</div></a>" +
    "</td></tr><tr class='text-dark-3'><td><a href='/deal/" +
    deal.id +
    "'>Show Details</a></td><td></td></tr></tbody></table></div></div></div></section>";

  return str; 
}
function make_CA_card(CA) {

  var deal_ids = '';
  if(CA.deals != null)
    for(var deal of CA.deals){ deal_ids += ' <a href="/deal/' + deal.id + '">' + deal.id + '</a>'; }
  else
    deal_ids = 'None';

  let str =
    "<div class='accordion' id='accordionExample'><div class='card'><div class='card-header' id='headingOne'><h2 class='mb-0'><button class='btn btn-link btn-block text-left' type='button' data-toggle='collapse' data-target='#collapseBuyer" +
    CA.person.id +
    "' aria-expanded='true' aria-controls='collapseBuyer" +
    CA.person.id +
    "'>" +
    CA.person.name +
    "</button></h2></div><div id='collapseBuyer" +
    CA.person.id +
    "' class='collapse' aria-labelledby='headingOne' data-parent='#accordionExample'><div class='card-body'>" +
    "<section class='my-3'><div class='container'><div class='row'><div class='col-12'><table class='table mt-4'><tbody><tr class='text-dark-3'><th scope='row'>Name</th><td>" +
    "<a href='/agent/" + CA.person.id + "'>" +
    CA.person.name +
    "</a></td></tr><tr class='text-dark-3'><th scope='row'>CNIC</th><td>" +
    CA.person.cnic +
    "</td></tr><tr class='text-dark-3'><th scope='row'>Phone</th><td>" +
    CA.person.phone +
    "</td></tr><tr class='text-dark-3'><th scope='row'>Email</th><td>" +
    CA.person.email + "</td></tr>";

  if(deal_ids != 'None'){
    str += "<tr class='text-dark-3'><th scope='row'>Deals</th><td>" + deal_ids + "</td></tr>";
  }
  str +=
    '</tbody></table></div></div></div></section>' +
    '</div></div></div></div>';

  return str;
}

function make_ET_card(ET) {
  let str =
    "<div class='accordion' id='accordionExample'><div class='card'><div class='card-header' id='headingOne'><h2 class='mb-0'><button class='btn btn-link btn-block text-left' type='button' data-toggle='collapse' data-target='#collapseBuyer" +
    ET.id +
    "' aria-expanded='true' aria-controls='collapseBuyer" +
    ET.id +
    "'>" +
    ET.name +
    "</button></h2></div><div id='collapseBuyer" +
    ET.id +
    "' class='collapse' aria-labelledby='headingOne' data-parent='#accordionExample'><div class='card-body'>" +
    "<section class='my-3'><div class='container'><div class='row'><div class='col-12'><table class='table mt-4'><tbody><tr class='text-dark-3'><th scope='row'>Id</th><td><a href='expenditure/" +
    ET.id +
    "'>" +
    ET.id +
    "</a></td></tr><tr class='text-dark-3'><th scope='row'>Type</th><td>" +
    ET.name +
    "</td></tr></tbody></table><a href='/expenditure/" +
    ET.id + "'>Show Details</a></div></div></div></section>" +
    '</div></div></div></div>';

  return str;
}
 
function make_employee_card(employee) {
  let str =
    "<div class='accordion' id='accordionExample'><div class='card'><div class='card-header' id='headingOne'><h2 class='mb-0'><button class='btn btn-link btn-block text-left' type='button' data-toggle='collapse' data-target='#collapseBuyer" +
    employee.id +
    "' aria-expanded='true' aria-controls='collapseBuyer" +
    employee.id +
    "'>" +
    employee.person.name +
    "</button></h2></div><div id='collapseBuyer" +
    employee.id +
    "' class='collapse' aria-labelledby='headingOne' data-parent='#accordionExample'><div class='card-body'>" +
    "<section class='my-3'><div class='container'><div class='row'><div class='col-12'><table class='table mt-4'><tbody>" +
    "<tr class='text-dark-3'>" + 
      "<th scope='row'>Name</th>" + 
      "<td><a href='/employee/" + employee.id +"'>" + employee.person.name + "</a></td>" + 
    "</tr>";

  if(employee.rank == 1){
    str +=  "<tr class='text-dark-3'>" + 
              "<th scope='row'>Type</th>" + 
              "<td>User</td>" + 
            "</tr>" +
            "<tr class='text-dark-3'>" + 
              "<th scope='row'>Email ID</th>" + 
              "<td>" + employee.person.email + "</td>" + 
            "</tr>";
  }
  else if(employee.rank == 2){
    str +=  "<tr class='text-dark-3'>" + 
              "<th scope='row'>Type</th>" + 
              "<td>Employee</td>" + 
            "</tr>";
  }

  return str + "</tbody></table></div></div></div></section></div></div></div></div>";
}


function inject_div(name, list) {
  let str = '';
  let make_card = window['make_' + name + '_card'];
  for (let element of list) {
    str = make_card(element);
    $('#' + name + '-info').append(str);
    if(name=='deal')
      getbuyer(element.buyer_id);
  }
}

function getall(name) {
  clicked(name || 'buyer');
  $.post('/rest/' + name + '/all', function (data) {
    inject_div(name, data.json_list);
  });
}

function getbuyer(id) {
  $.post('/rest/' + 'Buyer' + '/' + id, function (data) {
    for (let element of data.json_list) {
        $('.buyer-' + id).text(element.person.name);
      }
  });
}

$(document).ready(function () {
  $('#filterPlot-btn').on('click', function () {
    $.post('/rest/filterplot/' + $('#status').val(), function (plots) {
      $('#plot-info').html('');
      inject_div('plot', plots.json_list);
    });
  });
});
