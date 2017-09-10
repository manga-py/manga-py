; // https://bl.ocks.org/marcoslin/8026990
var boxzq = 'a5e8e2e9c2721be0a84ad660c472c1f3';
var chko = 'mshsdf832nsdbash20asdm';
var iv, key;
iv = CryptoJS['enc']['Hex']['parse'](boxzq);
key = CryptoJS.SHA256(chko);

function wrapKA(Mathb) {
    var Mathc = null;
    try {
        var Mathd = CryptoJS['lib']['CipherParams']['create']({
            ciphertext: CryptoJS['enc']['Base64']['parse'](Mathb)
        });
        var Mathe = CryptoJS['AES']['decrypt'](Mathd, key, {
            mode: CryptoJS['mode']['CBC'],
            iv: iv,
            padding: CryptoJS['pad']['Pkcs7']
        });
        Mathc = Mathe.toString(CryptoJS['enc'].Utf8);
        return Mathc
    } catch (err) {
        alert(err)
    }
}
