function SortFuntion(){
  var data = JSON.stringify({
    display: $('#display').val(),
    sort: $('#sort').val(),
    st: $('#st').val(),
    type:sortData.type,
    uid:sortData.uid,
    page:sortData.page
  });
  $.ajax ({
    type : "POST",
    url : "/order",
    data:data,
    contentType: 'application/json;charset=UTF-8',
    success: function(result) {
      $('div.topiclist').html(result);
    }
  });
}
$(document).ready(function(){
  $('#display').change(function() {
    SortFuntion();
  });
  $('#sort').change(function() {
    SortFuntion();
  });
  $('#st').change(function() {
    SortFuntion();
  });
});
