$(function() {
  $('div.month').click(function(){
    $('#year').val($('div.year-active').attr('data-value'));
    $('#month').val($(this).attr('data-value'));
    $('#date_form').submit();
  });
  $('div.year').click(function(){
    $('#year').val($(this).attr('data-value'));
    $('#month').val($('div.month-active').attr('data-value'));
    $('#date_form').submit();
  });
  if (update_month == 1)
    if (actual_month == 1 && actual_year == 1 )
      setInterval("update_vcpu_hours()", 120000);;
});
function update_vcpu_hours() {
  $.ajax({
    url: './get_vcpu_hours',
    type: 'post',
    dataType: 'json',
    success: function(data) {
      $('table#tenant_overview tr td:nth-child(3)').html(data.vcpu_hours);
    }
  });
}
