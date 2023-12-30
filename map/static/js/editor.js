var editor = ace.edit("json-editor");
editor.setTheme("ace/theme/monokai");
editor.session.setMode("ace/mode/json");

document.querySelector('.json-form').addEventListener('submit', function(e) {
    var json = editor.getValue();
    var input = document.createElement('input');
    input.type = 'hidden';
    input.name = 'json_data';
    input.value = json;
    this.appendChild(input);
});

document.getElementById('copyButton').addEventListener('click', function() {
    var code = document.querySelector('.json-sidebar code').innerText;
    var textarea = document.createElement('textarea');
    textarea.textContent = code;
    textarea.style.position = 'fixed';  
    document.body.appendChild(textarea);
    textarea.select();
    try {
        if (document.execCommand('copy')) {
            var copied = document.getElementById('copied');
            copied.style.visibility = 'visible';
            setTimeout(function() {
                copied.style.visibility = 'hidden';
            }, 3000);
        }
        return true;
    } catch (ex) {
        console.warn('Copy to clipboard failed.', ex);
        return false;
    } finally {
        document.body.removeChild(textarea);
    }
}, false);