from fpioa_manager import fm
fm.register(7, fm.fpioa.UART1_TX, force=True)
fm.register(6, fm.fpioa.UART1_RX, force=True)
from machine import UART
uart = UART(UART.UART1, 115200, 8, 1, 0, timeout=1000, read_buf_len=4096)
UART.set_repl_uart(uart)
