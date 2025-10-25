---
title: New South Wales Meshcore Network & Repeater Configuration Guide
---

The NSW Mesh Users Group uses the ANZ configuration as a baseline, but with one important modification: we run at Spreading Factor 11 instead of the standard SF10.
This is to keep transmission range decent till the mesh becomes more dense. At that time we may change the configuration.
This choice reflects Sydney's unique geography and the wide spacing of our users. SF11 provides improved range and stronger links across the metropolitan area, though it does mean our network is not directly interoperable with standard ANZ meshes running on SF10.

## Configuration Details

When configuring Repeaters we have a naming convention we ask you please follow. Name repeaters that are fixed by location. That can be suburb, or the name of the hill, mountain, building or similar where its located. This keeps it simple to pick traces out of a repeater listing. We also encourage new repeaters and roomservers to set a position, as this helps for future mesh network planning and future repeater placement plans. The location of your repeater does not have to be exactly precise, but other mesh users will appreciate it if it is as close as you can get to it's real location so that Meshcore app antenna signal and line of sight tools are useful. For instructions on how to set a position location on your node, please refer to the Meshcore inteoduction video (from 6:12 onward): https://youtu.be/t1qne8uJBAc. 

In that linked video above from 11:18 onwards is more information about repeaters. Please note that when you first turn a repeater node on, unless it is connected to a computer or GPs it will default to a clock time of 15 May 2024. This may cause issues with your adverts not being heard and will cause your new node name to drop to the bottom of the mesh contact list (when sorting by Last Heard.) To fix this, you can follow along in the video from 16:08 onwards, or do the following:

Once you have logged into your repeater via your companion node, select the Settings tab on the bottom-right. Scroll down until you see Sync Clock and tap that. Wait until you see the green success notification, and that's it. An alternative method is to select the Command Line tab after logging in to your repeater, typing clock sync in the text entry field, and hitting Send, whereupon you will get a reply saying OK once the repeater has received it and synced the clock.

For mobile repeaters please include the words mobile repeater in the name.

Please name your guest access password 'guest' if you intend to allow guest access.

| Option             | Value                              |
|--------------------|------------------------------------|
| Base Configuration | Australia                       |
| Spreading Factor   | SF11 **(Modified from Preset!)** |
| Coverage Area      | New South Wales wide               |
| Network Type       | Mesh networking                    |
| Sydney Channel     | #sydney (key is auto generated)    |
| Nepean Channel     | #nepean (key is auto generated)    |
| NSW Wide Channel   | #nsw (key is auto generated)       | 
| Macarthur Channel   | #macarthur (key is auto generated)      |
| test Channel   | #test (key is auto generated)       |
| Central Coast Channel   | #centralcoast (key is auto generated)       |
| Discord Bridge AI bot   | #rolojnr (key is auto generated)       |
