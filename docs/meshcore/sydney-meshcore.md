---
title: New South Wales Meshcore Network & Repeater Configuration Guide
---

### Getting started with MeshCore
📺 Helpful video explaining MeshCore. How it works and how to use/set it up. [How to get started with MeshCore off grid text messaging](https://www.youtube.com/watch?v=t1qne8uJBAc&t=372s)

### Setting Up Your Companion

**1. Flash and setup**

Flash using [Meshcore firmware flasher](https://flasher.meshcore.co.uk/). It is important you decide now what mode of connection to the node you are using as the firmware supports one connection type at a time (BLE,USB,Wifi). Make sure to erase before flashing meshcore for the first time.

**2. Connect and setup**

Now connect to your companion using the method you chose and configure the Name, radio settings and channels.

- The name and radio settings are set in the settings page (found under the `⚙️` at the top right of the app). Make sure to tap the `✔️` at the top right to save the settings. Wait for the green success notification.

- The channels are added from the channel page at the top right `⋮` → `+ Add Channel` → `Join a Hashtag Channel` Then enter the name of the channel (shown below such as `test`) and press join channel.

**3. Join the mesh**

Send an advert by hitting the `advert` → `Send Flood Advert` to send your node name to the mesh. Direct reachable repeaters can be discovered by `🔧` → `Discover Nearby Nodes` → `Discover Repeaters`. After a short while repeaters within range should reply with their info. you can hit the `+` to add them into your contacts.

Send a greeting to the public channel or a `test` to the **#test** channel. The **Public** channel is used for general chat, and if someone sees your greeting they will likely reply. The **test** channel is primarily used for sending test messages to check your connection to the mesh. There are bots on the test channel that will reply to `test`, `ping` or `path` and will respond accordingly with a reply. When a message is sent next to the message will say `heard X repeats` x representing the number of repeaters that you heard retransmitting your sent message. If this is 0 then a repeater was unable to be reached, or the radio settings are wrong. Double check the radio settings and then check the [NSW Meshcore Map](https://nswmesh.github.io/NSW-Sydney-Meshcore-Map/) to see if there are repeaters near you. Double click or long press on your location to check if there is expected coverage at your location. In order to be able to reach a repeater you must have direct line of sight to it due to the low transmission powers. If none are reachable try standing outside with the antenna pointing upwards, or find some height to clear buildings.

Repeaters send a local advert (an advert that can be heard if you are directly connected to that repeater only) every 240 minutes. And a flood advert every 12 hours. This means that the node list can take a while to populate. Companions also only advert when manually triggered. This means that a connection to the mesh can be present but there is not an advert being sent at that moment (This is good as it means that the mesh is not congested)


> **Important:** All nodes connecting to the Sydney mesh must use the **Australia preset** with SF11 (modified from the default SF10).
**Why SF11?** The NSW Mesh uses SF11 instead of the standard SF10 to provide improved range across Sydney's unique geography and wide user spacing. This means we are **not directly interoperable** with standard ANZ meshes running SF10.

### Radio Settings

| Setting | Value |
|---------|-------|
| Frequency | 915.800 MHz |
| Bandwidth | 250.0 kHz |
| Spreading Factor (SF) | **11** ⚠️ |
| Coding Rate (CR) | 5 |


### Channels

| Channel | Key |
|---------|-----|
| Public | Public Channel |
| Test (with test bot) | `#test` (auto-generated) |
| Sydney | `#sydney` (auto-generated) |
| NSW Wide | `#nsw` (auto-generated) |
| Macarthur | `#macarthur` (auto-generated) |
| Nepean | `#nepean` (auto-generated) |
| Central Coast | `#centralcoast` (auto-generated) |
| Illawarra | `#illawarra` (auto-generated) |
| Discord Bridge AI bot | `#jeff` (auto-generated) |
| RoloJnr | `#rolojnr` (auto-generated) |

---

## Repeater Naming & Setup

### Naming Convention

| Type | Naming | Example |
|------|-------------|---------|
| Fixed repeaters | Name by location (suburb, hill, building) | `⚡️- Mount Colah`, `🌱 - Camperdown`, `Davo - Centrepoint Tower` |
| Mobile repeaters | Include "mobile" in name | `Johns Mobile` |

### Setting Up Your Repeater

**1. Flash and setup**

Flash and setup the repeater using [Meshcore firmware flasher](https://flasher.meshcore.co.uk/) including Naming using the convention. Setting a position we encourage all repeaters to have a location for mesh planning purposes. It doesn't need to be exact, but accurate positions help other users with signal and line-of-sight tools. Set your guest password to `guest` to allow other mesh users to query your repeater's status and neighbors (without admin access). **Do not reboot node yet**

**2. Prefix Setting**

Go to [NSW key generator and configurator](https://nswmesh.au/docs/meshcore/key_generator) And generate a key either with the prefix you are already using, or an unused prefix. This is important as routes are based off the first two characters of the public key, and duplicates cause confusion. Once the key is generated it can be sent to the device from the page. Now you can reboot node.

**3. Sync the Clock and configure repeater**

Repeaters default to a clock time of 15 May 2024 on every reboot unless connected to a computer or GPS. This causes:
- Adverts not being heard
- Node appearing at bottom of contact list (when sorted by Last Heard)

**To fix:**
1. Log into your repeater via your companion node
2. Go to **Settings** tab → Scroll to **Sync Clock** → Tap it
3. Wait for green success notification

Once logged in and the clock is synced go to the `>_` - **`Command Line`** tab and enter the commands from the profiles below with your chosen repeater profile and common settings. Copy and paste each line and send. Wait up to 30 seconds to see an `OK` response - if no response then resend command.


📺 [Watch: More about repeaters (video, 11:18)](https://youtu.be/t1qne8uJBAc?t=678)

---

## Repeater Configuration Profiles

Choose the profile that matches your repeater's role and position in the mesh network. These settings work together to optimize packet flow and minimize collisions based on your repeater's location and how many neighbors it can hear.

> **📝 MeshCore Defaults:** `txdelay=0.5`, `direct.txdelay=0.2`, `rxdelay=0`, `af=1.0`. All profiles below modify these to optimize for the Sydney mesh.

### 🔴 CRITICAL — Hilltop/Tower Infrastructure

> **Role:** Highest elevation, most neighbors, backbone of the mesh

**When to use:** Your repeater is on a hilltop, tower, or tall building with clear line-of-sight to many other nodes. You can see 10+ neighbors well and your repeater is a key link in the network backbone.

```
set txdelay 2
set direct.txdelay 2
set rxdelay 15
set af 3
```

**Why these values:**
- **High txdelay (2.0):** Waits longer before retransmitting, letting smaller nodes serve their local areas first. Reduces collisions in your wide coverage area.
- **High rxdelay (15):** With many neighbors, you'll receive the same packet from multiple sources. Higher rxdelay gives more time to receive the best (strongest signal) copy before processing.
- **High af (3):** Enforces 25% duty cycle. Critical nodes see heavy traffic; this prevents channel hogging and gives other nodes a chance to transmit.

---

### 🟠 LINK — Mid-elevation Bridge

> **Role:** Connects critical nodes to local coverage, moderate neighbor count

**When to use:** Your repeater bridges between hilltop infrastructure and suburban coverage. You can see some critical nodes and some local nodes (5-10 neighbors typical).

```
set txdelay 1.5
set direct.txdelay 1
set rxdelay 8
set af 2
```

**Why these values:**
- **Moderate txdelay (1.5):** Balances responsiveness with collision avoidance. You're important for connectivity but not the primary backbone.
- **Moderate rxdelay (8):** You hear multiple sources but not as many as critical nodes. Moderate delay balances signal selection with responsiveness.
- **Moderate af (2):** 33% duty cycle balances your bridging role with fair channel access.

---

### 🟡 STANDARD — Suburban Coverage

> **Role:** Average positioning, serves local area, moderate neighbors

**When to use:** Typical deployment. Your repeater is in an elevated position, serving your local neighborhood. You see 3-8 neighbors.

```
set txdelay 0.8
set direct.txdelay 0.4
set rxdelay 4
set af 1.5
```

**Why these values:**
- **Lower txdelay (0.8):** More responsive for local coverage. Fewer neighbors means lower collision risk.
- **Lower rxdelay (4):** Less need to wait for better copies since you hear fewer sources.
- **Lower af (1.5):** 40% duty cycle. Reasonable responsiveness while still being a good mesh citizen.

---

### 🟢 LOCAL — Ground-level/Indoor

> **Role:** Low elevation, few neighbors, serves immediate area

**When to use:** Indoor repeater, rooftop repeater, ground-level installation, or endpoint coverage. You only see 1-3 neighbors and primarily serve your immediate area.

```
set txdelay 0.3
set direct.txdelay 0.1
set rxdelay 0
set af 1
```

**Why these values:**
- **Minimal txdelay (0.3):** Maximum responsiveness. With few neighbors, collision risk is low.
- **Zero rxdelay (0):** No need to wait for better signal copies when you only hear one or two sources.
- **Low af (1):** 50% duty cycle. You're not creating congestion with your limited coverage.

---

## Common Settings (All Repeaters)

Apply these settings to **all repeaters** regardless of role:

> **📝 Note:** Most of these differ from MeshCore defaults. See the Quick Reference table below for default comparisons.

```
set int.thresh 14
set agc.reset.interval 500
set multi.acks 1
set advert.interval 240
set flood.advert.interval 12
set guest.password guest
```

### Quick Reference

| Setting | Value | MeshCore Default | What it does |
|---------|-------|------------------|--------------|
| `int.thresh` | 14 | 0 (disabled) | Interference threshold (dB above noise floor) for Listen-Before-Talk |
| `agc.reset.interval` | 500 | 0 (disabled) | AGC reset every 500 seconds (~8 min) to prevent sensitivity drift |
| `multi.acks` | 1 | 1 | Send redundant ACKs for better delivery reliability |
| `advert.interval` | 240 | 0 | Local advert every 240 minutes (neighbors only) |
| `flood.advert.interval` | 12 | 12 | Network-wide advert every 12 hours |
| `guest.password` | guest | (none) | Standard guest access password |
| `radio` | 915.8,250,11,5 | 915.0,250,10,5 | Sydney mesh radio parameters (freq, bw, sf, cr) |

---

## Understanding the Settings

### Interference Threshold (`int.thresh`)

Implements Listen-Before-Talk (LBT) to avoid transmitting when the channel is busy.

**How it works:**
1. The radio periodically samples the channel to establish a baseline noise floor (typically around -120dBm)
2. Before transmitting, it checks: Is current RSSI > noise_floor + threshold?
3. If yes, the channel is considered busy and transmission is delayed

| Value | Behavior |
|-------|----------|
| 14 | Waits until most of the noise has dropped, balances waiting for the airspace to clear, vs delaying transmission forever |
| Higher | Less conservative, delays transmission for louder rf signals only (including other repeaters) |
| Lower | More conservative, waits longer for a clear channel, potentially waiting endlessly for a constant signal |
| **0** | **Disabled — MeshCore default** Transmits without checking channel. Can cause repeqters to step on each other |

**Recommended:** 14 for most deployments. Lower values may cause excessive transmission delays in noisy RF environments.

---

### AGC Reset Interval (`agc.reset.interval`)

The Automatic Gain Control (AGC) in LoRa radios adjusts receiver sensitivity automatically. However, AGC can drift in busy environments, reducing sensitivity over time.

**Known issue:** Loud RF signals (in or out of band) can lock up the AGC, preventing the repeater from receiving packets until it's reset.

**How it works:**
- The radio periodically re-initializes the receiver, resetting AGC to optimal sensitivity
- Value is in **seconds**

| Value | Behavior |
|-------|----------|
| 500 | Reset every ~8 minutes (recommended especially for noisy RF environments) |
| **0** | **Disabled — MeshCore default** (AGC can lockup but is not too common) |

---

### Multiple Acknowledgments (`multi.acks`)

Controls whether redundant ACKs are sent for direct (point-to-point) messages.

**How it works:**
- When enabled (1): Sends two ACK packets — first a "multi-ack", then the standard ACK
- When disabled (0): Sends only a single ACK packet

**Why use it:** ACKs are small packets that can easily be lost. Sending redundant ACKs significantly improves delivery confirmation reliability, especially over longer paths.

**Recommended:** 1 (enabled) for all repeaters.

---

### Advertisement Intervals

Repeaters periodically announce themselves so other nodes can discover them. There are two types:

| Setting | Type | Scope | Value Unit | MeshCore Default | Purpose |
|---------|------|-------|------------|------------------|---------|
| `advert.interval` | Local (zero-hop) | Immediate neighbors only | Minutes | 0 (disabled) | Neighbor discovery, NOT forwarded |
| `flood.advert.interval` | Network-wide | Entire mesh | Hours | 12 hrs | Network-wide discovery, IS forwarded |

Having all the repeaters adverting too fast will cause mesh congestion, so longer intervals are necessary to prevent too much traffic.

**How they interact:** The local advert timer automatically adjusts when a flood advert is sent to prevent overlap.

**Recommended values:**
- `advert.interval`: 240 minutes (4 hours) — frequent enough for neighbor discovery without excessive traffic
- `flood.advert.interval`: 12 hours — announces your repeater across the mesh twice daily

---

### Radio Parameters (`radio`)

Sets all LoRa radio parameters in a single command.

**Format:** `frequency,bandwidth,spreading_factor,coding_rate`

| Parameter | Sydney Value | MeshCore Default | What it means |
|-----------|--------------|------------------|---------------|
| **Frequency** | 915.8 MHz | 915.0 MHz | Operating frequency within Australian ISM band (915-928 MHz) |
| **Bandwidth** | 250 kHz | 250 kHz | Channel width. Wider = faster data rate but shorter range |
| **Spreading Factor** | 11 | 10 | Chirp spread. Higher = longer range, slower speed, better noise immunity |
| **Coding Rate** | 5 | 5 | Forward error correction (4/5). Higher = more redundancy, slower |

**Important:** All nodes on the Sydney mesh MUST use these exact parameters to communicate. The SF11 is a deliberate modification from the standard Australia preset (SF10) for improved range.

---

## Role-Specific Settings Explained

These four settings work together to optimize mesh performance based on your repeater's position and traffic load.

### Overview

| Setting | MeshCore Default | What it controls | Key insight |
|---------|------------------|------------------|-------------|
| `txdelay` | 0.5 | Wait time before retransmitting floods | Higher = lets other nodes go first |
| `direct.txdelay` | 0.2 | Wait time before retransmitting direct packets | Usually lower than txdelay |
| `rxdelay` | 0 (disabled) | Signal-based processing priority | Higher = waits for strongest signal copy |
| `af` | 1.0 (50% duty) | Radio silence after transmitting | Higher = more listening, less transmitting |

---

### Transmission Delay (`txdelay` / `direct.txdelay`)

Controls how long a repeater waits before retransmitting a packet it needs to forward.

#### The Formula

```
max_delay = estimated_airtime × txdelay × 5
actual_delay = random(0, max_delay)
```

**Step by step:**
1. Calculate estimated airtime for the packet (based on size and radio settings)
2. Multiply by txdelay factor (e.g., 2.0 for CRITICAL nodes)
3. Multiply by 5 to get maximum delay window
4. Pick a **random** delay between 0 and max_delay

#### Why Randomization?

Without random delays, repeaters at similar distances would always collide. The randomness creates natural separation — even two repeaters with identical settings won't transmit at the exact same moment.

#### Why is This Needed?

When a packet floods the mesh, multiple repeaters receive it almost simultaneously. Without transmission delays:

| Problem | What happens |
|---------|--------------|
| **Packet collisions** | Multiple transmissions overlap, corrupting both signals |
| **Wasted airtime** | Failed transmissions consume channel capacity |
| **Reduced reliability** | Messages fail to propagate properly |

#### Effect of Different Values

| txdelay | Delay Window | Collision Risk | Propagation Speed |
|---------|--------------|----------------|-------------------|
| **High (2.0)** | Wide | ✅ Lower | Slower |
| **Medium (0.8)** | Moderate | Moderate | Moderate |
| **0.5 (default)** | Moderate-Narrow | Moderate | Moderate-Fast |
| **Low (0.3)** | Narrow | ⚠️ Higher | Faster |

#### Why CRITICAL Nodes Use Higher Values

Hilltop/tower repeaters typically hear many other repeaters. When they receive a flooded packet, dozens of other nodes may have also received it.

If a critical node retransmits quickly (low txdelay), it might:
- Collide with transmissions from nodes that received the packet slightly later
- "Step on" retransmissions from lower-elevation nodes
- Cause the packet to fail reaching nodes that could only hear the critical repeater

**By using higher txdelay, critical nodes essentially say: "I'll wait and let the smaller nodes go first."**

This improves overall network reliability:
- Local nodes serve their immediate area quickly
- Critical nodes fill in gaps after the initial wave
- Fewer collisions occur in the critical node's wide coverage area

#### txdelay vs direct.txdelay

| Setting | MeshCore Default | Applies to | Why different values? |
|---------|------------------|------------|----------------------|
| `txdelay` | 0.5 | **Flooded packets** (broadcast to all) | Many nodes retransmit, high collision risk |
| `direct.txdelay` | 0.2 | **Direct packets** (routed point-to-point) | Follows predetermined path, fewer nodes involved, lower collision risk |

Direct packets typically use **lower** delays because only nodes along the specific route retransmit, not the entire mesh.

---

### Airtime Factor (`af`)

Enforces a "radio silence" period after each transmission, implementing a duty cycle limit.

#### The Formula

```
silence_period = transmission_time × airtime_factor
```

#### How It Works

After transmitting a packet, the repeater:
1. Calculates how long the transmission took (in milliseconds)
2. Multiplies by the airtime factor
3. Waits that long before transmitting again
4. During this silence period, the repeater can only **listen**

#### Example

| Transmission | af | Silence Period | Can transmit again after |
|--------------|----|--------------|-----------------------|
| 200ms packet | 1 | 200ms | 200ms |
| 200ms packet | 2 | 400ms | 400ms |
| 200ms packet | 3 | 600ms | 600ms |

#### Why This Matters

| Benefit | Explanation |
|---------|-------------|
| **Prevents channel hogging** | High-traffic nodes (hilltop repeaters) would otherwise dominate the airwaves |
| **Improves fairness** | Gives other nodes a chance to transmit |
| **Reduces collisions** | More listening time = better awareness of channel activity |

#### Recommended Values by Role

| af Value | Effective Duty Cycle | Best for |
|----------|---------------------|----------|
| **1.0 (default)** | 50% (transmit:listen = 1:1) | Local/endpoint nodes with few neighbors |
| **1.5** | 40% (1:1.5) | Standard suburban repeaters |
| **2** | 33% (1:2) | Link nodes bridging regions |
| **3** | 25% (1:3) | Critical infrastructure seeing heavy traffic |

**Rule of thumb:** Higher af = more conservative = more listening, less transmitting

---

### Receive Delay (`rxdelay`) — Signal-Based Processing

The `rxdelay` setting is more sophisticated than a simple timer. It uses **signal strength** to determine which copy of a packet to process first.

#### The Formula

```
delay = (rxdelay^(0.85 - score) - 1.0) × airtime
```

Where:
- **rxdelay** = configured base value (e.g., 10, 15)
- **score** = signal quality metric (0.0 to 1.0) calculated from SNR relative to the spreading factor threshold
- **airtime** = transmission time of the packet

#### What This Means in Practice

| Signal Strength | Score | Calculated Delay | Result |
|-----------------|-------|------------------|--------|
| **Strong** (nearby node) | ~0.8 | Short (~50ms) | Processed first |
| **Medium** | ~0.5 | Moderate (~300ms) | Processed after stronger signals |
| **Weak** (distant node) | ~0.3 | Long (~800ms) | Processed last, often discarded |

#### Why This Matters

In a mesh, the same flooded packet often arrives from **multiple sources** at different times and signal strengths. The rxdelay system creates intelligent packet selection:

1. **Strong signal copy arrives** → Short delay calculated → Processed quickly
2. **Weak signal copy arrives** → Long delay calculated → Sits in queue
3. **Strong copy finishes processing** → Packet marked as "seen"
4. **Weak copy's delay expires** → Already marked "seen" → **Discarded as duplicate**

**Result:** The mesh naturally prefers relaying packets received via the **strongest/most reliable path**.

#### Practical Example

A hilltop repeater receives the same packet from two sources:

| Source | Signal | Score | Delay | What happens |
|--------|--------|-------|-------|--------------|
| **Node A** (nearby) | Strong | 0.8 | ~50ms | Processed first, packet forwarded |
| **Node B** (distant) | Weak | 0.3 | ~800ms | By the time delay expires, packet already marked "seen" — discarded |

#### Why CRITICAL Nodes Use Higher rxdelay

Critical infrastructure nodes (hilltops/towers) hear **many** neighbors. When a packet floods:
- They receive it from potentially dozens of sources
- Some copies have excellent signal, others are weak
- Higher rxdelay (15) gives them more time to receive the **best copy** before committing to forward it

Local nodes use rxdelay 0 (the **MeshCore default**) because they typically only hear one or two sources — no need to wait for a "better" copy that won't arrive.