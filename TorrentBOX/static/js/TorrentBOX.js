$(document).ready(function() {
    $('.ui.menu a.item').tab();
})

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function sendFile(file) {
    const uri = '/torrent/add/';
    const xhr = new XMLHttpRequest();
    const fd = new FormData();
    const csrftoken = getCookie('csrftoken');

    fd.append("csrfmiddlewaretoken", csrftoken)
    fd.append('torrent_file', file);
    xhr.open("POST", uri, true);

    // Initiate a multipart/form-data upload
    xhr.send(fd);
}

window.onload = function() {
    const dropzone = document.getElementById("dropzone");

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

	const filesArray = event.dataTransfer.files;
	for (var i=0; i<filesArray.length; i++) {
	    sendFile(filesArray[i]);
	}
    }

    dropbox.addEventListener("dragenter", dragenter, false);
    dropbox.addEventListener("dragover", dragover, false);
    dropbox.addEventListener("drop", drop, false);

    function handleFiles() {
        const fileList = this.files; /* now you can work with the file list */
        for (var i=0; i<fileList.length; i++) {
            sendFile(fileList[i]);
	}
	
        location.reload(true);
    }

    const inputElement = document.getElementById("torrent_file");
    inputElement.addEventListener("change", handleFiles, false);

    $(function() {
        $("#upload_link").on('click', function(e){
            e.preventDefault();
            $("#torrent_file").trigger('click');
        });
    });
}


function setTextContents($elem, text) {
    $elem.get(0).lastChild.nodeValue = text;
}

function updateStatus(id, data) {
    $(id).attr('data-percent', data.progress);
    $(id + '_progress').text(data.progress+'%');
    $(id + '_bar').innerWidth(data.progress+'%');

    const drateText = ' ' + data.download_rate + ' (peers: ' + data.peers + ')';
    const drateElem = $(id + '_drate');
    setTextContents(drateElem, drateText);

    const dsizeText = ' ' + data.downloaded_size + ' / ' + data.size;
    const dsizeElem = $(id + '_dsize');
    setTextContents(dsizeElem, dsizeText);

    const rtimeText = 'Remaining time: ' + data.rtime;
    const rtimeElem = $(id + '_rtime');
    setTextContents(rtimeElem, rtimeText);
}

setInterval(function(){
  $.ajax({
    url: '/torrent/status/',
    dataType: 'json',
    success:function(data){
      for(var i in data){
        const id = '#' + data[i].id;
        const downloadURL = '/torrent/download/';

        if (data[i].status === 'finished' && Number($(id).attr('data-percent')) < 100) {
            updateStatus(id, data[i]);
            const downloadButton = '<a href="' + downloadURL + data[i].id + '/' +
                                   '" class="ui tiny basic right floated button">' +
                                   '<i class="arrow down large black icon"></i>Download</a>';
            console.log(downloadButton);
            $(id).parent().append(downloadButton);
        }

        // lst = $("#torrent-segments").children(); // lst[0] is not target
        // lst[5].children[1].id
        // lst.length
        // if (lst.length > 1) { ... }

        if (data[i].status === 'downloading' | data[i].status === 'finished') {
            // FIXME: Not efficient. Add new entry to the list
            if (!$(id).hasClass('progress')) {
                location.reload(true);
            }
        }

        if (data[i].status === 'downloading') {
            updateStatus(id, data[i]);
        }
      }
    }
  })
},3000)
