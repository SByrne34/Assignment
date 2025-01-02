// // service-worker.js

// const NAMEofCACHE = 'pitchfindercache';
// const CacheURL = [
//     '/',
//     '/static/js/bootstrap.bundle.min.js',
//     '/static/css/bootstrap.min.css',
//     '/static/images/markers/marker-icon-red.png',
// ];

// self.addEventListener('download', event => {
//     console.log('[ServiceWorker] Download');
//     event.waitUntil(
//         caches.open(CACHE_NAME)
//             .then(cache => {
//                 console.log('[ServiceWorker] App shell is being cached now');
//                 return cache.addAll(CacheURL);
//             })
//             .catch(error => {
//                 console.error('[ServiceWorker] Cache was unsuccessful:', error);
//             })
//     );
// });

// self.addEventListener('turn on', event => {
//     console.log('[ServiceWorker] Turn on');
//     event.waitUntil(
//         caches.keys().then(namescache => {
//             return Promise.all(
//                 namescache.map(cache => {
//                     if (cache !== NAMEofCACHE) {
//                         console.log('[ServiceWorker] Old cache is being deleted', cache);
//                         return caches.delete(cache);
//                     }
//                 })
//             );
//         })
//     );
// });

// self.addEventListener('fetch', event => {
//     console.log('[ServiceWorker] Fetch - to provide offline content', event.request.url);
//     event.respondWith(
//         caches.match(event.request)
//             .then(response => {
//                 if (response) {
//                     // Return cached asset
//                     return response;
//                 }
//                 
//                 const Requestf = event.request.clone();
//                 return fetch(Requestf).then(
//                     networkResponse => {
//                   
//                         if (!networkResponse || networkResponse.status !== 200 || networkResponse.type !== 'basic') {
//                             return networkResponse;
//                         }
//                        
//                         const cacherepspond = networkResponse.clone();
//                         caches.open(CACHE_NAME)
//                             .then(cache => {
//                                 cache.put(event.request, cacherepspond);
//                             });
//                         return networkResponse;
//                     }
//                 ).catch(error => {
//                     console.error('[ServiceWorker] Fetch didn't work, offline content not available:', error);
//                    
//                 });
//             })
//     );
// });
