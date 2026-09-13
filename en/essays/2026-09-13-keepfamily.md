# Not “monitoring” but “insect notifications”—A story about creating a monitoring app that gently senses signs

2026-09-13 / Android / SkyWay

## background

After a family member living far away became unwell, he became concerned about their daily safety.

There are various ``elderly and family monitoring services'' in the world. However, services that use cameras to view your room, constantly track your location using GPS, or use microphones to pick up the sounds of your daily life can leave you feeling suffocated, as if you are being``surveilled.'' The person being watched will also feel uncomfortable as their privacy will be completely exposed.

What I was looking for was not excessive surveillance, but a system that would gently convey the message, ``I see you are using your smartphone today as usual, and doing well.''

Therefore, I decided to create an app that uses smartphone screen lights and operations as triggers to gently communicate to each other that you are doing well.

![BugsLife UI](essays/2026-09-13-keepfamily.png)

## Special features and main features

- **Gradual activity detection by screen lighting**:
  - A system that allows you to "confirm your survival" by simply attaching your smartphone screen as usual, without requiring any special operations.
  - It's not a "monitor/be watched" relationship, but a natural way to make sure each other is doing well.
- **Thorough privacy protection**:
  - We do not collect or share any camera footage, audio, current location (GPS), etc.
  - All that is shared is the minimum status of ``whether it is currently active or not.''
- **Secure communication infrastructure (SkyWay/WebRTC)**:
  - Utilizes SkyWay as the communication infrastructure to achieve secure real-time communication.
  - A safe design that does not accumulate or store any personal data or action logs on the server.
- **Easy one-tap status sending**:
  - In addition to turning on the screen, it also has an auxiliary function that allows you to send simple messages such as "I'm fine" or "I'm not feeling well" to the other party with a single tap.

## ending

Overly generous monitoring functions sometimes threaten privacy, but not having any at all is worrying. We named the app ``BugsLife'' with the hope that it would be able to silently send us signs without over-intervening, just like``insect news'' or the whispers of insects in the grass.With this in mind, we named the app ``BugsLife.''

It seems like we can create a daily routine where we can quietly check on each other's safety while maintaining a reasonable distance.

## sauce

- [BugsLife (GitHub)](https://github.com/amekusa03/BugsLife)
