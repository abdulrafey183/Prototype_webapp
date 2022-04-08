var tabs              = ['buyer', 'plot', 'CA', 'ET', 'deal', 'employee'];
var default_selection = 'buyer'
var active_tab        = null

function clicked(tab) {
  /**
   * Function that turns on visibility of the clicked div, specified by 'tab' argment
   * and turns off the vsibility of every other div
   * 
   * @param
   * tab: Name of the div, can be one of [buyer, CA, deal, plot, ET, employee]
   */
  

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
   *
   * @params
   * tab: Name of the div, can be one of [buyer, CA, deal, plot, ET, employee]
   * data_list: A list of json objects, each object represents a row form database
   */


  //Defining variables
  let div = $('#' + tab + '-info')

  //Generating HTML for relevant div
  html = generate_table_html(tab, data_list)

  //Injecting HTML
  div.append(html)
}

function get_all(tab) {
  /**
   * Function that fetches all data from database about 'tab' enitity and injects 
   * it into the respective div
   * 
   * @param
   * tab: Name of the div, can be one of [buyer, CA, deal, plot, ET, employee]
   */
  

  //Checking is the clicked div is already active
  if (tab == active_tab) { return }
  else { active_tab = tab }

  //Configuring visibility of divs
  clicked(tab || default_selection);

  //Fetching data and injecting into respective div
  $.post('/rest/' + tab + '/all', function (data) {
    inject_div(tab, data.json_list);
  });
}

$(document).ready(function () {

  //Filter function for plot div
  $('#filterPlot-btn').on('click', function () {

    //Fetching filtered plot data 
    $.post('/rest/filterplot/' + $('#status').val(), function (plots) {

      //Emptying old html in div
      $('#plot-info').html('');

      //Injecting new html based on filtered data
      inject_div('plot', plots.json_list);
    });
  });


  //Filter function for deal div
  // YET TO IMPLEMENT

});