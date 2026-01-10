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
2. Configure your name and radio settings
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

| Advert Type | Frequency | Scope |
|-------------|-----------|-------|
| Local advert | Every 240 minutes | Directly connected repeaters only |
| Flood advert | Every 12 hours | Entire mesh |
| Companion advert | Manual only | When you trigger it |

> 💡 **Note:** The node list takes time to populate. A connection may exist even without seeing adverts — this is normal and keeps the mesh uncongested.

---

> ⚠️ **IMPORTANT: Radio Compatibility**
>
> All nodes on the Sydney mesh must use the **Australia preset** with **SF11** (modified from default SF10).
>
> **Why SF11?** Provides improved range across Sydney's unique geography and wide user spacing.
>
> ❌ **Not interoperable** with standard ANZ meshes running SF10.

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
<div class="cmd-row"><code>set flood.advert.interval 12</code><button onclick="copyCmd('set flood.advert.interval 12', this)">Copy</button></div>
<div class="cmd-row"><code>set guest.password guest</code><button onclick="copyCmd('set guest.password guest', this)">Copy</button></div>
<div class="cmd-row"><code>powersaving on</code><button onclick="copyCmd('powersaving on', this)">Copy</button></div>
</div>

### Quick Reference

| Setting | Value | MeshCore Default | What it does |
|---------|-------|------------------|--------------|
| `agc.reset.interval` | 500 | 0 (disabled) | AGC reset every 500 seconds (~8 min) to prevent sensitivity drift |
| `multi.acks` | 1 | 1 | Send redundant ACKs for better delivery reliability |
| `advert.interval` | 240 | 0 | Local advert every 240 minutes (neighbors only) |
| `flood.advert.interval` | 12 | 12 | Network-wide advert every 12 hours |
| `guest.password` | guest | (none) | Standard guest access password |
| `powersaving` | on | off | Power saving mode (light sleep between activity) |
| `radio` | 915.8,250,11,5 | 915.0,250,10,5 | Sydney mesh radio parameters (freq, bw, sf, cr) |

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
Time ──────────────────────────────────────────────────────────▶

                 Loud RF               AGC              Sensitivity
                 Signal                Lockup           Restored
                   │                     │                  │
 Sensitivity  ─────┼─────────────────────┼──────────────────┼─────
      │            ▼                     ▼                  ▼
   Optimal ═══════════╗                                 ╔═══════════
                      ║                                 ║
                      ╚════════════════════════════════╝
   Degraded                    ▲
                               │
                         Packets Lost!
                     (can't hear weak signals)
```

#### With AGC Reset Enabled (500 seconds)

```
Time ──────────────────────────────────────────────────────────▶
        0s        500s      1000s     1500s     2000s
        │          │          │          │          │
        ▼          ▼          ▼          ▼          ▼
      ┌───┐      ┌───┐      ┌───┐      ┌───┐      ┌───┐
      │RST│      │RST│      │RST│      │RST│      │RST│
      └───┘      └───┘      └───┘      └───┘      └───┘
        │          │          │          │          │
 Sensitivity restored every ~8 minutes
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
  Sender                                    Receiver
    │                                          │
    │ ─────────── Message ───────────────────▶ │
    │                                          │
    │ ◀─────────── ACK ─────────────────────── │
    │              │                           │
    │              ▼                           │
    │         If lost, sender                  │
    │         thinks message failed            │
```

**Multi-ACK (multi.acks = 1) ✅ Recommended:**
```
  Sender                                    Receiver
    │                                          │
    │ ─────────── Message ───────────────────▶ │
    │                                          │
    │ ◀─────────── ACK 1 (multi-ack) ───────── │
    │ ◀─────────── ACK 2 (standard) ────────── │
    │              │                           │
    │              ▼                           │
    │         Even if one ACK is lost,         │
    │         the other confirms delivery      │
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

**Local Advert (advert.interval = 240 min):**
```
                    Your Repeater
                         │
          ┌──────────────┼──────────────┐
          │              │              │
          ▼              ▼              ▼
      Neighbor 1    Neighbor 2    Neighbor 3
          │              │              │
          X              X              X      ◀── NOT forwarded
          │              │              │
      (stops)        (stops)        (stops)
```

**Flood Advert (flood.advert.interval = 12 hrs):**
```
                    Your Repeater
                         │
          ┌──────────────┼──────────────┐
          │              │              │
          ▼              ▼              ▼
      Neighbor 1    Neighbor 2    Neighbor 3
          │              │              │
          ▼              ▼              ▼         ◀── Forwarded!
      Far Node 1    Far Node 2    Far Node 3
          │              │              │
          ▼              ▼              ▼         ◀── Keeps spreading
         ...            ...            ...
```

---

**Two Types of Adverts:**

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
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│  Active     │────▶│ Pending work?│────▶│ Light Sleep │
│  (5 sec)    │     │              │ No  │ (≤30 min)   │
└─────────────┘     └──────┬───────┘     └──────┬──────┘
       ▲                   │ Yes                │
       │                   ▼                    │
       │           ┌──────────────┐             │
       └───────────│ Extend active│◀────────────┘
                   │   (+5 sec)   │   Wake on packet/timer
                   └──────────────┘
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

**Sydney Mesh Parameters:**

| Parameter | Sydney Value | Default | Description |
|-----------|--------------|---------|-------------|
| **Frequency** | 915.8 MHz | 915.0 MHz | Operating frequency (Australian ISM band) |
| **Bandwidth** | 250 kHz | 250 kHz | Channel width |
| **Spreading Factor** | **11** ⚠️ | 10 | Chirp spread (higher = longer range) |
| **Coding Rate** | 5 | 5 | Forward error correction (4/5) |

> ⚠️ **CRITICAL:** All nodes on the Sydney mesh **MUST** use these exact parameters. SF11 is intentionally different from the standard Australia preset (SF10) for improved range.

---

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

```
Frequency Spectrum
                         915.8 MHz (center)
                              │
  ◀─────────────────────────────────────────────────────▶

  500 kHz BW:    ████████████████████████████████████████
                 │◀───────────── Wide road ───────────▶│
                 Faster, but more noise, shorter range

  250 kHz BW:         ████████████████████████
                      │◀─── Medium road ───▶│
                      Balanced (Sydney mesh) ✅

  125 kHz BW:              ██████████████
                           │◀─ Narrow ─▶│
                           Slower, longer range
```

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

```
Chirp Modulation Visualization (simplified)

SF7 (128 chirps):     /\/\/\/\        Fast, short range
                      ────────
                      
SF10 (1024 chirps):   /\/\/\/\/\/\/\/\/\/\/\/\/\    Moderate
                      ──────────────────────────

SF11 (2048 chirps):   /\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\  ✅ Sydney
                      ──────────────────────────────────────────────────
                      
SF12 (4096 chirps):   /\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\
                      ────────────────────────────────────────────────────────────────────────────────────
                      Slowest, longest range

Higher SF = More chirps = Longer airtime = Better sensitivity = Longer range
```

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
Packet arrives at multiple repeaters simultaneously:

Time ──────────────────────────────────────────────────────────────────────▶
      │
      │   Packet          Random delay windows              Retransmit
      │   Received
      │      │
      │      ▼
      │   ┌──┬─────────────────────────────────────────────────────────────┐
LOCAL │   │██│▓▓▓▓▓▓▓▓░░░░░░░░░│                                          │
(0.3) │   │  │    narrow      │◀── Transmits early                        │
      │   └──┴─────────────────────────────────────────────────────────────┘
      │   ┌──┬─────────────────────────────────────────────────────────────┐
STANDARD  │██│▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓░░░░░│                              │
(0.8) │   │  │           medium            │◀── Transmits mid-range       │
      │   └──┴─────────────────────────────────────────────────────────────┘
      │   ┌──┬─────────────────────────────────────────────────────────────┐
CRITICAL  │██│▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓░░░░░░░░░░│
(2.0) │   │  │                           wide                            │
      │   └──┴─────────────────────────────────────────────────────────────┘
                                                              ▲
                                                              │
                                              Transmits last (lets others go first)

██ = Packet received    ▓▓ = Delay window (random point chosen)    ░░ = Available window
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
Time ──────────────────────────────────────────────────────────────────────▶

af = 1 (50% duty cycle):
┌───────────┐           ┌───────────┐           ┌───────────┐
│    TX     │  silence  │    TX     │  silence  │    TX     │
│  200ms    │   200ms   │  200ms    │   200ms   │  200ms    │
└───────────┴───────────┴───────────┴───────────┴───────────┘
            │◀──────────▶│
               1:1 ratio

af = 2 (33% duty cycle):
┌───────────┐                       ┌───────────┐
│    TX     │       silence         │    TX     │       silence
│  200ms    │        400ms          │  200ms    │        400ms
└───────────┴───────────────────────┴───────────┴─────────────────
            │◀──────────────────────▶│
                    1:2 ratio

af = 3 (25% duty cycle):
┌───────────┐                                   ┌───────────┐
│    TX     │            silence                │    TX     │
│  200ms    │             600ms                 │  200ms    │
└───────────┴───────────────────────────────────┴───────────┴───────
            │◀──────────────────────────────────▶│
                         1:3 ratio

Higher af = More listening time = Better for high-traffic nodes
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
Same packet arrives from multiple sources with different signal strengths:

                         Hilltop Repeater
                              │
    ┌─────────────────────────┼─────────────────────────┐
    │                         │                         │
    │   Strong signal         │        Weak signal      │
    │   (nearby node)         │        (distant node)   │
    │                         │                         │
    ▼                         │                         ▼
┌───────┐                     │                     ┌───────┐
│Node A │                     │                     │Node B │
│-85dBm │                     │                     │-125dBm│
└───┬───┘                     │                     └───┬───┘
    │                         │                         │
    │ Score: 0.8              │                         │ Score: 0.3
    │ Delay: ~50ms            │                         │ Delay: ~800ms
    │                         │                         │
    ▼                         ▼                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                         Processing Queue                         │
│                                                                  │
│  Time: 0ms        50ms                    800ms                  │
│    │               │                        │                    │
│    │               ▼                        ▼                    │
│    │          ┌────────┐              ┌────────┐                 │
│    │          │ Node A │              │ Node B │                 │
│    │          │ PROCESS│              │DISCARD │ (already seen)  │
│    │          └────────┘              └────────┘                 │
│                   ▲                        │                     │
│                   │                        ▼                     │
│              Packet marked           Duplicate!                  │
│              as "seen"               Thrown away                 │
└─────────────────────────────────────────────────────────────────┘

Result: Packet forwarded via STRONGEST path (Node A)
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