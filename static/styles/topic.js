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
          } else
          {
            window.location.href = response.data.url;
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
    }});
  $('.reply-author').click(function() {
    var _$this = $(this);
    var author = _$this.attr('data-id');
    $('#content').focus();
    $('#content').val('@' + author + ' ');
  });
});
function DoVote(voteData) {
  $(document).ready(function(){
    $('#topic-up-vote').click(function() {
      var data = JSON.stringify({
      });
      $.ajax ({
        type : "POST",
        url : voteData.vote_url,
        data:data,
        contentType: 'application/json;charset=UTF-8',
        success: function(response) {
          if (response.status === '200')
          {
            $('.votes').html(result.html);
          } else
          {
            window.location.href = result.url;
          }
        }});
    });
    $('#topic-down-vote').click(function() {
      var data = JSON.stringify({
      });
      $.ajax ({
        type : "DELETE",
        url : voteData.vote_url,
        data:data,
        contentType: 'application/json;charset=UTF-8',
        success: function(response) {
          if (response.status === '200')
          {
            $('.votes').html(result.html);
          } else
          {
            window.location.href = result.url;
          }
        }});
    });
  });
}
$(document).ready(function(){
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
    var form_data = $("form#topic-put").serializeArray();
    var url = '/topic/' + _$this.attr("data-id");
    var data = {};
    $.each(form_data,function() {
      data[this.name] = this.value;
    });
    $.ajax ({
      type : "PUT",
      url : url,
      data:JSON.stringify(data),
      contentType: 'application/json;charset=UTF-8',
      success: function(response) {
        if (response.status === '200') {
          window.location.href= url;
        }
      }
    });
  });
});
