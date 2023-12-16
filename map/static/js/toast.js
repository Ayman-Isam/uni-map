var toast = document.querySelector('.custom-toast');
var closeButton = document.querySelector('.close-button');
var progressBar = toast ? toast.querySelector('.toast-progress-bar') : null;

if (toast && closeButton && progressBar) {
    // Add a click event listener to the close button
  closeButton.addEventListener('click', function() {
    // Start the slideOut animation when the close button is clicked
    toast.classList.add('slideOut');
  });

  // Show the toast for 5 seconds
  toast.classList.add('slideIn');
  toast.style.display = 'block';

  // Add an animationend event listener to the toast
  toast.addEventListener('animationend', function(event) {
    // Check if the animation that ended is the slideIn animation
    if (event.animationName === 'slideIn') {
      // Start the countdown after the slideIn animation ends

      // Set the width of the progress bar to 100%
      progressBar.style.width = '100%';

  // Reduce the width of the progress bar over time
    var timeLeft = 5000; // 5 seconds
    var interval = setInterval(function() {
      if (!isPaused) { // Only reduce time left if not paused
        // Reduce the time left
        timeLeft -= 10; // Reduce by 10ms each time

        // Calculate the new width of the progress bar
        var newWidth = (timeLeft / 5000) * 100; // As a percentage of the total time

        // Update the width of the progress bar
        progressBar.style.width = newWidth + '%';
      }

      // If all time has passed, clear the interval and start slideOut animation
      if (timeLeft <= 0) {
        clearInterval(interval);
        toast.classList.add('slideOut');
      }
    }, 10); // Run every 10m

      // Add mouseover and mouseout event listeners to pause and resume countdown
      var isPaused = false;
      toast.addEventListener('mouseover', function() {
        isPaused = true;
      });
      toast.addEventListener('mouseout', function() {
        isPaused = false;
      });
    }
  });
}

