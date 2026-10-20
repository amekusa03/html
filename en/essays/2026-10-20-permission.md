# The Time AI Told Me "I Can't Read This" — Getting Stuck in the Quagmire of Permissions on Ubuntu

2026-10-20

## Before I knew it,

I was trying to get AI to help me check my essay for typos and missing characters, so I loaded the file into the program,
but what I got back was this error message.

```
Permission denied for read_file(/media/data/Users/ame/document/homepage/amekusa/essays/2026-10-20-specker.md). Matches default system policy.
```

Even though it was my own file, I was told, "I can't read it."

## The First Inference

There are no issues with the file permissions. I've also configured the system to trust the workspace. Yet it's still being denied.

What looked suspicious was the `/media` in the path.
The Documents folder is actually located on a different disk and is linked to the Home directory via a symbolic link.

```
/home/kusa/ドキュメント -> /media/data/Users/ame/document
```

The AI is looking at the actual path after expanding the link, and the path beyond that starts with `/media`. I wondered, “Isn’t `/media` blocked because it’s treated as removable media?”

## A Wrong Conclusion

So, I also bind-mounted the disk to `/data` and changed the target of the link.

```
/home/kusa/ドキュメント -> /data/Users/ame/document
```

As expected, it was rejected again. The error path had simply changed to `/data/...`.
My theory that `/media` was the cause turned out to be completely wrong.

## The Real Cause

If you read the error message carefully, it says that it matched the “default system policy.”
The workspace registered is `/home/kusa/ドキュメント/...`, while the actual path used by the AI for determination is `/data/...`. Since the two do not match, it appears the system considered it to be out of scope.

When I reopened the workspace, it became easy to read.
However, this is just a guess based on the circumstances. I haven't actually checked the internal decision-making logic.

## What I Learned

- The destination of a symbolic link may be determined based on the actual path.
- Before jumping to conclusions about the cause and changing the environment, it's better to reread the error message.
- All things considered, if I had just reopened the workspace from the beginning, I might have saved myself some trouble.

By the way, I could have accessed it via the shell. But I didn't want to bypass the policy, so I didn't do it.
After getting stuck in the "sound" quagmire, it seems I've now fallen into the "path" quagmire.
