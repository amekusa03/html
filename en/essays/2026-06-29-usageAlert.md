# A story about creating a packet remaining amount notification app

2026.06.29 / kotlin

## POVO at the end of the month

This month too, I ran out of giga on the 20th.

As soon as 2GB is used up, POVO goes into slow mode. 128kbps. As I wait for the page to open, I think to myself, ``Wow, this month came so early.'' Even though it happens every month, I see the same face every month.

## That day will come suddenly

I had set a setting to notify me when the size exceeds 2GB. But the moment the notification arrives, it's already too late, and it feels like being handed a fire extinguisher while being told there's a fire.

I wish you had told me earlier.

## First of all, the timing of the notification is strange.

What I noticed is that the granularity of notifications is too coarse. There are only two choices: 0% or 100%. Translated into humans, it is the same as being told, ``You ate too much,'' after feeling full.

Then you should make it yourself.

Calculate the usage rate, 80% is a yellow card, 100% is a red card. I wanted an app that could do just that.

## made

 [AndroidUsageAlert](https://github.com/amekusa03/AndroidUsageAlert)
