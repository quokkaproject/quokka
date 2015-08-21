

// function slugify(text)
// {
//   return text.toString().toLowerCase()
//     .replace(/\s+/g, '-')           // Replace spaces with -
//     .replace(/[^\w\-]+/g, '')       // Remove all non-word chars
//     .replace(/\-\-+/g, '-')         // Replace multiple - with single -
//     .replace(/^-+/, '')             // Trim - from start of text
//     .replace(/-+$/, '');            // Trim - from end of text
// }


var keys = keys || function (o) { var a = []; for (var k in o) a.push(k); return a; };

var slugify = function (string) {
 var accents = "ãàáäâèéëêìíïîõòóöôùúüûñç";
  // var accents = "\u00e0\u00e1\u00e4\u00e2\u00e8"
  //   + "\u00e9\u00eb\u00ea\u00ec\u00ed\u00ef"
  //   + "\u00ee\u00f2\u00f3\u00f6\u00f4\u00f9"
  //   + "\u00fa\u00fc\u00fb\u00f1\u00e7";

  var without = "aaaaaeeeeiiiiooooouuuunc";

  var map = {'@': ' at ', '\u20ac': ' euro ',
    '$': ' dollar ', '\u00a5': ' yen ',
    '\u0026': ' and ', '\u00e6': 'ae', '\u0153': 'oe'};

  return string
    // Handle uppercase characters
    .toLowerCase()

    // Handle accentuated characters
    .replace(
      new RegExp('[' + accents + ']', 'g'),
      function (c) { return without.charAt(accents.indexOf(c)); })

    // Handle special characters
    .replace(
      new RegExp('[' + keys(map).join('') + ']', 'g'),
      function (c) { return map[c]; })

    // Dash special characters
    .replace(/[^a-z0-9]/g, '-')

    // Compress multiple dash
    .replace(/-+/g, '-')

    // Trim dashes
    .replace(/^-|-$/g, '');
};


var onready = function(func){

if (document.addEventListener) {
  document.addEventListener('DOMContentLoaded', func, false);
} else if (window.addEventListener) {
  window.addEventListener('load', func, false);
} else if (document.attachEvent) {
  document.attachEvent('onreadystatechange', func);
} else if (window.attachEvent) {
  document.attachEvent('onload', func);
}

}