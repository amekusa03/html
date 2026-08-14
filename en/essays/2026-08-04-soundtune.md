# Frequency sweep sound source app

## 2026-08-04

## overview

Developed a frequency sweep sound source app.

![main](/en/essays/2026-08-04-soundtune.png)

## background

It all started when I suddenly noticed something. I wonder what kind of frequency response the PC speakers we usually use actually have. Is the bass really coming out, and how far does the treble extend? Instead of looking at catalog specs, I wanted to check it out with my own ears and equipment.

To do this, we need tools that can accurately produce sounds at specific frequencies. I've tried commercially available apps and websites, but I can't seem to get my hands on the itch. So, my usual approach is to make it myself. This is how the development of the frequency sweep sound source app began.

## Issues occur

When it comes to making music, it's not enough to just make sounds. I wanted to measure how much sound pressure was actually coming out of the speakers in my environment, down to the effective value. Therefore, I decided to implement a microphone input function.

After writing the code and getting to the stage of testing it, I hit an unexpected wall. The input from the microphone is somehow strange. I reviewed the code many times, suspected the settings, and searched for the cause, but I couldn't find the cause. The conclusion I finally arrived at was surprising. The microphone itself was broken.

## solution

When I think back to the time I spent struggling with what I thought was a software glitch, I feel a little frustrated. However, if you think about it differently, this may have been a positive outcome.

What would have happened if I hadn't noticed this microphone malfunction and was actually connected to someone on a call or video conference? Without realizing it, it would only be transmitted to the other party as noise or silence, causing trouble to the other party without them realizing it. It can be said that it was a blessing in disguise that we were able to find this flaw early during the development process.

Although the initial goal of measuring the effective value was not achieved, the byproduct was that ``I noticed a broken microphone.'' Maybe that's what development is all about. Sometimes you don't get the results you're aiming for, but sometimes other value comes in unexpectedly.

## sauce

[SoundTune](https://github.com/amekusa03/SoundTune)
