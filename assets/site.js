"use strict";
(function () {
  var nav = document.getElementById("primary-nav");
  var toggle = document.querySelector(".menu-toggle");
  if (nav && toggle) {
    function closeMenu() {
      nav.classList.remove("is-open");
      toggle.setAttribute("aria-expanded", "false");
      toggle.setAttribute("aria-label", "Open navigation");
    }
    toggle.addEventListener("click", function () {
      var open = toggle.getAttribute("aria-expanded") === "true";
      if (open) { closeMenu(); } else {
        nav.classList.add("is-open");
        toggle.setAttribute("aria-expanded", "true");
        toggle.setAttribute("aria-label", "Close navigation");
      }
    });
    nav.querySelectorAll("a").forEach(function (link) { link.addEventListener("click", closeMenu); });
    document.addEventListener("keydown", function (event) {
      if (event.key === "Escape") { closeMenu(); }
    });
    document.addEventListener("click", function (event) {
      if (!nav.contains(event.target) && !toggle.contains(event.target)) { closeMenu(); }
    });
  }

  var year = document.getElementById("copyright-year");
  if (year) { year.textContent = String(new Date().getFullYear()); }

  var form = document.getElementById("enquiry-form");
  var feedback = document.getElementById("form-feedback");
  if (form) {
    form.addEventListener("submit", function (event) {
      event.preventDefault();
      if (!form.reportValidity()) { return; }
      var name = document.getElementById("full-name").value.trim();
      var email = document.getElementById("email").value.trim();
      var service = document.getElementById("service").value;
      var message = document.getElementById("message").value.trim();
      var subject = "Silabs enquiry: " + service;
      var body = "Name: " + name + "\nEmail: " + email + "\nService: " + service +
        "\n\nProject details:\n" + message;
      var href = "mailto:silabtechnologies@gmail.com?subject=" +
        encodeURIComponent(subject) + "&body=" + encodeURIComponent(body);
      if (feedback) { feedback.textContent = "Your email app should open now. Review the draft and press Send there to complete your enquiry."; }
      window.location.href = href;
    });
  }
}());
