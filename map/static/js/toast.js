var toasts = document.querySelectorAll('.custom-toast');
var startTop = 100;

toasts.forEach(function(toast, index) {
  var top = startTop;

  for (var i = 0; i < index; i++) {
    top += toasts[i].offsetHeight + 20;
  }

  toast.style.top = top + 'px';

  var closeButton = toast.querySelector('.close-button');
  var progressBar = toast.querySelector('.toast-progress-bar');

  if (closeButton && progressBar) {
    closeButton.addEventListener('click', function() {
      toast.classList.add('slideOut');
    });

    toast.classList.add('slideIn');
    toast.style.display = 'block';

    toast.addEventListener('animationend', function(event) {
      if (event.animationName === 'slideIn') {
        progressBar.style.width = '100%';

        var timeLeft = 5000;
        var interval = setInterval(function() {
          var isPaused = toast.classList.contains('pause');
          if (!isPaused) {
            timeLeft -= 10;
            var newWidth = (timeLeft / 5000) * 100;
            progressBar.style.width = newWidth + '%';
          }

          if (timeLeft <= 0) {
            clearInterval(interval);
            toast.classList.add('slideOut');
          }
        }, 10);

        var isPaused = false;
        toast.addEventListener('mouseover', function() {
          toast.classList.add('pause');
        });
        toast.addEventListener('mouseout', function() {
          toast.classList.remove('pause');
        });
      }
    });
  }
});