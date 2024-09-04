from amaranth import *
from amaranth_cfu import InstructionBase, InstructionTestBase, simple_cfu, CfuTestBase
import unittest

class MeanInstruction(InstructionBase):
    def elab(self, m):
        with m.If(self.start):
            m.d.sync += self.output.eq(self.in0 + self.in1)
            m.d.sync += self.done.eq(1)
        with m.Else():
            m.d.sync += self.done.eq(0)

class MeanInstructionTest(InstructionTestBase):
    def create_dut(self):
        return MeanInstruction()
    def test(self):
        self.verify([
            (0, 0, 0),
            (4, 5, 9),
            (0xffffffff, 0xffffffff, 0xfffffffe),
        ])

def make_cfu():
    return simple_cfu({
        0: MeanInstruction(),
    })

class CfuTest(CfuTestBase):
    def create_dut(self):
        return make_cfu()
    def test(self):
        return self.run_ops([
            ((0, 34, 35), 69),
        ])

if __name__ == "__main__":
    unittest.main()
