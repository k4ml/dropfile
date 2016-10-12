(function() {
var form = document.getElementById('file-form');
var fileSelect = document.getElementById('file-select');
var uploadButton = document.getElementById('upload-button');

form.onsubmit = function(event) {
    event.preventDefault();
    uploadButton.innerHTML = 'Uploading ...';

    var files = fileSelect.files;
    var formData = new FormData();

    formData.append('myfile', files[0], files[0].name);
    var xhr = new XMLHttpRequest();
    xhr.open('POST', 'api/upload', true);

    xhr.onload = function () {
      if (xhr.status === 200) {
        // File(s) uploaded.
        uploadButton.innerHTML = 'Upload';
        fileSelect.value = '';
      } else {
        alert('An error occurred!');
      }
    };
    xhr.send(formData);
}
})();
