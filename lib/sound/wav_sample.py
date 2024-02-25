from math import floor, sqrt
import time
from file_utils import pp_file_size
from sound.super_sample import SuperSample
from vector import remap

try:
    from typing import Literal, Union, Tuple
    from io import BytesIO
except ImportError:
    pass

# def remap_int_size(n: int, from_bits: int, to_bits: int) -> int:
#     return floor(n * (2 ** to_bits / 2 ** from_bits))


class WavSample(SuperSample):
    size: int
    header_size: int
    data_size: int
    byte_rate: int
    block_align: int
    length: int

    def __init__(self, stream: BytesIO) -> None:
        riff = stream.read(4)
        if riff != b'RIFF':
            raise ValueError(f'Only RIFF wav files supported, got {riff}')

        self.size = int.from_bytes(stream.read(4), 'little') + 8

        wave = stream.read(4)
        if wave != b'WAVE':
            raise ValueError(f'Invalid wav file, expected `WAVE`, got {wave}')

        fmt = stream.read(4)
        if fmt != b'fmt ':
            raise ValueError(f'Invalid wav file, expected `fmt `, got {fmt}')

        subchunk1Size = int.from_bytes(stream.read(4), 'little')
        # 16 for PCM, but I just ignore everything after these 16 bytes
        # if subchunk1Size + 16 != file_size:
        #     raise ValueError(
        #         f'Invalid wav file, subchunk1Size ({subchunk1Size}B) denotes size inconsistent with chunkSize + 16 ({file_size}B)')

        format_type = int.from_bytes(stream.read(2), 'little')
        if format_type != 1:
            raise ValueError(
                f'Non-PCM wav format types not supported, got `{format_type}`')

        channel_count = int.from_bytes(stream.read(2), 'little')

        if channel_count != 1:
            raise ValueError(
                f'Only mono wav files supported for now, got `{channel_count}` channels')

        sample_rate = int.from_bytes(stream.read(4), 'little')

        self.byte_rate = int.from_bytes(stream.read(4), 'little')
        self.block_align = int.from_bytes(stream.read(2), 'little')

        bit_depth = int.from_bytes(stream.read(2), 'little')

        if bit_depth % 8 != 0:
            raise ValueError(f'Wav file bit depth is not a multiple of 8')

        # I got a wav file where two empty bytes came before "data", so skip them.
        # This is actually denoted by the subchunk1Size (bytes 16-19)
        stream.read(subchunk1Size - 16)

        data = stream.read(4)
        if data != b'data':
            raise ValueError(
                f'Invalid wav file, expected `data`, got `{data}`')

        data_length = int.from_bytes(stream.read(4), 'little')

        self.header_size = stream.tell()

        super().__init__(
            stream,
            sample_rate=sample_rate,
            channel_count=channel_count,
            bit_depth=bit_depth,
            data_length=data_length,
            start_point=self.header_size
        )

    def show_header(self) -> str:
        return f"""
sample_rate={self.sample_rate}Hz
bit_depth={self.bit_depth}b
byte_depth={self.bit_depth // 8}B
channel_count={self.channel_count}ch
data_size={pp_file_size(self.data_size)}
data_length={self.length} samples
file_size={pp_file_size(self.size)}
header_size={self.header_size}B (common is 44B)
byte_rate={self.byte_rate}B
block_align={self.block_align}B/sample
"""
