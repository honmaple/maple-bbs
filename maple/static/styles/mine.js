function Follow(obj,data,url){
  if(obj.hasClass('active'))
  {$.ajax ({
    type : "DELETE",
    url : url,
    data:data,
    contentType: 'application/json;charset=UTF-8',
    success: function(result) {
      if (result.judge === true)
      {
        obj.text('关注').removeClass('active');
      } else
      {alert('fail');}}});
  }else
  {$.ajax ({
    type : "POST",
    url : url,
    data:data,
    contentType: 'application/json;charset=UTF-8',
    success: function(result) {
      if (result.judge === true)
      {
        obj.text('取消关注').addClass('active');
      } else
      {alert('fail');}
    }});
  }
}
$(document).ready(function(){
  $('button.tagfollow').click(function(){
    var _$this = $(this);
    var url = "/user/follow/tag";
    var data = JSON.stringify({
      id:_$this.attr("id"),
    });
    Follow(_$this,data,url);
  });
  $('button.topicfollow').click(function(){
    var _$this = $(this);
    var url = "/user/follow/topic";
    var data = JSON.stringify({
      id:_$this.attr("id"),
    });
    Follow(_$this,data,url);
  });
  $('button.collectfollow').click(function(){
    var _$this = $(this);
    var url = "/user/follow/collect";
    var data = JSON.stringify({
      id:_$this.attr("id"),
    });
    Follow(_$this,data,url);
  });
  $('button.userfollow').click(function(){
    var _$this = $(this);
    var url = "/user/follow/user";
    var data = JSON.stringify({
      id:_$this.attr("id"),
    });
    Follow(_$this,data,url);
  });
});
function DoCollect(collectData) {
  $(document).ready(function(){
    $('button#edit-collect-form').click(function() {
      var data = JSON.stringify({
        name:$('#name').val(),
        description:$('#description').val(),
        is_privacy:$("input[name='is_privacy']:checked").val()
      });
      $.ajax ({
        type : "PUT",
        url : collectData.collect_action_url,
        data:data,
        contentType: 'application/json;charset=UTF-8',
        success: function(result) {
          if (result.judge === true)
          {
            window.location =collectData.collect_action_url ;
          }
        }
      });
    });
    $('button#delete-collect-form').click(function() {
      $.ajax ({
        type : "DELETE",
        url : collectData.collect_action_url,
        data:JSON.stringify(),
        contentType: 'application/json;charset=UTF-8',
        success: function(result) {
          if (result.judge === true)
          {
            window.location = collectData.collect_url;
          }
        }
      });
    });
    $('#delete-from-collect').click(function() {
      var _$this = $(this);
      var topicId = _$this.attr('data-id');
      var data = JSON.stringify({
        topicId:topicId
      });
      $.ajax ({
        type : "DELETE",
        url : collectData.delete_detail_action_url,
        data:data,
        contentType: 'application/json;charset=UTF-8',
        success: function(result) {
          if (result.judge === true)
          {
            _$this.parent().remove();
          }
        }
      });
    });
  });
}
