# Cronos Writeup

Name: Cronos
Date:  
Difficulty:  Medium
Goals:  
- No AI, no hints, no write up till 3 hours post enumeration
- Guided
Learnt:
Beyond Root:

No AI, no hints, 
## Recon

The time to live(ttl) indicates its OS. It is a decrementation from each hop back to original ping sender. Linux is < 64, Windows is < 128.
![ping](Screenshots/ping.png)

My previous `nmap` wet fine
![](previousnmap.png)

But I maybe being rate limited on `1000` for some arcane reason
![](niceignoring-potentialratelimited.png)
And hours would pass
![](hoursofnmapwaiting.png)

There are not only 2 ports
![](machinebrokenatm.png)

Realised later I am on the wrong network. Yikes - Face palm
## Exploit

## Foothold

## Privilege Escalation

## Post-Root-Reflection  

## Beyond Root


