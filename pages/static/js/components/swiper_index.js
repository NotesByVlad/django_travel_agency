document.addEventListener('DOMContentLoaded', function () {
    const swiperContainers = document.querySelectorAll('.swiper-container');
    
    swiperContainers.forEach(container => {
        const swiper = new Swiper(container, {
            loop: true,
            pagination: {
                el: '.swiper-pagination',
                clickable: true,
            },
            navigation: {
                nextEl: '.swiper-button-next',
                prevEl: '.swiper-button-prev',
            },
            slidesPerView: 1,
            spaceBetween: 10,
            breakpoints: {
                850: {
                    slidesPerView: 2,
                    spaceBetween: 10,
                },
                1200: {
                    slidesPerView: 3,
                    spaceBetween: 10,
                },
            },
        });
    });
});