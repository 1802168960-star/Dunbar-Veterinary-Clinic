/* English validation bubbles for the clinic's forms.
 *
 * The browser's own validation messages follow the language of the browser
 * that happens to open the page, and the clinic's copy is English. Forms mark
 * each required field with a "data-error" attribute and this script puts that
 * text into the bubble instead of the browser's own wording.
 */
(function () {
  "use strict";

  document.addEventListener(
    "invalid",
    function (event) {
      var field = event.target;
      if (field.dataset && field.dataset.error && field.validity.valueMissing) {
        field.setCustomValidity(field.dataset.error);
      }
    },
    true
  );

  ["input", "change"].forEach(function (name) {
    document.addEventListener(
      name,
      function (event) {
        var field = event.target;
        if (field.setCustomValidity) {
          field.setCustomValidity("");
        }
      },
      true
    );
  });
})();
