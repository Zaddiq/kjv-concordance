// Cache the page and data after first load so the concordance works offline.
// Bump VERSION whenever index.html or the data files change.
const VERSION = "v1";
const CACHE = "kjv-concordance-" + VERSION;

self.addEventListener("install", () => self.skipWaiting());

self.addEventListener("activate", event => {
  event.waitUntil(
    caches.keys()
      .then(keys => Promise.all(keys.filter(k => k.startsWith("kjv-concordance-") && k !== CACHE).map(k => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener("fetch", event => {
  const req = event.request;
  if (req.method !== "GET" || new URL(req.url).origin !== location.origin) return;
  event.respondWith(
    caches.open(CACHE).then(cache =>
      cache.match(req).then(hit => {
        if (hit) return hit;
        return fetch(req).then(res => {
          if (res.ok) cache.put(req, res.clone());
          return res;
        });
      })
    )
  );
});
