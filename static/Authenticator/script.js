document.addEventListener('DOMContentLoaded', () => {
    // Smooth scroll for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            document.querySelector(this.getAttribute('href')).scrollIntoView({
                behavior: 'smooth'
            });
        });
    });

    // Add a typing effect to the welcome message
    const welcomeText = document.querySelector('.text h3');
    if (welcomeText) {
        const text = welcomeText.innerText;
        welcomeText.innerHTML = '';
        let i = 0;
        const typingEffect = setInterval(() => {
            if (i < text.length) {
                welcomeText.innerHTML += text.charAt(i);
                i++;
            } else {
                clearInterval(typingEffect);
            }
        }, 50);
    }

    // Handle resizing
    window.addEventListener('resize', () => {
        document.querySelectorAll('.box').forEach(box => {
            if (window.innerWidth < 768) {
                box.style.maxWidth = '100%';
            } else {
                box.style.maxWidth = '400px';
            }
        });
    });
});
