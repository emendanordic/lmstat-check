# **************************************************************************************************
#  Emenda Ltd.
#  Uses FlexLM's lmstat utility to check if a given feature is available or not.
#  A sleep feature exists to make the script sleep until the license becomes available, or not.
#
#  $LastChangedBy: Jacob Larfors
#  $LastChangedDate: 2016-06-02
#  $Version: 1.0
#
# Disclaimer: Please note that this software or software component is released by Emenda Software Ltd
# on a non-proprietary basis for commercial or non-commercial use with no warranty. Emenda Software Ltd
# will not be liable for any damage or loss caused by the use of this software. Redistribution is only
# allowed with prior consent.
#
# **************************************************************************************************

# developed with Python v2.7

import argparse
import subprocess
import re
import time
import sys

class LicenseStatus:
    AVAILABLE, NOT_AVAILABLE, ERROR = range(3)

# function checks if the given feature is available for the given license file
#
# returns 1 if license is available, 0 otherwise
def is_license_available(lmstat, license_file, feature, sleep, sleep_checks, debug):
    # call lmstat and get output
    cmd = [lmstat, '-c', license_file, '-f', feature]
    print ' '.join(cmd)
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    out, err = p.communicate()

    sleep_checks = sleep_checks

    if debug:
        print out

    # for each line in lmstat output
    for line in out.splitlines():
        # check if the line is associated with the feature
        if line.startswith('Users of {}'.format(feature)):
            if debug:
                print 'Parsing line: \'{}\''.format(line)
            # get the total number of licenses and the used number of licenses
            total, used = [int(s) for s in line.split() if s.isdigit()]
            if debug:
                print 'Total licenses available: {}, total licenses used: {}'.format(total, used)
            if used < total:
                return LicenseStatus.AVAILABLE
            else:
                return LicenseStatus.NOT_AVAILABLE

    return LicenseStatus.ERROR

def main():
    parser = argparse.ArgumentParser(description='Check whether a particular feature is available or not')
    parser.add_argument('--feature', '-f', default='floatserver11', help='The FlexLM license feature to check, e.g. floatserver11. Default=floatserver11')
    parser.add_argument('--lmstat', default='lmstat', help='The full path (including the lmstat executable) to the lmstat executable. Default=lmstat if in path')
    parser.add_argument('--license-file', '-c', default='27000@localhost', help='The port and host of the license server, in the standard FlexLM form <port>@<host>. Default=27000@localhost')
    parser.add_argument('--sleep', '-s', type=int, help='How long to sleep for if a license is not available')
    parser.add_argument('--sleep-checks', '-x', default='1', type=int, help='The number of times to sleep before exiting')
    parser.add_argument('--debug', dest='debug', action='store_true')

    args = parser.parse_args()
    if args.debug:
        print 'lmstat executable: \'{}\''.format(args.lmstat)
        print 'License file: \'{}\''.format(args.license_file)
        print 'License feature: \'{}\''.format(args.feature)
        print 'Sleep time: \'{}\''.format(args.sleep)
        print 'Sleep checks: \'{}\''.format(args.sleep_checks)

    sleep_checks = args.sleep_checks

    isLicenseAvailable = is_license_available(args.lmstat, args.license_file, args.feature, args.sleep, sleep_checks, args.debug)


    # check if sleep has been supplied and then sleep...
    if args.sleep != None:
        while isLicenseAvailable == LicenseStatus.NOT_AVAILABLE and sleep_checks > 0:
            time.sleep(args.sleep)
            sleep_checks = sleep_checks - 1
            isLicenseAvailable = is_license_available(args.lmstat, args.license_file, args.feature, args.sleep, sleep_checks, args.debug)

    # print some information about the exit
    if isLicenseAvailable == LicenseStatus.AVAILABLE:
        print 'License feature \'{}\' available'.format(args.feature)
        sys.exit(isLicenseAvailable)
    elif isLicenseAvailable == LicenseStatus.NOT_AVAILABLE:
        print 'Warning: License feature \'{}\' not available'.format(args.feature)
        sys.exit(isLicenseAvailable)
    else:
        print 'Error: Something went wrong. Please re-run with --debug flag for more information'.format(args.feature)
        sys.exit(isLicenseAvailable)


#------------------------------------------------------------------------------
if __name__ == '__main__':
    main()
#------------------------------------------------------------------------------
