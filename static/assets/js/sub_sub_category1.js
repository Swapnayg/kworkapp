var response_cache = {};

function fill_subcategories(category_id) {
  if (response_cache[category_id]) {
    $("#id_sub_category").html(response_cache[category_id]);
  } else {
    $.getJSON("/subcategories_for_category/", {category_id: category_id},
      function(ret, textStatus) {
        var options = '<option value="" selected="selected">---------</option>';
        for (var i in ret) {
          options += '<option value="' + ret[i].pk + '">'
            + ret[i].fields["sub_category_Name"] + '</option>';
        }
        response_cache[category_id] = options;
        $("#id_sub_category").html(options);
      });
  }
}

$(document).ready(function() {
    $("#id_main_category").change(function() { fill_subcategories($(this).val()); });
});