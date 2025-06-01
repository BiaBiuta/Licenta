// // static/js/socket.js
// ;(function() {
//   "use strict";
//
//   // Wait until the page is parsed
//   document.addEventListener("DOMContentLoaded", function() {
//     // build the correct ws:// or wss:// URL
//    const wsScheme = window.location.protocol === "https:" ? "wss" : "ws";
//          window.socket = new WebSocket(  "ws://" + window.location.hostname + ":5000/ws/notifications/");
//
//     window.socket.onopen = () => {
//       console.log("[WS] connected");
//              // îl activezi aici
//     };
//
//         window.socket.onmessage = function(e) {
//             const data = JSON.parse(e.data);
//             console.log("Mesaj primit:", data);
//             // Dacă expeditorul este altul decât utilizatorul curent, afișăm notificarea
//             // if (data.sender !== currentUser) {
//                 //document.getElementById("notifications").innerText = data.message;
//              alert(data.message);
//             //}
//         };
//
//         window.socket.onerror = function(error) {
//             console.error("WebSocket error:", error);
//         };
//         window.socket.onclose = function(e) {
//         console.error('WebSocket closed unexpectedly');
//     };
//   });
// })();
