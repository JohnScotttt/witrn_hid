import hid
import struct
import time

__all__ = ["WITRN_HID"]


K2_TARGET_VID = 0x0716
K2_TARGET_PID = 0x5060


class WITRN_HID:
    _fmt = struct.Struct(
        "<xxxxxxxxxxxxxxffIIffxxxxfffBxxxxxxxxx"
    #   "<xxBBxxxxxxxxxxffIIffxxxxfffBxxxxxxxxx"
        )

    def __init__(self, vid=K2_TARGET_VID, pid=K2_TARGET_PID):
        # self.sec = None
        # self.ms = None
        self.nowtime = None
        self.Ah = None
        self.Wh = None
        self.Rectime = None
        self.Runtime = None
        self.DP = None
        self.DM = None
        self.Temperature = None
        self.VBus = None
        self.Current = None
        self.Group = None
        self.data = None

        self.dev = hid.device()
        self.dev.open(vid, pid)

    def read_data(self, dev: hid.device=None) -> list:
        if dev is not None:
            self.data = dev.read(64)
        else:
            self.data = self.dev.read(64)
        return self.data

    def unpack(self, data: list=None) -> tuple:
        if data is None:
            if self.data is None:
                raise ValueError("No data available to unpack")
            data = self.data
        if len(data) < 64:
            raise ValueError("Data length is less than expected (64 bytes)")
        package = self._fmt.unpack(bytes(data))
        (
            # self.sec,
            # self.ms,
            self.Ah,
            self.Wh,
            self.Rectime,
            self.Runtime,
            self.DP,
            self.DM,
            self.Temperature,
            self.VBus,
            self.Current,
            self.Group
        ) = package
        return package

    def now(self) -> tuple:
        self.read_data()
        t = time.localtime()
        ms = int(time.time() * 1000) % 1000
        self.nowtime = time.strftime("%H:%M:%S", t) + f".{ms:03d}"
        return (self.nowtime, ) + self.unpack()

    def close(self):
        self.dev.close()


if __name__ == "__main__":
    device = WITRN_HID()
    try:
        while True:
            print(device.now())
    except Exception as e:
        print(f"Error reading data: {e}")
    finally:
        device.close()