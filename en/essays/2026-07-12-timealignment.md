# I tried to create a car time alignment setting app and it failed.

2026.07.12 / Android

## greedy

The other day, I created a car equalizer setting app and was able to successfully adjust it.
The only disappointing thing was that even though I hadn't installed a woofer yet, the bass was coming out from around 45Hz.

DSP has another time alignment function.
If you input the measured distance to the speaker, it will be automatically adjusted, but I am not sure if it is correct.
That's right, let's make an app after all.

## What happened?

I was thinking of it as an idea for a function that automatically adjusts time alignment, but
I didn't understand some microphone APIs and relied on AI, but various problems were discovered.
In the end, most of it was created by AI.

## Don't rely on me even if I ask

I was often told this at work, but when I tried running an app that was mostly BlackBox,
I can't measure distance at all.

## guess

I had predicted this to some extent, but there will probably be a lot of time lag with smartphones.
The processor probably processes the audio data in various ways.
It would be foolish to try to measure even a small amount of time in such a situation.
(I thought it would work if I measured it several times and set it to the average or minimum value, but I was naive.)

## I have no choice after all

I've thought about other measures, but I don't have any ideas.

## summary

Suspicious things are often impossible.
I completely gave up.

## sauce

It's not open to the public because it's a failure.
