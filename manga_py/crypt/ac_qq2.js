_keyStr="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=";
function decode(c){
    var a="",b,d,h,f,g,e=0;
    c=c.replace(/[^A-Za-z0-9\\+\/=]/g,"");
    for(c;e<c.length;) {
        b = _keyStr.indexOf(c.charAt(e++));
        d = _keyStr.indexOf(c.charAt(e++));
        f = _keyStr.indexOf(c.charAt(e++));
        g = _keyStr.indexOf(c.charAt(e++));

        b = b << 2 | d >> 4;
        d = (d & 15) << 4 | f >> 2;
        h = (f & 3) << 6 | g;
        a += String.fromCharCode(b);

        if (64 !== f) {
            a += String.fromCharCode(d);
        }
        if (64 !== g) {
            a += String.fromCharCode(h);
        }
    }

    return a
}