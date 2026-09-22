// Відкрити форму
const openButton = document.getElementById('openFormBtn');
if (openButton) {
    openButton.addEventListener('click', function () { 
        const formContainer = document.getElementById('formWraper');
        if (formContainer) {
            formContainer.style.display = 'flex';
        }
    });
}

// Закрити форму
const closeButton = document.getElementById('closeZapisForm');
if (closeButton) {
    closeButton.addEventListener('click', function () {
        const formContainer = document.getElementById('formWraper');
        if (formContainer) {
            formContainer.style.display = 'none';
        }
    });
}

// Відкрити форму "Записатись" для кожної кнопки
document.querySelectorAll('.services-button-signUpForm').forEach(button => {
    button.addEventListener('click', function () {
        const formContainer = document.getElementById('formWraper');
        if (formContainer) formContainer.style.display = 'flex';
    });
});

// Очистити форму після відправлення
const submitButton = document.getElementById('submitZapisBtn');
if (submitButton) {
    submitButton.addEventListener('click', function () {
        const form = document.getElementById('zapisForm');
        if (form) {
            form.reset();
        }
    });
}

