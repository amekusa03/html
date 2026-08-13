# Google Nest Script

2026/04/12 / Google Nest

Google Nest Hub script

## About this Project

Introducing an example of customization using Google Nest Hub's script function.
                    Create conditions and actions with scripts to make Google Nest Hub function.

## Implementation

This time, I created a script to play a specific video on Google Nest Hub when I asked ``Introduce the Nest Hub Script.''
                    Similar settings can be made using the Google Nest Hub GUI, but I think it will be easier for engineers to understand. 


```
`metadata:
  name: ネストハブ スクリプト紹介
  description: 自己紹介
automations:
  - starters:
      - type: assistant.event.OkGoogle
        eventData: query
        is: "ネストハブ スクリプトを紹介して"
    condition:
      type: device.state.Online
      device: ネストハブ - リビングルーム
      state: online
      is: true
    actions:
      - type: assistant.command.OkGoogle
        devices:
          - ネストハブ - リビングルーム
        okGoogle: 動画を再生 "ネストハブ スクリプト紹介" `
```

#### Explanation


- **metadata: **Defines the basic information of the script. name is the name of the script and description is the description of the script. 
- **automations: **This section defines automation rules. 
- **starters: **Define the conditions to start the automation. Here, it's triggered when the user says "Introduce NestHub Script." 
- **condition: **Defines a condition that must be met before the action is performed. Here, we assume that the Nest Hub is online. 
- **actions: **Defines the actions to be performed when the condition is met. Here, Google Nest
                        I am setting an action to play a specific video on the Hub. 
**Supplementary note** I thought about creating logic that could only be done with a script, but I couldn't come up with it.

## OS / Environment

- Google Home Script Editor 
- Google Nest Hub (2nd generation)

## Key Features

- **Flexible schedule settings: **Difficult to understand conditions can be set using the GUI. 
- **Device broadcast cooperation: **Directly control Nest Hub functions and realize video playback.

## Known Issues

It has been confirmed that getting the date does not work correctly with older versions of the script.

## Resources

For official instructions on how to use Google Nest Hub's script editor, please refer to the document below. 

[View on GitHub](https://support.google.com/googlenest/answer/14125559?hl=ja)

## Bonus

Although it is not a script, this time I used Google Home for web,
                    I learned that you can control home appliances from your browser. . 

[View on GitHub](https://home.google.com/)
