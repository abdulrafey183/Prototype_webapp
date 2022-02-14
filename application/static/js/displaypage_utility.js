/*************** START UTILITIES ***************/

function inject_buyer_name(deal){

    //Fetching deal's byuer from database
    $.post('/rest/Buyer/' + deal.buyer_id, function(response){
        
        //Extracting buyer from response
        deal_buyer = response.json_list[0]
        
        //Injecting buyer into the deal's table row
        $('#buyer-name-of-deal' + deal.id).html(
            '<a href="buyer/'+ deal.buyer_id + '">' + deal_buyer.person.name +'</a>'
        )
    });
    
}

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
    // var deal_buyer;
    // $.ajax({
    //   async: false,
    //   type: "POST",
    //   url: '/rest/' + 'Buyer' + '/' + deal.buyer_id,
    //   success: function (data) {
    //     deal_buyer = data.json_list[0]
    //   }
    // });
  
    //Generating deal table row html
    let deal_table_row_html;
  
    deal_table_row_html = '<tr>'    +
                            '<td>'  +
                            //   '<a href="buyer/'+ deal.buyer_id + '">'      + 'Buyer' +'</a>' +
                                '<div id="buyer-name-of-deal' + deal.id + '"></div>' +
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
  
  
    // Getting information related to employee
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
  
  function generate_table_html(tab, data_list){
    /**
     * Function that generates HTML of Table, specified by 'tab' argument, on display page in 4 parts;
     * First part is the begining of div (containing 'section' tag and bootstrap rows and columns). 
     * Second part is the head of the table.
     * Third part is the body of the table (generates body row by row).
     * Foruth part is ending of the div 
     *
     * @params
     * tab: Name of the div, can be one of [buyer, CA, deal, plot, ET, employee]
     * data_list: A list of json objects, each object represents a row form database
     * 
     * @return
     * table_html: A String that represents the table HTML to be injected in display page  
     */
  
  
    //Defining variables
    let generatae_table_head_fn = window['generate_' + tab + '_table_head_html']
    let generatae_table_row_fn  = window['generate_' + tab + '_table_row_html' ]
  
    let div_start_html;
    let table_head_html;  
    let table_row_html;
    let div_end_html;
    let table_html;
  
  
    //Generating div start HTML
    div_start_html = get_div_start_html()
  
    //Generating Table Head HTML
    table_head_html = generatae_table_head_fn()
  
    //Generating table row for every elemet in the data_list               
    for (let element of data_list) {
  
      //Generating the Table Row HTML
      table_row_html += generatae_table_row_fn(element);
        
      //If the 'deal' tab is clicked then we need to inject the buyer of that deal in thata row
      if (tab == 'deal') { inject_buyer_name(element) }
    }
  
    //Generating div end HTML
    div_end_html = get_div_end_html()
  
    //Concatenating html strings for start of div, table head, table body rows and end of div
    table_html = div_start_html + table_head_html + table_row_html + div_end_html
  
    return table_html
  }
  /*************** END GENERATE TABLE UTILITIES ***************/
  
  /*************** END UTILITIES ***************/
  