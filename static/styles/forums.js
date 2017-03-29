function getQueryParams(k){
  var p={};
  location.search.replace(/[?&]+([^=&]+)=([^&]*)/gi,function(s,k,v){p[k]=v;});
  return k?p[k]:p;
}
function SortFuntion(){
  var within = $('select#within').val();
  var orderby =  $('select#orderby').val();
  var desc =  $('select#desc').val();
  var params = getQueryParams();
  params.within = within;
  params.orderby = orderby;
  params.desc = desc;
  window.location.href = window.location.pathname + '?' + $.param(params);
}
$(document).ready(function(){
  $('select#within').change(function() {
    SortFuntion();
  });
  $('select#orderby').change(function() {
    SortFuntion();
  });
  $('select#desc').change(function() {
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
