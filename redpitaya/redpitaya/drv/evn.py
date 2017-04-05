import numpy as np

class evn ():
    # control register masks
    CTL_TRG_MASK = np.uint32(1<<3) # 1 - sw trigger bit (sw trigger must be enabled)
    CTL_STP_MASK = np.uint32(1<<2) # 1 - stop/abort; returns 1 when stopped
    CTL_STR_MASK = np.uint32(1<<1) # 1 - start
    CTL_RST_MASK = np.uint32(1<<0) # 1 - reset state machine so that it is in known state

    def reset (self):
        """reset state machine, is used to synchronize alwways running streams"""
        self.regset.ctl_sts = self.CTL_RST_MASK

    def start (self):
        """start starte machine"""
        self.regset.ctl_sts = self.CTL_STR_MASK

    def stop (self):
        """stop state machine"""
        self.regset.ctl_sts = self.CTL_STP_MASK

    def trigger (self):
        """activate SW trigger"""
        self.regset.ctl_sts = self.CTL_TRG_MASK

    def status_run (self) -> bool:
        """Run status"""
        return (bool(self.regset.ctl_sts & self.CTL_STR_MASK))

    def status_trigger (self) -> bool:
        """Trigger status"""
        return (bool(self.regset.ctl_sts & self.CTL_TRG_MASK))

    @property
    def control_mask (self) -> tuple:
        """Enable masks for software event sources [reset, start, stop, trigger]"""
        return ([self.regset.cfg_rst,
                 self.regset.cfg_str,
                 self.regset.cfg_stp,
                 self.regset.cfg_swt])

    @control_mask.setter
    def control_mask (self, value: tuple):
        if isinstance(value, int):
            value = [value]*4
        """Enable masks for software event sources [reset, start, stop, trigger]"""
        self.regset.cfg_rst = value [0]
        self.regset.cfg_str = value [1]
        self.regset.cfg_stp = value [2]
        self.regset.cfg_swt = value [3]

    @property
    def trigger_mask (self) -> int:
        """Enable mask for hardware trigger sources"""
        return (self.regset.cfg_trg)

    @trigger_mask.setter
    def trigger_mask (self, value: int):
        """Enable mask for hardware trigger sources"""
        self.regset.cfg_trg = value
