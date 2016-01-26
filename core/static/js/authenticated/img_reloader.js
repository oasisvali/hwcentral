var IMG_RELOAD_RETRIES = 50;
function img_reload(image) {
    IMG_RELOAD_RETRIES -= 1;
    if (IMG_RELOAD_RETRIES > 0) {
        setTimeout(function () {
            console.log('reloading image');
            image.src = image.src;  // forces the browser to hit the src again
        }, 1000 + (Math.random() * 2000));
    }
}