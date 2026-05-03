// In your base.html or main JS file
if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register("{% static 'js/serviceworker.js' %}")
    .then(() => console.log("Service Worker Registered"));
}