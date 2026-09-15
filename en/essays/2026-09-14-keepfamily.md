# A Premonition—A More Natural, Subtle Way to Keep Watch

2026-09-14 / Android / SkyWay

## If the screen turns on, does that mean I'm alive?

In the system I built last time, I had it detect the moment the smartphone screen lit up as a "sign of life." However, as I continued with the implementation, I realized there was an unexpected pitfall.

`ACTION_SCREEN_ON`—This event, which detects the screen-on broadcast, fires without fail even when the phone receives an incoming call or a missed call notification. In other words, even a single nuisance call in the middle of the night could cause the system to interpret it as a “life sign” being received. That would certainly be a problem.

The solution was simple. Instead of checking when the screen “turned on,” check when the lock was “unlocked.” `ACTION_USER_PRESENT`—This indicates that a person actually touched the smartphone with their hand, so it significantly reduces false positives. This event isn’t triggered by incoming calls or notifications alone.

I also addressed another issue that had been on my mind. Android has a power-saving feature called “Doze Mode,” which gradually restricts background processes when the phone isn’t used for an extended period. As a monitoring app, I wanted it to continue running quietly even while I’m asleep. So, I redesigned it to run as a foreground service and send a periodic “alive” signal every hour at 05 minutes past the hour. This allows the app to more reliably detect situations where “the signal has been lost for a certain period of time.”

## Toward the Next Step in Weight Reduction

After implementing this much, I sometimes find myself taking a step back. Even though it’s just a system that sends a few dozen bytes of JSON once an hour, the underlying infrastructure—WebRTC (including ICE negotiation and signaling servers)—is quite a heavy-duty setup.

WebRTC offers privacy benefits unique to P2P communication—no data is stored on servers, and the connection is encrypted. That’s certainly appealing. However, it also presents the challenge of “rendezvous synchronization,” which requires both parties to be online at the same time. What if one party is about to send a message just as the other goes offline? Figuring out how to handle that “missed connection” is surprisingly tricky.

In the next version, I’d like to explore some lighter-weight options. “Cloudflare Workers + KV,” “MQTT,” and “FCM (Firebase Cloud Messaging)” come to mind as candidates. If I use a system that ensures reliable delivery even asynchronously, the code should be much simpler to write. However, that means the data will have to pass through the server. The trade-off between privacy and convenience—I haven’t reached a conclusion yet.

## sauce

- [BugsLife (GitHub)](https://github.com/amekusa03/BugsLife)
