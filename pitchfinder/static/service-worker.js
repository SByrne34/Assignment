// // service-worker.js

// const CACHE_NAME = 'pitchfinder-cache-v1';
// const urlsToCache = [
//     '/',
//     '/static/css/bootstrap.min.css',
//     '/static/js/bootstrap.bundle.min.js',
//     '/static/images/markers/marker-icon-red.png',
// ];

// // Install Event - Cache essential assets
// self.addEventListener('install', event => {
//     console.log('[ServiceWorker] Install');
//     event.waitUntil(
//         caches.open(CACHE_NAME)
//             .then(cache => {
//                 console.log('[ServiceWorker] Caching app shell');
//                 return cache.addAll(urlsToCache);
//             })
//             .catch(error => {
//                 console.error('[ServiceWorker] Failed to cache during install:', error);
//             })
//     );
// });

// // Activate Event - Clean up old caches
// self.addEventListener('activate', event => {
//     console.log('[ServiceWorker] Activate');
//     event.waitUntil(
//         caches.keys().then(cacheNames => {
//             return Promise.all(
//                 cacheNames.map(cache => {
//                     if (cache !== CACHE_NAME) {
//                         console.log('[ServiceWorker] Deleting old cache:', cache);
//                         return caches.delete(cache);
//                     }
//                 })
//             );
//         })
//     );
// });

// // Fetch Event - Serve cached content when offline
// self.addEventListener('fetch', event => {
//     console.log('[ServiceWorker] Fetch', event.request.url);
//     event.respondWith(
//         caches.match(event.request)
//             .then(response => {
//                 if (response) {
//                     // Return cached asset
//                     return response;
//                 }
//                 // Clone the request as it's a stream and can only be consumed once
//                 const fetchRequest = event.request.clone();
//                 return fetch(fetchRequest).then(
//                     networkResponse => {
//                         // Check for a valid response
//                         if (!networkResponse || networkResponse.status !== 200 || networkResponse.type !== 'basic') {
//                             return networkResponse;
//                         }
//                         // Clone the response to cache it
//                         const responseToCache = networkResponse.clone();
//                         caches.open(CACHE_NAME)
//                             .then(cache => {
//                                 cache.put(event.request, responseToCache);
//                             });
//                         return networkResponse;
//                     }
//                 ).catch(error => {
//                     console.error('[ServiceWorker] Fetch failed:', error);
//                     // Optionally, return a fallback page or image here
//                 });
//             })
//     );
// });
