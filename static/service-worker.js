const CACHE = "v1";
const STATIC = [
  "/",
  "/static/style.css",
  "/static/pwalogo.svg",
  "/static/icon-192x192.png",
  "/static/icon-512x512.png",
];
self.addEventListener("install", (e) => {
  e.waitUntil(caches.open(CACHE).then((c) => c.addAll(STATIC)));
  self.skipWaiting();
});
self.addEventListener("activate", (e) => {
  e.waitUntil(clients.claim());
});
self.addEventListener("fetch", (e) => {
  e.respondWith(
    caches.match(e.request).then((r) => r || fetch(e.request))
  );
});
