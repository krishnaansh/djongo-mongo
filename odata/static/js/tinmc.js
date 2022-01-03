var jQueryScript = document.createElement('script');
jQueryScript.setAttribute('src','https://cdn.tiny.cloud/1/no-api-key/tinymce/5/tinymce.min.js');
document.head.appendChild(jQueryScript);
setTimeout(function(){
    tinymce.init({
        selector: 'textarea',
        height: 500,
    });
}, 1000);

setTimeout(function(){
    django.jQuery(".tox-notifications-container").hide()
},1500);
