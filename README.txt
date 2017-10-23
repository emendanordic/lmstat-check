README: lmstat-check.py

Uses FlexLM's lmstat utility to check if a given feature is available or not.
A sleep feature exists to make the script sleep until the license becomes available, or not.

Developed with Python v2.7

Example usage:

 $ python lmstat-check.py --license-file 27000@flexlm-license-machine --feature floatserver11 --sleep 60 --sleep-checks 10
 
This will check for license feature floatserver11 on 27000@flexlm-license-machine, every 60 seconds, for 10 tries.


Return values:

0 if a license is available
1 if a license is not available when the script finishes
2 an error occurred

Note that the script finishes when a license becomes available