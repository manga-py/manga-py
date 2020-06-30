
((d) => {
    d.addEventListener('DOMContentLoaded', () => {
        /** global: repoUrl */
        if(typeof repoUrl == 'undefined')
        {
            // example: https://api.github.com/repos/manga-py/manga-py/releases/latest
            // example: https://api.github.com/repos/yuru-yuri/manga-py/releases/latest
            return;
        }

        fetch(repoUrl)
            .then(r => r.json())
            .then((r) => {
                const links = d.querySelector('#download-links');
                const tar = links.querySelector('.tar');
                const zip = links.querySelector('.zip');

                tar.setAttribute('href', r.tarball_url);
                tar.setAttribute('active', 'true');
                zip.setAttribute('href', r.zipball_url);
                zip.setAttribute('active', 'true');
            });

        const ul = d.querySelector('#supported-list');

        if(!ul)
        {
            return;
        }

        fetch('/manga-py/providers.json')
            .then(r => r.json())
            .then((r) => {
                let html = '', m = 0, done = 0;
                const sites = [];
                for(let i in r) {
                    if (!r.hasOwnProperty(i)) continue;
                    m+=1;
                    html += '<li><input id="I' + m + '" type="checkbox" ' +
                        (r[i][1] ? 'checked="" ' : '') +
                        'disabled=""><label for="I' + m + '"></label><span>' +
                        '<a target="_blank" href="' +
                        r[i][0] + '">' +
                        r[i][0] + '</a> ' +
                        r[i][2] + '</span></li>';
                    done += r[i][1] ? 1 : 0;
                    r[i][1] && sites.push(r[i][0]);
                }

                ul.innerHTML = ('<!-- ' + r.length + ' ( ' + done + ' ) -->') + html;

                const sitesLen = sites.length;
                const buttonElement = document.querySelector('#random-site');

                const lastSiteWrapper = document.querySelector('#last-site');
                const lastSiteLink = document.querySelector('#last-site > a');

                buttonElement.setAttribute('target', '_blank');

                buttonElement.addEventListener('click', () => {

                    const idx = parseInt(Math.random() * sitesLen);

                    buttonElement.setAttribute('href', sites[idx]);

                    lastSiteLink.setAttribute('href', sites[idx]);
                    lastSiteWrapper.style.display = null;

                    return true;
                });
            });
    });
})(document);
