class RadioBackend:
    def connect(self):
        raise NotImplementedError

    def disconnect(self):
        pass

    def set_ptt(self, enabled: bool):
        raise NotImplementedError

    def status(self):
        return "Unknown"


class MockRadio(RadioBackend):
    def __init__(self):
        self.connected = False
        self.ptt = False

    def connect(self):
        self.connected = True

    def disconnect(self):
        self.ptt = False
        self.connected = False

    def set_ptt(self, enabled: bool):
        if not self.connected:
            self.connect()
        self.ptt = bool(enabled)

    def status(self):
        if not self.connected:
            return "Mock radio disconnected"
        return "Mock PTT active — no RF" if self.ptt else "Mock radio connected"


class SerialPTTRadio(RadioBackend):
    """
    Generic serial-control-line PTT backend for a proper radio interface.

    This does NOT describe or assume any direct connection to a handheld radio.
    Use only with an interface specifically designed to expose PTT through a
    serial control line.

    RTS is used as the PTT signal.
    """

    def __init__(self, port):
        self.port = port
        self.ser = None
        self.ptt = False

    def connect(self):
        if not self.port:
            raise RuntimeError("No PTT serial port configured.")

        import serial

        self.ser = serial.Serial(self.port, baudrate=9600, timeout=0.2)
        self.ser.rts = False
        self.ptt = False

    def disconnect(self):
        if self.ser is not None:
            try:
                self.ser.rts = False
            finally:
                self.ser.close()
                self.ser = None
                self.ptt = False

    def set_ptt(self, enabled: bool):
        if self.ser is None:
            raise RuntimeError("Radio interface is not connected.")

        self.ser.rts = bool(enabled)
        self.ptt = bool(enabled)

    def status(self):
        if self.ser is None:
            return "Serial PTT interface disconnected"
        return "PTT asserted" if self.ptt else f"Connected on {self.port}"


class RadioManager:
    def __init__(self):
        self.backend = MockRadio()

    def connect(self, backend="mock", port=""):
        self.disconnect()

        if backend == "mock":
            self.backend = MockRadio()
        elif backend == "serial-ptt":
            self.backend = SerialPTTRadio(port)
        else:
            raise RuntimeError(f"Unsupported backend: {backend}")

        self.backend.connect()

    def disconnect(self):
        try:
            self.backend.disconnect()
        except Exception:
            pass

    def set_ptt(self, enabled):
        self.backend.set_ptt(enabled)

    def status(self):
        return self.backend.status()
