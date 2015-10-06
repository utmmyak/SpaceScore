$(document).ready(function() {
            /*$('.noscore').tooltipster({
                content: $('<span>We do not have enough data on this official to form an editorial opinion on his space preferences.</span>'),
                maxWidth: 350,
                interactive: true,
                iconDesktop: true,
                icon: '?',
                position: 'bottom',
            });
            $('#scorehsf').tooltipster({
                content: $('<span>The Human Spaceflight Score reflects our editorial opinion of how closely this official aligns with the needs of human spaceflight as outlined <a href="/methodology.html#hsf">here</a>.</span>'),
                maxWidth: 350,
                interactive: true,
                iconDesktop: true,
                icon: '?',
                position: 'bottom-right',
            });
            $('#scoreusf').tooltipster({
                content: $('<span>The Unmanned Spaceflight Score reflects our editorial opinion of how closely this official aligns with the needs of unmanned spaceflight as outlined <a href="/methodology.html#usf">here</a>.</span>'),
                maxWidth: 350,
                interactive: true,
                iconDesktop: true,
                icon: '?',
                iconTheme: 'tooltipster-icon right-tooltip',
                position: 'right'
            });
            $('#scorenat').tooltipster({
                content: $('<span>The Nationalization Spaceflight Score reflects our editorial opinion of how closely this official aligns with the needs of government operated spaceflight as outlined <a href="/methodology.html#nat">here</a>.</span>'),
                maxWidth: 350,
                interactive: true,
                iconDesktop: true,
                icon: '?',
                position: 'bottom-right',
            });*/
            $('#private-tooltip').tooltipster({
                content: $('<span>The Privatization Spaceflight Score reflects our editorial opinion of how closely this official aligns with the needs of privately operated spaceflight as outlined <a href="/methodology.html#priv">here</a>.</span>'),
                maxWidth: 350,
                interactive: true,
                iconDesktop: true,
                icon: ' ',
                iconTheme: 'tooltipster-icon private invisible-tooltip',
                position: 'bottom-right',
            });
            $('#public-tooltip').tooltipster({
                content: $('<span>The Privatization Spaceflight Score reflects our editorial opinion of how closely this official aligns with the needs of privately operated spaceflight as outlined <a href="/methodology.html#priv">here</a>.</span>'),
                maxWidth: 350,
                interactive: true,
                iconDesktop: true,
                icon: ' ',
                iconTheme: 'tooltipster-icon public invisible-tooltip',
                position: 'bottom-right',
            });
            $('#unmanned-tooltip').tooltipster({
                content: $('<span>The Privatization Spaceflight Score reflects our editorial opinion of how closely this official aligns with the needs of privately operated spaceflight as outlined <a href="/methodology.html#priv">here</a>.</span>'),
                maxWidth: 350,
                interactive: true,
                iconDesktop: true,
                icon: ' ',
                iconTheme: 'tooltipster-icon unmanned invisible-tooltip',
                position: 'bottom',
            });
            $('#human-tooltip').tooltipster({
                content: $('<span>The Privatization Spaceflight Score reflects our editorial opinion of how closely this official aligns with the needs of privately operated spaceflight as outlined <a href="/methodology.html#priv">here</a>.</span>'),
                maxWidth: 350,
                interactive: true,
                iconDesktop: true,
                icon: ' ',
                iconTheme: 'tooltipster-icon human invisible-tooltip',
                position: 'bottom',
            });
            $('#basescore-display').tooltipster({
                content: $('<span>The Base Score reflects our editorial opinion of how closely this official aligns with the needs of space in general as outlined <a href="/methodology.html#base">here</a>.</span>'),
                maxWidth: 350,
                interactive: true,
                iconDesktop: true,
                icon: '?',
                iconTheme: 'tooltipster-icon basescore-tooltip',
                position: 'bottom',
            });
        });