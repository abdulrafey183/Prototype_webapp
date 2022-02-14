/*************** START UTILITIES ***************/

/*************** TABLE BODY ROW UTILITIES ***************/

function generate_plot_table_row_html(plot) {
  /**
   * Function that generates html of a row of table from a json object.
   * 
   * @params
   * deal: JSON object that represents a plot in database
   * 
   * @return
   * buyer_table_row_html: An html string 
   */


  //Checking if plot price is set 
  if (plot.price){
    plot_price = plot.price
  }
  else{
    plot_price = '<span style="color: red;">Not Set</span>'
  }

  //Checking if plot is in a deal
  if (plot.deal){
    plot_deal = '<a href="/deal/' + plot.deal.id + '">Deal# ' + plot.deal.id + '</a>'
  }
  else{
    plot_deal = 'None'
  }

  //Generating buyer table row html
  let plot_table_row_html;

  plot_table_row_html =  '<tr>' +
                            '<td>' + plot.address + '</td>' +
                            '<td>' + plot.type    + '</td>' +
                            '<td>' + plot.status  + '</td>' +
                            '<td>' + plot_price   + '</td>' +
                            '<td>' + plot.size    + '</td>' +
                            '<td>' + plot_deal    + '</td>' +
                            '<td>' +
                              '<a href="/plot/' + plot.id + '">Show Detials</a>' +
                            '</td>'                         +
                          '</tr>'
         
  return plot_table_row_html;

}

function generate_buyer_table_row_html(buyer) {
  /**
   * Function that generates html of a row of table from a json object.
   * 
   * @params
   * deal: JSON object that represents a buyer in database
   * 
   * @return
   * buyer_table_row_html: An html string 
   */

  //Getting the deals related to this buyer
  var buyer_deals = '';

  if (buyer.deals != null){
    for (var deal of buyer.deals) {
      buyer_deals +=
        ' <a href="/deal/' + deal.id + '">Deal#' + deal.id + '</a><br>';
    }
  }
  else {
    buyer_deals = 'None';
  }

  //Generating buyer table row html
  let buyer_table_row_html

  buyer_table_row_html =  '<tr>' +
                            '<td>' + buyer.person.name  + '</td>' +
                            '<td>' + buyer.person.cnic  + '</td>' +
                            '<td>' + buyer.person.phone + '</td>' +
                            '<td>' + buyer_deals        + '</td>' +
                            '<td>' +
                              '<a href="/buyer/' + buyer.id + '">Show Detials</a>' +
                            '</td>'                               +
                          '</tr>'
         
  return buyer_table_row_html;
}

function generate_deal_table_row_html(deal) {
  /**
   * Function that generates html of a row of table from a json object.
   * 
   * @params
   * deal: JSON object that represents a deal in database
   * 
   * @return
   * deal_table_row_html: An html string 
   */


  //Getting the buyer reated to this deal
  var deal_buyer;
  $.ajax({
    async: false,
    type: "POST",
    url: '/rest/' + 'Buyer' + '/' + deal.buyer_id,
    success: function (data) {
      deal_buyer = data.json_list[0]
    }
  });

  //Generating deal table row html
  let deal_table_row_html;

  deal_table_row_html = '<tr>'    +
                          '<td>'  +
                            '<a href="buyer/'+ deal.buyer_id + '">'      + deal_buyer.person.name +'</a>' +
                          '</td>' +
                          '<td>'  + 
                            '<a href="plot/'+ deal.plot_id   + '">Plot #'+ deal.plot_id           +'</a>' +
                          '</td>' +
                          '<td>'  + 
                            deal.signing_date                                                             +
                          '</td>' +
                          '<td>'  +
                            //IMPLEMENT: Only show link to receive payment is deal status is 'on going'
                            '<a href="/add/transaction/receivepayment/'+ deal.id + '">Recieve Payment</a><br>' + 
                            '<a href="/deal/'                          + deal.id + '">Show Detials</a>'        +
                          '</td>' +
                        '</tr>'

  return deal_table_row_html;
}

function generate_CA_table_row_html(CA) {
  /**
   * Function that generates html of a row of table from a json object.
   * 
   * @params
   * deal: JSON object that represents a Commission Agent in database
   * 
   * @return
   * CA_table_row_html: An html string 
   */
  

  //Getting the deals reated to this CA
  var CA_deals = '';
  if (CA.deals != null){
    for (var deal of CA.deals) {
      CA_deals += ' <a href="/deal/' + deal.id + '">Deal #' + deal.id + '</a><br>';
    }
  }
  else {
    CA_deals = 'None';
  } 

  //Generating CA table row html
  let CA_table_row_html

  CA_table_row_html =  '<tr>' +
                            '<td>' + CA.person.name  + '</td>' +
                            '<td>' + CA.person.cnic  + '</td>' +
                            '<td>' + CA.person.phone + '</td>' +
                            '<td>' + CA.person.email + '</td>' +
                            '<td>' + CA_deals        + '</td>' +
                            '<td>' +
                              '<a href="/agent/' + CA.person.id + '">Show Detials</a>' +
                            '</td>'                            +
                          '</tr>'
         
  return CA_table_row_html;
}

function generate_ET_table_row_html(ET) {
  /**
   * Function that generates html of a row of table from a json object.
   * 
   * @params
   * deal: JSON object that represents a Expenditure Type in database
   * 
   * @return
   * ET_table_row_html: An html string 
   */

  let ET_table_row_html

  ET_table_row_html = '<tr>' +
                        '<td>' + ET.name  + '</td>' +
                        '<td>' +
                          '<a href="/expenditure/'  + ET.id + '">Show Detials</a>' +
                        '</td>'                     +
                      '</tr>'
         
  return ET_table_row_html;
}

function generate_employee_table_row_html(employee) {
  /**
   * Function that generates html of a row of table from a json object.
   * 
   * @params
   * deal: JSON object that represents a Employee in database
   * 
   * @return
   * CA_table_row_html: An html string 
   */

  // let str =
  //   "<div class='accordion' id='accordionExample'><div class='card'><div class='card-header' id='headingOne'><h2 class='mb-0'><button class='btn btn-link btn-block text-left' type='button' data-toggle='collapse' data-target='#collapseBuyer" +
  //   employee.id +
  //   "' aria-expanded='true' aria-controls='collapseBuyer" +
  //   employee.id +
  //   "'>" +
  //   employee.person.name +
  //   "</button></h2></div><div id='collapseBuyer" +
  //   employee.id +
  //   "' class='collapse' aria-labelledby='headingOne' data-parent='#accordionExample'><div class='card-body'>" +
  //   "<section class='my-3'><div class='container'><div class='row'><div class='col-12'><table class='table mt-4'><tbody>" +
  //   "<tr class='text-dark-3'>" +
  //   "<th scope='row'>Name</th>" +
  //   "<td><a href='/employee/" +
  //   employee.id +
  //   "'>" +
  //   employee.person.name +
  //   '</a></td>' +
  //   '</tr>';

  // if (employee.rank == 1) {
  //   str +=
  //     "<tr class='text-dark-3'>" +
  //     "<th scope='row'>Type</th>" +
  //     '<td>User</td>' +
  //     '</tr>' +
  //     "<tr class='text-dark-3'>" +
  //     "<th scope='row'>Email ID</th>" +
  //     '<td>' +
  //     employee.person.email +
  //     '</td>' +
  //     '</tr>';
  // } else if (employee.rank == 2) {
  //   str +=
  //     "<tr class='text-dark-3'>" +
  //     "<th scope='row'>Type</th>" +
  //     '<td>Employee</td>' +
  //     '</tr>';
  // }

  // return (
  //   str + '</tbody></table></div></div></div></section></div></div></div></div>'
  // );

  if (employee.person.email){
    employee_email = employee.person.email
  }
  else{
    employee_email = 'None'
  }

  if (employee.rank == 1) {
    employee_type = 'User'
  }
  else if (employee.rank == 2){
    employee_type = 'Employee'
  }


  let employee_table_row_html

  employee_table_row_html = '<tr>' +
                              '<td>' + employee.person.name  + '</td>' +
                              '<td>' + employee_type         + '</td>' +
                              '<td>' + employee_email        + '</td>' +
                              '<td>' +
                                '<a href="/employee/'  + employee.id + '">Show Detials</a>' +
                              '</td>'                                  +
                            '</tr>'
         
  return employee_table_row_html;
  
}
/*************** END TABLE BODY ROW UTILITIES ***************/



/*************** INFO-DIV UTILITIES***************/

function get_div_start_html(){
  /**
   * Function that genrates HTML for the start of divs that contain Info Tables
   * 
   * @return
   * div_start_html: A string of HTML.
   */
 

  let div_start_html;

  div_start_html =  '<section class="my-5">'    +
                      '<div class="container">' +
                        '<div class="row">'     +
                          '<div class="col-12">'         

  return div_start_html
}

function get_div_end_html(){
  /**
   * Function that genrates HTML for the end of divs that contain Info Tables
   * 
   * @return
   * div_end_html: A string of HTML.
   */

  let div_end_html;

  div_end_html =          '</table>' +
                        '</div>'     + 
                      '</div>'       +
                    '</div>'         +
                  '</section>'      

  return div_end_html
}
/*************** END INFO-DIV UTILITIES***************/

/*************** TABLE HEAD UTILITIES ***************/

function generate_buyer_table_head_html(){

  let buyer_table_head_html;

  buyer_table_head_html = '<table class="table mt-4">' +
                            '<tr>'                     +
                              '<th>Name</th>'          +
                              '<th>CNIC</th>'          +
                              '<th>Phone</th>'         +
                              '<th>Deals</th>'         +
                              '<th>Details</th>'       +
                            '</tr>'

  return buyer_table_head_html
}

function generate_CA_table_head_html() {

  let CA_table_head_html;

  CA_table_head_html = '<table class="table mt-4">'  +
                          '<tr>'                     +
                            '<th>Name</th>'          +
                            '<th>CNIC</th>'          +
                            '<th>Phone</th>'         +
                            '<th>Email</th>'         +
                            '<th>Deals</th>'         +
                            '<th>Details</th>'       +
                          '</tr>'

  return CA_table_head_html
}

function generate_deal_table_head_html() {

  let deal_table_head_html;

  deal_table_head_html =  '<table class="table mt-4">' +
                            '<tr>'                     +
                              '<th>Buyer</th>'         +
                              '<th>Plot</th>'          +
                              '<th>Signing Date</th>'  +
                              '<th>Details</th>'       +
                            '</tr>'

  return deal_table_head_html
}

function generate_plot_table_head_html() {

  let plot_table_head_html;

  plot_table_head_html =  '<table class="table mt-4">' +
                            '<tr>'                     +
                              '<th>Address</th>'       +
                              '<th>Type</th>'          +
                              '<th>Status</th>'        +
                              '<th>Price</th>'         +
                              '<th>Size</th>'          +
                              '<th>Deal</th>'          +
                              '<th>Details</th>'       +
                            '</tr>'

  return plot_table_head_html
}

function generate_ET_table_head_html() {

  let ET_table_head_html;

  ET_table_head_html =  '<table class="table mt-4">' +
                          '<tr>'                     +
                            '<th>Name</th>'          +
                            '<th>Details</th>'       +
                          '</tr>'

  return ET_table_head_html
}

function generate_employee_table_head_html() {

  let employee_table_head_html;

  employee_table_head_html =  '<table class="table mt-4">' +
                                '<tr>'                     +
                                  '<th>Name</th>'          +
                                  '<th>Type</th>'          +
                                  '<th>Email</th>'         +
                                  '<th>Details</th>'       +
                                '</tr>'

  return employee_table_head_html
}
/*************** END TABLE HEAD UTILITIES ***************/


/*************** GENERATE TABLE UTILITY ***************/

function generate_table_html(name, data_list){
  /**
   * Function that generates HTML of Table, specified by 'name' argument, on display page in 4 parts;
   * First part is the begining of div (containing 'section' tag and bootstrap rows and columns). 
   * Second part is the head of the table.
   * Third part is the body of the table (generates body row by row).
   * Foruth part is ending of the div 
   *
   * @params
   * name: Name of the div, can be one of [buyer, CA, deal, plot, ET, employee]
   * data_list: A list of json objects, each object represents a row form database
   * 
   * @return
   * table_html: A String that represents the table HTML to be injected in display page  
   */

  console.log('inside genrate_table')
  //Defining variables
  let generatae_table_head_fn = window['generate_' + name + '_table_head_html']
  let generatae_table_row_fn  = window['generate_' + name + '_table_row_html' ]

  let div_start_html;
  let table_head_html;  
  let table_row_html;
  let div_end_html;
  let table_html;


  //Generating div start HTML
  div_start_html = get_div_start_html()
  console.log('div_start_html generated')

  //Generating Table Head HTML
  table_head_html = generatae_table_head_fn()
  console.log('table_head_html generated')

  //Generating table row for every elemet in the data_list               
  for (let element of data_list) {

    //Generating the Table Row HTML
    table_row_html += generatae_table_row_fn(element);
  }
  console.log('table_body_html generated')

  //Generating div end HTML
  div_end_html = get_div_end_html()
  console.log('div_end_html generated')

  //Concatenating html strings for start of div, table head, table body rows and end of div
  table_html = div_start_html + table_head_html + table_row_html + div_end_html

  return table_html
}
/*************** END GENERATE TABLE UTILITIES ***************/

/*************** END UTILITIES ***************/



/*************** START MAIN SECTION ***************/

let tabs = ['buyer', 'plot', 'CA', 'ET', 'deal', 'employee'];

function clicked(tab) {
  /**
   * Function that turns on visibility of the clicked div, specified by 'tab' argment
   * and turns off the vsibility of every other div
   * 
   * @param
   * tab: Name of the div, can be one of [buyer, CA, deal, plot, ET, employee]
   */


  //Defining Variables
  // let div = document.getElementById(tab + '-div')
  
  //Making the clicked div visible
  document.getElementById(tab + '-div').style.display = 'block';

  //Turning off the visibility of rest of the divs
  for (let current_tab of tabs) {
    if (current_tab != tab) {
      document.getElementById(current_tab + '-div').style.display = 'none';
      $('#' + current_tab + '-info').html('');
    }
  }
}

function inject_div(tab, data_list) {
  /**
   * Function that generates and injects HTML into div on the display page.

   * @params
   * tab: Name of the div, can be one of [buyer, CA, deal, plot, ET, employee]
   * data_list: A list of json objects, each object represents a row form database
   */

  console.log('inside inject_div')
  console.log(tab)
  //Defining variables
  let div = $('#' + tab + '-info')

  //Generating HTML for relevant div
  html = generate_table_html(tab, data_list)

  //Injecting HTML
  div.append(html)
}

function get_all(tab) {

  default_selection = 'buyer'

  clicked(tab || default_selection);
  $.post('/rest/' + tab + '/all', function (data) {
    inject_div(tab, data.json_list);
  });
}

// function getbuyer(id) {
//   $.post('/rest/' + 'Buyer' + '/' + id, function (data) {
//     deal_buyer = data
//     for (let element of data.json_list) {
//       $('.buyer-' + id).text(element.person.name);
//     }
//   });
// }

$(document).ready(function () {

  $('#filterPlot-btn').on('click', function () {
    $.post('/rest/filterplot/' + $('#status').val(), function (plots) {
      $('#plot-info').html('');
      inject_div('plot', plots.json_list);
    });
  });
});

/*************** END MAIN SECTION ***************/
