# devops/serial/serial_windows.py

import ctypes
import winreg


class SerialWindows:
    GENERIC_READ = 0x80000000
    GENERIC_WRITE = 0x40000000
    OPEN_EXISTING = 3
    FILE_ATTRIBUTE_NORMAL = 0x80
    INVALID_HANDLE_VALUE = ctypes.c_void_p(-1).value
    DCB_LENGTH = 28

    def devices(self):
        devices = []

        try:
            with winreg.OpenKey(
                winreg.HKEY_LOCAL_MACHINE,
                r"HARDWARE\DEVICEMAP\SERIALCOMM",
            ) as key:
                index = 0

                while True:
                    try:
                        _, value, _ = (
                            winreg.EnumValue(
                                key,
                                index,
                            )
                        )
                    except OSError:
                        break

                    devices.append(
                        str(value)
                    )

                    index += 1

        except OSError:
            return []

        return sorted(devices)

    def open(self, device):
        kernel32 = ctypes.windll.kernel32

        handle = kernel32.CreateFileW(
            device,
            self.GENERIC_READ
            | self.GENERIC_WRITE,
            0,
            None,
            self.OPEN_EXISTING,
            self.FILE_ATTRIBUTE_NORMAL,
            None,
        )

        if handle == self.INVALID_HANDLE_VALUE:
            return None

        try:
            self.configure(handle)
        except OSError:
            self.close(handle)
            return None

        return handle

    def configure(self, handle):
        kernel32 = ctypes.windll.kernel32

        dcb = ctypes.create_string_buffer(
            self.DCB_LENGTH
        )

        if not kernel32.GetCommState(
            handle,
            dcb,
        ):
            raise OSError

        ctypes.c_uint32.from_buffer(
            dcb,
            4,
        ).value = 115200

        flags = ctypes.c_uint32.from_buffer(
            dcb,
            8,
        )

        flags.value = (
            (flags.value & ~0x3)
            | 0x1
        )

        ctypes.c_ubyte.from_buffer(
            dcb,
            23,
        ).value = 8

        if not kernel32.SetCommState(
            handle,
            dcb,
        ):
            raise OSError

        timeouts = ctypes.create_string_buffer(
            20
        )

        ctypes.c_uint32.from_buffer(
            timeouts,
            0,
        ).value = 50

        ctypes.c_uint32.from_buffer(
            timeouts,
            4,
        ).value = 10

        ctypes.c_uint32.from_buffer(
            timeouts,
            8,
        ).value = 10

        ctypes.c_uint32.from_buffer(
            timeouts,
            12,
        ).value = 10

        ctypes.c_uint32.from_buffer(
            timeouts,
            16,
        ).value = 10

        if not kernel32.SetCommTimeouts(
            handle,
            timeouts,
        ):
            raise OSError

    def close(self, handle):
        if handle is None:
            return 0

        try:
            ctypes.windll.kernel32.CloseHandle(
                handle
            )
        except OSError:
            pass

        return 0

    def read(self, handle):
        if handle is None:
            return None

        kernel32 = ctypes.windll.kernel32

        buffer = ctypes.create_string_buffer(
            4096
        )

        count = ctypes.c_uint32()

        result = kernel32.ReadFile(
            handle,
            buffer,
            4096,
            ctypes.byref(count),
            None,
        )

        if not result:
            return None

        if count.value == 0:
            return b""

        return buffer.raw[:count.value]

    def write(self, handle, data):
        if handle is None:
            return False

        kernel32 = ctypes.windll.kernel32

        buffer = ctypes.create_string_buffer(
            data
        )

        count = ctypes.c_uint32()

        result = kernel32.WriteFile(
            handle,
            buffer,
            len(data),
            ctypes.byref(count),
            None,
        )

        if not result:
            return False

        return count.value == len(data)