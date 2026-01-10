---
title: New South Wales Meshcore Network & Repeater Configuration Guide
---

<style>
/* Responsive table wrapper */
table {
  display: block;
  width: 100%;
  overflow-x: auto;
  -webkit-overflow-scrolling: touch;
}

@media screen and (max-width: 768px) {
  table {
    font-size: 14px;
  }
  table td, table th {
    padding: 6px 8px;
    word-break: break-word;
  }
}

.cmd-block {
  background: #eef;
  border: 1px solid #e8e8e8;
  border-radius: 3px;
  padding: 8px 12px;
  font-family: "Courier New", Courier, monospace;
  font-size: 15px;
  overflow-x: auto;
  margin: 16px 0;
  color: #111;
}
.cmd-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 3px 0;
}
.cmd-row code {
  background: none;
  border: none;
  padding: 0;
  font-size: inherit;
  color: #111;
}
.cmd-row button {
  background: #fff;
  border: 1px solid #ccc;
  border-radius: 3px;
  padding: 2px 10px;
  cursor: pointer;
  font-size: 12px;
  color: #333;
}
.cmd-row button:hover {
  background: #eee;
}
</style>

<script>
function copyCmd(text, btn) {
  navigator.clipboard.writeText(text).then(() => {
    btn.textContent = '✓ Copied';
    btn.style.color = '#1a7f37';
    setTimeout(() => {
      btn.textContent = 'Copy';
      btn.style.color = '';
    }, 1500);
  });
}
</script>

## Table of Contents

- [Getting Started with MeshCore](#getting-started-with-meshcore)
  - [Setting Up Your Companion](#setting-up-your-companion)
  - [Radio Settings](#radio-settings)
  - [Channels](#channels)
  - [Privacy Considerations](#privacy-considerations)
- [Repeater Naming & Setup](#repeater-naming--setup)
  - [Naming Convention](#naming-convention)
  - [Setting Up Your Repeater](#setting-up-your-repeater)
- [Repeater Configuration Profiles](#repeater-configuration-profiles)
  - [🔴 CRITICAL — Hilltop/Tower Infrastructure](#critical--hilltoptower-infrastructure)
  - [🟠 LINK — Mid-elevation Bridge](#link--mid-elevation-bridge)
  - [🟡 STANDARD — Suburban Coverage](#standard--suburban-coverage)
  - [🟢 LOCAL — Ground-level/Indoor](#local--ground-levelindoor)
- [Common Settings (All Repeaters)](#common-settings-all-repeaters)
- [Understanding the Settings](#understanding-the-settings)
  - [AGC Reset Interval](#agc-reset-interval)
  - [Multiple Acknowledgments](#multiple-acknowledgments)
  - [Advertisement Intervals](#advertisement-intervals)
  - [Radio Parameters](#radio-parameters)
- [Role-Specific Settings Explained](#role-specific-settings-explained)
  - [Transmission Delay](#transmission-delay)
  - [Airtime Factor](#airtime-factor)
  - [Receive Delay](#receive-delay)

---

## Getting Started with MeshCore {#getting-started-with-meshcore}

📺 Helpful video explaining MeshCore. How it works and how to use/set it up. [How to get started with MeshCore off grid text messaging](https://www.youtube.com/watch?v=t1qne8uJBAc&t=372s)

---

### Setting Up Your Companion {#setting-up-your-companion}

**1. Flash and setup**

Flash using [Meshcore firmware flasher](https://flasher.meshcore.co.uk/). It is important you decide now what mode of connection to the node you are using, as the firmware supports one connection type at a time (BLE, USB, WiFi). Make sure to erase before flashing MeshCore for the first time.

**2. Connect and setup**

Now connect to your companion using the method you chose and configure the name, radio settings, and channels.

- The name and radio settings are set in the settings page (found under the `⚙️` at the top right of the app). Make sure to tap the `✔️` at the top right to save the settings. Wait for the green success notification.

- The channels are added from the channel page at the top right `⋮` → `+ Add Channel` → `Join a Hashtag Channel`. Then enter the name of the channel (shown below, such as `test`) and press join channel.

**3. Join the mesh**

Send an advert by hitting the `Advert` (button next to `⚙️`) → `Send Flood Advert` to send your node name to the mesh. Directly reachable repeaters can be discovered by `🔧` → `Discover Nearby Nodes` → `Discover Repeaters`. After a short while, repeaters within range should reply with their info. You can hit the `+` to add them to your contacts.

Send a greeting to the public channel or a `test` to the **#test** channel. The **Public** channel is used for general chat, and if someone sees your greeting they will likely reply. The **test** channel is primarily used for sending test messages to check your connection to the mesh. There are bots on the test channel that will reply to `test`, `ping` or `path` and will respond accordingly with a reply. When a message is sent, next to the message it will say `heard X repeats`, with X representing the number of repeaters that you heard retransmitting your sent message. If this is 0, then a repeater was unable to be reached, or the radio settings are wrong. Double check the radio settings and then check the [NSW Meshcore Map](https://nswmesh.github.io/NSW-Sydney-Meshcore-Map/) to see if there are repeaters near you. Double click or long press on your location to check if there is expected coverage at your location. In order to be able to reach a repeater, you must have direct line of sight to it due to the low transmission powers. If none are reachable, try standing outside with the antenna pointing upwards, or find some height to clear buildings.

Repeaters send a local advert (an advert that can be heard if you are directly connected to that repeater only) every 240 minutes and a flood advert every 12 hours. This means that the node list can take a while to populate. Companions also only advert when manually triggered. This means that a connection to the mesh can be present, but there is not an advert being sent at that moment. (This is good as it means that the mesh is not congested.)


> **Important:** All nodes connecting to the Sydney mesh must use the **Australia preset** with SF11 (modified from the default SF10).
> **Why SF11?** The NSW Mesh uses SF11 instead of the standard SF10 to provide improved range across Sydney's unique geography and wide user spacing. This means we are **not directly interoperable** with standard ANZ meshes running SF10.

---

### Radio Settings {#radio-settings}

| Setting | Value |
|---------|-------|
| Frequency | 915.800 MHz |
| Bandwidth | 250.0 kHz |
| Spreading Factor (SF) | **11** ⚠️ |
| Coding Rate (CR) | 5 |

---

### Channels {#channels}

| Channel | Key |
|---------|-----|
| Public | Public Channel |
| Test (with test bot) | `#test` (auto-generated) |
| Emergency  | `#emergency` (auto-generated) |
| Sydney | `#sydney` (auto-generated) |
| NSW Wide | `#nsw` (auto-generated) |
| Macarthur | `#macarthur` (auto-generated) |
| Nepean | `#nepean` (auto-generated) |
| Central Coast | `#centralcoast` (auto-generated) |
| Illawarra | `#illawarra` (auto-generated) |
| Discord Bridge AI bot Jeff | `#jeff` (auto-generated) |
| Discord Bridge AI bot RoloJnr | `#rolojnr` (auto-generated) |

---

### Privacy Considerations {#privacy-considerations}

> ⚠️ **Important:** Anything sent via adverts or on public channels, including `#` channels that are publicly known, is subject to whatever the receiver chooses to do with the data.

Messages, locations, and other data sent to the mesh should be considered **public information**. Be aware that:

- **Internet-accessible tools exist** — There are maps and other services that display packet and location data from the mesh publicly on the internet.
- **No guaranteed privacy** — Your messages are only as private as the trust you place in **every single person** who receives them. This means privacy is only guaranteed in `Direct Messages` and `Private Channels` to the degree that you trust the privacy of the key, and the users with the keys.
- **Data persistence** — Once data is transmitted, you have no control over how it is stored, shared, or used by recipients.
- **Location precision** — Locations set on your device and repeaters are transmitted with high precision. You can use this to your advantage by setting a location that is approximate rather than exact — close enough to be useful for planning and coverage assessment, but offset enough to provide a buffer against nefarious use. Consider setting your location to a nearby intersection, park, or general area rather than your exact address.

**Take care** if you are not 100% certain who will receive your data. Avoid sharing sensitive personal information, precise home locations, or anything you would not want publicly accessible.

**Encryption:** MeshCore uses **AES-256-CTR** encryption for securing communications. This means that for `Channels` and `Direct Messages` with secured keys and trustworthy recipients, your data is more than safe.

---

## Repeater Naming & Setup {#repeater-naming--setup}

### Naming Convention {#naming-convention}

| Type | Naming | Example |
|------|-------------|---------|
| Fixed repeaters | Name by location (suburb, hill, building) | `⚡️- Mount Colah`, `🌱 - Camperdown`, `Davo - Centrepoint Tower` |
| Mobile repeaters | Include "mobile" in name | `Johns Mobile` |

---

### Setting Up Your Repeater {#setting-up-your-repeater}

**1. Flash and Config Repeater**

Flash the repeater using [Meshcore firmware flasher](https://flasher.meshcore.co.uk/). When flashed, the node will have a random public key. The first two characters of this key are the prefix. This is used to show routing paths for messages. If multiple nodes have the same prefix, it can cause confusion for the route of the messages. In order to fix this, go to the [NSW key generator and configurator](https://nswmesh.au/docs/meshcore/key_generator) and tick `Avoid NSW Repeaters`. This will avoid prefixes already in the mesh. Then press `Generate Key` and wait for it to finish. Once the key is generated, it can be sent to the device from the `Send To Device` button. This may fail if the COM port is still open. To fix that, unplug and plug the node back in. Now you can go to [Meshcore USB Config](https://config.meshcore.dev/) and set the radio settings, name, and location. We encourage all repeaters to have a location for mesh planning purposes. It doesn't need to be exact, but accurate positions help other users with signal and line-of-sight tools. Also set your guest password to `guest` to allow other mesh users to query your repeater's status and neighbors (without admin access).

**2. ⏰ Sync the Clock — REQUIRED STEP**

> ⚠️ **CRITICAL:** Your repeater **will not work properly** without syncing the clock first!

Repeaters default to a clock time of **15 May 2024** on every reboot unless connected to a computer. 

**Why this matters:**
- ❌ **Your repeater will be invisible** — Other nodes won't hear your adverts correctly
- ❌ **Messages may not route properly** — Time synchronization is critical for mesh routing
- ❌ **Your node appears offline** — Shows at bottom of contact lists (sorted by Last Heard as an old date)
- ❌ **Network diagnostics fail** — Path tracking and network health monitoring rely on accurate timestamps

**How to sync the clock:**
1. Log into your repeater via your companion node
2. Go to `Settings` tab → Scroll to `Sync Clock` → Tap it
3. Wait for green success notification
4. Tap `Advert` to tell the repeater to send an advert
5. Wait for green success notification
4. ✅ **Verify:** Check that the "Last Heard" time for your repeater in your companions contact list is current (not showing May 2024)

> 💡 **Note:** You must re-sync the clock after **every power cycle or reboot** unless your repeater has GPS or remains connected to a computer.

**3. Configure repeater CLI settings**

Once logged in and the clock is synced, go to the `>_` - **`Command Line`** tab and enter the commands from the profiles and common settings below with your chosen repeater profile. Copy and paste each line and send. Wait up to 30 seconds to see an `OK` response - if no response then resend command.


📺 [Watch: More about repeaters (video, 11:18)](https://youtu.be/t1qne8uJBAc?t=678)

---

## Repeater Configuration Profiles {#repeater-configuration-profiles}

Choose the profile below that matches your repeater's role and position in the mesh network. These settings work together to optimize packet flow and minimize collisions based on your repeater's location and how many neighbors it can hear.

> **📝 MeshCore Defaults:** `txdelay=0.5`, `direct.txdelay=0.2`, `rxdelay=0`, `af=1.0`. All profiles below modify these to optimize for the Sydney mesh.

---

### 🔴 CRITICAL — Hilltop/Tower Infrastructure {#critical--hilltoptower-infrastructure}

> **Role:** Highest elevation, most neighbors, backbone of the mesh

**When to use:** Your repeater is on a tall hilltop, tower, or tall building with clear line-of-sight to many other nodes. It can see most of the mesh and is an important hop for many routes. You can see 20+ neighbors well and your repeater is a key link in the network backbone.

<div class="cmd-block">
<div class="cmd-row"><code>set txdelay 2</code><button onclick="copyCmd('set txdelay 2', this)">Copy</button></div>
<div class="cmd-row"><code>set direct.txdelay 2</code><button onclick="copyCmd('set direct.txdelay 2', this)">Copy</button></div>
<div class="cmd-row"><code>set rxdelay 3</code><button onclick="copyCmd('set rxdelay 3', this)">Copy</button></div>
<div class="cmd-row"><code>set af 3</code><button onclick="copyCmd('set af 3', this)">Copy</button></div>
</div>

**Why these values:**
- **High txdelay (2.0):** Waits longer before retransmitting, letting smaller nodes serve their local areas first. Reduces collisions in your wide coverage area.
- **rxdelay (3):** Standard rxdelay for all Sydney mesh repeaters. Provides optimal signal-based packet selection timing.
- **High af (3):** Enforces 25% duty cycle. Critical nodes see heavy traffic; this prevents channel hogging and gives other nodes a chance to transmit.

---

### 🟠 LINK — Mid-elevation Bridge {#link--mid-elevation-bridge}

> **Role:** Connects critical nodes to local coverage, moderate neighbor count

**When to use:** Your repeater bridges between tall infrastructure and suburban coverage. You can see some critical nodes and some local nodes (15-20 neighbors typical).

<div class="cmd-block">
<div class="cmd-row"><code>set txdelay 1.5</code><button onclick="copyCmd('set txdelay 1.5', this)">Copy</button></div>
<div class="cmd-row"><code>set direct.txdelay 1</code><button onclick="copyCmd('set direct.txdelay 1', this)">Copy</button></div>
<div class="cmd-row"><code>set rxdelay 3</code><button onclick="copyCmd('set rxdelay 3', this)">Copy</button></div>
<div class="cmd-row"><code>set af 2</code><button onclick="copyCmd('set af 2', this)">Copy</button></div>
</div>

**Why these values:**
- **Moderate txdelay (1.5):** Balances responsiveness with collision avoidance. You're important for connectivity but not the primary backbone.
- **rxdelay (3):** Standard rxdelay for all Sydney mesh repeaters. Provides optimal signal-based packet selection timing.
- **Moderate af (2):** 33% duty cycle balances your bridging role with fair channel access.

---

### 🟡 STANDARD — Suburban Coverage {#standard--suburban-coverage}

> **Role:** Average positioning, serves local area, moderate neighbors

**When to use:** Typical deployment. Your repeater is in an elevated position, serving a more localized area. You see 5-10 neighbors.

<div class="cmd-block">
<div class="cmd-row"><code>set txdelay 0.8</code><button onclick="copyCmd('set txdelay 0.8', this)">Copy</button></div>
<div class="cmd-row"><code>set direct.txdelay 0.4</code><button onclick="copyCmd('set direct.txdelay 0.4', this)">Copy</button></div>
<div class="cmd-row"><code>set rxdelay 3</code><button onclick="copyCmd('set rxdelay 3', this)">Copy</button></div>
<div class="cmd-row"><code>set af 1.5</code><button onclick="copyCmd('set af 1.5', this)">Copy</button></div>
</div>

**Why these values:**
- **Lower txdelay (0.8):** More responsive for local coverage. Fewer neighbors means lower collision risk.
- **rxdelay (3):** Standard rxdelay for all Sydney mesh repeaters. Provides optimal signal-based packet selection timing.
- **Lower af (1.5):** 40% duty cycle. Reasonable responsiveness while still being a good mesh citizen.

---

### 🟢 LOCAL — Ground-level/Indoor {#local--ground-levelindoor}

> **Role:** Low elevation, few neighbors, serves immediate area

**When to use:** Indoor repeater, low rooftop repeater, ground-level installation, or low node without clear line of sight to many other repeaters. You only see 1-3 neighbors and primarily serve your immediate area.

<div class="cmd-block">
<div class="cmd-row"><code>set txdelay 0.3</code><button onclick="copyCmd('set txdelay 0.3', this)">Copy</button></div>
<div class="cmd-row"><code>set direct.txdelay 0.1</code><button onclick="copyCmd('set direct.txdelay 0.1', this)">Copy</button></div>
<div class="cmd-row"><code>set rxdelay 3</code><button onclick="copyCmd('set rxdelay 3', this)">Copy</button></div>
<div class="cmd-row"><code>set af 1</code><button onclick="copyCmd('set af 1', this)">Copy</button></div>
</div>

**Why these values:**
- **Minimal txdelay (0.3):** Maximum responsiveness. With few neighbors, collision risk is low.
- **rxdelay (3):** Standard rxdelay for all Sydney mesh repeaters. Provides optimal signal-based packet selection timing.
- **Low af (1):** 50% duty cycle. You're not creating congestion with your limited coverage.

---

## Common Settings (All Repeaters) {#common-settings-all-repeaters}

Apply these settings to **all repeaters** regardless of role:

> **📝 Note:** Most of these differ from MeshCore defaults. See the Quick Reference table below for default comparisons.

<div class="cmd-block">
<div class="cmd-row"><code>set agc.reset.interval 500</code><button onclick="copyCmd('set agc.reset.interval 500', this)">Copy</button></div>
<div class="cmd-row"><code>set multi.acks 1</code><button onclick="copyCmd('set multi.acks 1', this)">Copy</button></div>
<div class="cmd-row"><code>set advert.interval 240</code><button onclick="copyCmd('set advert.interval 240', this)">Copy</button></div>
<div class="cmd-row"><code>set flood.advert.interval 12</code><button onclick="copyCmd('set flood.advert.interval 12', this)">Copy</button></div>
<div class="cmd-row"><code>set guest.password guest</code><button onclick="copyCmd('set guest.password guest', this)">Copy</button></div>
</div>

### Quick Reference

| Setting | Value | MeshCore Default | What it does |
|---------|-------|------------------|--------------|
| `agc.reset.interval` | 500 | 0 (disabled) | AGC reset every 500 seconds (~8 min) to prevent sensitivity drift |
| `multi.acks` | 1 | 1 | Send redundant ACKs for better delivery reliability |
| `advert.interval` | 240 | 0 | Local advert every 240 minutes (neighbors only) |
| `flood.advert.interval` | 12 | 12 | Network-wide advert every 12 hours |
| `guest.password` | guest | (none) | Standard guest access password |
| `radio` | 915.8,250,11,5 | 915.0,250,10,5 | Sydney mesh radio parameters (freq, bw, sf, cr) |

---

## Understanding the Settings {#understanding-the-settings}

### AGC Reset Interval (`agc.reset.interval`) {#agc-reset-interval}

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

### Multiple Acknowledgments (`multi.acks`) {#multiple-acknowledgments}

Controls whether redundant ACKs are sent for direct (point-to-point) messages.

**How it works:**
- When enabled (1): Sends two ACK packets — first a "multi-ack", then the standard ACK
- When disabled (0): Sends only a single ACK packet

**Why use it:** ACKs are small packets that can easily be lost. Sending redundant ACKs significantly improves delivery confirmation reliability, especially over longer paths.

**Recommended:** 1 (enabled) for all repeaters.

---

### Advertisement Intervals {#advertisement-intervals}

Repeaters periodically announce themselves so other nodes can discover them. There are two types:

| Setting | Type | Scope | Value Unit | MeshCore Default | Purpose |
|---------|------|-------|------------|------------------|---------|
| `advert.interval` | Local (zero-hop) | Immediate neighbors only | Minutes | 0 (disabled) | Neighbor discovery, NOT forwarded |
| `flood.advert.interval` | Network-wide | Entire mesh | Hours | 12 hrs | Network-wide discovery, IS forwarded |

Having all repeaters advertising too fast will cause mesh congestion, so longer intervals are necessary to prevent too much traffic.

**How they interact:** The local advert timer automatically adjusts when a flood advert is sent to prevent overlap.

**Recommended values:**
- `advert.interval`: 240 minutes (4 hours) — frequent enough for neighbor discovery without excessive traffic
- `flood.advert.interval`: 12 hours — announces your repeater across the mesh twice daily

---

### Radio Parameters (`radio`) {#radio-parameters}

Sets all LoRa radio parameters in a single command.

**Format:** `frequency,bandwidth,spreading_factor,coding_rate`

| Parameter | Sydney Value | MeshCore Default | What it means |
|-----------|--------------|------------------|---------------|
| **Frequency** | 915.8 MHz | 915.0 MHz | Operating frequency within Australian ISM band (915-928 MHz) |
| **Bandwidth** | 250 kHz | 250 kHz | Channel width. Wider = faster data rate but shorter range |
| **Spreading Factor** | 11 | 10 | Chirp spread. Higher = longer range, slower speed, better noise immunity |
| **Coding Rate** | 5 | 5 | Forward error correction (4/5). Higher = more redundancy, slower |

**Important:** All nodes on the Sydney mesh MUST use these exact parameters to communicate. The SF11 is a deliberate modification from the standard Australia preset (SF10) for improved range.

#### Frequency (915.800 MHz)

The operating frequency determines which part of the radio spectrum your node transmits and receives on. All nodes must use the **exact same frequency** to communicate.

| Aspect | Details |
|--------|---------|
| **Australian ISM Band** | 915-928 MHz (license-free for low-power devices) |
| **Why 915.8 MHz?** | Slightly offset from default to reduce interference with other LoRa networks |
| **Regulatory** | Must comply with ACMA regulations for power and duty cycle |

> **Important:** Using a different frequency means you cannot communicate with the mesh at all.

---

#### Bandwidth (BW) — 250 kHz

Bandwidth determines the width of the frequency channel used for transmission. Think of it like the "width of the road" your signal travels on.

| Bandwidth | Data Rate | Range | Noise Immunity | Best For |
|-----------|-----------|-------|----------------|----------|
| **500 kHz** | Fastest | Shortest | Lower | High-throughput, short range |
| **250 kHz** ✅ | Moderate | Moderate | Moderate | Balanced performance (Sydney mesh) |
| **125 kHz** | Slower | Longer | Higher | Maximum range, low throughput |
| **62.5 kHz** | Slowest | Longest | Highest | Extreme range, minimal data |

**Trade-offs:**
- **Wider bandwidth (500 kHz):** Faster data transfer, but signal is more susceptible to noise and has shorter range
- **Narrower bandwidth (125 kHz):** Longer range and better noise immunity, but slower data transfer and higher airtime per packet

**Why 250 kHz for Sydney?** Provides a good balance between range and speed. Wide enough for reasonable message throughput, narrow enough for decent range across Sydney's urban and suburban areas.

---

#### Spreading Factor (SF) — 11

Spreading Factor is one of the most important LoRa parameters. It determines how the signal is "spread" across the bandwidth using chirp modulation.

| SF | Chirps per Symbol | Time on Air | Range | Sensitivity | Data Rate |
|----|-------------------|-------------|-------|-------------|-----------|
| **SF7** | 128 | Shortest | Shortest | -123 dBm | ~5.5 kbps |
| **SF8** | 256 | Short | Short | -126 dBm | ~3.1 kbps |
| **SF9** | 512 | Moderate | Moderate | -129 dBm | ~1.8 kbps |
| **SF10** | 1024 | Long | Long | -132 dBm | ~1.0 kbps |
| **SF11** ✅ | 2048 | Longer | Longer | -134.5 dBm | ~0.5 kbps |
| **SF12** | 4096 | Longest | Longest | -137 dBm | ~0.3 kbps |

**How it works:**
- Each increase in SF **doubles** the number of chirps per symbol
- This means each SF increase roughly **doubles the time on air**
- But also improves receiver sensitivity by ~2.5 dB (can hear weaker signals)

**Trade-offs:**

| Higher SF (e.g., SF11-12) | Lower SF (e.g., SF7-8) |
|---------------------------|------------------------|
| ✅ Longer range | ✅ Faster transmission |
| ✅ Better sensitivity | ✅ Lower airtime/power usage |
| ✅ Better penetration through obstacles | ✅ Higher throughput |
| ❌ Slower data rate | ❌ Shorter range |
| ❌ Higher airtime (battery drain) | ❌ More susceptible to interference |
| ❌ More susceptible to collisions | ❌ Requires stronger signal |

**Why SF11 for Sydney?**
- Sydney's mesh covers a large geographic area with users spread far apart
- SF11 provides ~3 dB better sensitivity than the standard Australia preset (SF10)
- This translates to roughly **40% more range** in ideal conditions
- The slower data rate is acceptable given the text-based nature of mesh messages

> ⚠️ **Compatibility Note:** SF11 nodes **cannot communicate** with SF10 nodes. All Sydney mesh participants must use SF11.

---

#### Coding Rate (CR) — 5

Coding Rate (also written as 4/5, 4/6, 4/7, or 4/8) determines the amount of Forward Error Correction (FEC) applied to transmissions.

| CR Setting | Ratio | Overhead | Error Correction | Airtime Impact |
|------------|-------|----------|------------------|----------------|
| **CR5** ✅ | 4/5 | 25% | Basic | Fastest |
| **CR6** | 4/6 | 50% | Moderate | +20% slower |
| **CR7** | 4/7 | 75% | Good | +40% slower |
| **CR8** | 4/8 | 100% | Maximum | +60% slower |

**How it works:**
- For every 4 bits of data, additional redundant bits are added
- CR 4/5 means 4 data bits + 1 redundancy bit = 5 total bits (25% overhead)
- CR 4/8 means 4 data bits + 4 redundancy bits = 8 total bits (100% overhead)

**Trade-offs:**

| Higher CR (4/7, 4/8) | Lower CR (4/5) |
|----------------------|----------------|
| ✅ Better error recovery | ✅ Faster transmission |
| ✅ More reliable in noisy environments | ✅ Lower airtime |
| ❌ Slower data rate | ❌ Less error tolerance |
| ❌ Higher airtime | ❌ May need retransmissions |

**Why CR 4/5 for Sydney?** The combination of SF11 already provides excellent noise immunity. CR 4/5 keeps airtime reasonable while still providing basic error correction. Higher CR would significantly increase already-long transmission times at SF11.

---

#### TX Power (Transmission Power)

While not explicitly set in the radio string, TX power determines how strong your transmitted signal is.

| Power Level | Typical Range | Battery Impact | Use Case |
|-------------|---------------|----------------|----------|
| **Low (10-14 dBm)** | Short (1-3 km) | Minimal | Indoor, close nodes |
| **Medium (17-20 dBm)** | Moderate (3-8 km) | Moderate | Suburban use |
| **High (22 dBm / 158 mW)** | Long (8-15+ km) | Higher | Hilltop repeaters, max range |

**Regulatory limits (Australia):**
- Maximum EIRP: 1 Watt (30 dBm) in the 915-928 MHz band
- Most devices max out at 22 dBm (~158 mW) from the radio chip
- Antenna gain adds to effective power (must stay under 1W EIRP total)

**Trade-offs:**

| Higher TX Power | Lower TX Power |
|-----------------|----------------|
| ✅ Longer range | ✅ Longer battery life |
| ✅ Better building penetration | ✅ Less interference to others |
| ❌ Faster battery drain | ❌ Shorter range |
| ❌ More interference potential | ❌ May not reach distant repeaters |

**Recommendations:**
- **Companions (mobile nodes):** Use maximum power (22 dBm) for best chance of reaching repeaters
- **Repeaters:** Use maximum power to provide widest coverage
- **Indoor/close range:** Can reduce power to save battery if needed

---

#### Combined Effect Summary

The Sydney mesh settings (915.8 MHz, 250 kHz BW, SF11, CR 4/5) are optimized for:

| Goal | How Settings Achieve It |
|------|------------------------|
| **Maximum range** | SF11 provides excellent sensitivity (-134.5 dBm) |
| **Reasonable speed** | 250 kHz BW and CR 4/5 keep airtime manageable |
| **Network compatibility** | All nodes use identical settings |
| **Regulatory compliance** | Within Australian ISM band limits |

**Approximate performance at these settings:**
- **Effective bitrate:** ~490 bps (after coding overhead)
- **Typical message airtime:** 1-3 seconds depending on length
- **Theoretical max range:** 15-20+ km line-of-sight (real-world varies significantly)

---

## Role-Specific Settings Explained {#role-specific-settings-explained}

These four settings work together to optimize mesh performance based on your repeater's position and traffic load.

### Overview

| Setting | MeshCore Default | What it controls | Key insight |
|---------|------------------|------------------|-------------|
| `txdelay` | 0.5 | Wait time before retransmitting floods | Higher = lets other nodes go first |
| `direct.txdelay` | 0.2 | Wait time before retransmitting direct packets | Usually lower than txdelay |
| `rxdelay` | 0 (disabled) | Signal-based processing priority | Higher = waits for strongest signal copy |
| `af` | 1.0 (50% duty) | Radio silence after transmitting | Higher = more listening, less transmitting |

---

### Transmission Delay (`txdelay` / `direct.txdelay`) {#transmission-delay}

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

### Airtime Factor (`af`) {#airtime-factor}

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

### Receive Delay (`rxdelay`) — Signal-Based Processing {#receive-delay}

The `rxdelay` setting is more sophisticated than a simple timer. It uses **signal strength** to determine which copy of a packet to process first.

#### The Formula

```
delay = (rxdelay^(0.85 - score) - 1.0) × airtime
```

Where:
- **rxdelay** = configured base value (e.g., 2, 4)
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

#### Why All Sydney Mesh Repeaters Use rxdelay 3

The Sydney mesh uses a standardized rxdelay of 3 for all repeater profiles. This provides:
- Consistent behavior across all repeaters in the network
- Sufficient time for signal-based packet selection without excessive delays
- A good balance between processing speed and selecting optimal signal paths
- Simplified configuration and troubleshooting

The MeshCore default is rxdelay 0 (disabled), but rxdelay 3 has been found to provide better overall mesh performance for the Sydney network.