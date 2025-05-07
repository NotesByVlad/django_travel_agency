document.addEventListener('DOMContentLoaded', function () {
    const swiperContainers = document.querySelectorAll('.swiper-container');

    swiperContainers.forEach(container => {
        new Swiper(container, {
            loop: true,
            slidesPerView: 1,
            spaceBetween: 0,
            autoplay: {
                delay: 3000,
                disableOnInteraction: false,
            },
            pagination: {
                el: container.querySelector('.swiper-pagination'),
                clickable: true,
            },
            navigation: {
                nextEl: container.querySelector('.swiper-button-next'),
                prevEl: container.querySelector('.swiper-button-prev'),
            },
        });
    });
});