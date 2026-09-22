// Вибір елементів DOM
const reviewForm = document.getElementById('reviewForm');
const reviewsList = document.getElementById('reviewsList');
const prevBtn = document.querySelector('.prev-btn');
const nextBtn = document.querySelector('.next-btn');

// Масив для зберігання відгуків
const reviews = Array.from(reviewsList.children);
let currentReviewIndex = 0;

// Функція для оновлення видимого відгуку
function updateVisibleReview() {
    reviews.forEach((review, index) => {
        review.style.display = index === currentReviewIndex ? 'block' : 'none';
    });
}

// Ініціалізація першого відгуку
updateVisibleReview();

// Подія на стрілку "Назад"
prevBtn.addEventListener('click', () => {
    currentReviewIndex = (currentReviewIndex - 1 + reviews.length) % reviews.length;
    updateVisibleReview();
});

// Подія на стрілку "Вперед"
nextBtn.addEventListener('click', () => {
    currentReviewIndex = (currentReviewIndex + 1) % reviews.length;
    updateVisibleReview();
});

// Обробка подання форми
reviewForm.addEventListener('submit', (event) => {
    event.preventDefault(); // Запобігаємо перезавантаженню сторінки

    // Отримуємо значення з форми
    const name = document.getElementById('name').value.trim();
    const message = document.getElementById('message').value.trim();

    if (name && message) {
        // Створюємо новий відгук
        const newReview = document.createElement('li');
        newReview.classList.add('review-item');
        newReview.innerHTML = `<h3>${name}</h3><p>${message}</p>`;

        // Додаємо новий відгук до списку
        reviewsList.appendChild(newReview);
        reviews.push(newReview);

        // Очищаємо форму
        reviewForm.reset();

        // Оновлюємо відображення
        currentReviewIndex = reviews.length - 1; // Показуємо новий відгук
        updateVisibleReview();
    }
});
