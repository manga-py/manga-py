function ytc(y) {
    var x = "", y = y.split(" ");
    for (var i = 0, n = y.length; i < n; i++) x += String.fromCharCode(y[i]);
    return x;
}

function kxatz() {
    for (i = ytaw.length - 1; i >= 0; i--) {
        ytaw[i] = ytc(ytaw[i]);
        var obj = $('#imgs .wrap_img:eq(' + i + ') img'), alt = $('#imgs').attr('data-alt');
        obj.attr('alt', alt + ' - ' + obj.attr('alt'));
        obj.attr('data-src', ytaw[i]);
    }
}