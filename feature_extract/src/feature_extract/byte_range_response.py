from typing import Iterator


class ByteRangeResponse:
    def __init__(
        self,
        content_range: str,
        content_type: str,
        byte_iterator: Iterator[bytes],
    ):
        self.content_range = content_range
        self.content_type = content_type
        self.byte_iterator = byte_iterator
