# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
from __future__ import division, absolute_import, with_statement, print_function, unicode_literals
import subprocess
import re

__author__ = "Mike Long"
__license__ = "MPL 2.0"

TYPE = "Antivirus"
NAME = "Cylance"

SCORE = "/opt/infinity/bin/mono /opt/infinity/bin/InfinityDaemonClient localhost:9002 p ScoreFile "

DEFAULTCONF = {
    "ENABLED": True,
    "score": SCORE
}


def ping():
    try:
        # If Cylance service runs locally on port 9002 by default, change if configured differently
        status = "(echo >/dev/tcp/127.0.0.1/9002) &>/dev/null && echo '0' || echo '1'"
        return bool(subprocess.check_output([status], shell=True))
    except:
        raise


def scan(filelist, conf=DEFAULTCONF):
    results = []

    if ping():
        try:
            for f in filelist:
                scoreFile = conf["score"] + f
                output = subprocess.check_output([scoreFile], shell=True)

                ## Cleaning up the output ##
                ## Let's Remove the first two lines, not needed
                output = output.split("\n", 2)[2]
                ## Splitting output at funky characaters
                output = re.split('---- | ----|{|}|,|\n', output)
                ## There are emptying strings in the list, removing....
                output = [i for i in output if i != '']
                ## Cleaning up leading whitespaces
                output = [x.strip(' ') for x in output]
                ## End of cleaning ##

                # Add list to result
                # results.append(f,output)
                # Add score only to result
                results.append(f, output[9])

        except:
            raise
    else:
        print("Cylance Service on port 9002 is not running...")

    metadata = {
        'Name': "Cylance",
        'Type': "Antivirus"
    }

    return (results, metadata)
