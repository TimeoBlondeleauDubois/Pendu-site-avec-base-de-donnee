window.onload = function () {
    if (window.history && window.history.pushState) {
        window.history.pushState('forward', null, './#no-back-button');
        window.onpopstate = function () {
            window.history.pushState('forward', null, './#no-back-button');
        };
    }
}