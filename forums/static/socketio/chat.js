var socket;
var namespace;
$(document).ready(function(){
  namespace = '/chat';
  socket = io.connect('http://' + document.domain + ':' +  location.port + namespace);
  socket.on('connect', function() {
    socket.emit('joined', {room:'tags'});
  });
  socket.on('status', function(data) {
    var exdata = $('#chat').html();
    var addata = exdata + '<div class="text-center" style="margin-bottom:8px;"><span class="chatroom-msg">' +  data.msg + '</span></div>';
    $('#chat').html(addata);
    $('#chat').scrollTop($('#chat')[0].scrollHeight);
  });
  socket.on('message', function(data) {
    var exdata = $('#chat').html();
    var addata = exdata + data.html;
    $('#chat').html(addata);
    $('#chat').scrollTop($('#chat')[0].scrollHeight);
  });
  $('#text').keypress(function(e) {
    if (e.ctrlKey && e.which == 13 || e.which == 10) {
      text = $('#text').val();
      if (text === ''){
        alert('输入不能为空!');
        return false;
      }else{
        $('#text').val('');
        socket.emit('text', {msg: text});
      }
    }
  });
  $('.send-msg').click(function() {
    text = $('#text').val();
    if (text === ''){
      alert('输入不能为空!');
      return false;
    }else{
      $('#text').val('');
      socket.emit('text', {msg: text});
    }
  });
});
