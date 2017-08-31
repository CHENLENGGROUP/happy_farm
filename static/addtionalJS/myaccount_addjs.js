$(document).ready(function () {
     /* Basic Init*/
	$('.dropify').dropify({
        messages:{
          'default': '编辑头像',
          'replace': '',
          'remove':  '移除',
          'error':   '头像图片上传失败'
        },
        error:{
          'fileSize': '图片文件大于500KB，上传失败',
        },
        tpl: {
                wrap:            '<div class="dropify-wrapper"></div>',
                loader:          '<div class="dropify-loader"></div>',
                message:         '<div class="dropify-message"><p id = "edit-message" style="color: #eee; display:none;">{{ default }}</p></div>',
                preview:         '<div class="dropify-preview"><span class="dropify-render"></span><div class="dropify-infos"><div class="dropify-infos-inner"><p class="dropify-infos-message">{{ replace }}</p></div></div></div>',
                filename:        '',
                clearButton:     '<button type="button" class="dropify-clear">{{ remove }}</button>',
                errorLine:       '<p class="dropify-error">{{ error }}</p>',
                errorsContainer: '<div class="dropify-errors-container"><ul></ul></div>'
            }
      });
});