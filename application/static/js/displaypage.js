let tabs = ['buyer', 'plot', 'CA', 'ET', 'deal'];

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
    plot.address +
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
    str +=
      "<tr class='text-dark-3'><th scope='row'>Price</th><td><span style='color: red;'>Not Set</span></td></tr>";
  else
    str +=
      "<tr class='text-dark-3'><th scope='row'>Price</th><td>" +
      plot.price +
      '</td></tr>';

  str +=
    "<tr class='text-dark-3'><th scope='row'>Size</th><td>" +
    plot.size +
    "</td></tr><tr class='text-dark-3'><th scope='row'>Comments</th><td>" +
    plot.comments +
    '</td></tr>';

  if (plot.deal) {
    str +=
      "<tr class='text-dark-3'><th scope='row'>Deal</th><td><a href='/dealinfo/" +
      plot.deal.id +
      "'>" +
      plot.deal.id +
      '</a></td></tr>';
  }

  return (
    str + '</tbody></table></div></div></div></section></div></div></div></div>'
  );
}

function make_buyer_card(buyer) {
  let str =
    "<div class='accordion' id='accordionExample'><div class='card'><div class='card-header' id='headingOne'><h2 class='mb-0'><button class='btn btn-link btn-block text-left' type='button' data-toggle='collapse' data-target='#collapseBuyer" +
    buyer.id +
    "' aria-expanded='true' aria-controls='collapseBuyer" +
    buyer.id +
    "'>" +
    buyer.name +
    "</button></h2></div><div id='collapseBuyer" +
    buyer.id +
    "' class='collapse' aria-labelledby='headingOne' data-parent='#accordionExample'><div class='card-body'>" +
    "<section class='my-3'><div class='container'><div class='row'><div class='col-12'><table class='table mt-4'><tbody><tr class='text-dark-3'><th scope='row'>Id</th><td>" + "<a href='/buyer/" +
    buyer.id +
    "'>" +
    buyer.id +
    "</a></td></tr><tr class='text-dark-3'><th scope='row'>Name</th><td>" +
    buyer.name +
    "</td></tr><tr class='text-dark-3'><th scope='row'>CNIC</th><td>" +
    buyer.cnic +
    '</td></tr></tbody></table></div></div></div></section>' +
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
    deal.id +
    "</button></h2></div><div id='collapseBuyer" +
    deal.id +
    "' class='collapse' aria-labelledby='headingOne' data-parent='#accordionExample'><div class='card-body'>" +
    "<section class='my-3'><div class='container'><div class='row'><div class='col-12'><table class='table mt-4'><tbody><tr class='text-dark-3'><th scope='row'>Id</th><td>" +
    deal.id +
    "<a href='/add/transaction/receivepayment/" +
    deal.id +
    "'>Recieve Payment</a></td></tr><tr class='text-dark-3'><th scope='row'>Date of Signing</th><td>" +
    deal.signing_date +
    "</td></tr><tr class='text-dark-3'><th scope='row'>Respective Plot</th><td>" +
    deal.plot_id +
    "</td></tr><tr class='text-dark-3'><th scope='row'>Respective Buyer</th><td>" +
    deal.buyer_id +
    "</td></tr><tr class='text-dark-3'><td><a href='/deal/" +
    deal.id +
    "'>Show Details</a></td></tr></tbody></table></div></div></div></section>";

  return str; 
}
function make_CA_card(CA) {
  let str =
    "<div class='accordion' id='accordionExample'><div class='card'><div class='card-header' id='headingOne'><h2 class='mb-0'><button class='btn btn-link btn-block text-left' type='button' data-toggle='collapse' data-target='#collapseBuyer" +
    CA.id +
    "' aria-expanded='true' aria-controls='collapseBuyer" +
    CA.id +
    "'>" +
    CA.name +
    "</button></h2></div><div id='collapseBuyer" +
    CA.id +
    "' class='collapse' aria-labelledby='headingOne' data-parent='#accordionExample'><div class='card-body'>" +
    "<section class='my-3'><div class='container'><div class='row'><div class='col-12'><table class='table mt-4'><tbody><tr class='text-dark-3'><th scope='row'>Id</th><td><a href='/agent/" +
    CA.id +
    "'>" +
    CA.id +
    "</a></td></tr><tr class='text-dark-3'><th scope='row'>Name</th><td>" +
    CA.name +
    "</td></tr><tr class='text-dark-3'><th scope='row'>CNIC</th><td>" +
    CA.cnic +
    '</td></tr></tbody></table></div></div></div></section>' +
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
    "<section class='my-3'><div class='container'><div class='row'><div class='col-12'><table class='table mt-4'><tbody><tr class='text-dark-3'><th scope='row'>Id</th><td><a href='" +
    ET.id +
    "'>" +
    ET.id +
    "</a></td></tr><tr class='text-dark-3'><th scope='row'>Type</th><td>" +
    ET.name +
    "</td></tr><tr class='text-dark-3'><th scope='row'>Add</th><td>" +
    "<a href='/add/transaction/expense/" +
    ET.id +
    "'>Add Expense of this type</a>" +
    '</td></tr></tbody></table></div></div></div></section>' +
    '</div></div></div></div>';

  return str;
}

function inject_div(name, list) {
  console.log(list);
  let str = '';
  let make_card = window['make_' + name + '_card'];
  for (let element of list) {
    str = make_card(element);
    $('#' + name + '-info').append(str);
  }
}

function getall(name) {
  clicked(name || 'buyer');
  $.post('/rest/' + name + '/all', function (data) {
    inject_div(name, data.json_list);
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
