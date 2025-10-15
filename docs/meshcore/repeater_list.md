---
title: NSW Meshcore Repeater List
---

As of October 2025, Meshcore identifies repeaters and roomservers using the first two bytes of the node's key prefix. If two repeater nodes share the same key prefix, it may cause the node path to not display correctly and cause issues when pinging a zero-hop node. As a result, a list of repeaters and their public keys can be found here so that when meshers create a new node they can confirm whether their node key may need to be updated.


### Legend
- ⚠️ and **bolded public_key_prefixes** indicate that **multiple nodes share the same key prefix**.
- Shared key prefixes can cause:
  - Incorrect or missing path rendering on Meshcore maps  
  - Failed or misrouted pings to nearby (zero-hop) nodes  
  - Ambiguity when routing via repeaters or roomservers

| public_key_prefix | name | public_key |
| --- | --- | --- |
| 01 | VK2MR Roof (V4) | 012905f6fe2b496e89400b5c698e1c214602d4931dc1b5ef1145e7feeaff57ab |
| 02 | Overkill (VK2FBAE) - TD | 022810bc804fd14e4fa69d08b695c4ff0e0a450b7d5949bb315e225824f1d6cb |
| ⚠️**05** | Overkill - Mt Colah | 05265b086d2548b1eb1d60716f282972fd1451ff2edd124aa832c7b99fc3c3b0 |
| ⚠️**05** | 🌱Roomserver Tester | 05cf287c9f7f3a6a796972430fcad8ee5ef22f5445f2b0a5a9e1e400651d8db4 |
| 0c | ✝️Wst Syd Airport | 0cdb20c2f916c35e1479d663b53f9380cb236ca7de0a25195251cb909d60ca6b |
| 11 | 🌱Chester Street | 113e9bce50a7a003c97fc13edeb093975a06087fbf16a3b62411931d0ac4f642 |
| 1a | Gym_Reps | 1adc8fa347c61f28812c1b20710ad97b0f958daccfa8e0accf3b64fb2303c5e8 |
| 22 | ✝️ Cleric Test Repe | 22e3daa55da62589ee5c93fe0313762d9268f7f5243fb20ba1d279ccf4a53524 |
| 23 | Gregory Hills Rpt | 23fc50160778f87caf7af401d786692b74efded66d9bff5b20cf40395341d688 |
| 27 | Ivy Desk 🌱 | 27ecf222f0f7ff9628db54b0b2a492d72a2300c3c9f0430738bbca2840461b7d |
| 28 | Mount Annan Rpt | 28c222747e12122a04b8a4196e82d7f2dd490d8a5789b194bd8d6514845b4b16 |
| 2a | FaRTdeck | 2a1bc3b6ddc5a0c40ed28272ff59c0f1b643fa538492a71f17834b90ae4a6f42 |
| 2e | 🛜LUX08 - Knights Hil | 2eabc4c665c7785321aafb5dbd8ae8e07355e64739e78d3fbb5cf790871cca05 |
| 30 | Overkill - Asquith | 30b0840ed68aff84bab3721f956191ee51098970b429b730798e9eb01f7422ff |
| 32 | Overkill - Staples | 32d8f527e7a40cd2921e17d41d8379c0d49122cf3afe01fef84e9fb776dfe2c9 |
| 33 | Overkill - Mt Colah 2 | 338a1e97b4a37a45d9ac0912cb34637965e9d907e1e04518d124c256d78519a0 |
| 35 | Loftus Heights G2 | 35d60039b97f8048498a40fe4b9c1cb4f7e5aec08ade9f5c845d87211e1a254d |
| 36 | 🌱Camperdown | 36e2d2f59c5cc149aa7217787dba78ea3d29a85f86d4a40f2c50823bf93eb092 |
| 41 | SHITDECK | 411eee3df0e249f5202f544bd4e42960fbf0f72c9aa102aaa212d1c59f7ece9a |
| 49 | Overkill - St Leonards | 49296fae69a742e2c7be2092712860320cd2cec80d69bf64b637d4eeda9ebdff |
| 4b | Dingus repeater | 4ba9c51b34d518ec8f22bf3f93621d1a11b67368818ae228adc63dbff250dd6a |
| 4c | 🛜LUX03 - Keira Nth | 4c05703c81e953185a2d4282827c3e8a3aef846749a32e7b1a215e1edc03911a |
| 4e | Overkill - Cherrybrook | 4eddfdd6e9ccafa99ce893e5f3d0223befa7d0c9ca7b1c98572a223dd1671e6c |
| 5d | 🌱Ivy V4 | 5d5a8e887a1761a216be8344195b231def3b078684aece22b05bef23f273bbb3 |
| 67 | HangingRock Repeater | 67d693ad2bf9d5f5984a1f9ec8fa0dc2c65d774b865cd945f301c0c0db88270a |
| 68 | 🐄Marsden Park | 68beeffb44555e09fc8e5696394352d9eb6e9d6454785cf107d7628d08b5d763 |
| ⚠️**6d** | North Sydney (test) | 6d401a198adb37d239393e01a02eeedb8f26ecbaec4399487e4c917397f5e8a3 |
| ⚠️**6d** | 🛜LUX06 - Kiama | 6d4ec1f2204fafe7f778490dbdfcf1f96553a00ca16c33f2e942eaaa022b631c |
| 7c | CN01 - Circular Quay | 7c01528294e97c9119b7014acd9d81e3f7783300c973d7c5cb49a998a0362ec4 |
| 87 | 👾Sonic - Green Point | 870c2dbd3df1bce7dadb85d3cb22f181d44e0d06785c6f2868b782872742e046 |
| 88 | 🌱T114 | 88549ea7f45942ab5d5b716b6fdb50ebd0c6e904abf4537a2311037cbb53ba31 |
| 92 | RF Guy | 922f6c56d0ddb5b084c6f7c26e9a4a09fe90aa3387826e580f446ccf5a03bb6f |
| 95 | CarlSagan-G2 | 95a6ae9f43ff31e8d1541ed017b48e79486bdd4df00c42f9eb34e7f9b415d476 |
| 9e | 🌱Roomserver | 9e47420d2d2c77d221d8cd15598f4b12408c3c19143d4f1957d9a94b5365f013 |
| a0 | DHCP | a033ee9cfb943dbeed7d0a468f9362cb6b3954d29388c8258597a6be1b54cab2 |
| a4 | 🛜LUX02 - Keira Sth | a468c8cda7d0531cc5b8f7607c0f234a1647e3ee89ab8b7443a8c75c540e3f1f |
| ⚠️**a7** | Pfych Repeater | a7fc405db7cead41c105522020879c6ca19ac06f97f85a63dc8e7914aa9932a3 |
| ⚠️**a7** | ✝️Cleric G2 🛻 | a70565285faeacff0b330779577cb25865d215fcc23664080ba5ab3c8602b89c |
| a9 | Greendale Repeater | a97b453e4f9622cd013acf59bfbf3d0eb510d2d13b3b218ba4c700780ac8e8ea |
| aa | VK2BRM Repeater | aa7083bb94e776410d17cfed356172ec580a4d8481b4bc4a73f9a562da8c420e |
| ab | 🛜LUX07 - Mt Gibralta | ab687e3dbbef93fbba17101f2b81e498c50ca6c1898b941586baf9f15d37d575 |
| ⚠️**b7** | Kenny Hill Repeater | b745d1254f0639695fd7326c23f3a0bcb92aa4c5e08f6cfc43ba9527db88515d |
| ⚠️**b7** | VK2IVY🌱 | b7a7b3efa9a62f2ee655b1f2e67d63fc68b6f1869f65ec7e3b3a225218b5bf03 |
| bd | ☎️ Jamberoo | bd00f382f921bbd739cbd277309b104ccb58743aa62a3ea3f9fed681e54fa6a8 |
| be | 🌱nrf52 Battery Test | beede836a76e2354b16ee1e738fff607565a4dfb40d6d0ba38f0a93f05d6a880 |
| c1 | Overkill - Roof | c1cc1f7ba116e955fb0552432570ec76a99473b6563ccd6c8231375448d86a98 |
| c7 | NONAME | c796108126bb8c889841174e91d93c383d50a98a1fc682278732ef2b7bfdf4cd |
| c8 | 🛜LUX05 - Bald Hill | c84e5ab84acbd0f2e660ae5213274fb3353d2f7ce1c9d9ff3ba10ebf0e963e1c |
| c9 | ✝️ADF OrchardHills | c994088710b5279e7e162f914d8321e73f340bf27c869a0c00feaebe4100ba3a |
| ⚠️**d7** | ✝️ | d79c7b0b122b8b4a71285245bd13554b8b5afcb41baf7be8897125f3f1a0bf78 |
| ⚠️**d7** | 🌱Ivy MeshPocket | d74cd556745e2c0164e0eca7b3b01e1de0ba1defb21fbf69908e271d6d18aeaa |
| da | NONAME | da6ab6c9e23af99e0164484e5adb0ffdeecbcd9a9f9f9036513142c9ab98eac8 |
| dd | Apples1234 | dd1a89031007c8e98947ddff8b9b27ed70680056ea477bfc8644ee91909fdb61 |
| de | HiveMesh.au G2 | de728887835917e4148244bf8bd14be7b8f11ba1d4c9daa48cd9ba9dc721e5ab |
| e4 | 🛜LUX04 - Port Kembla | e4093953a6408506c962a158b65d07eac37782f4d428d23e6eb11ddc6652e4fd |
| e9 | ✝️Fairlight | e95170cc52e2d5a39bacc92fb60922bfefff12d553bc56e733533709943dfcab |
| ee | 🌱 | ee2f3f5b849f27f8be1fce4ba85ceeff72142606e9389161606f018164e12378 |
| f1 | ✝️Lapstone | f1fc699ff05e41738524af480a24ccf5ada1f3248bd23d83f47ae69f44060193 |
| f5 | ✝️ Leonay | f58e1ca5e95ca03d516b80c4839ecd8c76855f63e9e9dea371f3384b24a1b705 |
| f9 | XiaoS3 Repeater | f93549c8600ee5c7c063b66e7636d237bd49470c61dcb5ec8cc310e85ae9afab |
| ⚠️**fe** | RIPPLE-SYD-ILLAWONG-RPT | fef2dcf0570fdd0d9c9dfed38c35d0e25ce0aeeb98ed6ad5533e51f57c4c05ee |
| ⚠️**fe** | VK2MR 🏠 | fe35051d7636a86aec254efd3de8d7d6a0e0ef7302ee0ca8f1b96cfb6ad7888a |

 Last Modified: 2025-10-16 00:29:42  
