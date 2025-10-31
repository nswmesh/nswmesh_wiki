---
title: Aldi Solar Repeater
author: mukw
---

**Last Updated:** 11/10/2025

**Node Type:** Repeater

**Build Version:** v1.0

---

## 📝 Overview

This is a build guide using the exisitng solar panel light from Aldi. The idea is to utilise an existing cheap item that includes the battery, solar panel and case.
IF you can find the prioduct at Aldi it was $15, otherwise Bunnings sell them for $30.

---

## 🧰 Components

| Component | Details | 💰 Price (AUD) | 🔗 Link |
|----------|---------|---------------|---------|
| **Controller** | XIAO S3 + WIO | $22.00 | [Buy](https://www.aliexpress.com/item/1005008094638318.html) |
| **Antenna** | DIYmall 915 MHz Fibreglass, 5 dBi | $8.00 | [Buy](https://www.aliexpress.com/item/1005006712636707.html) |
| **Solar Panel** | Aldi “Special Buy” 10 W | $15.00 Aldi ($30 Bunnings) | [Buy](https://www.bunnings.com.au/solar-magic-100-300lm-hi-low-led-spotlight_p0185888) |
| **Solar Charge Controller** | AS21 5V | $3.00 | [Buy](https://www.aliexpress.com/item/1005001728396318.html) |

**💰 Estimated Total:** $48.00 AUD

---

## ⚡ Power Specs *(Optional)*

| Parameter | Value |
|----------|-------|
| **Panel Voltage** | 6 V |
| **Battery Voltage** | 3.7 V (1S) |
| **Charge Voltage** | 4.2 V |
| **Average Draw** | 40 mA |
| **Expected Runtime** | ~48 h on battery |

---

## 🛠️ Build Notes

- Unscrew the clear panel and disconnect the LEDS from the PCB.
- Desolder the solar and battery cables from the PCB and connect to the new solar charge controller
- Solder 2 cables from the Xiao battery pads on the back to the load terminals on the charge controller
- Drill a hole in the side of the enclosure to mount the antenna.
- You will need to remove some of the plastic from the inside to be able to screw the antenna on.

---

## 📸 Photos

![](/images/aldi-solar-1.jpg)

![](/images/aldi-solar-2.jpg)
