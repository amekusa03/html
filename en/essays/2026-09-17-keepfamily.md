# A Premonition (Continued) — “A Note Left Behind” and Automatic Recovery

2026-09-17 / Android / Firebase

## Toward "Notes Left Behind" That Avoid Misunderstandings

After I built a P2P safety monitoring system using WebRTC last time, the issue that had been bothering me ever since was the problem of “missed connections.”

Connecting with someone for just the split second their smartphone screen lights up—while ideal from a privacy standpoint, it’s fragile in practice. “What if the connection drops?” “What if the other person is asleep?” The more retry logic you write to prevent missed connections, the more the code expands.

So we took the plunge and switched our backend to **Firebase Cloud Firestore**.

I changed my approach from “talking directly on the phone” to “leaving a note in the mailbox (store-and-forward).” I gently place the time I used my smartphone—as a timestamp—into a little cloud-based box. If the other person casually checks the mailbox at 5 past the hour, they’re sure to receive the latest update. This has completely freed us from the hassle of trying to coordinate our online schedules.

## So You Don't Have to Ask Your Parents to "Open the App"

Now that we’ve simplified the server side, we’ve had to deal with the “gritty realities” on the Android device side.

It’s not realistic to ask parents who live far away to “tap the monitoring app again to open it once the phone restarts.” When the phone runs out of battery, plugs into the charger, and restarts, I want the app to start running in the background right away, as if nothing had happened.

So we embedded `BootReceiver` and configured the monitoring service to automatically activate once the device had fully booted up (`BOOT_COMPLETED`).

As a measure to address the issue of repeatedly turning the smartphone on and off in quick succession, the system incorporates a mechanism that “merges operations performed within one minute with the most recent time and reduces their frequency,” as well as a “mutual approval” protocol (which prevents data from being displayed until the other party presses “OK”) to prevent unauthorized individuals from viewing the screen using a password.

Before I knew it, it had evolved beyond a mere prototype into a robust framework that allowed me to write a solid system specification document.

## The experiment is still in progress.

...So, while the design and implementation seem to have come together nicely, there’s still a bit of a gap between “working in theory” and “being truly useful in everyday life.”

Right now, I'm checking the behavior by running the actual device myself—I'm right in the middle of the "development process."

How gentle is hourly synchronization on the battery? Can it reliably trigger an alert only when a real anomaly occurs, without generating false alarms in the middle of the night? The trial and error involved stripping away theoretical speculation and refining this tool into one that quietly supports me seems likely to continue for a while longer.

## Source Code and Specifications

- [BugsLife (GitHub)](https://github.com/amekusa03/BugsLife)
- [System Specification Document (docs/SPECIFICATION.md)](https://github.com/amekusa03/BugsLife/blob/main/docs/SPECIFICATION.md)
