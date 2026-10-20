"use strict";
const assert = require("node:assert/strict");
const fs = require("node:fs");
const vm = require("node:vm");
const path = require("node:path");

const app = fs.readFileSync(path.join(__dirname, "../assets/site.js"), "utf8");
let valid = true;
let submit;
let prefill;
const fields = {
  "full-name": { value: "A Customer" },
  email: { value: "" },
  service: {
    value: "",
    options: [
      { value: "Software development" },
      { value: "AI & automation" },
      { value: "Training & academy" },
      { value: "Other enquiry" }
    ]
  },
  stage: { value: "Existing system" },
  budget: { value: "Prefer to discuss" },
  message: { value: "Our ordering workflow needs a better mobile system." },
  "form-feedback": { textContent: "" },
  "copyright-year": { textContent: "" },
  "enquiry-form": {
    reportValidity: () => valid,
    addEventListener: (event, cb) => {
      if (event === "submit") submit = cb;
    }
  }
};
const quickLink = {
  getAttribute: (name) => name === "data-enquiry-service" ? "Software development" : null,
  addEventListener: (event, cb) => {
    if (event === "click") prefill = cb;
  }
};
const document = {
  getElementById: (id) => fields[id] || null,
  querySelector: () => null,
  querySelectorAll: (selector) => selector === "a[data-enquiry-service]" ? [quickLink] : []
};
const win = { location: { href: "" } };
vm.runInNewContext(app, { document, window: win });

assert.equal(typeof submit, "function");
assert.equal(typeof prefill, "function");
prefill();
assert.equal(fields.service.value, "Software development");
assert.equal(fields["copyright-year"].textContent, String(new Date().getFullYear()));

function fire(channel) {
  let prevented = false;
  submit({
    preventDefault: () => { prevented = true; },
    submitter: { dataset: { channel } }
  });
  assert(prevented);
}

fire("whatsapp");
assert(win.location.href.startsWith("https://wa.me/2349039930006?text="));
let content = new URL(win.location.href).searchParams.get("text");
for (const token of ["A Customer", "Not provided", "Software development", "Existing system", "Prefer to discuss", "ordering workflow"]) {
  assert(content.includes(token), "missing field in WhatsApp message: " + token);
}
assert(fields["form-feedback"].textContent.includes("Nothing has been sent yet"));

fields.email.value = "customer@example.com";
fire("email");
assert(win.location.href.startsWith("mailto:silabtechnologies@gmail.com?"));
const url = new URL(win.location.href);
assert(url.searchParams.get("subject").includes("Software development"));
assert(url.searchParams.get("body").includes("customer@example.com"));
assert(fields["form-feedback"].textContent.includes("Nothing has been sent yet"));

valid = false;
win.location.href = "unchanged";
fire("whatsapp");
assert.equal(win.location.href, "unchanged");
console.log("PASS: preselected offers, encoded WhatsApp and email, validity, consent to send");
