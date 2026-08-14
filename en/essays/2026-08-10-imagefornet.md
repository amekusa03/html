# Face mosaic processing added to Android image processing app

2026-08-10

## overview

ImageForNet is an Android app that allows you to easily protect your privacy (mosaic your face, remove EXIF ​​information), resize images, and add watermarks, and is compatible with Android 6.0 (API 23) or higher.

![Main screen](essays/2026-08-10-imagefornet.png)

## background

ImageForNet was originally created as an app that only added watermarks and deleted EXIF ​​information. If you upload a photo you just took to SNS, it will come with information such as location information and the date and time the photo was taken, so this is a tool to erase that information.

When I first made it, I was satisfied with it, but after using it for a while, I suddenly noticed something. When you post a photo online and later realize that it's gone, I think it's far more likely to be because a person's face was in it, rather than because of the EXIF ​​information. A photo you took with a friend, someone you happened to pass by on a trip, the face of your child—you realize it after posting it and then rush to delete it, or forget to delete it. I'm sure many people have similar experiences.

So, I decided to add a face mosaic function.

## Summary of functions including this addition of functions

- **Automatic face mosaic (Privacy Protection)**
  - Automatic face detection using AI using Google ML Kit
  - Instantly apply mosaic (pixelization) to detected faces
  - Mosaic strength can be adjusted freely
- **Delete EXIF ​​information**
  - Permanently removes metadata such as GPS location information, shooting date and time, camera model name, etc.
- **Resize image**
  - Image size (small, medium, large, original) can be selected according to the purpose
- **Real-time watermark**
  - Free text can be set
  - Placement location can be selected (top left, top right, bottom left, bottom right)
  - Customizable font color, size, and opacity
  - Parameter changes are immediately reflected in the preview
- **Simple operability**
  - Simply select an image from the gallery, process it with an intuitive UI, and save it.

## Resolved (or rather, resolved)

To be honest, since the face mosaic is set to ``automatic'', there are cases where the mosaic is not applied due to missed detections. AI isn't perfect either, so that can't be helped.

However, the purpose of this app is to make it easy for anyone to use without hesitation. It might be possible to prevent detection failures by manually selecting faces one by one and filling them in, but that would make the operation cumbersome, and in the end no one would use it. Safety features that are not used have no meaning.

Therefore, this time, I decided to release it as is, with a policy of prioritizing ease of use, while allowing for some missed detections. Rather than perfect automation, it should be easy to use. I would like to maintain that stance in the future.

## sauce

- [GitHub View](https://github.com/amekusa03/AndroidImageForNet)
