 // Знаходимо всі блоки "galery-change"
 const galleries = document.querySelectorAll('.galery-change');

 // Проходимо по кожному блоку
 galleries.forEach((gallery) => {
   const beforeImage = gallery.querySelector('.before');
   const afterImage = gallery.querySelector('.after');

    setInterval(() => {
      // Перемикання видимості
      if (beforeImage.style.opacity === '0') {
        beforeImage.style.opacity = '1'; // Показати "до"
        afterImage.style.opacity = '0'; // Приховати "після"
      } else {
        beforeImage.style.opacity = '0'; // Приховати "до"
        afterImage.style.opacity = '1'; // Показати "після"
      }
    }, 3000); // Інтервал зміни 3 секунди
});
