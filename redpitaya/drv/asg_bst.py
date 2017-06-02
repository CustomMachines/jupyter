from ctypes import *

class asg_bst (object):
    """
    Generator FPGA module driver.
    """

    #: sampling frequency
    FS = 125000000.0
    # burst counter parameters
    CWR = 14  #: counter width - burst data repetition
    CWL = 32  #: counter width - burst period length
    CWN = 16  #: counter width - burst period number
    _CWRr = 2**CWR
    _CWLr = 2**CWL
    _CWNr = 2**CWN

    class _regset_t (Structure):
        _fields_ = [('cfg_bdr', c_uint32),  # burst data   repetitions
                    ('cfg_bdl', c_uint32),  # burst data   length
                    ('cfg_bpl', c_uint32),  # burst period length (data+pause)
                    ('cfg_bpn', c_uint32),  # burst period number
                    ('sts_bln', c_uint32),  # length (current position inside burst length)
                    ('sts_bnm', c_uint32)]  # number (current burst counter)

    def show_regset (self):
        """Print FPGA module register set for debugging purposes."""
        print (
            "cfg_bdr = 0x{reg:08x} = {reg:10d}  # burst data   repetition        \n".format(reg=self.regset.bst.cfg_bdr)+
            "cfg_bdl = 0x{reg:08x} = {reg:10d}  # burst data   length            \n".format(reg=self.regset.bst.cfg_bdl)+
            "cfg_bpl = 0x{reg:08x} = {reg:10d}  # burst period length            \n".format(reg=self.regset.bst.cfg_bpl)+
            "cfg_bpn = 0x{reg:08x} = {reg:10d}  # burst period number            \n".format(reg=self.regset.bst.cfg_bpn)+
            "sts_bln = 0x{reg:08x} = {reg:10d}  # burst length (current position)\n".format(reg=self.regset.bst.sts_bln)+
            "sts_bnm = 0x{reg:08x} = {reg:10d}  # burst number (current counter) \n".format(reg=self.regset.bst.sts_bnm)
        )

    @property
    def burst_data_repetitions (self) -> int:
        """Burst data repetitions, up to 2**`CWL`."""
        return (self.regset.bst.cfg_bdr + 1)

    @burst_data_repetitions.setter
    def burst_data_repetitions (self, value: int):
        if (value <= self._CWRr):
            self.regset.bst.cfg_bdr = value - 1
        else:
            raise ValueError("Burst data repetitions should be less or equal to {}.".format(self._CWRr))

    @property
    def burst_data_length (self) -> int:
        """Burst data length, up to waveform array size."""
        return (self.regset.bst.cfg_bdl + 1)

    @burst_data_length.setter
    def burst_data_length (self, value: int):
        if (value <= self._CWMr):
            self.regset.bst.cfg_bdl = value - 1
        else:
            raise ValueError("Burst data length should be less or equal to {}.".format(self._CWMr))

    @property
    def burst_period_length (self) -> int:
        """Burst period length (data+pause), up to 2**`CWL`."""
        return (self.regset.bst.cfg_bpl + 1)

    @burst_period_length.setter
    def burst_period_length (self, value: int):
        if (value <= self._CWLr):
            self.regset.bst.cfg_bpl = value - 1
        else:
            raise ValueError("Burst period length should be less or equal to {}.".format(self._CWLr))

    @property
    def burst_period_number (self) -> int:
        """Number of burst period reperitions, up to 2**`CWN`."""
        return (self.regset.bst.cfg_bpn + 1)

    @burst_period_number.setter
    def burst_period_number (self, value: int):
        if (value <= self._CWNr):
            self.regset.bst.cfg_bpn = value - 1
        else:
            raise ValueError("Burst period number should be less or equal to {}.".format(self._CWNr))
