function loadFile(event) {
  var _file=document.getElementById("avatar");
  var i=_file.value.lastIndexOf('.');
  var len=_file.value.length;
  var extEndName=_file.value.substring(i+1,len);
  var extName="JPG,PNG";
  if(extName.indexOf(extEndName.toUpperCase())==-1){
    alert("您只能上传"+extName+"格式的文件");
    $('#avatar').val('');
  }else{
    var reader = new FileReader();
    reader.onload = function(){
      var icon = '<i class="icon-exchange"></i>' + '\n';
      var img = '<img src="' + reader.result + '" title="avatar" class="avatar img-circle">';
      $("#show-avatar").html(icon + img);
    };
    reader.readAsDataURL(event.target.files[0]);
  }
}
