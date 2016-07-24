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
  $('span#email-confirm').click(function(){
    $.ajax ({
      type : "POST",
      url : "/confirm-email",
      data:JSON.stringify({
      }),
      contentType: 'application/json;charset=UTF-8',
      success: function(result) {
        if (result.judge === true)
        {
          alert(result.error);
        } else
        {
          alert(result.error);
        }}
    });
  });
});
function dispatch() {
  var q = document.getElementById("search");
  if (q.value !== "") {
    var url = 'https://www.google.com/search?q=site:forums.honmaple.org%20' + q.value;
    if (navigator.userAgent.indexOf('iPad') > -1 || navigator.userAgent.indexOf('iPod') > -1 || navigator.userAgent.indexOf('iPhone') > -1) {
      location.href = url;
    } else {
      window.open(url, "_blank");
    }
    return false;
  } else {
    return false;
  }
}
