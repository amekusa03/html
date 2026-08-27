# Ubuntu automatic shutdown repair

2026-08-27

## chance

When I tried using [Auto-shutdown tool I made previously](https://amekusa.vercel.app/en/essays#essay=2026-05-28-autoshutdown) to encode a video, I encountered a problem. It even shuts down in the middle of batch processing. I would like to wait until the process is finished, but it will be considered as no operation and will be dropped.

## correspondence

I looked at the CPU utilization rate, and if it was high, it was determined that batch processing was in progress, and the shutdown was postponed. If the operating rate drops, automatic shutdown will occur as usual. The logic is simple, but it's sufficient for our purposes.

## result

Previously, you had to manually close the app until the backup or conversion process was completed. That's gone. If you leave it alone, it will shut down as soon as it finishes processing. It's unassuming, but it's slowly becoming more convenient.

## sauce

- [AutoShutdown](https://github.com/amekusa03/AutoShutdown)
