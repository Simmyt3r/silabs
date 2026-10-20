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
      if (open) { closeMenu(); return; }
      nav.classList.add("is-open");
      toggle.setAttribute("aria-expanded", "true");
      toggle.setAttribute("aria-label", "Close navigation");
    });
    nav.querySelectorAll("a").forEach(function (link) {
      link.addEventListener("click", closeMenu);
    });
    document.addEventListener("keydown", function (event) {
      if (event.key === "Escape") { closeMenu(); }
    });
    document.addEventListener("click", function (event) {
      if (!nav.contains(event.target) && !toggle.contains(event.target)) {
        closeMenu();
      }
    });
  }

  var year = document.getElementById("copyright-year");
  if (year) { year.textContent = String(new Date().getFullYear()); }

  var form = document.getElementById("enquiry-form");
  var feedback = document.getElementById("form-feedback");
  var serviceSelect = document.getElementById("service");
  document.querySelectorAll("a[data-enquiry-service]").forEach(function (link) {
    link.addEventListener("click", function () {
      if (!serviceSelect) { return; }
      var selected = link.getAttribute("data-enquiry-service");
      var exists = Array.prototype.some.call(serviceSelect.options, function (option) {
        return option.value === selected;
      });
      if (exists) { serviceSelect.value = selected; }
    });
  });

  if (!form) { return; }
  form.addEventListener("submit", function (event) {
    event.preventDefault();
    if (!form.reportValidity()) { return; }

    var name = document.getElementById("full-name").value.trim();
    var email = document.getElementById("email").value.trim();
    var service = serviceSelect.value;
    var stage = document.getElementById("stage").value || "Not specified";
    var budget = document.getElementById("budget").value || "Not specified";
    var message = document.getElementById("message").value.trim();
    if (!name || !message || !service) { return; }

    var body = "Hello Silabs And Co Technologies Ltd,\n\n" +
      "Name: " + name + "\n" +
      "Email: " + (email || "Not provided") + "\n" +
      "Service: " + service + "\n" +
      "Project stage: " + stage + "\n" +
      "Budget range: " + budget + "\n\n" +
      "Project needs:\n" + message;

    var channel = event.submitter && event.submitter.dataset.channel === "email" ? "email" : "whatsapp";
    if (channel === "email") {
      var subject = "Project enquiry: " + service;
      if (feedback) { feedback.textContent = "Your email app should open with a draft. Review it and press Send there. Nothing has been sent yet."; }
      window.location.href = "mailto:silabtechnologies@gmail.com?subject=" +
        encodeURIComponent(subject) + "&body=" + encodeURIComponent(body);
    } else {
      if (feedback) { feedback.textContent = "WhatsApp should open with a prepared message. Press Send in WhatsApp to complete the enquiry. Nothing has been sent yet."; }
      window.location.href = "https://wa.me/2349039930006?text=" + encodeURIComponent(body);
    }
  });
}());
