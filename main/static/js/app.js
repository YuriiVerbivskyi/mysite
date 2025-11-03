'use strict';

document.addEventListener('DOMContentLoaded', function() {
    console.log('E-Queue loaded');

    const navLinks = document.querySelectorAll('.nav-link');
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            const url = this.getAttribute('href');
            if (url && url !== '/') {
                console.log('Navigating to:', url);
            }
        });
    });
});
