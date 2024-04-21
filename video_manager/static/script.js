function changeIndex(delta) {
    // Update current index based on delta
    current_index += delta;

    // Ensure current index stays within bounds
    if (current_index < 0) {
        current_index = 0;
    } else if (current_index >= max_index) {
        current_index = max_index - 1;
    }

    // Update video source URL dynamically
    var videoPlayer = document.getElementById('videoPlayer');
    videoPlayer.src = videoServeURL + videos_metadata[current_index]['fid']; // Assuming '_id' is the video ID field
    videoPlayer.load();

    // Update other UI elements
    var videoTitle = document.getElementById('videoTitle');
    videoTitle.textContent = videos_metadata[current_index]['title'];

    var modifiedData = document.getElementById('modifiedData');
    var metadata = videos_metadata[current_index];
    modifiedData.value = JSON.stringify(metadata, null, 2);

    var videoIndexText = document.getElementById('videoIndexText');
    videoIndexText.textContent = (current_index + 1) + " / " + max_index;
}





function updateData(videoId) {
    var modifiedData = document.getElementById('modifiedData').value;
    try {
        var parsedData = JSON.parse(modifiedData);
        sendRequest('/update_video', 'PUT', { videoId: videoId, data: parsedData }, 'Video data updated successfully', 'Failed to update video data');
    } catch (error) {
        console.error('Error parsing JSON:', error);
    }
}

function deleteVideo() {
    sendRequest('/delete_video', 'DELETE', null, 'Video deleted successfully', 'Failed to delete video');
}

function forwardVideo() {
    sendRequest('/forward_video', 'POST', null, 'Video forwarded successfully', 'Failed to forward video');
}

function sendRequest(url, method, data, successMessage, errorMessage) {
    var xhr = new XMLHttpRequest();
    xhr.open(method, url, true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send(JSON.stringify(data));
    xhr.onload = function() {
        if (xhr.status === 200) {
            console.log(successMessage);
            // Optionally, update the UI or perform other actions
        } else {
            console.error(errorMessage);
        }
    };
}

