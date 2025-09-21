# SwagShop Writeup

Name: SwagShop
Date:  
Difficulty:  Easy
Goals:  
- Try to go from Notes to writing Writeup
- Do a post root reflection
- Try to make and apply a methodology about hacking that everyone better seems to have about (or something like this):
	- I have X
	- Environment Y
	- How does do I get Z with:
		- ... etc
Learnt:
Beyond Root:

Try to return to Notes 
- [[SwagShop-Notes.md]]
- [[SwagShop-CMD-by-CMDs.md]]


## Recon

The time to live(ttl) indicates its OS. It is a decrementation from each hop back to original ping sender. Linux is < 64, Windows is < 128.
![ping](Screenshots/ping.png)

![](nmap-swagshop.png)

![](nuclei.png)

![](configexposed.png)

`ssh root` does not work

![](sqlversions-admin.png)

![](magento-version.png)

Website is so over-exposed `nikto` is actually very good.
![](nikto.png)

There are multiple RCEs for pre 1.9.0.1

Awesomely name shoplift
![1080](explainingtheexploit.png)

It 404ed 

![](irememberedtheindexphpfromtheexploitandaaaahed.png)

![](shoplifter.png)

![](adminpanel.png)


searchsploit -m php/webapps/37811.py

![](whatcommentingout.png)

Bad regression

![](pythonisreREEEEEEEEEEEEE.png)

![](wtfisthisexploit.png)
## Exploit

## Foothold

## Privilege Escalation

## Post-Root-Reflection  

## Beyond Root


