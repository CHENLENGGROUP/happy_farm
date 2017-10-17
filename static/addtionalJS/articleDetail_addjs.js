$(document).ready(function () {
    $('#content').attr('disabled',true);
    var content = "{{article_list[0]['content']}}";
    content = content.replace(/&lt;/g, "<");
    content = content.replace(/&gt;/g, ">");
    <!--var html = "<textarea>"+content+"</textarea>"-->
	<!--$('#articleDetail').append(html);-->

	$('#article_edit').click(function(){
	    if($('.btn-text').html() == "编辑"){
            $('.textarea_editor').wysihtml5({
                toolbar: {
                  fa: true,
                  "link": true,
                }
            });
            $('input').removeAttr('disabled')
            $('.btn-text').html('保存');
        }else{
           $('.wysihtml5-toolbar').css('display','none');
           $('.btn-text').html('编辑');
           $('input').attr('disabled',true);
            alert(123);
        }
	});


})
$(document).ready(function () {
	$('.dropify').dropify(
	    {
        messages:{
          'default': '点击上传图片',
          'replace': '',
          'remove':  '移除',
          'error':   '文章图片上传失败'
        },
        error:{
          'fileSize': '图片文件大于500KB，上传失败',
        },
        tpl: {
                wrap:            '<div class="dropify-wrapper"></div>',
                loader:          '<div class="dropify-loader"></div>',
                message:         '<div class="dropify-message"><p id = "edit-message" style="color: #eee; display:none;">{{ default }}</p></div>',
                preview:         '<div class="dropify-preview"><span class="dropify-render"></span><div class="dropify-infos"><div class="dropify-infos-inner"><p class="dropify-infos-message">{{ replace }}</p></div></div></div>',
                filename:        '<p class="dropify-filename"><span class="file-icon"></span> <span class="dropify-filename-inner"></span></p>',
                clearButton:     '<button type="button" class="dropify-clear">{{ remove }}</button>',
                errorLine:       '<p class="dropify-error">{{ error }}</p>',
                errorsContainer: '<div class="dropify-errors-container"><ul></ul></div>'
            }
      }
      );
});