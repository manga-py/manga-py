
((d) => {
    d.addEventListener('DOMContentLoaded', () => {
        if(typeof repoUrl == 'undefined')
        {
            return;
        }
        fetch(repoUrl)
            .then(response => response.json())
            .then((response) => {
                const links = d.querySelector('#download-links');
                const tar = links.querySelector('.tar');
                const zip = links.querySelector('.zip');

                tar.setAttribute('href', response.tarball_url);
                tar.setAttribute('active', 'true');
                zip.setAttribute('href', response.zipball_url);
                zip.setAttribute('active', 'true');
            });
        const ul = d.querySelector('#supported-list');
        if(!ul)
        {
            return;
        }
        fetch('./providers.json')
            .then(response => response.json())
            .then((list) => {
                let html = '', m = 0, done = 0;
                for(let i in list) {
                    if (!list.hasOwnProperty(i)) continue;
                    m+=1;
                    html += '<li><input id="I' + m + '" type="checkbox" ' +
                        (list[i][1] ? 'checked="" ' : '') +
                        'disabled=""><label for="I' + m + '"></label><span>' +
                        '<a target="_blank" href="' +
                        list[i][0] + '">' +
                        list[i][0] + '</a> ' +
                        list[i][2] + '</span></li>';
                    done += parseInt(list[i][1]);
                }
                ul.innerHTML = html + ('<!-- ' + list.length + ' ( ' + done + ' ) -->');
            });
    });
})(document);
