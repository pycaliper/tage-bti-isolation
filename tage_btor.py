import sys
import logging

from pycaliper.per import *
from pycaliper.pycconfig import DesignConfig
from pycaliper.proofmanager import mk_btordesign
from pycaliper.verif.btorverifier import BTORVerifier1Trace

from myspecs.tage import boundary_spec, tage_config

# Log to a debug file with overwriting
logging.basicConfig(filename="debug.log", level=logging.DEBUG, filemode="w")


def test_main(bw):
    BHTWIDTH = bw
    TAGEWIDTH = BHTWIDTH - 2

    des = mk_btordesign(f"full_design_{BHTWIDTH}_{TAGEWIDTH}", 
                        f"tage-predictor/btor/full_design_{BHTWIDTH}_{TAGEWIDTH}.btor")

    dc = DesignConfig(clk="clk_i")

    verifier = BTORVerifier1Trace()

    tage_conf = tage_config(BHT_IDX_WIDTH=BHTWIDTH, TAGE_IDX_WIDTH=TAGEWIDTH)

    result = verifier.verify(boundary_spec(config=tage_conf).instantiate(), des, dc)

    print(
        f"Verification result for {BHTWIDTH} {TAGEWIDTH}: ",
        "PASS" if result else "FAIL",
    )


if __name__ == "__main__":
    # Take the BHTWIDTH as an argument from the command line
    bw = int(sys.argv[1])
    test_main(bw)