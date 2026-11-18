---
title: Homelab
meta: September 2026 - Present
summary: 3-node Proxmox cluster and a Raspberry Pi running about two dozen self-hosted services, with my own DNS, DHCP, VPN, single sign-on, backups, and a Wazuh security lab. An AI rig is in progress.
tags: Proxmox VE, Docker, Pi-hole, WireGuard, Tailscale, Wazuh, OPNsense, Authelia
---
![Homelab network diagram](01-network-diagram.png)
> **Note:** This diagram was generated with the help of an LLM. It's temporary while I am still testing and changing the technology and tools I use.

## Hardware
- **OptiPlex 7060** (i7-8700, 32 GB RAM): the main machine. It has the strongest CPU and a fast NVMe drive, so it runs the heavier everyday services.
- **ThinkCentre M800** (i5-6400, 24 GB RAM): the learning box. The security lab and the GNS3 server live here, and I power it off when I'm not studying.
- **Intel NUC** (8 GB RAM, 2 TB SSD): always-on infrastructure. It's low power, so it handles the network services, logins, VPN, and backups.
- **Raspberry Pi 4**: DNS, DHCP, monitoring, alerts, and remote access. It's kept separate so the internet and my alerts keep working when a node reboots.
- **OptiPlex AIO**: basically just a screen for the Homepage dashboard. Nothing important lives on it. Working on macro keyboard that switches betwene services with dashboards.
- **AI rig** (in progress): Z490 board, i3-10100, and 32 GB RAM. It's waiting on GPUs, then it will run Ollama, Open WebUI, and LiteLLM outside the cluster.

If you are interested in how I got everything here for your own homelab, everything here was off of Facebook Marketplace, either free or at a really good price.

## What each service is for
> If you are interested in hosting any of these yourself...

### OptiPlex 7060
| Service | What I use it for |
|---|---|
| Immich | Photo and video backup from my phone, with face and object search, basically Google Photos |
| Nextcloud | File sync, calendar, and contacts, pretty much google Drive |
| Home Assistant | Home automation that runs locally. It's a full VM so USB dongles can pass through. This will give me a clean UI and hub for all smart devices. |
| Actual Budget | Budgetting tool, very lightweight so I figured I would try it. |
| Jellyfin | Media server, basically a self-hosted Netflix |
| Scrutiny | Drive health, so I get a warning before a drive dies |
| AMP | Game server panel for modded Minecraft and other games. If you are interested in hosting different games with ease, AMP is a really good service. |
| Watchtower | Keeps this machine's containers updated |

### Intel NUC
| Service | What I use it for |
|---|---|
| AdGuard Home | Backup DNS, with the same local records as Pi-hole so names still work if the Pi goes down |
| Nginx Proxy Manager | Gives services names like nextcloud.home instead of an IP and port |
| Authelia | One login with 2FA in front of my web pages |
| CrowdSec | Blocks IPs that probe me, security |
| WireGuard | Full-tunnel VPN, so everything on public Wi-Fi goes through home. More of a backup as Tailscale is built on WireGuard |
| Vaultwarden | Password manager |
| FileBrowser | Drag-and-drop file manager in the browser |
| Speedtest Tracker | Graphs my internet speed over time |
| Backups | A 2 TB NFS share that Proxmox backs up to |
| Watchtower | Keeps this machine's containers updated |

### Raspberry Pi 4
| Service | What I use it for |
|---|---|
| Pi-hole | DNS and DHCP for the whole network, plus ad blocking |
| Unbound | Lets Pi-hole look up DNS itself, so no upstream provider sees my lookups |
| Uptime Kuma | Checks every service and alerts me when one goes down |
| ntfy | Sends those alerts to my phone |
| Tailscale | Day-to-day remote access, still reachable if the whole cluster is down |

### ThinkCentre M800
| Service | What I use it for |
|---|---|
| Security lab | Kali, OPNsense, Wazuh, and deliberately vulnerable targets (Metasploitable2, Juice Shop, DVWA) |
| GNS3 server | Network topologies for CCNA practice |

### OptiPlex AIO
| Service | What I use it for |
|---|---|
| Homepage | A dashboard with every service on it |

## Design choices
- **Three nodes, one login:** the cluster is for managing everything from one place and moving things between machines. The NUC is the third vote, so the M800 can be turned off without breaking the cluster. I also love the UI of Proxmox, makes it very easy to start new VM's or other services with combined compute.
- **DNS and DHCP:** Pi-hole on the Pi is the main server, with Unbound resolving lookups itself, and AdGuard Home on the NUC is the backup DNS.
- **Monitoring:** Uptime Kuma on the Pi, with alerts through ntfy. Monitoring can't live on the machines it's watching.
- **Remote access:** admin pages are only reachable over Tailscale or WireGuard, behind Authelia. The only open ports are for game servers, and UPnP is off.
- **Filtering:** per-device Pi-hole groups, including a child mode group that blocks DNS-over-HTTPS so filtering can't be bypassed. I check it with Pi-hole's query logs and Wireshark captures.
- **Security lab:** two internal-only Proxmox bridges on the M800, with OPNsense between Kali and the targets. I run Nmap scans and SSH brute-force tests, make sure the Wazuh alerts fire, and write firewall rules to block them.
- **Power:** C-states on in the BIOS, the powersave governor and powertop on every node, and Wake-on-LAN for the machines that don't need to be on all the time.

## What it doesn't do
The cluster has no shared storage or high availability, since it's only clustered for one login and moving things around. I plan to add a NAS as a second backup target, but NASs are pretty dang expensive and I am a college student... The AI rig is also still waiting on GPUs.

If you want to talk more about this project or give me some advice, please reach out to me! I am extremely passionate about learning and self-hosting services.
