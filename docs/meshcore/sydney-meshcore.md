---
title: New South Wales Meshcore Network & Repeater Configuration Guide
---

<style>
/* Responsive table styling */
.table-wrapper {
  overflow-x: auto;
  -webkit-overflow-scrolling: touch;
  margin: 1em 0;
}

table {
  display: table;
  width: 100%;
  border-collapse: collapse;
  margin: 1em 0;
  font-size: 15px;
}

table th, table td {
  padding: 10px 12px;
  text-align: left;
  border: 1px solid #ddd;
  white-space: nowrap;
}

table th {
  background: #f5f5f5;
  font-weight: 600;
}

table tr:nth-child(even) {
  background: #fafafa;
}

table tr:hover {
  background: #f0f0f0;
}

/* Allow wrapping on specific columns */
table td:last-child {
  white-space: normal;
  min-width: 150px;
}

@media screen and (max-width: 768px) {
  table {
    display: block;
    overflow-x: auto;
    font-size: 13px;
  }
  table th, table td {
    padding: 8px 10px;
  }
}

/* Code blocks in tables */
table code {
  background: #e8e8e8;
  padding: 2px 6px;
  border-radius: 3px;
  font-size: 13px;
  white-space: nowrap;
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

### Getting Started
- [Getting Started with MeshCore](#getting-started-with-meshcore)
  - [Setting Up Your Companion](#setting-up-your-companion)
  - [Radio Settings](#radio-settings)
  - [Channels](#channels)
  - [Privacy Considerations](#privacy-considerations)

### Repeater Setup
- [Repeater Naming & Setup](#repeater-naming--setup)
  - [Naming Convention](#naming-convention)
  - [Setting Up Your Repeater](#setting-up-your-repeater)

### Configuration Profiles
- [Repeater Configuration Profiles](#repeater-configuration-profiles)
  - [🔴 CRITICAL — Hilltop/Tower Infrastructure](#critical--hilltoptower-infrastructure)
  - [🟠 LINK — Mid-elevation Bridge](#link--mid-elevation-bridge)
  - [🟡 STANDARD — Suburban Coverage](#standard--suburban-coverage)
  - [🟢 LOCAL — Ground-level/Indoor](#local--ground-levelindoor)
- [Common Settings (All Repeaters)](#common-settings-all-repeaters)

### Technical Reference
- [Understanding the Settings](#understanding-the-settings)
  - [AGC Reset Interval](#agc-reset-interval)
  - [Multiple Acknowledgments](#multiple-acknowledgments)
  - [Advertisement Intervals](#advertisement-intervals)
  - [Power Saving Mode](#power-saving-mode)
  - [Radio Parameters](#radio-parameters)
- [Role-Specific Settings Explained](#role-specific-settings-explained)
  - [Transmission Delay](#transmission-delay)
  - [Airtime Factor](#airtime-factor)
  - [Receive Delay](#receive-delay)

---

## Getting Started with MeshCore {#getting-started-with-meshcore}

> 📺 **Video Guide:** [How to get started with MeshCore off grid text messaging](https://www.youtube.com/watch?v=t1qne8uJBAc&t=372s) — A helpful walkthrough explaining MeshCore, how it works, and how to set it up.

---

### Setting Up Your Companion {#setting-up-your-companion}

#### Step 1: Flash Your Device

Flash your device using the [Meshcore firmware flasher](https://flasher.meshcore.co.uk/).

> ⚠️ **Before flashing:** Choose your connection method now — the firmware only supports **one connection type at a time**:
> - **BLE** (Bluetooth Low Energy)
> - **USB** (wired connection)
> - **WiFi** (wireless)
>
> 💡 **First time flashing?** Make sure to select "Erase" before flashing MeshCore.

---

#### Step 2: Connect and Configure

Connect to your companion using your chosen method, then configure:

**Set Name and Radio Settings:**
1. Tap the `⚙️` icon (top right of the app)
2. Configure your name and radio settings - Preset `Australia: Victoria`
3. Tap `✔️` (top right) to save
4. Wait for the green success notification

**Add Channels:**
1. Tap `⋮` (top right) → `+ Add Channel` → `Join a Hashtag Channel`
2. Enter the channel name (e.g., `test`)
3. Press **Join Channel**

---

#### Step 3: Join the Mesh

**Advertise Your Node:**
1. Tap `Advert` (button next to `⚙️`) → `Send Flood Advert`
2. This broadcasts your node name to the mesh

**Discover Nearby Repeaters:**
1. Tap `🔧` → `Discover Nearby Nodes` → `Discover Repeaters`
2. Wait for repeaters within range to respond
3. Tap `+` to add them to your contacts

---

#### Step 4: Test Your Connection

**Send a Test Message:**
- Send a greeting to the **Public** channel (general chat), or
- Send `test`, `ping`, or `path` to the **#test** channel (bots will auto-reply)

**Check Your Results:**

After sending, look for `heard X repeats` next to your message:

| Result | Meaning |
|--------|--------|
| `heard 1+ repeats` | ✅ Success! Your message reached repeater(s) |
| `heard 0 repeats` | ❌ No repeater heard your message |

**If you see 0 repeats:**
1. Double-check your [radio settings](#radio-settings)
2. Check the [NSW Meshcore Map](https://nswmesh.github.io/NSW-Sydney-Meshcore-Map/) for nearby repeaters
3. Long-press your location on the map to check expected coverage
4. Try standing outside with antenna pointing upward
5. Find higher ground to clear buildings (line-of-sight is required)

---

#### Understanding Adverts

Advertisements are how nodes announce their presence on the mesh. Each advert packet contains:
- **Public Key** — Your node's unique cryptographic identity (32 bytes)
- **Timestamp** — When the advert was generated (used for routing and deduplication)
- **Digital Signature** — Cryptographic proof the advert is authentic (64 bytes)
- **Node Type** — Whether you're a companion, repeater, room server, or sensor
- **Name** — Your node's display name
- **Location** — Latitude/longitude (if sharing is enabled)

| Advert Type | Frequency | Scope | Effect |
|-------------|-----------|-------|--------|
| **Local advert** | Every 240 minutes | Directly connected repeaters only | Zero-hop broadcast — announces to immediate neighbors without flooding the network. Helps nearby nodes discover you quickly. |
| **Flood advert** | Every 24 hours | Entire mesh | Network-wide broadcast — every repeater that receives it will rebroadcast, spreading across the entire mesh. Use sparingly as it consumes significant airtime. |
| **Direct advert** | On login/manual | Specific path only | Point-to-point — sent along a known path to a specific node. Used when you need to refresh your presence with a distant node without flooding. Most efficient for targeted updates. |
| **Companion advert** | Manual only | When you trigger it | User-initiated flood advert from your companion node. |

> ⚠️ **Why 24 hours for flood adverts?** Each flood advert is rebroadcast by every repeater on the mesh. With many nodes, frequent flood adverts create substantial traffic that can congest the network and delay actual messages. A 24-hour interval balances network discovery with airtime conservation.

> 💡 **Note:** The node list takes time to populate. A connection may exist even without seeing adverts — this is normal and keeps the mesh uncongested.

---

> ⚠️ **IMPORTANT: Radio Compatibility**
>
> All nodes on the NSW mesh use the **Australia: Victoria** preset. This uses a very narrow 62.5 kHz bandwidth with SF7 and CR8 for optimal performance.
>
> **Why Australia: Victoria?**
> - **Narrow bandwidth (62.5 kHz)** provides better receiver sensitivity and noise rejection, allowing signals to be decoded at much lower power levels
> - **Lower spreading factor (SF7)** means faster transmission times, reducing airtime and collision risk
> - **Higher coding rate (CR8)** adds maximum forward error correction to compensate for the faster SF, improving reliability
> - The combination provides excellent range while keeping messages short and the channel responsive
>
> ❌ **Not interoperable** with standard ANZ meshes using different settings.

---

### Radio Settings {#radio-settings}

| Setting | Value |
|---------|-------|
| Frequency | 916.575 MHz |
| Bandwidth | 62.5 kHz |
| Spreading Factor (SF) | **7** |
| Coding Rate (CR) | **8** |

---

### Channels {#channels}

#### Core Channels

| Channel | Key | Purpose |
|---------|-----|---------|
| **Public** | Public Channel | General chat for all mesh users |
| **Test** | `#test` | Connection testing (bots auto-reply to `test`, `ping`, `path`) |
| **Emergency** | `#emergency` | Emergency communications only |

#### Regional Channels

| Channel | Key |
|---------|-----|
| Sydney | `#sydney` |
| NSW Wide | `#nsw` |
| Macarthur | `#macarthur` |
| Nepean | `#nepean` |
| Central Coast | `#centralcoast` |
| Illawarra | `#illawarra` |

#### Bot Bridges (Discord Integration)

| Channel | Key | Bot |
|---------|-----|-----|
| Jeff | `#jeff` | Discord bridge AI bot |
| RoloJnr | `#rolojnr` | Discord bridge AI bot |

> 💡 **Tip:** All `#` channel keys are auto-generated from the channel name.

---

### Privacy Considerations {#privacy-considerations}

> ⚠️ **Important:** Anything sent via adverts or on public channels (including publicly known `#` channels) is subject to whatever the receiver chooses to do with the data.

---

#### What You Should Know

Messages, locations, and other data sent to the mesh should be considered **public information**.

| Concern | Details |
|---------|--------|
| 🌐 **Internet-accessible tools** | Maps and services display packet and location data publicly online |
| 🔓 **No guaranteed privacy** | Messages are only as private as **every person** who receives them |
| 💾 **Data persistence** | Once transmitted, you have no control over storage, sharing, or use |
| 📍 **Location precision** | Locations are transmitted with high precision |

---

#### Location Privacy Tip

You can set an **approximate location** instead of your exact address:
- Close enough for planning and coverage assessment
- Offset enough to provide a privacy buffer
- Consider using a nearby intersection, park, or general area

---

#### Best Practices

✅ **Do:**
- Use `Direct Messages` for private conversations (with trusted keys)
- Use `Private Channels` for group privacy (with trusted participants)
- Set approximate locations for your devices

❌ **Don't:**
- Share sensitive personal information on public channels
- Broadcast your exact home address
- Assume any public message is private

---

#### Encryption

| Feature | Encryption | Privacy Level |
|---------|------------|---------------|
| Public channels | AES-256-CTR | 🔓 Public (key is shared) |
| `#` hashtag channels | AES-256-CTR | 🔓 Semi-public (key derived from name) |
| Private channels | AES-256-CTR | 🔒 Private (if key is secret) |
| Direct messages | AES-256-CTR | 🔒 Private (unique per conversation) |

> 💡 MeshCore uses **AES-256-CTR** encryption. With secured keys and trustworthy recipients, your data is cryptographically protected.

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

**Step 1: Flash the Firmware**

Flash the repeater using [Meshcore firmware flasher](https://flasher.meshcore.co.uk/). 

**Step 2: Generate a Unique Key Prefix**

When flashed, the node will have a random public key. The first two characters of this key are the **prefix**, which is used to show routing paths for messages. If multiple nodes have the same prefix, it can cause confusion for message routes.

To generate a unique prefix:
1. Go to the [NSW key generator and configurator](https://nswmesh.au/docs/meshcore/key_generator)
2. Tick `Avoid NSW Repeaters` — this avoids prefixes already in use on the mesh
3. Press `Generate Key` and wait for it to finish
4. Click `Send To Device` to upload the key to your repeater
   - **Note:** If this fails, the COM port may still be open. Unplug and plug the node back in, then retry.

**Step 3: Configure Radio Settings, Name, and Location**

Go to [Meshcore USB Config](https://config.meshcore.dev/) and configure:

- **Radio Settings:** Set the correct frequency, bandwidth, spreading factor, and coding rate (see [Radio Settings](#radio-settings))
- **Name:** Give your repeater a meaningful name following the [Naming Convention](#naming-convention)
- **Location:** Set your repeater's location for mesh planning purposes
  - Doesn't need to be exact, but accurate positions help other users with signal and line-of-sight tools
- **Guest Password:** Set to `guest` to allow other mesh users to query your repeater's status and neighbors (without admin access)
- **Send Advert:** After configuring your settings, click the `Send Advert` button in the USB Config tool to broadcast your repeater to the mesh
  - This announces your repeater's presence and allows other nodes to discover it and for it to appear in your node list for login
  - The USB Config tool will automatically sync the clock before sending the advert

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

**3. Configure Repeater CLI Settings**

Once logged in and the clock is synced, configure your repeater via the command line.

**How to enter commands:**
1. Go to the `>_` — **Command Line** tab
2. Copy each command from your chosen [profile](#repeater-configuration-profiles) below
3. Paste and send one command at a time
4. Wait up to 30 seconds for an `OK` response
5. If no response, resend the command

> 📺 **Video Guide:** [More about repeaters (11:18)](https://youtu.be/t1qne8uJBAc?t=678)

---

## Repeater Configuration Profiles {#repeater-configuration-profiles}

Choose the profile that matches your repeater's **role** and **position** in the mesh network.

### How to Choose Your Profile

| Profile | Elevation | Neighbors | Typical Location |
|---------|-----------|-----------|------------------|
| 🔴 **CRITICAL** | Highest | 20+ | Hilltop, tower, tall building |
| 🟠 **LINK** | Mid | 15-20 | Ridge, elevated position |
| 🟡 **STANDARD** | Average | 5-10 | Suburban roof, elevated home |
| 🟢 **LOCAL** | Low | 1-3 | Indoor, ground-level, low roof |

> **📝 MeshCore Defaults:** `txdelay=0.5`, `direct.txdelay=0.2`, `rxdelay=0`, `af=1.0`
>
> All profiles below modify these defaults to optimize for the Sydney mesh.

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

Apply these settings to **all repeaters** regardless of role.

> 📝 **Note:** Most of these differ from MeshCore defaults. See the Quick Reference table below.

### Commands to Apply

<div class="cmd-block">
<div class="cmd-row"><code>set agc.reset.interval 500</code><button onclick="copyCmd('set agc.reset.interval 500', this)">Copy</button></div>
<div class="cmd-row"><code>set multi.acks 1</code><button onclick="copyCmd('set multi.acks 1', this)">Copy</button></div>
<div class="cmd-row"><code>set advert.interval 240</code><button onclick="copyCmd('set advert.interval 240', this)">Copy</button></div>
<div class="cmd-row"><code>set flood.advert.interval 24</code><button onclick="copyCmd('set flood.advert.interval 24', this)">Copy</button></div>
<div class="cmd-row"><code>set guest.password guest</code><button onclick="copyCmd('set guest.password guest', this)">Copy</button></div>
<div class="cmd-row"><code>powersaving on</code><button onclick="copyCmd('powersaving on', this)">Copy</button></div>
</div>

### Quick Reference

| Setting | Value | MeshCore Default | What it does |
|---------|-------|------------------|--------------|
| `agc.reset.interval` | 500 | 0 (disabled) | AGC reset every 500 seconds (~8 min) to prevent sensitivity drift |
| `multi.acks` | 1 | 1 | Send redundant ACKs for better delivery reliability |
| `advert.interval` | 240 | 0 | Local advert every 240 minutes (neighbors only) |
| `flood.advert.interval` | 24 | 12 | Network-wide advert every 24 hours |
| `guest.password` | guest | (none) | Standard guest access password |
| `powersaving` | on | off | Power saving mode (light sleep between activity) |
| `radio` | 916.575,62.5,7,8 | 915.0,250,10,5 | NSW mesh radio parameters (freq, bw, sf, cr) |

---

## Understanding the Settings {#understanding-the-settings}

This section explains what each setting does and why it matters for mesh performance.

---

### AGC Reset Interval (`agc.reset.interval`) {#agc-reset-interval}

The **Automatic Gain Control (AGC)** in LoRa radios adjusts receiver sensitivity automatically. However, AGC can drift in busy environments, reducing sensitivity over time.

> ⚠️ **Known Issue:** Loud RF signals (in or out of band) can lock up the AGC, preventing the repeater from receiving packets until it's reset.

---

#### How AGC Drift Happens

```
Sensitivity over time:

  Optimal  ────╮           ╭────
               │  Lockup  │
  Degraded     ╰─────────╯
                    ↑
              Packets lost!
```

#### With AGC Reset (500s)

```
 0s     500s    1000s   1500s
  │       │       │       │
[RST]   [RST]   [RST]   [RST]
  │       │       │       │
  ↓ Sensitivity restored
```

---

**How it works:**
- The radio periodically re-initializes the receiver
- This resets AGC to optimal sensitivity
- Value is in **seconds**

**Recommended Values:**

| Value | Behavior | Use Case |
|-------|----------|----------|
| **500** ✅ | Reset every ~8 minutes | Recommended for all repeaters (especially noisy RF environments) |
| **0** | Disabled (MeshCore default) | AGC can lock up, but this is uncommon |

---

### Multiple Acknowledgments (`multi.acks`) {#multiple-acknowledgments}

Controls whether redundant ACKs are sent for direct (point-to-point) messages.

---

#### Single ACK vs Multi-ACK

**Single ACK (multi.acks = 0):**
```
Sender        Receiver
   │───Msg────>│
   │<──ACK────│
        ↓
   If lost --> fail
```

**Multi-ACK (multi.acks = 1) ✅:**
```
Sender        Receiver
   │───Msg────>│
   │<──ACK 1──│
   │<──ACK 2──│
        ↓
   Redundancy!
```

---

**How it works:**

| Value | ACK Behavior |
|-------|--------------|
| **1** (enabled) ✅ | Sends two ACK packets: a "multi-ack" first, then the standard ACK |
| **0** (disabled) | Sends only a single ACK packet |

**Why use it:**
- ACKs are small packets that can easily be lost
- Redundant ACKs significantly improve delivery confirmation reliability
- Especially helpful over longer paths

> 💡 **Recommended:** `1` (enabled) for all repeaters.

---

### Advertisement Intervals {#advertisement-intervals}

Repeaters periodically announce themselves so other nodes can discover them.

---

#### Local vs Flood Adverts

**Local Advert (240 min):**
```
     [You]
    /  |  \
   N1  N2  N3
   X   X   X   <-- stops here
```

**Flood Advert (24 hrs):**
```
     [You]
    /  |  \
   N1  N2  N3
   |   |   |   <-- forwards
   v   v   v
  ...spreads...
```

---

**Two Types of Adverts:**

| Setting | Type | Scope | Value Unit | MeshCore Default | Purpose |
|---------|------|-------|------------|------------------|---------|
| `advert.interval` | Local (zero-hop) | Immediate neighbors only | Minutes | 0 (disabled) | Neighbor discovery, NOT forwarded |
| `flood.advert.interval` | Network-wide | Entire mesh | Hours | 12 hrs | Network-wide discovery, IS forwarded |

> ⚠️ **Flood Advert Interval Range:** MeshCore enforces a speed of **48 hours** for the flood advert interval to prevent network congestion.

Having all repeaters advertising too fast will cause mesh congestion, so longer intervals are necessary to prevent too much traffic. Each flood advert is rebroadcast by every repeater on the mesh, so the total airtime consumed scales with the number of nodes.

**How they interact:** The local advert timer automatically adjusts when a flood advert is sent to prevent overlap.

**Recommended values:**
- `advert.interval`: 240 minutes (4 hours) — frequent enough for neighbor discovery without excessive traffic
- `flood.advert.interval`: 24 hours — announces your repeater across the mesh once daily, minimizing network-wide traffic while maintaining presence

---

### Power Saving Mode (`powersaving`) {#power-saving-mode}

Power saving mode puts the repeater into **light sleep** between periods of activity to reduce power consumption.

---

#### How It Works

When enabled, the repeater follows this cycle:

1. **Active period** (5 seconds) — Process packets, send adverts, handle requests
2. **Check for pending work** — Are there packets queued or tasks running?
3. **If no pending work** → Enter **light sleep** for up to 30 minutes
4. **Wake triggers:**
   - ⏰ Timer expires (30 minutes max)
   - 📡 LoRa packet received (DIO1 interrupt)
5. **Repeat cycle**

```
┌──────────┐     ┌──────────┐     ┌──────────┐
│  Active  │────>│ Pending? │────>│  Sleep   │
│   (5s)   │     │          │ No  │ (≤30min) │
└──────────┘     └────┬─────┘     └────┬─────┘
      ▲               │Yes             │
      │               v                │
      │          ┌──────────┐          │
      └──────────│  Extend  │<─────────┘
                 │  +5 sec  │   wake
                 └──────────┘
```

---

#### Power Consumption

| Mode | Behavior | Power Draw |
|------|----------|------------|
| **Off** (default) | Always active, always listening | Higher (continuous) |
| **On** | Cycles between sleep and active | Lower (intermittent) |

> ⚠️ **Trade-off:** Power saving reduces availability. During sleep, the repeater cannot process or forward packets until it wakes.

---

#### When to Use Power Saving

| Scenario | Recommendation |
|----------|----------------|
| ⚡ **Mains powered repeater** | `powersaving off` — Always available |
| 🔋 **Battery/solar repeater** | `powersaving on` — Extend battery life |
| 🏔️ **Critical infrastructure** | `powersaving off` — Maximum availability |
| 🏠 **Local/indoor repeater** | Consider `on` if power-constrained |

---

#### Commands

| Command | Effect |
|---------|--------|
| `powersaving` | Check current status (returns `on` or `off`) |
| `powersaving on` | Enable power saving mode (recommended for most repeaters) |
| `powersaving off` | Disable power saving mode |

> 💡 **Sydney Mesh Recommendation:** `powersaving on` for most repeaters to reduce power consumption and heat generation while maintaining good mesh performance.

Sets all LoRa radio parameters in a single command.

**Command Format:** `set radio frequency,bandwidth,spreading_factor,coding_rate`

**NSW Mesh Parameters (Australia: Victoria Preset):**

| Parameter | NSW Value | Default | Description |
|-----------|-----------|---------|-------------|
| **Frequency** | 916.575 MHz | 915.0 MHz | Operating frequency (Australian ISM band) |
| **Bandwidth** | 62.5 kHz | 250 kHz | Channel width (narrow = better sensitivity) |
| **Spreading Factor** | **7** | 10 | Chirp spread (lower = faster transmission) |
| **Coding Rate** | **8** | 5 | Forward error correction (4/8 = maximum) |

> ⚠️ **CRITICAL:** All nodes on the NSW mesh **MUST** use these exact parameters. The Australia: Victoria preset provides optimal performance through the combination of narrow bandwidth (sensitivity), low SF (speed), and high CR (reliability).

---

#### Frequency (916.575 MHz)

The operating frequency determines which part of the radio spectrum your node transmits and receives on. All nodes must use the **exact same frequency** to communicate.

| Aspect | Details |
|--------|---------|
| **Australian ISM Band** | 915-928 MHz (license-free for low-power devices) |
| **Why 916.575 MHz?** | Part of the Australia: Victoria preset, provides separation from other LoRa networks |
| **Regulatory** | Must comply with ACMA regulations for power and duty cycle |

> **Important:** Using a different frequency means you cannot communicate with the mesh at all.

---

#### Bandwidth (BW) — 62.5 kHz

Bandwidth determines the width of the frequency channel used for transmission. Think of it like the "width of the road" your signal travels on.

```
Bandwidth comparison:

500kHz:  ████████████  Wide (fast, short range)
250kHz:  ██████        Moderate
125kHz:  ████          Narrow
62.5kHz: ██            ✅ NSW (narrowest, best sensitivity)
```

| Bandwidth | Data Rate | Range | Noise Immunity | Best For |
|-----------|-----------|-------|----------------|----------|
| **500 kHz** | Fastest | Shortest | Lower | High-throughput, short range |
| **250 kHz** | Moderate | Moderate | Moderate | Balanced performance |
| **125 kHz** | Slower | Longer | Higher | Maximum range, low throughput |
| **62.5 kHz** ✅ | Slowest | Longest | **Highest** | Best sensitivity, minimal data |

**Trade-offs:**
- **Wider bandwidth (500 kHz):** Faster data transfer, but signal is more susceptible to noise and has shorter range
- **Narrower bandwidth (62.5 kHz):** Best receiver sensitivity and noise immunity, but slower data transfer per packet

**Why 62.5 kHz for NSW?**
- **Maximum receiver sensitivity** — The narrow bandwidth allows the radio to detect much weaker signals (down to ~-137 dBm)
- **Superior noise rejection** — Narrow bandwidth filters out more interference from other radio sources
- **Extended range** — Combined with proper SF, achieves excellent range even with lower spreading factors
- **Compensated by SF7** — The faster transmission time of SF7 offsets the slower bandwidth, keeping messages short

> 💡 **Key insight:** The 62.5 kHz bandwidth provides approximately 6 dB better sensitivity than 250 kHz, which translates to roughly **double the range** for the same signal strength.

---

#### Spreading Factor (SF) — 7

Spreading Factor is one of the most important LoRa parameters. It determines how the signal is "spread" across the bandwidth using chirp modulation.

```
Chirps per symbol:

SF7:  /\/\           128   ✅ NSW (fastest)
SF10: /\/\/\/\       1024  (moderate)
SF11: /\/\/\/\/\     2048  (slow)
SF12: /\/\/\/\/\/\   4096  (slowest)

Lower SF = faster transmission
```

| SF | Chirps per Symbol | Time on Air | Range | Sensitivity | Data Rate |
|----|-------------------|-------------|-------|-------------|-----------|
| **SF7** ✅ | 128 | **Shortest** | Short (at 250kHz) | -123 dBm (at 250kHz) | ~5.5 kbps |
| **SF8** | 256 | Short | Short | -126 dBm | ~3.1 kbps |
| **SF9** | 512 | Moderate | Moderate | -129 dBm | ~1.8 kbps |
| **SF10** | 1024 | Long | Long | -132 dBm | ~1.0 kbps |
| **SF11** | 2048 | Longer | Longer | -134.5 dBm | ~0.5 kbps |
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
| ❌ Slower data rate | ❌ Shorter range (at same bandwidth) |
| ❌ Higher airtime (battery drain) | ❌ More susceptible to interference |
| ❌ More susceptible to collisions | ❌ Requires stronger signal (at same bandwidth) |

**Why SF7 for NSW?**
- **Fast transmission times** — Messages take 8-16x less airtime than SF11-12, dramatically reducing collision risk
- **Channel efficiency** — More messages can fit in the same time window
- **Compensated by narrow bandwidth** — The 62.5 kHz bandwidth provides excellent sensitivity even at SF7
- **Compensated by CR8** — Maximum error correction improves reliability
- **Combined effect** — SF7 + 62.5kHz + CR8 achieves similar range to higher SF configurations while keeping messages short

> ⚠️ **Compatibility Note:** SF7 nodes **cannot communicate** with SF10/SF11 nodes. All NSW mesh participants must use the same settings.

---

#### Coding Rate (CR) — 8

Coding Rate (also written as 4/5, 4/6, 4/7, or 4/8) determines the amount of Forward Error Correction (FEC) applied to transmissions.

| CR Setting | Ratio | Overhead | Error Correction | Airtime Impact |
|------------|-------|----------|------------------|----------------|
| **CR5** | 4/5 | 25% | Basic | Fastest |
| **CR6** | 4/6 | 50% | Moderate | +20% slower |
| **CR7** | 4/7 | 75% | Good | +40% slower |
| **CR8** ✅ | 4/8 | 100% | **Maximum** | +60% slower |

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

**Why CR 4/8 for NSW?**
- **Compensates for lower SF** — SF7 is more susceptible to noise than higher spreading factors; CR8 adds the redundancy needed for reliable decoding
- **Maximum error correction** — Can recover from burst errors and interference that would corrupt messages at lower CR
- **Airtime tradeoff is acceptable** — The +60% overhead from CR8 is more than offset by the 8-16x time savings from using SF7 instead of SF11-12
- **Net result** — Messages are still much shorter than high-SF configurations while maintaining excellent reliability

> 💡 **The Australia: Victoria Formula:** By combining narrow bandwidth (sensitivity), low SF (speed), and high CR (reliability), the preset achieves an optimal balance that outperforms traditional "high SF, wide bandwidth" approaches.

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

The NSW mesh settings (916.575 MHz, 62.5 kHz BW, SF7, CR 4/8) — the **Australia: Victoria** preset — are optimized for:

| Goal | How Settings Achieve It |
|------|------------------------|
| **Excellent sensitivity** | 62.5 kHz bandwidth provides maximum receiver sensitivity (~-137 dBm effective) |
| **Fast transmissions** | SF7 keeps messages short, reducing collision risk and channel congestion |
| **Maximum reliability** | CR 4/8 provides 100% redundancy for robust error correction |
| **Network compatibility** | All nodes use identical settings |
| **Regulatory compliance** | Within Australian ISM band limits |

**Approximate performance at these settings:**
- **Effective bitrate:** ~2.7 kbps (SF7 base rate, with CR8 overhead)
- **Typical message airtime:** 200-600ms depending on length (much faster than SF11)
- **Theoretical max range:** 15-25+ km line-of-sight (narrow bandwidth compensates for lower SF)

---

## Role-Specific Settings Explained {#role-specific-settings-explained}

These four settings work together to optimize mesh performance based on your repeater's **position** and **traffic load**.

---

### Quick Reference

| Setting | Default | What It Controls | Rule of Thumb |
|---------|---------|------------------|---------------|
| `txdelay` | 0.5 | Wait before retransmitting floods | Higher = let other nodes go first |
| `direct.txdelay` | 0.2 | Wait before retransmitting direct packets | Usually lower than txdelay |
| `rxdelay` | 0 | Signal-based processing priority | Higher = prefer strongest signal |
| `af` | 1.0 | Radio silence after transmitting | Higher = more listening |

---

### Transmission Delay (`txdelay` / `direct.txdelay`) {#transmission-delay}

Controls how long a repeater waits before retransmitting a packet it needs to forward.

---

#### Transmission Delay Visualization

```
Delay windows by role:

        ├──Delay Window──┤
LOCAL   │██│▓▓░░         │  (0.3) early
STD     │██│▓▓▓▓▓▓░░     │  (0.8) mid
CRIT    │██│▓▓▓▓▓▓▓▓▓▓▓▓▓│  (2.0) late

██ = RX    ▓▓ = Delay    ░░ = Available

Higher txdelay = Waits longer
```

---

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

**Problems with quick retransmission:**
- 💥 Collides with transmissions from nodes that received the packet slightly later
- 🛑 "Steps on" retransmissions from lower-elevation nodes
- ❌ Prevents packets from reaching nodes that could only hear the critical repeater

> 💡 **Key insight:** By using higher txdelay, critical nodes essentially say: *"I'll wait and let the smaller nodes go first."*

**Benefits:**
- ✅ Local nodes serve their immediate area quickly
- ✅ Critical nodes fill in gaps after the initial wave
- ✅ Fewer collisions in the critical node's wide coverage area

---

#### txdelay vs direct.txdelay

| Setting | Default | Applies To | Collision Risk |
|---------|---------|------------|-----------------|
| `txdelay` | 0.5 | **Flooded packets** (broadcast to all) | ⚠️ High (many nodes retransmit) |
| `direct.txdelay` | 0.2 | **Direct packets** (routed point-to-point) | ✅ Lower (specific route only) |

> 💡 Direct packets use **lower** delays because only nodes along the specific route retransmit, not the entire mesh.

---

### Airtime Factor (`af`) {#airtime-factor}

Enforces a "radio silence" period after each transmission, implementing a **duty cycle limit**.

---

#### Airtime Factor Visualization

```
TX/Silence duty cycles:

af=1: │TX│░░│TX│░░│TX│      50% (1:1)
af=2: │TX│░░░░│TX│░░░░│     33% (1:2)
af=3: │TX│░░░░░░│TX│        25% (1:3)

TX = Transmit    ░░ = Silence

Higher af = More listening time
```

---

#### How It Works

**The Formula:**
```
silence_period = transmission_time × airtime_factor
```

**After transmitting a packet:**
1. Calculate how long the transmission took (in milliseconds)
2. Multiply by the airtime factor
3. Wait that long before transmitting again
4. During silence → **listen only**

---

#### Example

| Transmission | af | Silence Period |
|--------------|-----|----------------|
| 200ms packet | 1 | 200ms |
| 200ms packet | 2 | 400ms |
| 200ms packet | 3 | 600ms |

---

#### Why This Matters

| Benefit | Explanation |
|---------|------------|
| 🚫 **Prevents channel hogging** | High-traffic nodes won't dominate the airwaves |
| ⚖️ **Improves fairness** | Gives other nodes a chance to transmit |
| 📻 **Reduces collisions** | More listening = better channel awareness |

---

#### Recommended Values by Role

| af | Duty Cycle | Best For |
|----|------------|---------|
| **1.0** | 50% (1:1) | 🟢 Local nodes with few neighbors |
| **1.5** | 40% (1:1.5) | 🟡 Standard suburban repeaters |
| **2** | 33% (1:2) | 🟠 Link nodes bridging regions |
| **3** | 25% (1:3) | 🔴 Critical infrastructure (heavy traffic) |

> 💡 **Rule of thumb:** Higher af = more conservative = more listening, less transmitting

---

### Receive Delay (`rxdelay`) — Signal-Based Processing {#receive-delay}

The `rxdelay` setting uses **signal strength** to determine which copy of a packet to process first.

---

#### Signal-Based Packet Selection Visualization

```
Same packet from different sources:

Node A: -85dBm  (strong) --> 50ms delay
Node B: -125dBm (weak)   --> 800ms delay

Processing order:
0ms─────────50ms─────────────────800ms────>
             │                     │
        ┌────┴────┐          ┌─────┴─────┐
        │ A: PROC │          │B: DISCARD │
        └─────────┘          └───────────┘
             ▲                   (dup!)
        Seen first

Result: Best path (A) wins
```

---

#### How It Works

**The Formula:**
```
delay = (rxdelay^(0.85 - score) - 1.0) × airtime
```

| Variable | Description |
|----------|------------|
| `rxdelay` | Configured base value (e.g., 2, 3, 4) |
| `score` | Signal quality (0.0–1.0) from SNR vs. spreading factor threshold |
| `airtime` | Transmission time of the packet |

---

#### What This Means

| Signal Strength | Score | Delay | Result |
|-----------------|-------|-------|--------|
| **Strong** (nearby) | ~0.8 | ~50ms | ✅ Processed first |
| **Medium** | ~0.5 | ~300ms | Processed after stronger signals |
| **Weak** (distant) | ~0.3 | ~800ms | ❌ Often discarded as duplicate |

---

#### Why This Matters

In a mesh, the same packet often arrives from **multiple sources**. The rxdelay system creates **intelligent packet selection**:

1. 📡 **Strong signal arrives** → Short delay → Processed quickly
2. 📡 **Weak signal arrives** → Long delay → Sits in queue
3. ✅ **Strong copy processed** → Packet marked as "seen"
4. ❌ **Weak copy expires** → Already "seen" → Discarded

> **Result:** The mesh naturally prefers relaying packets via the **strongest/most reliable path**.

---

#### Practical Example

A hilltop repeater receives the same packet from two sources:

| Source | Signal | Score | Delay | Outcome |
|--------|--------|-------|-------|---------|
| **Node A** (nearby) | Strong | 0.8 | ~50ms | ✅ Processed first, forwarded |
| **Node B** (distant) | Weak | 0.3 | ~800ms | ❌ Discarded (already "seen") |

---

#### Why Sydney Mesh Uses rxdelay 3

All Sydney mesh repeaters use `rxdelay 3` for:

| Benefit | Description |
|---------|------------|
| 🔄 **Consistency** | Same behavior across all repeaters |
| ⚡ **Balance** | Fast enough processing, smart path selection |
| 🔧 **Simplicity** | Easier configuration and troubleshooting |

> 📝 **Note:** MeshCore default is `rxdelay 0` (disabled), but `rxdelay 3` provides better performance for the Sydney network.