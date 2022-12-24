django.jQuery(function($) { 
  $(".field-view_request").css({"width":"150px"});
  $(".field-view_request a").css({"color":"#2E5DC5","font-weight":"bold","font-size":"13px"});
  $("#result_list tbody tr").each(function() {
      var statusfield = $(this).find('td.field-log_type').text();
      if(statusfield == "Withdrawal")
      {
        $(this).find('td.field-log_type').css('color', 'red');
      }
      else if (statusfield == "Support") {
        $(this).find('td.field-log_type').css('color', 'green');
      }
      else {
        $(this).find('td.field-log_type').css('color', '#2E5DC5');
    }
});

})