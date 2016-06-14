function Follow(obj,data){
  if(obj.hasClass('active'))
  {$.ajax ({
    type : "DELETE",
    url : "/user/follow",
    data:data,
    contentType: 'application/json;charset=UTF-8',
    success: function(result) {
      if (result.judge === true)
      {
        obj.text('关注').removeClass('active');
      }
      else
      {alert('asd');}}});
  }else
  {$.ajax ({
    type : "POST",
    url : "/user/follow",
    data:data,
    contentType: 'application/json;charset=UTF-8',
    success: function(result) {
      if (result.judge === true)
      {
        obj.text('取消关注').addClass('active');
      } else
      {alert('asd');}
    }});
  }
}
$(document).ready(function(){
  $('button.tagfollow').click(function(){
    var _$this = $(this);
    var data = JSON.stringify({
      id:_$this.attr("id"),
      type:'tag'
    });
    Follow(_$this,data);
  });
  $('button.topicfollow').click(function(){
    var _$this = $(this);
    var data = JSON.stringify({
      id:_$this.attr("id"),
      type:'topic'
    });
    Follow(_$this,data);
  });
  $('button.collectfollow').click(function(){
    var _$this = $(this);
    var data = JSON.stringify({
      id:_$this.attr("id"),
      type:'collect'
    });
    Follow(_$this,data);
  });
});
