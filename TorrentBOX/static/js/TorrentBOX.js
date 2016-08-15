function getCookie(name) {
	var cookieValue = null;
	if (document.cookie && document.cookie != '') {
		var cookies = document.cookie.split(';');
		for (var i = 0; i < cookies.length; i++) {
			var cookie = jQuery.trim(cookies[i]);
			if (cookie.substring(0, name.length + 1) == (name + '=')) {
				cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
				break;
			}
		}
	}
	return cookieValue;
}

function sendFile(file) {
	var uri = '/torrent/add/';
	var xhr = new XMLHttpRequest();
	var fd = new FormData();
	var csrftoken = getCookie('csrftoken');
	fd.append("csrfmiddlewaretoken", csrftoken)
		fd.append('torrent_file', file);
	xhr.open("POST", uri, true);
	// Initiate a multipart/form-data upload
	xhr.send(fd);
}

window.onload = function() {
	var dropzone = document.getElementById("dropzone");

	dragover = function(event) {
		event.stopPropagation();
		event.preventDefault();
	}
	dragenter = function(event) {
		event.stopPropagation();
		event.preventDefault();
	}

	drop = function(event) {
		event.stopPropagation();
		event.preventDefault();

		var filesArray = event.dataTransfer.files;
		for (var i=0; i<filesArray.length; i++) {
			sendFile(filesArray[i]);
		}
	}
	dropbox.addEventListener("dragenter", dragenter, false);
	dropbox.addEventListener("dragover", dragover, false);
	dropbox.addEventListener("drop", drop, false);

	function handleFiles() {
		var fileList = this.files; /* now you can work with the file list */
		for (var i=0; i<fileList.length; i++) {
			sendFile(fileList[i]);
		}
		location.reload(true);
	}
	var inputElement = document.getElementById("torrent_file");
	inputElement.addEventListener("change", handleFiles, false);
	$(function(){
			$("#upload_link").on('click', function(e){
				e.preventDefault();
				$("#torrent_file").trigger('click');
				});
			});
}
  $(document)
    .ready(function() {
      $('.ui.menu a.item')
                .tab()
      ;
    })
  ;
