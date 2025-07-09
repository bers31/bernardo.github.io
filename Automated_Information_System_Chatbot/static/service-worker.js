const CACHE_NAME = 'lapas-chatbot-v1.0.0';
const STATIC_CACHE = 'lapas-static-v1.0.0';
const API_CACHE = 'lapas-api-v1.0.0';
const OFFLINE_PAGE = '/offline.html';

// Assets yang akan di-cache
const STATIC_ASSETS = [
  '/',
  '/static/favicon.ico',
  '/admin/login',
];

// API endpoints yang akan di-cache
const API_ENDPOINTS = [
  '/api/ask',
  '/api/v1/chat',
  '/api/v1/chat/session',
  '/api/admin/faq',
  '/api/admin/schedules',
  '/api/admin/requirements',
  '/api/admin/health-services',
  '/api/admin/contacts',
  '/api/admin/rehab-programs'
];

// Offline responses untuk berbagai endpoint
const OFFLINE_RESPONSES = {
  '/api/ask': {
    answer: 'Maaf, Anda sedang offline. Silakan coba lagi ketika koneksi internet tersedia.',
    source: 'offline',
    session_id: 'offline_session'
  },
  '/api/v1/chat': {
    success: false,
    error: 'Tidak ada koneksi internet',
    message: 'Silakan periksa koneksi internet Anda dan coba lagi.'
  },
  '/api/v1/chat/session': {
    success: false,
    error: 'Offline mode',
    response: {
      message: 'Maaf, fitur chat tidak tersedia saat offline. Silakan periksa koneksi internet Anda.',
      source: 'offline',
      timestamp: new Date().toISOString(),
      metadata: {
        intent: 'offline',
        is_greeting: false,
        is_gratitude: false,
        is_goodbye: false,
        has_links: false,
        has_table: false
      }
    },
    session_id: 'offline_session'
  }
};

// Install event - cache static assets
self.addEventListener('install', event => {
  console.log('Service Worker: Installing...');
  
  event.waitUntil(
    Promise.all([
      // 1. Loop manual untuk static assets
      caches.open(STATIC_CACHE)
        .then(async cache => {
          console.log('Service Worker: Caching static assets');
          for (const url of STATIC_ASSETS.filter(asset => asset !== OFFLINE_PAGE)) {
            try {
              const res = await fetch(url);
              if (!res.ok) {
                console.error(`❌ [SW Install] Fetch failed for ${url}:`, res.status, res.statusText);
              } else {
                await cache.put(url, res.clone());
                console.log(`✅ [SW Install] Cached ${url}`);
              }
            } catch (err) {
              console.error(`❌ [SW Install] Error fetching ${url}:`, err);
            }
          }
        }),

      // 2. Buat halaman offline
      caches.open(CACHE_NAME)
        .then(cache => {
          const offlineHtml = generateOfflinePage();
          return cache.put(OFFLINE_PAGE, new Response(offlineHtml, {
            headers: { 'Content-Type': 'text/html' }
          }));
        })
    ])
    .then(() => {
      console.log('Service Worker: Installation complete');
      return self.skipWaiting();
    })
    .catch(error => {
      console.error('Service Worker: Installation failed', error);
    })
  );
});

// Activate event - cleanup old caches
self.addEventListener('activate', event => {
  console.log('Service Worker: Activating...');
  
  event.waitUntil(
    caches.keys()
      .then(cacheNames => {
        return Promise.all(
          cacheNames.map(cacheName => {
            if (cacheName !== CACHE_NAME && 
                cacheName !== STATIC_CACHE && 
                cacheName !== API_CACHE) {
              console.log('Service Worker: Deleting old cache:', cacheName);
              return caches.delete(cacheName);
            }
          })
        );
      })
      .then(() => {
        console.log('Service Worker: Activation complete');
        return self.clients.claim();
      })
  );
});

// Fetch event - handle requests
self.addEventListener('fetch', event => {
  const { request } = event;
  const url = new URL(request.url);
  
  // Skip cross-origin requests
  if (url.origin !== location.origin) {
    return;
  }
  
  // Handle different types of requests
  if (isAPIRequest(request)) {
    event.respondWith(handleAPIRequest(request));
  } else if (isStaticAsset(request)) {
    event.respondWith(handleStaticAsset(request));
  } else {
    event.respondWith(handlePageRequest(request));
  }
});

// Check if request is for API
function isAPIRequest(request) {
  return request.url.includes('/api/');
}

// Check if request is for static asset
function isStaticAsset(request) {
  const url = new URL(request.url);
  return url.pathname.startsWith('/static/') || 
         url.pathname.endsWith('.ico') ||
         url.pathname.endsWith('.png') ||
         url.pathname.endsWith('.jpg') ||
         url.pathname.endsWith('.css') ||
         url.pathname.endsWith('.js');
}

// Handle API requests with caching strategy
async function handleAPIRequest(request) {
  const url = new URL(request.url);
  const pathname = url.pathname;
  
  // For GET requests, try cache first
  if (request.method === 'GET') {
    try {
      // Try network first for fresh data
      const networkResponse = await fetch(request);
      
      if (networkResponse.ok) {
        // Cache successful responses
        const cache = await caches.open(API_CACHE);
        cache.put(request, networkResponse.clone());
        return networkResponse;
      }
    } catch (error) {
      console.log('Service Worker: Network failed, trying cache for:', pathname);
    }
    
    // Fallback to cache
    const cachedResponse = await caches.match(request);
    if (cachedResponse) {
      return cachedResponse;
    }
  }
  
  // For POST requests (chat), handle offline
  if (request.method === 'POST') {
    try {
      const networkResponse = await fetch(request);
      return networkResponse;
    } catch (error) {
      console.log('Service Worker: Chat request failed, returning offline response');
      return createOfflineAPIResponse(pathname);
    }
  }
  
  // 3) DELETE → forward ke server, jangan cache
  if (request.method === 'DELETE') {
    try {
      const networkResponse = await fetch(request);
      return networkResponse;
    } catch (error) {
      console.log('Service Worker: DELETE failed, returning offline response for', pathname);
      return createOfflineAPIResponse(pathname);
    }
  }

  // 4) PUT → forward ke server, jangan cache
  if (request.method === 'PUT') {
    try {
      const networkResponse = await fetch(request);
      return networkResponse;
    } catch (error) {
      console.log('Service Worker: PUT failed, returning offline response for', pathname);
      return createOfflineAPIResponse(pathname);
    }
  }
  
  // Final fallback
  return createOfflineAPIResponse(pathname);
}

// Handle static asset requests
async function handleStaticAsset(request) {
  try {
    // Try cache first for static assets
    const cachedResponse = await caches.match(request);
    if (cachedResponse) {
      return cachedResponse;
    }
    
    // Fallback to network
    const networkResponse = await fetch(request);
    
    if (networkResponse.ok) {
      // Cache the asset
      const cache = await caches.open(STATIC_CACHE);
      cache.put(request, networkResponse.clone());
    }
    
    return networkResponse;
  } catch (error) {
    console.log('Service Worker: Static asset request failed:', request.url);
    
    // Return placeholder for images
    if (request.url.includes('.png') || request.url.includes('.jpg')) {
      return new Response('', { status: 200, statusText: 'OK' });
    }
    
    return new Response('Asset not available offline', { 
      status: 404, 
      statusText: 'Not Found' 
    });
  }
}

// Handle page requests
async function handlePageRequest(request) {
  // Jika bukan GET, langsung coba fetch dan fallback ke offline page
  if (request.method !== 'GET') {
    try {
      return await fetch(request);
    } catch (err) {
      return caches.match(OFFLINE_PAGE);
    }
  }

  // Untuk GET: network-first, kemudian cache
  try {
    const networkResponse = await fetch(request);
    if (networkResponse.ok) {
      const cache = await caches.open(CACHE_NAME);
      await cache.put(request, networkResponse.clone());
    }
    return networkResponse;
  } catch (error) {
    console.log('Service Worker: Page request failed, trying cache');
    const cachedResponse = await caches.match(request);
    if (cachedResponse) return cachedResponse;
    return caches.match(OFFLINE_PAGE);
  }
}

// Create offline API response
function createOfflineAPIResponse(pathname) {
  const offlineResponse = OFFLINE_RESPONSES[pathname] || {
    error: 'Service tidak tersedia saat offline',
    message: 'Silakan periksa koneksi internet Anda'
  };
  
  return new Response(JSON.stringify(offlineResponse), {
    status: 200,
    headers: { 'Content-Type': 'application/json' }
  });
}

// Generate offline page HTML
function generateOfflinePage() {
  return `
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Offline - Chatbot Lapas 2 Ambarawa</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
        }
        
        .offline-container {
            text-align: center;
            max-width: 500px;
            padding: 2rem;
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            border: 1px solid rgba(255, 255, 255, 0.2);
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        }
        
        .offline-icon {
            font-size: 4rem;
            margin-bottom: 1rem;
            opacity: 0.8;
        }
        
        .offline-title {
            font-size: 2rem;
            margin-bottom: 1rem;
            font-weight: 600;
        }
        
        .offline-message {
            font-size: 1.1rem;
            margin-bottom: 2rem;
            opacity: 0.9;
            line-height: 1.6;
        }
        
        .retry-button {
            background: rgba(255, 255, 255, 0.2);
            border: 2px solid rgba(255, 255, 255, 0.3);
            color: white;
            padding: 12px 30px;
            border-radius: 50px;
            cursor: pointer;
            font-size: 1rem;
            font-weight: 500;
            transition: all 0.3s ease;
        }
        
        .retry-button:hover {
            background: rgba(255, 255, 255, 0.3);
            transform: translateY(-2px);
        }
        
        .offline-tips {
            margin-top: 2rem;
            padding-top: 2rem;
            border-top: 1px solid rgba(255, 255, 255, 0.2);
            text-align: left;
        }
        
        .offline-tips h3 {
            margin-bottom: 1rem;
            font-size: 1.2rem;
        }
        
        .offline-tips ul {
            list-style: none;
            padding-left: 0;
        }
        
        .offline-tips li {
            margin-bottom: 0.8rem;
            padding-left: 1.5rem;
            position: relative;
            opacity: 0.9;
        }
        
        .offline-tips li:before {
            content: '•';
            position: absolute;
            left: 0;
            color: rgba(255, 255, 255, 0.7);
        }
        
        @media (max-width: 600px) {
            .offline-container {
                margin: 1rem;
                padding: 1.5rem;
            }
            
            .offline-title {
                font-size: 1.5rem;
            }
            
            .offline-message {
                font-size: 1rem;
            }
        }
    </style>
</head>
<body>
    <div class="offline-container">
        <div class="offline-icon">📡</div>
        <h1 class="offline-title">Anda Sedang Offline</h1>
        <p class="offline-message">
            Koneksi internet tidak tersedia. Beberapa fitur mungkin tidak berfungsi dengan baik.
        </p>
        
        <button class="retry-button" onclick="window.location.reload()">
            Coba Lagi
        </button>
        
        <div class="offline-tips">
            <h3>Tips Saat Offline:</h3>
            <ul>
                <li>Periksa koneksi WiFi atau data seluler Anda</li>
                <li>Coba refresh halaman setelah koneksi kembali</li>
                <li>Beberapa informasi mungkin masih tersedia dari cache</li>
                <li>Fitur chat membutuhkan koneksi internet</li>
            </ul>
        </div>
    </div>
    
    <script>
        // Auto-retry when online
        window.addEventListener('online', () => {
            window.location.reload();
        });
        
        // Check connection status
        if (navigator.onLine) {
            window.location.reload();
        }
    </script>
</body>
</html>`;
}

// Push notification handling
self.addEventListener('push', event => {
  console.log('Service Worker: Push notification received');
  
  const options = {
    title: 'Chatbot Lapas 2 Ambarawa',
    body: event.data ? event.data.text() : 'Ada pesan baru untuk Anda',
    icon: '/static/favicon.ico',
    badge: '/static/favicon.ico',
    vibrate: [200, 100, 200],
    data: {
      url: '/'
    },
    actions: [
      {
        action: 'open',
        title: 'Buka Chat',
        icon: '/static/favicon.ico'
      }
    ]
  };
  
  event.waitUntil(
    self.registration.showNotification(options.title, options)
  );
});

// Notification click handling
self.addEventListener('notificationclick', event => {
  console.log('Service Worker: Notification clicked');
  
  event.notification.close();
  
  event.waitUntil(
    clients.matchAll({ type: 'window', includeUncontrolled: true })
      .then(clientList => {
        // Try to focus existing window
        for (const client of clientList) {
          if (client.url === '/' && 'focus' in client) {
            return client.focus();
          }
        }
        
        // Open new window
        if (clients.openWindow) {
          return clients.openWindow('/');
        }
      })
  );
});

// Background sync for offline chat messages
self.addEventListener('sync', event => {
  console.log('Service Worker: Background sync triggered');
  
  if (event.tag === 'chat-sync') {
    event.waitUntil(syncChatMessages());
  }
});

// Sync offline chat messages when online
async function syncChatMessages() {
  try {
    // Get offline messages from IndexedDB or cache
    // This would require additional implementation for storing offline messages
    console.log('Service Worker: Syncing offline chat messages');
    
    // Implementation would go here to send queued messages
    // when connection is restored
  } catch (error) {
    console.error('Service Worker: Failed to sync chat messages', error);
  }
}

// Message handling from main thread
self.addEventListener('message', event => {
  if (event.data && event.data.type === 'SKIP_WAITING') {
    self.skipWaiting();
  }
  
  if (event.data && event.data.type === 'CACHE_CHAT_DATA') {
    // Cache important chat data
    cacheChatData(event.data.payload);
  }
});

// Cache important chat data
async function cacheChatData(data) {
  try {
    const cache = await caches.open(API_CACHE);
    const response = new Response(JSON.stringify(data), {
      headers: { 'Content-Type': 'application/json' }
    });
    await cache.put('/api/cached-data', response);
  } catch (error) {
    console.error('Service Worker: Failed to cache chat data', error);
  }
}

console.log('Service Worker: Loaded successfully');