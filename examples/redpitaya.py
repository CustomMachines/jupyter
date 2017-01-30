from ctypes import *
import os
import numpy as np

class redpitaya (object):
    CH_1 = 0
    CH_2 = 1

    TRIG_SRC_DISABLED = 0 # Trigger is disabled
    TRIG_SRC_NOW      = 1 # Trigger triggered now (immediately)
    TRIG_SRC_CHA_PE   = 2 # Trigger set to Channel A threshold positive edge
    TRIG_SRC_CHA_NE   = 3 # Trigger set to Channel A threshold negative edge
    TRIG_SRC_CHB_PE   = 4 # Trigger set to Channel B threshold positive edge
    TRIG_SRC_CHB_NE   = 5 # Trigger set to Channel B threshold negative edge
    TRIG_SRC_EXT_PE   = 6 # Trigger set to external trigger positive edge (DIO0_P pin)
    TRIG_SRC_EXT_NE   = 7 # Trigger set to external trigger negative edge (DIO0_P pin)
    TRIG_SRC_AWG_PE   = 8 # Trigger set to arbitrary wave generator application positive edge
    TRIG_SRC_AWG_NE   = 9 # Trigger set to arbitrary wave generator application negative edge

    WAVEFORM_SINE      = 0 # Wave form sine
    WAVEFORM_SQUARE    = 1 # Wave form square
    WAVEFORM_TRIANGLE  = 2 # Wave form triangle
    WAVEFORM_RAMP_UP   = 3 # Wave form sawtooth (/|)
    WAVEFORM_RAMP_DOWN = 4 # Wave form reversed sawtooth (|\)
    WAVEFORM_DC        = 5 # Wave form dc
    WAVEFORM_PWM       = 6 # Wave form pwm
    WAVEFORM_ARBITRARY = 7 # Use defined wave form

    TRIG_STATE_TRIGGERED = 0 # Trigger is triggered/disabled
    TRIG_STATE_WAITING   = 1 # Trigger is set up and waiting (to be triggered)

    TRIG_SRC_DISABLED = 0 # Trigger is disabled
    TRIG_SRC_NOW      = 1 # Trigger triggered now (immediately)
    TRIG_SRC_CHA_PE   = 2 # Trigger set to Channel A threshold positive edge
    TRIG_SRC_CHA_NE   = 3 # Trigger set to Channel A threshold negative edge
    TRIG_SRC_CHB_PE   = 4 # Trigger set to Channel B threshold positive edge
    TRIG_SRC_CHB_NE   = 5 # Trigger set to Channel B threshold negative edge
    TRIG_SRC_EXT_PE   = 6 # Trigger set to external trigger positive edge (DIO0_P pin)
    TRIG_SRC_EXT_NE   = 7 # Trigger set to external trigger negative edge (DIO0_P pin)
    TRIG_SRC_AWG_PE   = 8 # Trigger set to arbitrary wave generator application positive edge
    TRIG_SRC_AWG_NE   = 9 # Trigger set to arbitrary wave generator application negative edge

    def __init__(self, bitstream = "/opt/redpitaya/fpga/v0.94/fpga.bit"):
        os.system('cat '+bitstream+' > /dev/xdevcfg')
        self.rp_api = CDLL('/opt/redpitaya/lib/librp.so')
        self.Init()

    def __del__(self):
        self.Release()

    def Init(self):
        return self.rp_api.rp_Init()

    def Release(self):
        return self.rp_api.rp_Release()

    def GenReset(self):
        return self.rp_api.rp_GenReset()

    def GenFreq(self,channel, freq):
        return self.rp_api.rp_GenFreq(channel, c_float(freq))

    def GenAmp(self, channel, freq):
        return self.rp_api.rp_GenAmp(channel, c_float(freq))

    def GenWaveform(self, channel, form):
        return self.rp_api.rp_GenWaveform(channel, form)

    def GenArbWaveform(self, channel, buf):
        arr = (c_float * len(buf))(*buf)
        return self.rp_api.rp_GenArbWaveform(channel, arr, len(buf));

    def GenOutEnable(self, channel):
        return self.rp_api.rp_GenOutEnable(channel)

    def AcqReset(self):
        return self.rp_api.rp_AcqReset()

    def AcqSetDecimation(self, dec_factor):
        return self.rp_api.rp_AcqSetDecimation(dec_factor)

    def AcqSetTriggerLevel(self, channel, level):
        return self.rp_api.rp_AcqSetTriggerLevel(channel, c_float(level))

    def AcqSetTriggerDelay(self, delay):
        return self.rp_api.rp_AcqSetTriggerDelay(delay)

    def AcqStart(self):
        return self.rp_api.rp_AcqStart()

    def AcqSetTriggerSrc(self, source):
        return self.rp_api.rp_AcqSetTriggerSrc(source)

    def AcqGetTriggerState(self, ):
        state = c_long(self.TRIG_STATE_WAITING)
        self.rp_api.rp_AcqGetTriggerState(byref(state))
        return state.value

    def AcqGetBufSize(self):
        size = c_long(0)
        self.rp_api.rp_AcqGetBufSize(byref(size))
        return size.value

    def AcqGetOldestDataV(self, channel, size):
        buff = (c_float*size)()
        buff_size = c_long(size)
        self.rp_api.rp_AcqGetOldestDataV(channel, byref(buff_size), byref(buff));
        nbuff = np.frombuffer(buff, np.float32)
        return nbuff

    def AIpinGetValue(self, pin):
        value = c_float(0)
        self.rp_api.rp_AIpinGetValue(pin, byref(value))
        return value.value

    def AOpinSetValue(self, pin, value):
        return self.rp_api.rp_AOpinSetValue(pin, c_float(value))
