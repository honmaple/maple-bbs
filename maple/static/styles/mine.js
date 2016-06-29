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
  $('button.userfollow').click(function(){
    var _$this = $(this);
    var data = JSON.stringify({
      id:_$this.attr("id"),
      type:'user'
    });
    Follow(_$this,data);
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
        url : collectData.edit_url,
        data:data,
        contentType: 'application/json;charset=UTF-8',
        success: function(result) {
          if (result.judge == true)
          {
            window.location =collectData.edit_url ;
          }
        }
      });
    });
    $('button#delete-collect-form').click(function() {
      $.ajax ({
        type : "DELETE",
        url : collectData.delete_url,
        data:JSON.stringify(),
        contentType: 'application/json;charset=UTF-8',
        success: function(result) {
          if (result.judge == true)
          {
            window.location = collectData.url;
          }
        }
      });
    });
    $('#delete-from-collect').click(function() {
      var _$this = $(this);
      var topicId = _$this.attr('data-id');
      var collectId = collectData.collectId;
      var data = JSON.stringify({
        collectId:collectId,
        topicId:topicId
      });
      $.ajax ({
        type : "DELETE",
        url : collectData.delete,
        data:data,
        contentType: 'application/json;charset=UTF-8',
        success: function(result) {
          if (result.judge == true)
          {
            _$this.parent().remove();
          }
        }
      });
    });
  });
}
