import sys
import logging
from time import time

from pycaliper.pycmanager import PYCArgs, setup_all
from pycaliper.verif.jgverifier import JGVerifier1Trace

from tage import boundary_spec, tage_config
from tage_tcl_template import template

# Log to a debug file with overwriting
logging.basicConfig(filename="debug.log", level=logging.DEBUG, filemode="w")

def test_main(bw):
    BHTWIDTH = bw
    TAGEWIDTH = BHTWIDTH - 2

    # Create tcl using template
    with open("tage.tcl", "w") as f:
        f.write(template(BHTWIDTH, TAGEWIDTH))

    args = PYCArgs(jgcpath="config_boundary.json")
    is_conn, pyconfig, tmgr = setup_all(args)

    time_start = time()

    tage_conf = tage_config(BHT_IDX_WIDTH=BHTWIDTH, TAGE_IDX_WIDTH=TAGEWIDTH)

    verifier = JGVerifier1Trace()
    res = verifier.verify(boundary_spec(config=tage_conf).instantiate(), pyconfig)

    time_end = time()
    print("Time taken: ", time_end - time_start)
    print(
        f"Verification result for {BHTWIDTH} {TAGEWIDTH}: ",
        "PASS" if res else "FAIL",
    )

if __name__ == "__main__":
    # Take the BHTWIDTH as an argument from the command line
    bw = int(sys.argv[1])
    test_main(bw)