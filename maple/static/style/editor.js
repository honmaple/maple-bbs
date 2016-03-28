var imgNum=0;
function loadFile(event) {
    var _file=document.getElementById("photo");
    var i=_file.value.lastIndexOf('.');
    var len=_file.value.length;
    var extEndName=_file.value.substring(i+1,len);
    var extName="JPG,PNG";
    if (imgNum > 5){ alert('仅允许上传小于6张图片'); }
    else {
        if(extName.indexOf(extEndName.toUpperCase())==-1){
            alert("您只能上传"+extName+"格式的文件");
        }else{
            var reader = new FileReader();
            reader.onload = function(){
                var img = '<img src="' + reader.result + '" title="">'
                $("#content").after(img);
                imgNum += 1;
            };
            reader.readAsDataURL(event.target.files[0]);
        };
    }
};
$(document).ready(function() {
    var cursorPosition = {
        get: function (textarea) {
            var rangeData = {text: "", start: 0, end: 0 };
            if (textarea.setSelectionRange) { // W3C
                textarea.focus();
                rangeData.start= textarea.selectionStart;
                rangeData.end = textarea.selectionEnd;
                rangeData.text = (rangeData.start != rangeData.end) ? textarea.value.substring(rangeData.start, rangeData.end): "";
            } else if (document.selection) { // IE
                textarea.focus();
                var i,
                oS = document.selection.createRange(),
                    oR = document.body.createTextRange();
                    oR.moveToElementText(textarea);
                    rangeData.text = oS.text;
                    rangeData.bookmark = oS.getBookmark();
                    for (i = 0; oR.compareEndPoints('StartToStart', oS) < 0 && oS.moveStart("character", -1) !== 0; i ++) {

                        if (textarea.value.charAt(i) == '\r' ) {
                            i ++;
                        }
                    }
                    rangeData.start = i;
                    rangeData.end = rangeData.text.length + rangeData.start;
            }
            return rangeData;
        }
    };
    $('a#editor-a').click(function() {
        var tx = $("#content")[0];
        var result;
        var text;
        var oValue,nValue;
        var choice=$('#choice').val();
        result = cursorPosition.get(tx);
        if (result.text == '') {text = '链接';}
        else {text = result.text;}
        if (choice == 'Default') { text = '<a href="' + text +'" target="_blank"></a>';}
        else {text = '[](' + text + ')';}
        oValue = $("#content").val();
        nValue = oValue.substring(0, result.start) + text + oValue.substring(result.end);
        $("#content").val(nValue);
        if (result.text == '') {
            if (choice == "Default"){start=9;end=11}
            else {start=3;end=5};
            if(tx.createTextRange){
                var range = tx.createTextRange();
                range.moveStart("character", result.start+start);
                range.moveEnd("character",result.start+end);
                range.select();
            }else{
                tx.setSelectionRange(result.start+start,result.start+end);
                tx.focus();
            }};
    });
    $('a#editor-b').click(function() {
        var tx = $("#content")[0];
        var result;
        var text;
        var oValue,nValue;
        var choice=$('#choice').val();
        result = cursorPosition.get(tx);
        if (result.text == '') {text = '文本';}
        else {text = result.text;}
        if (choice == 'Default') { text = '<b>' + text + '</b>';}
        else {text = '**' + text + '**';}
        oValue = $("#content").val();
        nValue = oValue.substring(0, result.start) + text + oValue.substring(result.end);
        $("#content").val(nValue);
        if (result.text == '') {
            if (choice == "Default"){start=3;end=5}
            else {start=2;end=4};
            if(tx.createTextRange){
                var range = tx.createTextRange();
                range.moveStart("character", result.start+start);
                range.moveEnd("character",result.start+end);
                range.select();
            }else{
                tx.setSelectionRange(result.start+start,result.start+end);
                tx.focus();
            }};
    });
    $('a#editor-i').click(function() {
        var tx = $("#content")[0];
        var result;
        var text = "文本";
        var oValue,nValue;
        var choice=$('#choice').val();
        result = cursorPosition.get(tx);
        if (result.text == '') {text = '文本';}
        else {text = result.text;}
        if (choice == 'Default')
            { text = '<i>' + text + '</i>';}
        else {text = '*' + text + '*';}
        oValue = $("#content").val();
        nValue = oValue.substring(0, result.start) + text + oValue.substring(result.end);
        $("#content").val(nValue);
        if (result.text == '') {
            if (choice == "Default"){start=3;end=5}
            else {start=1;end=3};
            if(tx.createTextRange){
                var range = tx.createTextRange();
                range.moveStart("character", result.start+start);
                range.moveEnd("character",result.start+end);
                range.select();
            }else{
                tx.setSelectionRange(result.start+start,result.start+end);
                tx.focus();
            }};
    });
    $('a#editor-bq').click(function() {
        var tx = $("#content")[0];
        var result;
        var text;
        var oValue,nValue;
        var choice=$('#choice').val();
        result = cursorPosition.get(tx);
        if (result.text == '') {text = '引用';}
        else {text = result.text;}
        if (choice == 'Default')
            { text = '<blockquote>' + text + '</blockquote>';}
        else {text = '\r\n> ' + text;}
        oValue = $("#content").val();
        nValue = oValue.substring(0, result.start) + text + oValue.substring(result.end);
        $("#content").val(nValue);
        if (result.text == '') {
            if (choice == "Default"){start=12;end=14}
            else {start=3;end=5};
            if(tx.createTextRange){
                var range = tx.createTextRange();
                range.moveStart("character", result.start+start);
                range.moveEnd("character",result.start+end);
                range.select();
            }else{
                tx.setSelectionRange(result.start+start,result.start+end);
                tx.focus();
            }};
    });
    $('a#editor-c').click(function() {
        var tx = $("#content")[0];
        var result;
        var text ;
        var oValue,nValue;
        var choice=$('#choice').val();
        result = cursorPosition.get(tx);
        if (result.text == '') {text = '代码';}
        else {text = result.text;}
        if (choice == 'Default')
            { text = '\r\n<pre>' + text + '</pre>';}
        else {text = "\r\n'''\r\n" + text + "\r\n'''";}
        oValue = $("#content").val();
        nValue = oValue.substring(0, result.start) + text + oValue.substring(result.end);
        $("#content").val(nValue);
        if (result.text == '') {
            if (choice == "Default"){start=6;end=8}
            else {start=5;end=7};
            if(tx.createTextRange){
                var range = tx.createTextRange();
                range.moveStart("character", result.start+start);
                range.moveEnd("character",result.start+end);
                range.select();
            }else{
                tx.setSelectionRange(result.start+start,result.start+end);
                tx.focus();
            }};
    });
    $('a#editor-h').click(function() {
        var tx = $("#content")[0];
        var result;
        var text;
        var oValue,nValue;
        var choice=$('#choice').val();
        result = cursorPosition.get(tx);
        if (result.text == '') {text = '标题';}
        else {text = result.text;}
        if (choice == 'Default')
            { text = '<h3>' + text + '</h3>';}
        else {text = "\r\n### " + text + "\r\n";}
        oValue = $("#content").val();
        nValue = oValue.substring(0, result.start) + text + oValue.substring(result.end);
        $("#content").val(nValue);
        if (result.text == '') {
            if (choice == "Default"){start=4;end=6}
            else {start=5;end=7};
            if(tx.createTextRange){
                var range = tx.createTextRange();
                range.moveStart("character", result.start+start);
                range.moveEnd("character",result.start+end);
                range.select();
            }else{
                tx.setSelectionRange(result.start+start,result.start+end);
                tx.focus();
            }};
    });
    $('a#editor-hr').click(function() {
        var tx = $("#content")[0];
        var result;
        var text;
        var oValue,nValue;
        var choice=$('#choice').val();
        result = cursorPosition.get(tx);
        if (choice == 'Default')
            { text = '\r\n<hr>\r\n'; }
        else {text = '\r\n------\r\n';}
        oValue = $("#content").val();
        nValue = oValue.substring(0, result.start) + text + oValue.substring(result.end);
        $("#content").val(nValue);
    });
    $('button#uploadFile').click(function() {
        var formData = new FormData($('#uploadForm')[0]);
        var content=$("#content").val();
        var choice=$("#choice").val();
        var img_url;
        $.ajax({
            type: 'POST',
            url: '/question/uploads',
            data: formData,
            contentType: false,
            processData: false,
            dataType: 'json',
            error: function(XMLHttpRequest) {
                if (XMLHttpRequest.status == 413) {
                    alert('文件太大');
                }
            },
            success: function(result) {
                if (choice == 'Default'){
                    img_url = '\r\n<img src="' +'/uploads/' + result.error + '" alt="photo">\r\n';
                }
                else {
                    img_url = '\r\n![photo](/uploads/' + result.error +')  \r\n';
                }
                if (result.judge == true) {
                    $("#content").val(content+img_url);
                    $("#content").focus();
                }
                else {
                    alert(result.error);
                }
            },
        });
    });
})
