---
name: WebDAV
title: ESP-KVM recordings to Nextcloud or a NAS
page_title: IP-KVM recordings to Nextcloud, Synology or QNAP over WebDAV - ESP-KVM
description: ESP-KVM sends recordings, dashcam clips and screenshots from its microSD card to a WebDAV folder, such as Nextcloud, ownCloud or a Synology or QNAP share. When you press Upload, or as soon as a file is saved.
tip: Recordings and screenshots to Nextcloud or a NAS
summary: Recordings and screenshots to Nextcloud or a NAS share.
mark: mark.svg
order: 9
foot: Nextcloud, ownCloud, Synology and QNAP are trademarks of their owners. ESP-KVM is an independent open-source project and is not affiliated with or endorsed by them.
link.Uploads in the API: https://github.com/espkvm/espkvm/blob/main/docs/API.md
link.Try the console: https://demo.espkvm.io/
---

ESP-KVM saves recordings and screenshots on its microSD card. With a WebDAV folder set, it also sends them to that folder. Files go from the device straight to your server, with no server of mine in between. Nothing is sent until you set a folder.

## Where it can send

Any server that speaks WebDAV:

- **Nextcloud or ownCloud.** The address looks like `https://cloud.example.com/remote.php/dav/files/you/espkvm/`. Use an app password, made under Settings, Security, not your own password.
- **Synology.** Install WebDAV Server from the Package Center and turn it on. The address is `http://nas:5005/shared-folder/`, or port 5006 for HTTPS. The user needs write access to the shared folder.
- **QNAP.** Turn on WebDAV in the file services settings and give the user write access to the shared folder.
- **Apache or nginx** with the WebDAV module on.

The folder in the address has to exist on the server. The device makes the rest.

## Setting up the device

1. In the console open Settings, Video, and scroll to Upload.
2. Fill in WebDAV folder, User name and Password.
3. Press Check the folder. The device makes a folder named after itself there, with VIDEO and SCREENSHOTS inside, so several devices can share one address.
4. Save.

The password stays on the device and is never sent back to the console.

## By hand

Each file in the recordings panel has an Upload button, and Upload all sends the whole tab, oldest first. Files go one at a time, and the panel shows how far each one got. A recording takes its .srt file with the keys pressed along. Cancel stops the file that is going and the ones still waiting.

## On its own

Under Upload automatically, tick what goes as soon as it is saved on the card: recordings, clips saved by hand, dashcam clips, screenshots and timelapses.

The dashcam is where this helps most. It keeps the last minutes of the screen and saves a clip when the screen stops or a watched phrase shows up. With dashcam clips ticked, the clip goes to the NAS right after that. If the device dies later, the clip is already off it.

## When the server is down

The whole queue waits. The first retry comes after 30 seconds, then the gaps double up to 10 minutes. Pressing Upload tries again at once. The list of waiting files is kept on the card, so a restart or a power cut does not lose it.

A refusal is not retried: a wrong password, a folder that is not there, a full disk. The panel says which one it was.

## Good to know

- The device reads a file from the card in small pieces as it sends it, so a 4 GB recording needs no more memory than a screenshot.
- On my bench, over plain http on the local network, a 21 MB recording took 3.4 seconds. While someone watches the picture, an upload slows down to about 1 MB/s and leaves the network to the live video.
- Over HTTPS the device checks the server's certificate against the public roots built into it. A certificate from a public authority such as Let's Encrypt is accepted. A self-signed one is not.
- Plain http sends the password unencrypted, so keep it to your own network.
- A reverse proxy in front of the server may limit the size of one upload. The panel then says the server does not take a file this big.
- A file stays on the card after it is sent.
