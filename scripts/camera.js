const video = document.querySelector('video');
const img = document.getElementById('inp_img');
const canvas = document.querySelector('canvas');

function hasGetUserMedia() {
  return !!(navigator.mediaDevices &&
    navigator.mediaDevices.getUserMedia);
}

function captureImage() {
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    canvas.getContext('2d').drawImage(video, 0, 0);
    img.value = canvas.toDataURL('image/png');
    document.getElementById("imageForm").submit();
}

if (hasGetUserMedia())
{
    const constraints = {
      video: true
    };

    const video = document.querySelector('video');

    navigator.mediaDevices.getUserMedia(constraints).
      then((stream) => {video.srcObject = stream});
}

else
{
  alert('Your browser does not support cameras.');
}
