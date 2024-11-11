

function changeIndex(delta) {
    // Update current index based on delta
    current_index += delta;

    // Ensure current index stays within bounds
    if (current_index < 0) {
        current_index = 0;
    } else if (current_index >= videos_metadata.length) {
        current_index = videos_metadata.length - 1;
    }

    _updateUi();
}

function _updateUi() {
    // Update video source URL dynamically
    var videoPlayer = document.getElementById('videoPlayer');
    if (videos_metadata.length > 0 && current_index >= 0 && current_index < videos_metadata.length) {
        videoPlayer.src = videoServeURL + videos_metadata[current_index].fid; // Assuming 'fid' is the video ID field
        videoPlayer.load();
    } else {
        videoPlayer.src = ''; // Clear the video source
    }

    var modifiedData = document.getElementById('modifiedData');
    if (videos_metadata.length > 0 && current_index >= 0 && current_index < videos_metadata.length) {
        modifiedData.value = JSON.stringify(videos_metadata[current_index], null, 2);
    } else {
        modifiedData.value = ''; // Clear the modified data
    }

    var videoIndexText = document.getElementById('videoIndexText');
    if (videos_metadata.length > 0 && current_index >= 0 && current_index < videos_metadata.length) {
        videoIndexText.textContent = (current_index + 1) + " / " + videos_metadata.length;
    } else {
        videoIndexText.textContent = "No videos found";
    }
}


function _remove_metadata(){
    videos_metadata.splice(current_index, 1)
    if (current_index >= videos_metadata.length) {
        current_index = videos_metadata.length - 1;
    }
}

function updateData() {
    var url = '/videos/' + videos_metadata[current_index].fid;
    var modifiedData = document.getElementById('modifiedData').value;
    try {
        var parsedData = JSON.parse(modifiedData);
        sendRequest(url, 'PUT', { data: parsedData }, 'Video data updated successfully', 'Failed to update video data', _updateUi, _remove_metadata);
    } catch (error) {
        console.error('Error parsing JSON:', error);
    }
}

function deleteVideo(video_id=null) {
    if (!video_id){
        video_id = videos_metadata[current_index].fid
    }
    var url = '/videos/' + video_id;
    console.log('deleting' + url)

    sendRequest(url, 'DELETE', null, 'Video deleted successfully', 'Failed to delete video', _updateUi, _remove_metadata);
}

function forwardVideo() {
    window.location.href = '/upload/' + videos_metadata[current_index].fid;
}

function sendRequest(url, method, data, successMessage, errorMessage, callback, removefunction=null, callbackArgs=null) {
    var xhr = new XMLHttpRequest();
    xhr.open(method, url, true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send(JSON.stringify(data));
    xhr.onload = function() {
        if (xhr.status === 200) {
            console.log(successMessage);
            if (removefunction) {
                removefunction();
            }
            if (callback) {
                if (callbackArgs !== null) {
                    callback(...callbackArgs)
                }else{
                    callback();
                }
            }
        } else {
            console.error(errorMessage);
        }
    };
}


// UPLOAD

function goBack(){
    window.history.back()
}

function _delete(video_id){
    window.location.href = '/'
    console.log('_delete video id: ' + video_id)
    deleteVideo(video_id)

}

function uploadToSocial(video_id){
    url = '/upload/' + video_id;
    console.log('uploading to Social')
    sendRequest(url, 'POST', null, 'Video sent to upload successfully', 'Failed to upload video', _delete, null, [video_id]);

}
