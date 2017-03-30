$(document).ready(function(){
  $('.like-reply').click(function() {
    var _$this = $(this);
    var replyId = _$this.attr('data-id');
    var like_url = "/replies/" + replyId + '/like';
    var data = JSON.stringify({
    });
    if(_$this.hasClass('like-active')){
      $.ajax ({
        type : "DELETE",
        url : like_url,
        data:data,
        contentType: 'application/json;charset=UTF-8',
        success: function(response) {
          if (response.status === '200')
          {
            _$this.attr("title","赞");
            _$this.removeClass("like-active");
            _$this.addClass("like-no-active");
          } else {
            window.location.href = response.url;
          }
        }});
    }else {
      $.ajax ({
        type : "POST",
        url : like_url,
        data:data,
        contentType: 'application/json;charset=UTF-8',
        success: function(response) {
          if (response.status === '200')
          {
            _$this.attr("title","取消赞");
            _$this.removeClass("like-no-active");
            _$this.addClass("like-active");
          } else
          {
            window.location.href = response.url;
          }
        }});
    }
  });
  $('.reply-author').click(function() {
    var _$this = $(this);
    var author = _$this.attr('data-id');
    $('#content').focus();
    $('#content').val('@' + author + ' ');
  });
  $('#topic-preview').click(function() {
    var content = $('#content').val();
    $.post('/topic/preview', {
      content: $("#content").val(),
      content_type: $("#content_type").val()
    }, function(data) {
      $("#show-preview").html(data);
    });
  });
  $('#tokenfield').tokenfield({
    limit:4
  });
  $('#topic-put-btn').click(function() {
    var _$this = $(this);
    var url = '/topic/' + _$this.attr("data-id");
    var data = {
      csrf_token:$('input[name="csrf_token"]').val(),
      title:$('input[name="title"]').val(),
      tags:$('input[name="tags"]').val(),
      category:$('select[name="category"]').val(),
      content:$('textarea[name="content"]').val(),
      content_type:$('select[name="content_type"]').val()
    };
    $.ajax ({
      type : "PUT",
      url : url,
      data:JSON.stringify(data),
      contentType: 'application/json;charset=UTF-8',
      success: function(response) {
        if (response.status === '200') {
          window.location.href= url;
        }else {
          if (response.description !==""){
            alert(response.description);
          }else {
            alert(response.message);
          }
        }
      }
    });
  });
});
