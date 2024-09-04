from amaranth import *
from amaranth.back import verilog
from cfu import make_cfu

if __name__ == "__main__":
    cfu = make_cfu()
    verilog = verilog.convert(cfu, name="cfu", ports=cfu.ports)
    with open("cfu.v", "w") as file:
        file.write(verilog)
