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
    plot.id +
    "</button></h2></div><div id='collapseBuyer" +
    plot.id +
    "' class='collapse' aria-labelledby='headingOne' data-parent='#accordionExample'><div class='card-body'>" +
    'Plot ID: ' +
    plot.id +
    '</br>' +
    'Plot Type: ' +
    plot.type +
    '</br>' +
    'Plot Address: ' +
    plot.address +
    '</br>' +
    'Plot Status: ' +
    plot.status +
    '</br>';

  if (!plot.price)
    str += "Plot Price: <span style='color: red;'>Not Set</span></br>";
  else str += 'Plot Price: ' + plot.price + ' </br>';

  str +=
    'Plot Size: ' +
    plot.size +
    '</br>' +
    'Plot Comments: ' +
    plot.comments +
    '</br>';

  if (plot.deal) {
    str +=
      "Plot's Deal: " +
      "<a href='" +
      '/dealinfo/' +
      plot.deal.id +
      "''>" +
      plot.deal.id +
      '</a></br>';
  }

  return str + '</div></div></div></div>';
}

function make_buyer_card(buyer) {
  let str =
    "<div class='accordion' id='accordionExample'><div class='card'><div class='card-header' id='headingOne'><h2 class='mb-0'><button class='btn btn-link btn-block text-left' type='button' data-toggle='collapse' data-target='#collapseBuyer" +
    buyer.id +
    "' aria-expanded='true' aria-controls='collapseBuyer" +
    buyer.id +
    "'>" +
    buyer.id +
    "</button></h2></div><div id='collapseBuyer" +
    buyer.id +
    "' class='collapse' aria-labelledby='headingOne' data-parent='#accordionExample'><div class='card-body'>" +
    buyer.name +
    buyer.cnic +
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
    '<p>' +
    'Deal ID: ' +
    deal.id +
    "(<a href='/add/transaction/receivepayment/" +
    deal.id +
    "'>Recieve Payment</a>)</br>" +
    'Date of Signing: ' +
    deal.signing_date +
    '</br>' +
    'Respective Plot ID: ' +
    deal.plot_id +
    '</br>' +
    'Respective Buyer ID: ' +
    deal.plot_id +
    '</br>' +
    '</p></div></div></div></div>';

  return str;
}
function make_CA_card(CA) {
  let str =
    "<div class='accordion' id='accordionExample'><div class='card'><div class='card-header' id='headingOne'><h2 class='mb-0'><button class='btn btn-link btn-block text-left' type='button' data-toggle='collapse' data-target='#collapseBuyer" +
    CA.id +
    "' aria-expanded='true' aria-controls='collapseBuyer" +
    CA.id +
    "'>" +
    CA.id +
    "</button></h2></div><div id='collapseBuyer" +
    CA.id +
    "' class='collapse' aria-labelledby='headingOne' data-parent='#accordionExample'><div class='card-body'>" +
    '<p>' +
    "<a href='/agent/" +
    CA.id +
    "'>Commission Agent ID: " +
    CA.id +
    '</a></br>' +
    'Commission Agent Name: ' +
    CA.name +
    '</br>' +
    'Commission Agent CNIC: ' +
    CA.cnic +
    '</br>' +
    '</p></div></div></div></div>';

  return str;
}

function make_ET_card(ET) {
  let str =
    '<p>' +
    'Expenditure Type: ' +
    ET.name +
    "(<a href='/add/transaction/expense/" +
    ET.id +
    "'>Add Expense of this type</a>)</br>";

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
