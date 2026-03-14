$(document).ready(function () {

  /* =========================================
     1. Navbar Active Link Highlighting
     ========================================= */
  var path = window.location.pathname;
  $('.navbar-nav .nav-link').each(function () {
    var href = $(this).attr('href');
    if (href && path === href) {
      $(this).addClass('active');
    } else if (href && href !== '/' && path.startsWith(href)) {
      $(this).addClass('active');
    }
  });


  /* =========================================
     2. Post Ride Form Validation (#postRideForm)
     ========================================= */
  $('#postRideForm').on('submit', function (e) {
    e.preventDefault();
    clearErrors('#postRideForm');

    var isValid = true;
    var emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    var today = new Date().toISOString().split('T')[0];

    // Driver Name
    var driverName = $.trim($('#driver_name').val());
    if (!driverName) {
      showError('driver_name', 'Driver name is required.');
      isValid = false;
    }

    // Driver Email
    var driverEmail = $.trim($('#driver_email').val());
    if (!driverEmail) {
      showError('driver_email', 'Driver email is required.');
      isValid = false;
    } else if (!emailRegex.test(driverEmail)) {
      showError('driver_email', 'Please enter a valid email address.');
      isValid = false;
    }

    // From Location
    var fromLoc = $.trim($('#from_location').val());
    if (!fromLoc) {
      showError('from_location', 'From location is required.');
      isValid = false;
    }

    // To Location
    var toLoc = $.trim($('#to_location').val());
    if (!toLoc) {
      showError('to_location', 'To location is required.');
      isValid = false;
    } else if (fromLoc && toLoc.toLowerCase() === fromLoc.toLowerCase()) {
      showError('to_location', 'From and To cannot be the same location.');
      isValid = false;
    }

    // Ride Date
    var rideDate = $('#ride_date').val();
    if (!rideDate) {
      showError('ride_date', 'Ride date is required.');
      isValid = false;
    } else if (rideDate < today) {
      showError('ride_date', 'Ride date must be today or in the future.');
      isValid = false;
    }

    // Ride Time
    var rideTime = $('#ride_time').val();
    if (!rideTime) {
      showError('ride_time', 'Ride time is required.');
      isValid = false;
    }

    // Seats
    var seats = parseInt($('#seats_available').val());
    if (isNaN(seats) || seats < 1 || seats > 8) {
      showError('seats_available', 'Seats must be between 1 and 8.');
      isValid = false;
    }

    // Price
    var price = parseFloat($('#price_per_seat').val());
    if (isNaN(price) || price < 0) {
      showError('price_per_seat', 'Price must be 0 or more.');
      isValid = false;
    }

    if (isValid) {
      this.submit();
    }
  });


  /* =========================================
     3. Request Ride Form Validation (#requestRideForm)
     ========================================= */
  $('#requestRideForm').on('submit', function (e) {
    e.preventDefault();
    clearErrors('#requestRideForm');

    var isValid = true;
    var emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    // Passenger Name
    var pName = $.trim($('#passenger_name').val());
    if (!pName) {
      showError('passenger_name', 'Your name is required.');
      isValid = false;
    }

    // Passenger Email
    var pEmail = $.trim($('#passenger_email').val());
    if (!pEmail) {
      showError('passenger_email', 'Your email is required.');
      isValid = false;
    } else if (!emailRegex.test(pEmail)) {
      showError('passenger_email', 'Please enter a valid email address.');
      isValid = false;
    }

    // Seats Requested
    var seatsReq = parseInt($('#seats_requested').val());
    if (isNaN(seatsReq) || seatsReq < 1) {
      showError('seats_requested', 'Please request at least 1 seat.');
      isValid = false;
    }

    if (isValid) {
      // Show spinner
      $('#requestSeatBtn .btn-text').addClass('d-none');
      $('#reqSpinner').removeClass('d-none');
      $('#requestSeatBtn').prop('disabled', true);
      this.submit();
    }
  });


  /* =========================================
     4. Search Date Auto-Submit
     ========================================= */
  $('input[data-auto-submit="true"]').on('change', function () {
    $(this).closest('form').submit();
  });


  /* =========================================
     5. Seat Availability Warning
     ========================================= */
  var seatBadge = $('.seat-badge[data-seats]').first();
  if (seatBadge.length) {
    var seats = parseInt(seatBadge.data('seats'));
    if (seats > 0 && seats <= 2) {
      $('#seatCount').text(seats);
      $('#seatWarning').removeClass('d-none');
    }
  }


  /* =========================================
     6. Set min date for all date inputs
     ========================================= */
  var today = new Date().toISOString().split('T')[0];
  $('input[type="date"]').attr('min', today);

}); // end ready


/* ---------- Helpers ---------- */
function showError(fieldId, message) {
  $('#' + fieldId).addClass('field-error');
  $('#err-' + fieldId).text(message);
}

function clearErrors(formSelector) {
  $(formSelector + ' .form-control').removeClass('field-error');
  $(formSelector + ' .error-msg').text('');
}
