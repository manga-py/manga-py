// https://static.animemark.com/ss/batoto.js?v11
const _jss = {
  confs: {
    domain: {"main":"animemark.com","static":"static.animemark.com","account":"id.animemark.com","account_prefix":"id","id":"id","linkto":"aclink.to","linkto_rank":"aclink.to/rank/","linkto_file":"aclink.to/file/","atoto":"ato.to","amark":"animemark.com","editor":"aniedit.org","file_preview_comic_release":"zz-cr-o.aniedit.org","file_avatars":"file-avatars.animemark.com","file_avatars_old":"file-avatar.anyacg.com","file_archive":"file-archive.animemark.com","file_uploads":"file-uploads.animemark.com","file_torrents":"file-torrents.animemark.com","file_comics":"file-comics.animemark.com","file_torrents_anime":"file-torrents-anime.animemark.com","file_torrents_comic":"file-torrents-comic.animemark.com","file_torrents_novel":"file-torrents-novel.animemark.com","file_comic_release_orig":"zz-cr-o.ato.to","file_comic_release_dest":"zz-cr-d.ato.to","anime":"animewindow.com","comic":"comicwindow.com","novel":"novelwindow.com","fb_login":"anyacg.com","allies":["animemark.com","ato.to","aniedit.org","bato.to","mangapark.net","mangawindow.net","anyacg.com"],"archive":"animemark.com"},
    status: {
      full: {"draft":{"file":"draft","text":"Draft","color":"#90a4ae"},"normal":{"file":"normal","text":"Normal","color":"#81c784"},"hidden":{"file":"hidden","text":"Hidden","color":"#fff176"},"trashed":{"file":"trashed","text":"Trashed","color":"#e57373"}},
    },
    lang: {
      items: {"af":{"file":"af","code":"af","text":"Afrikaans","sort":0,"show":3,"flag":"flags-country_flag-south_africa"},"sq":{"file":"sq","code":"sq","text":"Albanian","sort":0,"show":3,"flag":"flags-country_flag-albania"},"am":{"file":"am","code":"am","text":"Amharic","sort":0,"show":3,"flag":"flags-country_flag-ethiopia"},"ar":{"file":"ar","code":"ar","text":"Arabic","sort":2,"show":2,"flag":"flags-country_flag-saudi_arabia"},"an":{"file":"an","code":"an","text":"Aragonese","sort":0,"show":0,"flag":""},"hy":{"file":"hy","code":"hy","text":"Armenian","sort":0,"show":3,"flag":"flags-country_flag-armenia"},"ast":{"file":"ast","code":"ast","text":"Asturian","sort":0,"show":0,"flag":""},"az":{"file":"az","code":"az","text":"Azerbaijani","sort":0,"show":3,"flag":"flags-country_flag-azerbaijan"},"eu":{"file":"eu","code":"eu","text":"Basque","sort":0,"show":0,"flag":""},"be":{"file":"be","code":"be","text":"Belarusian","sort":0,"show":3,"flag":"flags-country_flag-belarus"},"bn":{"file":"bn","code":"bn","text":"Bengali","sort":0,"show":3,"flag":"flags-country_flag-bangladesh"},"bh":{"file":"bh","code":"bh","text":"Bihari","sort":0,"show":0,"flag":""},"bs":{"file":"bs","code":"bs","text":"Bosnian","sort":0,"show":3,"flag":"flags-country_flag-bosnia_and_herzegovina"},"br":{"file":"br","code":"br","text":"Breton","sort":0,"show":0,"flag":""},"bg":{"file":"bg","code":"bg","text":"Bulgarian","sort":2,"show":2,"flag":"flags-country_flag-bulgaria"},"my":{"file":"my","code":"my","text":"Burmese","sort":0,"show":3,"flag":"flags-country_flag-myanmar_burma_"},"km":{"file":"km","code":"km","text":"Cambodian","sort":0,"show":3,"flag":"flags-country_flag-cambodia"},"ca":{"file":"ca","code":"ca","text":"Catalan","sort":0,"show":3,"flag":"flags-country_flag-andorra"},"ceb":{"file":"ceb","code":"ceb","text":"Cebuano","sort":0,"show":3,"flag":"flags-country_flag-philippines"},"zh":{"file":"zh","code":"zh","text":"Chinese","sort":1,"show":1,"flag":"flags-country_flag-china"},"zh_hk":{"file":"zh_hk","code":"zh-HK","text":"Chinese (Cantonese)","sort":0,"show":3,"flag":"flags-country_flag-hong_kong_sar_china"},"zh_cn":{"file":"zh_cn","code":"zh-CN","text":"Chinese (Simplified)","sort":2,"show":0,"flag":"flags-country_flag-china","hide":true},"zh_tw":{"file":"zh_tw","code":"zh-TW","text":"Chinese (Traditional)","sort":0,"show":3,"flag":"flags-country_flag-taiwan"},"co":{"file":"co","code":"co","text":"Corsican","sort":0,"show":0,"flag":""},"hr":{"file":"hr","code":"hr","text":"Croatian","sort":0,"show":3,"flag":"flags-country_flag-croatia"},"cs":{"file":"cs","code":"cs","text":"Czech","sort":2,"show":2,"flag":"flags-country_flag-czechia"},"da":{"file":"da","code":"da","text":"Danish","sort":2,"show":2,"flag":"flags-country_flag-denmark"},"nl":{"file":"nl","code":"nl","text":"Dutch","sort":2,"show":2,"flag":"flags-country_flag-netherlands"},"en":{"file":"en","code":"en","text":"English","sort":1,"show":1,"flag":"flags-country_flag-united_kingdom"},"en_au":{"file":"en_au","code":"en-AU","text":"English (Australia)","sort":0,"show":0,"flag":""},"en_ca":{"file":"en_ca","code":"en-CA","text":"English (Canada)","sort":0,"show":0,"flag":""},"en_in":{"file":"en_in","code":"en-IN","text":"English (India)","sort":0,"show":0,"flag":""},"en_nz":{"file":"en_nz","code":"en-NZ","text":"English (New Zealand)","sort":0,"show":0,"flag":""},"en_za":{"file":"en_za","code":"en-ZA","text":"English (South Africa)","sort":0,"show":0,"flag":""},"en_gb":{"file":"en_gb","code":"en-GB","text":"English (United Kingdom)","sort":0,"show":0,"flag":"flags-country_flag-united_kingdom","hide":true},"en_us":{"file":"en_us","code":"en-US","text":"English (United States)","sort":0,"show":3,"flag":"flags-country_flag-united_states"},"eo":{"file":"eo","code":"eo","text":"Esperanto","sort":0,"show":3,"flag":"flags-flag-rainbow_flag"},"et":{"file":"et","code":"et","text":"Estonian","sort":0,"show":3,"flag":"flags-country_flag-estonia"},"fo":{"file":"fo","code":"fo","text":"Faroese","sort":0,"show":3,"flag":"flags-country_flag-faroe_islands"},"fil":{"file":"fil","code":"fil","text":"Filipino","sort":2,"show":2,"flag":"flags-country_flag-philippines"},"fi":{"file":"fi","code":"fi","text":"Finnish","sort":2,"show":2,"flag":"flags-country_flag-finland"},"fr":{"file":"fr","code":"fr","text":"French","sort":2,"show":2,"flag":"flags-country_flag-france"},"fr_ca":{"file":"fr_ca","code":"fr-CA","text":"French (Canada)","sort":0,"show":0,"flag":""},"fr_fr":{"file":"fr_fr","code":"fr-FR","text":"French (France)","sort":0,"show":0,"flag":"","hide":true},"fr_ch":{"file":"fr_ch","code":"fr-CH","text":"French (Switzerland)","sort":0,"show":0,"flag":""},"fy":{"file":"fy","code":"fy","text":"Frisian","sort":0,"show":0,"flag":""},"gl":{"file":"gl","code":"gl","text":"Galician","sort":0,"show":0,"flag":""},"ka":{"file":"ka","code":"ka","text":"Georgian","sort":0,"show":3,"flag":"flags-country_flag-georgia"},"de":{"file":"de","code":"de","text":"German","sort":2,"show":2,"flag":"flags-country_flag-germany"},"de_at":{"file":"de_at","code":"de-AT","text":"German (Austria)","sort":0,"show":0,"flag":""},"de_de":{"file":"de_de","code":"de-DE","text":"German (Germany)","sort":0,"show":0,"flag":"","hide":true},"de_li":{"file":"de_li","code":"de-LI","text":"German (Liechtenstein)","sort":0,"show":0,"flag":""},"de_ch":{"file":"de_ch","code":"de-CH","text":"German (Switzerland)","sort":0,"show":0,"flag":""},"el":{"file":"el","code":"el","text":"Greek","sort":2,"show":2,"flag":"flags-country_flag-greece"},"gn":{"file":"gn","code":"gn","text":"Guarani","sort":0,"show":3,"flag":"flags-country_flag-paraguay"},"gu":{"file":"gu","code":"gu","text":"Gujarati","sort":0,"show":3,"flag":"flags-country_flag-india"},"ht":{"file":"ht","code":"ht","text":"Haitian Creole","sort":0,"show":3,"flag":"flags-country_flag-haiti"},"ha":{"file":"ha","code":"ha","text":"Hausa","sort":0,"show":3,"flag":"flags-country_flag-niger"},"haw":{"file":"haw","code":"haw","text":"Hawaiian","sort":0,"show":0,"flag":""},"he":{"file":"he","code":"he","text":"Hebrew","sort":2,"show":2,"flag":"flags-country_flag-israel"},"hi":{"file":"hi","code":"hi","text":"Hindi","sort":2,"show":2,"flag":"flags-country_flag-india"},"hmn":{"file":"hmn","code":"hmn","text":"Hmong","sort":0,"show":0,"flag":""},"hu":{"file":"hu","code":"hu","text":"Hungarian","sort":2,"show":2,"flag":"flags-country_flag-hungary"},"is":{"file":"is","code":"is","text":"Icelandic","sort":0,"show":3,"flag":"flags-country_flag-iceland"},"ig":{"file":"ig","code":"ig","text":"Igbo","sort":0,"show":3,"flag":"flags-country_flag-nigeria"},"id":{"file":"id","code":"id","text":"Indonesian","sort":2,"show":2,"flag":"flags-country_flag-indonesia"},"ia":{"file":"ia","code":"ia","text":"Interlingua","sort":0,"show":0,"flag":""},"ga":{"file":"ga","code":"ga","text":"Irish","sort":0,"show":3,"flag":"flags-country_flag-iceland"},"it":{"file":"it","code":"it","text":"Italian","sort":2,"show":2,"flag":"flags-country_flag-italy"},"it_it":{"file":"it_it","code":"it-IT","text":"Italian (Italy)","sort":0,"show":0,"flag":"","hide":true},"it_ch":{"file":"it_ch","code":"it-CH","text":"Italian (Switzerland)","sort":0,"show":0,"flag":""},"ja":{"file":"ja","code":"ja","text":"Japanese","sort":1,"show":1,"flag":"flags-country_flag-japan"},"jv":{"file":"jv","code":"jv","text":"Javanese","sort":0,"show":3,"flag":"flags-country_flag-indonesia"},"kn":{"file":"kn","code":"kn","text":"Kannada","sort":0,"show":3,"flag":"flags-country_flag-india"},"kk":{"file":"kk","code":"kk","text":"Kazakh","sort":0,"show":3,"flag":"flags-country_flag-kazakhstan"},"ko":{"file":"ko","code":"ko","text":"Korean","sort":2,"show":1,"flag":"flags-country_flag-south_korea"},"ku":{"file":"ku","code":"ku","text":"Kurdish","sort":0,"show":3,"flag":"flags-country_flag-iraq"},"ckb":{"file":"ckb","code":"ckb","text":"Kurdish (Arabci), Sorani","sort":0,"show":0,"flag":"","hide":true},"ky":{"file":"ky","code":"ky","text":"Kyrgyz","sort":0,"show":3,"flag":"flags-country_flag-kyrgyzstan"},"lo":{"file":"lo","code":"lo","text":"Laothian","sort":0,"show":3,"flag":"flags-country_flag-laos"},"la":{"file":"la","code":"la","text":"Latin","sort":0,"show":0,"flag":""},"lv":{"file":"lv","code":"lv","text":"Latvian","sort":0,"show":3,"flag":"flags-country_flag-latvia"},"ln":{"file":"ln","code":"ln","text":"Lingala","sort":0,"show":0,"flag":""},"lt":{"file":"lt","code":"lt","text":"Lithuanian","sort":0,"show":3,"flag":"flags-country_flag-lithuania"},"lb":{"file":"lb","code":"lb","text":"Luxembourgish","sort":0,"show":3,"flag":"flags-country_flag-luxembourg"},"mk":{"file":"mk","code":"mk","text":"Macedonian","sort":0,"show":3,"flag":"flags-country_flag-north_macedonia"},"mg":{"file":"mg","code":"mg","text":"Malagasy","sort":0,"show":3,"flag":"flags-country_flag-madagascar"},"ms":{"file":"ms","code":"ms","text":"Malay","sort":2,"show":2,"flag":"flags-country_flag-malaysia"},"ml":{"file":"ml","code":"ml","text":"Malayalam","sort":0,"show":3,"flag":"flags-country_flag-india"},"mt":{"file":"mt","code":"mt","text":"Maltese","sort":0,"show":3,"flag":"flags-country_flag-malta"},"mi":{"file":"mi","code":"mi","text":"Maori","sort":0,"show":3,"flag":"flags-country_flag-new_zealand"},"mr":{"file":"mr","code":"mr","text":"Marathi","sort":0,"show":3,"flag":"flags-country_flag-india"},"mo":{"file":"mo","code":"mo","text":"Moldavian","sort":0,"show":3,"flag":"flags-country_flag-moldova"},"mn":{"file":"mn","code":"mn","text":"Mongolian","sort":0,"show":3,"flag":"flags-country_flag-mongolia"},"ne":{"file":"ne","code":"ne","text":"Nepali","sort":0,"show":3,"flag":"flags-country_flag-nepal"},"no":{"file":"no","code":"no","text":"Norwegian","sort":0,"show":3,"flag":"flags-country_flag-norway"},"nb":{"file":"nb","code":"nb","text":"Norwegian (Bokmal)","sort":0,"show":0,"flag":"flags-country_flag-norway"},"nn":{"file":"nn","code":"nn","text":"Norwegian (Nynorsk)","sort":0,"show":0,"flag":"flags-country_flag-norway"},"ny":{"file":"ny","code":"ny","text":"Nyanja","sort":0,"show":3,"flag":"flags-country_flag-malawi"},"oc":{"file":"oc","code":"oc","text":"Occitan","sort":0,"show":0,"flag":""},"or":{"file":"or","code":"or","text":"Oriya","sort":0,"show":0,"flag":""},"om":{"file":"om","code":"om","text":"Oromo","sort":0,"show":0,"flag":""},"ps":{"file":"ps","code":"ps","text":"Pashto","sort":0,"show":3,"flag":"flags-country_flag-afghanistan"},"fa":{"file":"fa","code":"fa","text":"Persian","sort":0,"show":3,"flag":"flags-country_flag-iran"},"pl":{"file":"pl","code":"pl","text":"Polish","sort":2,"show":2,"flag":"flags-country_flag-poland"},"pt":{"file":"pt","code":"pt","text":"Portuguese","sort":2,"show":2,"flag":"flags-country_flag-portugal"},"pt_br":{"file":"pt_br","code":"pt-BR","text":"Portuguese (Brazil)","sort":2,"show":2,"flag":"flags-country_flag-brazil"},"pt_pt":{"file":"pt_pt","code":"pt-PT","text":"Portuguese (Portugal)","sort":2,"show":0,"flag":"flags-country_flag-portugal","hide":true},"pa":{"file":"pa","code":"pa","text":"Punjabi","sort":0,"show":0,"flag":""},"qu":{"file":"qu","code":"qu","text":"Quechua","sort":0,"show":0,"flag":""},"ro":{"file":"ro","code":"ro","text":"Romanian","sort":2,"show":2,"flag":"flags-country_flag-romania"},"rm":{"file":"rm","code":"rm","text":"Romansh","sort":0,"show":3,"flag":"flags-country_flag-switzerland"},"ru":{"file":"ru","code":"ru","text":"Russian","sort":2,"show":2,"flag":"flags-country_flag-russia"},"sm":{"file":"sm","code":"sm","text":"Samoan","sort":0,"show":3,"flag":"flags-country_flag-samoa"},"gd":{"file":"gd","code":"gd","text":"Scots Gaelic","sort":0,"show":0,"flag":""},"sr":{"file":"sr","code":"sr","text":"Serbian","sort":0,"show":3,"flag":"flags-country_flag-serbia"},"sh":{"file":"sh","code":"sh","text":"Serbo-Croatian","sort":0,"show":3,"flag":"flags-country_flag-serbia"},"st":{"file":"st","code":"st","text":"Sesotho","sort":0,"show":3,"flag":"flags-country_flag-lesotho"},"sn":{"file":"sn","code":"sn","text":"Shona","sort":0,"show":3,"flag":"flags-country_flag-zimbabwe"},"sd":{"file":"sd","code":"sd","text":"Sindhi","sort":0,"show":3,"flag":"flags-country_flag-pakistan"},"si":{"file":"si","code":"si","text":"Sinhalese","sort":0,"show":3,"flag":"flags-country_flag-sri_lanka"},"sk":{"file":"sk","code":"sk","text":"Slovak","sort":0,"show":3,"flag":"flags-country_flag-slovakia"},"sl":{"file":"sl","code":"sl","text":"Slovenian","sort":0,"show":3,"flag":"flags-country_flag-slovenia"},"so":{"file":"so","code":"so","text":"Somali","sort":0,"show":3,"flag":"flags-country_flag-somalia"},"es":{"file":"es","code":"es","text":"Spanish","sort":2,"show":2,"flag":"flags-country_flag-spain"},"es_ar":{"file":"es_ar","code":"es-AR","text":"Spanish (Argentina)","sort":0,"show":0,"flag":""},"es_cl":{"file":"es_cl","code":"es-CL","text":"Spanish (Chile)","sort":0,"show":0,"flag":""},"es_co":{"file":"es_co","code":"es-CO","text":"Spanish (Colombia)","sort":0,"show":0,"flag":""},"es_cr":{"file":"es_cr","code":"es-CR","text":"Spanish (Costa Rica)","sort":0,"show":0,"flag":""},"es_hn":{"file":"es_hn","code":"es-HN","text":"Spanish (Honduras)","sort":0,"show":0,"flag":""},"es_419":{"file":"es_419","code":"es-419","text":"Spanish (Latin America)","sort":2,"show":2,"flag":"flags-country_flag-mexico"},"es_mx":{"file":"es_mx","code":"es-MX","text":"Spanish (Mexico)","sort":2,"show":0,"flag":"flags-country_flag-mexico"},"es_pe":{"file":"es_pe","code":"es-PE","text":"Spanish (Peru)","sort":0,"show":0,"flag":""},"es_es":{"file":"es_es","code":"es-ES","text":"Spanish (Spain)","sort":2,"show":0,"flag":"flags-country_flag-spain","hide":true},"es_us":{"file":"es_us","code":"es-US","text":"Spanish (US)","sort":0,"show":0,"flag":""},"es_uy":{"file":"es_uy","code":"es-UY","text":"Spanish (Uruguay)","sort":0,"show":0,"flag":""},"es_ve":{"file":"es_ve","code":"es-VE","text":"Spanish (Venezuela)","sort":0,"show":0,"flag":""},"su":{"file":"su","code":"su","text":"Sundanese","sort":0,"show":0,"flag":""},"sw":{"file":"sw","code":"sw","text":"Swahili","sort":0,"show":3,"flag":"flags-country_flag-kenya"},"sv":{"file":"sv","code":"sv","text":"Swedish","sort":2,"show":2,"flag":"flags-country_flag-sweden"},"tg":{"file":"tg","code":"tg","text":"Tajik","sort":0,"show":3,"flag":"flags-country_flag-tajikistan"},"ta":{"file":"ta","code":"ta","text":"Tamil","sort":0,"show":3,"flag":"flags-country_flag-sri_lanka"},"tt":{"file":"tt","code":"tt","text":"Tatar","sort":0,"show":0,"flag":""},"te":{"file":"te","code":"te","text":"Telugu","sort":0,"show":0,"flag":""},"th":{"file":"th","code":"th","text":"Thai","sort":2,"show":2,"flag":"flags-country_flag-thailand"},"ti":{"file":"ti","code":"ti","text":"Tigrinya","sort":0,"show":3,"flag":"flags-country_flag-eritrea"},"to":{"file":"to","code":"to","text":"Tonga","sort":0,"show":3,"flag":"flags-country_flag-tonga"},"tr":{"file":"tr","code":"tr","text":"Turkish","sort":2,"show":2,"flag":"flags-country_flag-turkey"},"tk":{"file":"tk","code":"tk","text":"Turkmen","sort":0,"show":3,"flag":"flags-country_flag-turkmenistan"},"tw":{"file":"tw","code":"tw","text":"Twi","sort":0,"show":0,"flag":""},"ug":{"file":"ug","code":"ug","text":"Uighur","sort":0,"show":0,"flag":""},"uk":{"file":"uk","code":"uk","text":"Ukrainian","sort":2,"show":2,"flag":"flags-country_flag-ukraine"},"ur":{"file":"ur","code":"ur","text":"Urdu","sort":0,"show":3,"flag":"flags-country_flag-pakistan"},"uz":{"file":"uz","code":"uz","text":"Uzbek","sort":0,"show":3,"flag":"flags-country_flag-uzbekistan"},"vi":{"file":"vi","code":"vi","text":"Vietnamese","sort":2,"show":2,"flag":"flags-country_flag-vietnam"},"wa":{"file":"wa","code":"wa","text":"Walloon","sort":0,"show":0,"flag":""},"cy":{"file":"cy","code":"cy","text":"Welsh","sort":0,"show":0,"flag":""},"xh":{"file":"xh","code":"xh","text":"Xhosa","sort":0,"show":0,"flag":"flags-country_flag-south_africa"},"yi":{"file":"yi","code":"yi","text":"Yiddish","sort":0,"show":0,"flag":""},"yo":{"file":"yo","code":"yo","text":"Yoruba","sort":0,"show":3,"flag":"flags-country_flag-nigeria"},"zu":{"file":"zu","code":"zu","text":"Zulu","sort":0,"show":3,"flag":"flags-country_flag-south_africa"}},
    },
    regexp: {
      url: /(ftp|http|https):\/\/(\w+:{0,1}\w*@)?(\S+)(:[0-9]+)?(\/|\/([\w#!:.?+=&%@!\-/]))?/i,
http: /(http|https):\/\/(\w+:{0,1}\w*@)?(\S+)(:[0-9]+)?(\/|\/([\w#!:.?+=&%@!\-/]))?/i,
ftp: /ftp:\/\/(\w+:{0,1}\w*@)?(\S+)(:[0-9]+)?(\/|\/([\w#!:.?+=&%@!\-/]))?/i,
ed2k: /^ed2k:\/\/\|file\|*\|\d+\|[0-9a-zA-Z]{32}\|$/i,
thunder: /thunder:\/\/(\w+:{0,1}\w*@)?(\S+)(:[0-9]+)?(\/|\/([\w#!:.?+=&%@!\-/]))?/i,
magnet: /magnet:\?xt=urn:[a-z0-9]*/i,
irc: /([#&][^\x07\x2C\s]{,200})/i,
provider: /(http|https):\/\/(\w+:{0,1}\w*@)?(\S+)(:[0-9]+)?(\/|\/([\w#!:.?+=&%@!\-/]))?/i,
email: /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$/,
p_and_br: /<p.*?>|<\/p>|<br.*?>/gi,
hex_color: /^#([a-f0-9]{3,4}|[a-f0-9]{4}(?:[a-f0-9]{2}){1,2})\b$/i,
user_account_name: /^[a-zA-Z0-9\_]{6,18}$/i,
user_name: function (str) {
    if (!str) {
      return 1;
    }
    str = String(str).trim();
    if (String(str).length < 6 || String(str).length > 18) {
      return 2;
    }
    if (/^[a-zA-Z0-9\_]{6,18}$/i.test(str) === false) {
      return 3;
    }
    if (String(str).includes('__')) {
      return 4;
    }
    const mat = String(str).match(/\_/g);
    if (mat && mat.length > 3) {
      return 5;
    }
    return 0;
  },
    },
    timezone: {
      zones: {"-12:00":{"file":"-12:00","text":"-12:00","diff":-720},"-11:00":{"file":"-11:00","text":"-11:00","diff":-660},"-10:00":{"file":"-10:00","text":"-10:00","diff":-600},"-09:30":{"file":"-09:30","text":"-09:30","diff":-570},"-09:00":{"file":"-09:00","text":"-09:00","diff":-540},"-08:00":{"file":"-08:00","text":"-08:00","diff":-480},"-07:00":{"file":"-07:00","text":"-07:00","diff":-420},"-06:00":{"file":"-06:00","text":"-06:00","diff":-360},"-05:00":{"file":"-05:00","text":"-05:00","diff":-300},"-04:00":{"file":"-04:00","text":"-04:00","diff":-240},"-03:30":{"file":"-03:30","text":"-03:30","diff":-210},"-03:00":{"file":"-03:00","text":"-03:00","diff":-180},"-02:00":{"file":"-02:00","text":"-02:00","diff":-120},"-01:00":{"file":"-01:00","text":"-01:00","diff":-60},"+00:00":{"file":"+00:00","text":"UTC","diff":0},"+01:00":{"file":"+01:00","text":"+01:00","diff":60},"+02:00":{"file":"+02:00","text":"+02:00","diff":120},"+03:00":{"file":"+03:00","text":"+03:00","diff":180},"+03:30":{"file":"+03:30","text":"+03:30","diff":210},"+04:00":{"file":"+04:00","text":"+04:00","diff":240},"+04:30":{"file":"+04:30","text":"+04:30","diff":270},"+05:00":{"file":"+05:00","text":"+05:00","diff":300},"+05:30":{"file":"+05:30","text":"+05:30","diff":330},"+05:45":{"file":"+05:45","text":"+05:45","diff":345},"+06:00":{"file":"+06:00","text":"+06:00","diff":360},"+06:30":{"file":"+06:30","text":"+06:30","diff":390},"+07:00":{"file":"+07:00","text":"+07:00","diff":420},"+08:00":{"file":"+08:00","text":"+08:00","diff":480},"+08:45":{"file":"+08:45","text":"+08:45","diff":525},"+09:00":{"file":"+09:00","text":"+09:00","diff":540},"+09:30":{"file":"+09:30","text":"+09:30","diff":570},"+10:00":{"file":"+10:00","text":"+10:00","diff":600},"+10:30":{"file":"+10:30","text":"+10:30","diff":630},"+11:00":{"file":"+11:00","text":"+11:00","diff":660},"+11:30":{"file":"+11:30","text":"+11:30","diff":690},"+12:00":{"file":"+12:00","text":"+12:00","diff":720},"+12:45":{"file":"+12:45","text":"+12:45","diff":765},"+13:00":{"file":"+13:00","text":"+13:00","diff":780},"+14:00":{"file":"+14:00","text":"+14:00","diff":840}},
    },
  },
  utils:{
    math: {
      random(min, max) {
    return Math.floor(Math.random() * (max - min + 1) + min)
  },
      random8char() {
    return Math.random().toString(36).substr(2, 8)
  },
    },
    url: {
      alter_query(url, dels = [], adds = null, encode = true) {
    url = String(url);
    if (url.includes('?') && dels && dels.length) {
      const parts = url.split('?');
      const base = parts[0];
      const pars = [];
      for (const q_and_v of String(parts[1]).split('&')) {
        const q = String(q_and_v).split('=')[0];
        if (dels.includes(q) === false) {
          pars.push(q_and_v);
        }
      }
      if (pars.length) {
        url = `${base}?${pars.join('&')}`;
      } else {
        url = `${base}`;
      }
    }
    if (adds && (adds.length || Object.keys(adds).length)) {
      if (url.includes('?') === false) {
        url += '?';
      }
      if (url.endsWith('?') === false) {
        url += '&';
      }
      if (Array.isArray(adds)) {
        url += adds.join('&');
      } else if (typeof adds === 'string') {
        url += adds;
      } else {
        const pars = [];
        for (const [key, val] of Object.entries(adds)) {
          if (val === undefined || val === null || Number.isNaN(val)) {
            pars.push(key);
            continue;
          }
          pars.push(`${key}=${encode ? encodeURIComponent(val) : val}`);
        }
        url += pars.join('&');
      }
    }
    return url;
  },
    },
    string: {
      range_str_to_arr(str, min = null, max = null, glue = '~') {
    const arr = [];
    const exp = new RegExp(`[^0-9\-\,\s\\${glue}]`, 'g');
    str = String(str).replace(exp, '');
    str.split(',').forEach(s => {
      let [vl, vr] = String(s).split(glue);
      if (!vl) return;
      vl = Number(vl);
      if (Number.isInteger(vl) === false || (min !== null && vl < min) || (max !== null && vl > max)) {
        return;
      }

      if (vr) {
        vr = Number(vr);
        if (Number.isInteger(vr) && vr > vl && (min === null || vr >= min) && (max === null || vr <= max)) {
          for (let n = vl; n <= vr; n++) {
            if (arr.includes(n) === false) {
              arr.push(n);
            }
          }
          return;
        }
      }

      if (arr.includes(vl) === false) {
        arr.push(vl);
      }
    });
    return arr.sort((a, b) => a - b);
  },
      range_arr_to_str(arr, min = null, max = null, glue = '~') {
    if (!arr || Array.isArray(arr) === false) return '';
    arr = arr
      .map(n => Number(n))
      .filter(n => Number.isInteger(n) && (min === null || n >= min) && (max === null || n <= max))
      .sort((a, b) => a - b)
      .filter((val, idx, self) => self.indexOf(val) === idx);
    arr.push('END');

    const str = [];

    let last = null;
    let temp = [];
    arr.forEach(curr => {
      if (last === 'END') return;
      if (curr !== 'END') {
        // first one || continuous
        if (last === null || curr - last === 1) {
          temp.push(curr);
          last = curr;
          return;
        }
      }

      // Discontinuous then End this section
      if (temp.length === 1) {
        str.push(temp.pop())
      } else if (temp.length === 2) {
        str.push(temp.shift())
        str.push(temp.shift())
      } else if (temp.length >= 3) {
        str.push(`${temp.shift()}${glue}${temp.pop()}`)
      }

      temp = [curr];
      last = curr;
    }); // end forEach

    return str.join(',');
  },
      int_str_to_arr(str, opt = {}) {
    opt = Object.assign({ min: null, max: null, unique: false, sort: false, glue: ',', hyphen: '~' }, opt);

    const arr = [];
    const exp = new RegExp(`[^0-9\-\s\\${opt.glue}\\${opt.hyphen}]`, 'g');
    str = String(str).replace(exp, '');
    str.split(opt.glue).forEach(s => {
      let [vl, vr] = String(s).split(opt.hyphen);
      if (!vl) return;
      vl = Number(vl);
      if (Number.isInteger(vl) === false || (opt.min !== null && vl < opt.min) || (opt.max !== null && vl > opt.max)) {
        console.log(`return ${vl}`);
        return;
      }

      if (vr) {
        vr = Number(vr);
        if (Number.isInteger(vr) && (opt.min === null || vr >= opt.min) && (opt.max === null || vr <= opt.max)) {
          if (vr >= vl) {
            for (let n = vl; n <= vr; n++) {
              if (!opt.unique || arr.includes(n) === false) {
                arr.push(n);
              }
            }
            return;
          }
          for (let n = vl; n >= vr; n--) {
            if (!opt.unique || arr.includes(n) === false) {
              arr.push(n);
            }
          }
          return;
        }
      }

      if (!opt.unique || arr.includes(vl) === false) {
        arr.push(vl);
      }
    });
    if (opt.sort) {
      const func = typeof opt.sort === 'function' ? opt.sort : (a, b) => a - b;
      arr.sort(func);
    }
    return arr;
  },
      int_arr_to_str(arr, opt = {}) {
    opt = Object.assign({ min: null, max: null, unique: false, sort: false, glue: ',', hyphen: '~' }, opt);

    if (!arr || Array.isArray(arr) === false) return '';
    arr = arr
      .map(n => Number(n))
      .filter(n => Number.isInteger(n) && (opt.min === null || n >= opt.min) && (opt.max === null || n <= opt.max))

    if (opt.unique) {
      arr = arr
        .filter((val, idx, self) => self.indexOf(val) === idx);// unique array
    }

    if (opt.sort) {
      const func = typeof opt.sort === 'function' ? opt.sort : (a, b) => a - b;
      arr.sort(func);
    }

    arr.push('END');

    const str = [];

    let last = null;
    let temp = [];// range
    let sign = 0;// -1 0 1
    arr.forEach(curr => {
      if (last === 'END') return;
      if (curr !== 'END') {
        // first one || continuous
        if (last === null) {
          temp.push(curr);
          last = curr;
          return;
        }
        const diff = curr - last;
        if (Math.abs(diff) === 1) {
          if (sign === 0 || diff === sign) {
            temp.push(curr);
            sign = diff;
            last = curr;
            return;
          }
        }
      }

      // Discontinuous then End this section
      if (temp.length === 1) {
        str.push(temp.pop())
      } else if (temp.length === 2) {
        str.push(temp.shift())
        str.push(temp.shift())
      } else if (temp.length >= 3) {
        str.push(`${temp.shift()}${opt.hyphen}${temp.pop()}`)
      }

      temp = [curr];
      sign = 0;
      last = curr;
    }); // end forEach

    return str.join(opt.glue);
  },
    },
  },
};


/* -BLOCK- */

/**
 * random int between [min, max]
 * min and max can be negative number
 */
function random(min, max) {
  return Math.floor(Math.random() * (max - min + 1) + min);
};

function random8char() {
  return Math.random().toString(36).substr(2, 8) // 8char length
};

/**
 * @deprecated change to "let O = new URL(url);"
 * parseURL
 *
 * @param {any} url
 * @returns
 */
function parseURL(url) {
  return new URL(url);
};

function toggle_body_modal_mode(mask = null) {
  //console.log('toggle_body_modal_mode:', mask);
  const toggler = function (mask) {
    const class_name = 'body-for-modal-mask';
    if (mask) {
      if (document.body.classList.contains(class_name) === false) {
        document.body.classList.add(class_name);
      }
      return;
    }
    if (document.body.classList.contains(class_name)) {
      document.body.classList.remove(class_name);
    }
  }
  if (mask === 1 || mask === true) {
    toggler(true);
    return;
  }
  if (mask === 0 || mask === false) {
    toggler(false);
    return;
  }
  setTimeout(function () {
    const mask = document.querySelector('.modal-mask');
    toggler(mask ? true : false);
  }, 1000);
}

function format_image_url(name, width = null) {
  if (!name) {
    return `//${_cfg.static}/img/no-image.png`;
  }
  const ws = width ? `/W${width}` : '';
  return `//${_jss.confs.domain.file_archive}${ws}/${name}`;
}

function flash_msg(msg, type = 'primary', timeout = 3000, icon = true) {
  app._notify_b({
    type,
    text: msg,
    icon,
  })
}

/**
 * Catch defined system error
 * Or trigger an error
 * return false if no defined system error catched
 *
 * Test if error exists
 * if(handle_defined_error(eno)){
 *  return
 * }
 * OR
 * Throw an error
 * handle_defined_error(401)
 *
 * @param {*} data | eno
 * @returns {Boolean} Catch defined error then return true else return false
 */
function handle_defined_error(data) {
  if (data && data.error) {
    flash_msg(`System error, please try again!`, 'danger');
    return true;
  }
  let eno = data && data.eno ? data.eno : data;
  switch (eno) {
    case 4001:
      flash_msg(`Unknown error, please try again!`, 'danger');
      break;
    case 4002:
      flash_msg(`System error, please try again!`, 'danger');
      break;
    case 4003:
      flash_msg(`FileSystem error, please try again!`, 'danger');
      break;
    case 4004:
      flash_msg(`Database error, please try again!`, 'danger');
      break;
    case 4005:
      flash_msg(`Session error, please try again!`, 'danger');
      break;
    case 4006:
      flash_msg(`Account error, please try again!`, 'danger');
      break;
    case 4007:
      flash_msg(`Please login first!`, 'danger');
      break;
    case 4008:
      flash_msg(`Param error , please try again!`, 'danger');
      break;
    case 4009:
      flash_msg(`Input error , please try again!`, 'danger');
      break;
    case 4010:
      flash_msg(`Duplicate entry exists!`, 'danger');
      break;
    case 4011:
      flash_msg(`Mail server failure, please try again!`, 'danger');
      break;
    case 4012:
      flash_msg(`Captcha verification failure, please try again!`, 'danger');
      break;

    default:
      return false
  }

  return true
}

if (axios) {
  axios.defaults.params = {
    _r: random8char()
  };
  axios.defaults.timeout = 59000;
}

/**
 * global mixin
 */
const VueMixin_Global = function () {
  return {
    directives: {
      // indeterminate: function (value) {
      //   this.el.indeterminate = Boolean(value)
      // },
      indeterminate: function (el, binding) {
        el.indeterminate = Boolean(binding.value)
      },
    },
    data() {
      return {
        ss: {
          _uid: _uid,
          _cfg: _cfg,
          _jss: _jss,
        },
      }
    },
    methods: {
      _go_login(cf = false) {
        if (!cf || confirm(cf)) {
          const url = `//${_jss.confs.domain.id}.${_cfg.base}/login`;
          window.location.href = url
        }
      },
      _go_logout(cf = false) {
        if (!cf || confirm(cf)) {
          const url = `//${_jss.confs.domain.id}.${_cfg.base}/logout`;
          window.location.href = url;
        }
      },
      _format_image_url(name, width = null) {
        return format_image_url(name, width);
      },
      __lang_code_to_flag(code) {
        return _jss.confs.lang.items[code].flag;
      },
      __emoji(name, addClass = '') {
        return `emoji emoji-${name}` + (addClass ? ` ${addClass}` : '');
      },
    }
  }
}; // global mixin end

Vue.component('notification', {
  props: ['msg'],
  data() {
    return {
      time: 0,
      left: 0,
    };
  },
  computed: {
    item() {
      const val = this.msg.text ? this.msg : { text: this.msg };
      let time = 5;
      switch (val.type) {
        case 'danger':
          time = 15
          break;
        case 'warning':
          time = 10;
          break;
      }
      const def = {
        type: 'primary',
        text: '',
        time,
        icon: false,
      }
      return Object.assign({}, def, val);
    },
    icon() {
      if (!this.item.icon) return '';
      switch (this.item.type) {
        case 'primary':
        case 'secondary':
          return '<i class="mr-2 fas fa-info-circle"></i>';
        case 'success':
          return '<i class="mr-2 fas fa-check-circle"></i>';
        case 'danger':
          return '<i class="mr-2 fas fa-times-circle"></i>';
        case 'warning':
          return '<i class="mr-2 fas fa-exclamation-triangle"></i>';
        case 'info':
          return '<i class="mr-2 fas fa-info-circle"></i>';
        case 'light':
          return '<i class="mr-2 fas fa-info-circle"></i>';
        case 'dark':
          return '<i class="mr-2 fas fa-info-circle"></i>';
      }
      return '';
    },
    prog() {
      if (this.time <= 0) return '0%';
      return `${(this.left / this.time).toFixed(4) * 100}%`;
    }
  },
  mounted() {
    if (this.item.time > 0) {
      this.time = Number(this.item.time);
      this.left = Number(this.item.time);
      this.countdown();
    }
  },
  methods: {
    countdown(step = 100) {
      if (this.left < 0) {
        return;
      }
      this.left = this.left - (step / 1000);
      setTimeout(() => {
        this.countdown(step);
      }, step);
    },
    close() {
      this.left = -1;
      console.log(this.left);
    }
  },
  template: `<transition name="fade">
    <div v-if="left >= 0" class="alert alert-dismissible fade show" :class="'alert-'+this.item.type">
      <span v-if="icon" v-html="icon"></span>{{item.text}}
      <button type="button" class="close" @click="close">
        <span aria-hidden="true">&times;</span>
      </button>
      <div v-if="left > 0" class="progress">
        <div class="progress-bar" :class="'bg-'+this.item.type" :style="'width: '+ this.prog"></div>
      </div>
    </div>
  </transition>`,
});

const VueMixin_Notify = function () {
  return {
    data() {
      return {
        notify_msg_t: [],
        notify_msg_b: [],
      }
    },
    methods: {
      _notify_t(msg) {
        if (!msg) return;
        this.notify_msg_t.push(msg);
      },
      _notify_b(msg) {
        if (!msg) return;
        this.notify_msg_b.push(msg);
      }
    },
  }
};

function notify_t(msg) {
  app._notify_t(msg);
}

function notify_b(msg) {
  app._notify_b(msg);
}

Vue.component('back-to-top-btn', {
  data() {
    return {
      show: false,
    };
  },
  computed: {

  },
  mounted() {
    window.addEventListener('scroll', this.handleScroll);
  },
  methods: {
    handleScroll(event) {
      const scrollY = window.scrollY;
      if (scrollY >= 300) {
        this.show = true;
      } else {
        this.show = false;
      }
    },
    scrollToTop() {
      window.scrollTo({
        top: 0,
        //left: 0,
        behavior: "smooth"
      });
    }
  },
  template: `<transition name="back-to-top-btn">
    <div v-if="show" class="back-to-top-btn" @click="scrollToTop">
      <i class="fas fa-fw fa-arrow-up"></i>
    </div>
  </transition>`,
});

Vue.component('amlink', {
  data: function () { return {} },
  template: '<a>[[amlink]]</a>'
})
Vue.component('spoiler', {
  data: function () { return {} },
  template: '<div>[[spoiler]]</div>'
})

/* -BLOCK- */

/**
 * type: radio check multi
 */

const VueMixin_Filter = function (filterType) {
  return {
    data: function () {
      return {
        filterParams: params,
        filterFattrs: fattrs,

        filterType,
        filterTimer: null,
        filterDone: false,
        filterShow: false,
        filterTree: {

          genres: {
            type: 'multi',
            title: 'Genres',
            hasAll: true,
            hasCount: true,
            items: []
          },

          langs: {
            type: 'check',
            title: 'Translated',
            hasAll: true,
            hasCount: true,
            items: []
          },

          origs: {
            type: 'check',
            title: 'Original',
            hasAll: true,
            hasCount: true,
            items: []
          },

          release: {
            type: 'radio',
            title: 'Status',
            hasAll: true,
            items: [
              {
                title: 'Pending',
                value: 'pending',
                state: 0
              },
              {
                title: 'Ongoing',
                value: 'ongoing',
                state: 0
              },
              {
                title: 'Completed',
                value: 'completed',
                state: 0
              },
              {
                title: 'Hiatus',
                value: 'hiatus',
                state: 0
              },
              {
                title: 'Cancelled',
                value: 'cancelled',
                state: 0
              },
            ]
          },

          chapters: {
            title: 'Chapters',
            name: 'chapters',
            type: 'radio',
            hasAll: true,
            hasCount: false,
            default: 'all',
            items: [{
              title: '1 ~ 9',
              value: '1-9',
              state: 0
            },
            {
              title: '10 ~ 29',
              value: '10-29',
              state: 0
            },
            {
              title: '30 ~ 99',
              value: '30-99',
              state: 0
            },
            {
              title: '100 ~ 199',
              value: '100-199',
              state: 0
            },
            {
              title: '200+',
              value: '200',
              state: 0
            },
            {
              title: '100+',
              value: '100',
              state: 0
            },
            {
              title: '50+',
              value: '50',
              state: 0
            },
            {
              title: '10+',
              value: '10',
              state: 0
            },
            {
              title: '1+',
              value: '1',
              state: 0
            },
            ]
          },

        },
      }
    },
    created: function () {
      this.filterBuildTree(this.filterParams)
    },
    methods: {
      filterBuildTree: function (states) {

        const _confs = {
          langs: { all: _jss.confs.lang.items, has: this.filterFattrs.langs, },
          origs: { all: _jss.confs.lang.items, has: this.filterFattrs.origs, },
          genres: { all: _genres, has: this.filterFattrs.genres, },
        }

        for (let field in this.filterTree) {
          const items = this.filterTree[field].items;

          // from _confs
          if (_confs[field]) {
            const _all = _confs[field].all;
            const _has = _confs[field].has;

            let last_sort = 1;
            for (const [file, item] of Object.entries(_all)) {
              if (_has.includes(file) === false) continue;
              items.push({
                title: item.text,
                value: item.file,
                state: 0,
                break: (field === 'genres' && item.sort !== last_sort ? 1 : 0),
              })
              last_sort = item.sort;
            }
          }

          // from saved state
          let selectAll = true
          for (let key in items) {
            let item = items[key]
            let state = 0
            if (states[field]) {
              if (states[field].inc.includes(item.value) === true) {
                state = 1
                selectAll = false
              }
              if (states[field].exc.includes(item.value) === true) {
                state = 2
                selectAll = false
              }
            }
            //console.log(state)
            items[key].state = state;//randomInt(0, 2)
          }

          // add the all item
          if (this.filterTree[field].hasAll) {
            const item = {
              title: 'All',
              value: 'all',
              state: selectAll ? 1 : 0,
              isAll: true,
            }
            items.unshift(item)
          }

          this.filterTree[field].items = items
        }

        this.filterDone = true
        setTimeout(function () {
          this.filterShow = true
        }.bind(this), 300)
      }, // end build tree

      filterOnClick: function (field, idx) {
        idx = parseInt(idx)

        let group = this.filterTree[field]
        let items = group.items
        let item = items[idx]
        let oldState = item.state
        let maxState = group.type == 'multi' ? 2 : 1

        // change
        if (item.isAll || group.type == 'radio') {
          item.state = 1
        } else {
          let newState = oldState + 1
          if (newState > maxState) {
            newState = 0
          }
          item.state = newState
        }

        // compress
        if (item.isAll || group.type == 'radio') {
          // all clicked or radio mode
          for (let key in items) {
            key = parseInt(key)
            if (key !== idx) {
              items[key].state = 0
            }
          }
        } else {
          // not clicked the all button
          let hasU = false, hasI = false, hasE = false;
          let arrU = [], arrI = [], arrE = [];
          let I2U = false, E2U = false;
          let A2V = -1;// all to value

          for (let k in items) {
            let item = items[k]

            // exclude the all item
            if (item.isAll) {
              continue
            }

            let state = item.state
            if (state == 0) {
              hasU = true
              arrU.push(k)
            } else if (state == 1) {
              hasI = true
              arrI.push(k)
            } else if (state == 2) {
              hasE = true
              arrE.push(k)
            }
          }

          if (hasU && hasI && hasE) {
            // has all, ignore
            A2V = 0
          } else if (hasU && hasI) {
            // ignore
            A2V = 0
          } else if (hasI && hasE) {
            // I change to U
            I2U = true
            A2V = 0
          } else if (hasU && hasE) {
            // ignore
            A2V = 0
          } else if (hasU) {
            // ignore
            A2V = 1
          } else if (hasI) {
            // I change to U
            I2U = true
            A2V = 1
          } else if (hasE) {
            // E change to U
            E2U = true
            A2V = 1
          }

          if (I2U) {
            for (let i = 0; i < arrI.length; i++) {
              items[arrI[i]].state = 0
            }
          }

          if (E2U) {
            for (let i = 0; i < arrE.length; i++) {
              items[arrI[i]].state = 0
            }
          }

          if (A2V > -1) {
            if (group.hasAll) {
              for (let key in items) {
                if (items[key].isAll) {
                  items[key].state = A2V
                  break
                }
              }
            }
          }
        }
        // @todo this.filterApplyChange()
        if (this.filterTimer) {
          clearTimeout(this.filterTimer)
        }
        this.filterTimer = setTimeout(() => {
          this.filterApplyChange()
        }, 2000)
      }, // end onClick

      filterBuildUrl: function (page) {
        let arrays = {}

        for (let field in this.filterTree) {
          let group = this.filterTree[field]
          let items = group.items

          for (let key in items) {
            let item = items[key]
            if (item.isAll && item.state == 1) {
              break
            }

            if (item.state == 0) {
              continue
            }

            if (!arrays[field]) {
              arrays[field] = {
                inc: [],
                exc: [],
              }
            }

            if (item.state == 1) {
              arrays[field].inc.push(item.value)
            }
            if (item.state == 2) {
              arrays[field].exc.push(item.value)
            }
          }
        }

        let parts = []
        for (let field in arrays) {

          let str = ''
          let array = arrays[field]
          if (array.inc && array.inc.length) {
            str += array.inc.join(',')
          }
          if (array.exc && array.exc.length) {
            str += '|'
            str += array.exc.join(',')
          }

          if (str) {
            parts.push(field + '=' + str)
          }
        }

        // base path
        let path = '/' + this.filterType

        // if has orderBy
        if (lister && lister.sort) {
          parts.push('sort=' + lister.sort)
        }

        // add page
        page = page ? page : 1
        page = Math.max(1, page)
        if (page > 1) {
          parts.push('page=' + page)
        }

        return path + (parts.length > 0 ? '?' + parts.join('&') : '')
      }, // end tree to params

      filterApplyChange: function () {
        let url = this.filterBuildUrl(1)
        window.location.href = url
      }, // end apply change
    }
  }
};
/*
styles: {
  type: 'multi',
  title: 'Styles',
  hasAll: true,
  hasCount: false,
  items: []
},
demogs: {
  type: 'multi',
  title: 'Demographic',
  hasAll: true,
  hasCount: true,
  items: []
},

stars: {
  type: 'radio',
  title: 'Stars',
  hasAll: true,
  hasCount: false,
  items: [{
    title: '5 Stars',
    value: '5',
    state: 0
  },
  {
    title: '4 Stars',
    value: '4',
    state: 0
  },
  {
    title: '3 Stars',
    value: '3',
    state: 0
  },
  {
    title: '2 Stars',
    value: '2',
    state: 0
  },
  {
    title: '1 Stars',
    value: '1',
    state: 0
  }
  ]
},
*/

/* -BLOCK- */

const VueModule_Default = function () {
  return {
    el: '#app',
    delimiters: ['${', '}'],
    mixins: [
      VueMixin_Global(),
      VueMixin_Notify(),
    ],
  };
};


/* -BLOCK- */

const VueModule_Home = function () {
  return {
    el: '#app',
    delimiters: ['${', '}'],
    mixins: [
      VueMixin_Global(),
      VueMixin_Notify(),
    ],
    data() {
      return {
        page: 1,
        loading: 0, // 0 normal, 1 loading, 2 no-more
      }
    },
    created() { },
    methods: {
      latestLoadMore() {
        if (this.loading != 0) {
          return;
        }
        const nextPage = this.page + 1;
        const data = {
          page: nextPage
        }
        this.loading = 1;
        axios.post('/ajax/home-latest-more', data)
          .then(resp => resp.data)
          .then((json) => {
            if (json.res.html) {
              const obj = document.getElementById('series-list');
              obj.innerHTML += json.res.html;
            }
            this.page = nextPage;
            this.loading = json.res.more ? 0 : 2;
          }).catch((err) => {
            this.loading = 0;
          })

        return;
      }
    },
  };
};


/* -BLOCK- */

const VueModule_Latest = function () {
  return {
    el: '#app',
    delimiters: ['${', '}'],
    mixins: [
      VueMixin_Global(),
      VueMixin_Notify(),
      VueMixin_Filter('latest'),
    ],
    data() {
      return {
        page: 1,
        limit: 36,
        loading: 0, // 0 normal, 1 loading, 2 no-more
      }
    },
    created() { },
    methods: {
      latestLoadMore() {
        if (this.loading != 0) {
          return;
        }

        const nextPage = this.page + 1;;
        const url = this.filterBuildUrl(nextPage);
        console.log('next url:', url);

        this.loading = 1;
        axios.get(url)
          .then((json) => {
            const data = json.data;
            if (data.res.html) {
              const obj = document.getElementById('series-list');
              obj.innerHTML += data.res.html;
            }
            this.page = nextPage;
            this.loading = data.res.more ? 0 : 2;
          }).catch((err) => {
            this.loading = 0;
          })

        return;
      }
    },
  };
};


/* -BLOCK- */

const VueModule_Browse = function () {
  return {
    el: '#app',
    delimiters: ['${', '}'],
    mixins: [
      VueMixin_Global(),
      VueMixin_Notify(),
      VueMixin_Filter('browse'),
    ],
    data() {
      return {}
    },
    created() { },
    methods: {},
  };
};


/* -BLOCK- */

const VueModule_Search = function () {
  return {
    el: '#app',
    delimiters: ['${', '}'],
    mixins: [
      VueMixin_Global(),
      VueMixin_Notify(),
    ],
    data() {
      return {}
    },
    created() { },
    methods: {},
  };
};


/* -BLOCK- */

const VueModule_Subject = function () {
  return {
    el: '#app',
    delimiters: ['${', '}'],
    mixins: [
      VueMixin_Global(),
      VueMixin_Notify(),
    ],
    data: function () {
      return {
        load: {
          favorite: false,
          favFolder: false, // if show the favorite folder change overlay
        },
        favFolders: [],
        favorite: null,
        newFavFolderId: null,
        history: null,

        modal_favorite: null,

        // new code ====
        follows: null,
        followed: null,
      }
    },
    created: function () { },
    mounted: function () {
      this.loadFavorite()
      this.loadHistory()
      const ele_modal_favorite = document.getElementById('modal-favorite');
      this.modal_favorite = new bootstrap.Modal(ele_modal_favorite);
      ele_modal_favorite.addEventListener('hidden.bs.modal', (e) => {
        this.load.favorite = false;
      })
    },
    methods: {
      loadHistory: function () {
        if (!_uid) {
          return
        }
        var that = this
        axios.get('/ajax/history-item?seriesId=' + subjectIid)
          .then((res) => {
            var data = res.data
            if (data.result) {
              that.history = data.result
            }
          })
          .catch((err) => {
            console.log(err)
          })
      },
      loadFavorite: function () {
        if (!_uid) {
          return
        }
        var that = this
        that.load.favorite = true
        axios.get('/ajax/favorite/one?seriesId=' + subjectIid)
          .then((res) => {
            var data = res.data
            if (data.result) {
              that.favorite = data.result
            }
            that.load.favorite = false
          })
          .catch((err) => {
            console.log(err)
            that.load.favorite = false
          })
      },
      onClickFavorite: function () {
        if (!_uid) {
          this._go_login()
          return
        }
        var that = this
        that.load.favorite = true
        axios.get('/ajax/favorite/one?withFolders=1&seriesId=' + subjectIid)
          .then((res) => {
            var data = res.data
            if (data.result) {
              that.favorite = data.result
              that.newFavFolderId = that.favorite.folderId
            }
            if (data.folders) {
              that.favFolders = data.folders
            }
            this.modal_favorite.show();
          })
          .catch((err) => {
            console.log(err)
            that.load.favorite = false
          })
      },
      favoriteFolderOnChange: function () {
        var that = this
        this.load.favFolder = true
        axios.post('/ajax/favorite/upsert', {
          seriesId: subjectIid,
          folderId: that.newFavFolderId,
        })
          .then((res) => {
            var data = res.data
            if (data.eno) {
              throw new Error(eno)
            }
            if (data.result) {
              that.favorite = data.result
            }
            that.load.favFolder = false
          })
          .catch((err) => {
            console.log(err)
            // if fail, restore the newFavFolderId to favorite.folderId
            that.newFavFolderId = that.favorite ? that.favorite.folderId : null
            that.load.favFolder = false
          })
      },
      favoriteFolderOnDelete: function () {
        var that = this
        this.load.favFolder = true
        axios.post('/ajax/favorite/delete', {
          seriesIds: subjectIid,
        })
          .then((res) => {
            var data = res.data
            if (data.eno) {
              throw new Error(eno)
            }
            if (data.result) {
              that.favorite = null
              that.newFavFolderId = null
            }
            that.load.favFolder = false
          })
          .catch((err) => {
            console.log(err)
            that.load.favFolder = false
          })
      },
    }
  }
};

/* -BLOCK- */


function manga_page_left_right(evt) {
  var e = evt ? evt : top.window.event;
  if (e.keyCode == 37 || e.keyCode == 188) {
    if (page) {
      if (page == 1) {
        if (prevEpi) {
          window.location.href = '/chapter/' + prevEpi.iid + '/1'
        } else {
          window.location.href = '/series/' + subjectIid
        }
      } else {
        window.location.href = '/chapter/' + episodeIid + '/' + (page - 1)
      }
    } else {
      if (prevEpi) {
        window.location.href = '/chapter/' + prevEpi.iid
      } else {
        window.location.href = '/series/' + subjectIid
      }
    }
  }
  if (e.keyCode == 39 || e.keyCode == 190) {
    if (page) {
      if (page == pages) {
        if (nextEpi) {
          window.location.href = '/chapter/' + nextEpi.iid + '/1'
        } else {
          window.location.href = '/series/' + subjectIid
        }
      } else {
        window.location.href = '/chapter/' + episodeIid + '/' + (page + 1)
      }
    } else {
      if (nextEpi) {
        window.location.href = '/chapter/' + nextEpi.iid
      } else {
        window.location.href = '/series/' + subjectIid
      }
    }
  }
}

const VueModule_Episode = function () {
  return {
    el: '#app',
    delimiters: ['${', '}'],
    mixins: [
      VueMixin_Global(),
      VueMixin_Notify(),
    ],
    data: function () {
      return {
        clientWidth: document.documentElement.clientWidth || document.body.clientWidth || window.innerWidth,
        clientHeight: window.innerHeight,
        fixedWidth: document.getElementById('container').clientWidth || 960,
        eiid: episodeIid,
        server: JSON.parse(CryptoJS.AES.decrypt(server, batojs).toString(CryptoJS.enc.Utf8)),
        images: images,
        pages: pages,
        page: page,
        load: 'a',
        zoom: 'f',
        items: [],
        loaded: 1, // Manually mode, current loaded

        report_loading: 0,
        report_chapterIid: episodeIid,
        report_reason: null,
        report_explanation: '',

        modal_report_chapter: null,
      }
    },
    created: function () { },
    mounted: function () {
      this.prepareData();
      window.addEventListener('resize', () => {
        this.prepareData()
      });
      document.onkeyup = manga_page_left_right;
    },
    methods: {

      prepareData: function () {
        this._readClient();
        this._parseItems();
      },

      _readClient: function () {

        this.clientWidth = document.documentElement.clientWidth || document.body.clientWidth || window.innerWidth;
        this.clientHeight = window.innerHeight;
        this.fixedWidth = document.getElementById('container').clientWidth || 960;

        // cookie
        let load;
        if (this.page) {
          load = 'o';
        } else {
          load = Cookies.get('read_load');
          if (['a', 'm'].indexOf(load) === -1) {
            load = 'a';
          }
        }
        this.load = load;

        let zoom;
        if (this.clientWidth <= 992) {
          // small screen always full width image
          zoom = 'f';
        } else {
          zoom = Cookies.get('read_zoom');
          if (['f', 'o', 'a'].indexOf(zoom) === -1) {
            zoom = 'o';
          }
        }
        this.zoom = zoom;
      },

      _parseItems: function () {
        this.items = [];
        if (this.load == 'o') {
          let page = this.page
          let name = this.images[page - 1];
          let item = this._parseImgSrc(page, name)
          this.items.push(item);

          this.preLoadNextImg(page)
          return
        }
        if (this.load == 'a') {
          for (let iidx in this.images) {
            iidx = Number(iidx);
            let page = iidx + 1;
            let name = this.images[iidx]
            let item = this._parseImgSrc(page, name)
            this.items.push(item)
          }
          return
        }
        if (this.load == 'm') {
          for (let iidx in this.images) {
            iidx = Number(iidx);
            let page = iidx + 1;
            let name = this.images[iidx];
            let item = this._parseImgSrc(page, name)
            this.items.push(item)
            if (page >= this.loaded) {
              break
            }
          }

          this.preLoadNextImg(this.loaded + 1)
          return
        }

      },
      _parseImgSrc: function (page, name) {
        const arr = String(name).split('/').pop().split('.').shift().split('_').map(i => Number(i));

        const imW = arr[0] > 1500000 ? Number(arr[1]) : Number(arr[2]);
        const imH = arr[0] > 1500000 ? Number(arr[2]) : Number(arr[3]);

        let toW = imW;
        let toH = imH;
        switch (this.zoom) {
          case 'o':
            // original width
            toW = imW;
            toH = imH;
            break;

          case 'a':
            // 600 <= w <= screen width - 60
            toW = imW;
            toW = Math.min(toW, this.clientWidth - 60);
            toW = Math.max(toW, 600);
            toH = Number(toW * imH / imW);
            break;

          case 'f':
          default:
            // fixed width
            toW = this.fixedWidth;
            toH = Number(toW * imH / imW);
            break;
        }

        const item = {
          page: Number(page),
          src: `${this.server}${name}`,
          ow: imW,
          oh: imH,
          tw: toW,
          th: toH,
        }
        return item
      },
      changeChap: function () {
        let url = '/chapter/' + this.eiid;
        if (this.page) {
          url += '/1';
        }
        window.location.href = url;
      },
      changePage: function () {
        let url = '/chapter/' + episodeIid + '/' + this.page;
        window.location.href = url
      },
      changeLoad: function () {
        console.log('this.laod:', this.load);
        Cookies.set('read_load', this.load, {
          expires: 365 * 100,
          path: '/',
          domain: '.' + _cfg.host
        });

        var url
        if (this.load == 'o') {
          url = '/chapter/' + episodeIid + '/1';
        } else {
          url = '/chapter/' + episodeIid;
        }
        window.location.href = url;
      },
      changeZoom: function () {
        console.log('this.zoom:', this.zoom);
        Cookies.set('read_zoom', this.zoom, {
          expires: 365 * 100,
          path: '/',
          domain: '.' + _cfg.host
        })
        this.prepareData();
      },

      loadMore: function (num) {
        if (this.loaded >= this.pages) {
          return
        }
        if (num == 'a') {
          this.loaded = this.pages;
          this.prepareData()
          return
        }
        this.loaded = Math.min(this.loaded + num, pages)
        this.prepareData()
      },
      onClickImg: function (page) {
        console.log('clicked page: ' + page)
        switch (this.load) {
          case 'o':
            this.goNextPage()
            break
          case 'm':
            if (page == this.loaded) {
              this.loadMore(1)
            }
            this.scrollDown()
            break
          case 'a':
            this.scrollDown()
            break
        }
      },
      preLoadNextImg: function (next) {
        try {
          if (this.images[next]) {
            const o_img = new Image()
            o_img.src = `${this.server}${this.images[next]}`;
          }
        } catch (error) {
          console.log(error);
        }
      },
      goNextPage: function () {
        if (page) {
          if (page == pages) {
            if (nextEpi) {
              window.location.href = '/chapter/' + nextEpi.iid + '/1'
            } else {
              window.location.href = '/series/' + subjectIid
            }
          } else {
            window.location.href = '/chapter/' + episodeIid + '/' + (page + 1)
          }
        } else {
          if (nextEpi) {
            window.location.href = '/chapter/' + nextEpi.iid
          } else {
            window.location.href = '/series/' + subjectIid
          }
        }
      },
      scrollDown: function () {
        const win_h = this.clientHeight;
        if (win_h) {
          window.scrollBy({
            top: win_h * 0.8,
            left: 0,
            behavior: 'smooth'
          });
        }
      },
      onKeyupLeft: function () {
        console.log('left')
      },
      onKeyupRight: function () {
        console.log('right')
      },

      /* ===== reports ===== */
      report_toggle() {
        if (!this.modal_report_chapter) {
          this.modal_report_chapter = new bootstrap.Modal(document.getElementById('modal_report_chapter'));
        }
        this.modal_report_chapter.toggle();
      },
      report_submit() {
        this.report_loading = 1;

        const data = {
          chapterIid: this.report_chapterIid,
          reason: this.report_reason,
          explanation: this.report_explanation,
        };
        axios.post('/ajax/report-chapter', data)
          .then((resp) => resp.data)
          .then((json) => {
            switch (json.eno) {
              case 1001:
                alert('Unknown Error 1.');
                break

              case 1002:
                alert('Explanation required for "Other" reason.');
                break

              case 0:
                alert('Report submited!');
                this.modal_report_chapter.hide();
                break;

              default:
                alert('Unknown Error 2.');
                break;
            }

            this.report_loading = 0;
          })
          .catch((err) => {
            console.log(err)
            alert('Unknown Error 3.');
            this.report_loading = 1;
          });
      },
    },// end methods
  }
}


/* -BLOCK- */

const VueModule_Settings = function () {
  return {
    el: '#app',
    delimiters: ['${', '}'],
    mixins: [
      VueMixin_Global(),
      VueMixin_Notify(),
    ],
    data() {
      return {
        loading: 0,
        disabled: _uid ? false : true,
        site_theme: settingsDef && settingsDef.site_theme ? settingsDef.site_theme : null,
        block_genres: settingsDef && settingsDef.block_genres ? settingsDef.block_genres : [],
        filter_langs: settingsDef && settingsDef.filter_langs ? settingsDef.filter_langs : [],
      }
    },
    mounted() {
      console.log('site_theme', this.site_theme);
      console.log('block_genres', this.block_genres);
      console.log('filter_langs', this.filter_langs);
    },
    methods: {
      submit() {
        const data = {
          site_theme: this.site_theme,
          block_genres: this.block_genres,
          filter_langs: this.filter_langs,
        }

        this.loading = 1;
        axios.post('/ajax/save-settings', data)
          .then((json) => {
            const data = json.data;
            if (handle_defined_error(data.eno)) {
              this.loading = 0;
              return
            }
            switch (data.eno) {
              default:
                notify_b({
                  type: 'success',
                  text: 'Settings saved successfully!',
                });
                break;
            }
            this.loading = 0;
          })
          .catch((error) => {
            notify_b({
              type: 'danger',
              text: 'Failed to save the settings, unknown errors.',
            })
            this.loading = 0;
            console.log(error);
          });
      },
    },
  };
};
