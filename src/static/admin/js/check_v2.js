function set_bad_1 (te_id) {
    let url = new URL(location.href);
    url.searchParams.set('set-bad-1', te_id);
    location.href = url;
}

function set_bad_2 (te_id) {
    let url = new URL(location.href);
    url.searchParams.set('set-bad-2', te_id);
    location.href = url;
}

function set_check (te_id) {
    let url = new URL(location.href);
    url.searchParams.set('set-check', te_id);
    location.href = url;
}

function set_bad_3 (te_id) {
    let url = new URL(location.href);
    url.searchParams.set('set-bad-3', te_id);
    location.href = url;
}

function set_bad_4 (te_id) {
    let url = new URL(location.href);
    url.searchParams.set('set-bad-4', te_id);
    location.href = url;
}

window.addEventListener("load", function(event) {
    console.log("All resources finished loading!");
    Fancybox.bind('[data-fancybox]', {
        Image: {
            zoom: false,
        },
    });
});


