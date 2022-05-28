# Overview

## What is shipper?

shipper is an artifact release manager for custom ROM teams looking for easy build artifact distribution, starting from maintainers right up to the users. Maintainers can easily upload builds that users can then download for their respective devices. Access control makes sure that maintainers can only upload for their devices, and useful features in shipper help users get builds more easily and allows for other services to access the downloads server, like OTA (over-the-air) update applications embedded in custom ROMs.

## Why use shipper?

shipper has several key advantages that custom ROM teams may want:

- shipper provides the backend and frontend required to serve build artifacts to users. Traditional setup requires a bit more manual work, whereas with shipper it's easy to get going with just a couple of configuration tweaks.
- shipper comes with shippy, a client tool that allows maintainers to upload builds with ease. shippy comes with a couple of neat features that integrates well with shipper, such as chunked uploads for reliable build artifact upload and a client-side check to validate builds before wasting bandwidth. (For a full rundown, please visit the shippy repository.)
- Access control means that maintainers can only upload builds for their own devices. It's also simple to provision, modify, and delete accounts, straight in the admin panel!
- shipper has an API system that allows users to query for devices and builds they are looking for, and fetch the build directly from the server. The API also integrates well with OTA (over-the-air) update applications.
- shipper comes with a statistics system, providing insight into the most downloaded builds and the most popular devices.

## Why not use traditional Linux tools to achieve the same thing?

Yes, things like SFTP and nginx or h5ai can be cobbled together to serve custom ROM build artifacts. But they come with several downsides and limitations:

- Access control is hard if not impossible to implement. To restrict maintainers from uploading to other devices, each maintainer account needs to be `chroot`ed into the device directory. Unfortunately, the requirement for this is that the parent folder must be owned by `root`, which may not be possible for certain server configurations.
- User management is hard: traditional Linux tools require you to create a Linux user and setup a bunch of configuration to make sure that the user cannot log on via SSH, or do other things through SFTP, etc. Forget a configuration step and the user may gain unauthorized access to the server. And if a maintainer leaves the ROM team, you must now remember to de-provision the account and remove the access and change the `chroot` configuration for the new maintainer, etc. This is all very unwieldy and requires you to remember several commands.
- While SFTP is quite stable and resilient when uploading, it does not support chunked uploads (although it will resume an incomplete upload if the server supports it).
- h5ai (and other directory listing software) do not show information about the device or the build. You have to write a separate frontend if you want this functionality.
- You will need to write your own API system. Some ROM teams try and implement an API/OTA system by having a Python script go through all the builds in the download directory every now and then and make a JSON file that is served next to the build artifacts. Unfortunately this approach requires you to periodically scan the server, using up resources and generally making the server sluggish. With shipper, the API is instantly updated thanks to Django's model database.