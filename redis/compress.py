from lz4.frame import decompress as _decompress
import lz4.frame

class Lz4:
    '''
    compression_level :: specifies the level of compression used with 0 (default) being the lowest compression (0-2 are the same value),
         and 16 the highest compression. Values below 0 will enable “fast acceleration”, proportional to the value.
         Values above 16 will be treated as 16.
    block_size :: specifies the maximum block size to use for the blocks in a frame
    block_linked :: specifies whether to use block-linked compression
    content_checksum :: specifies whether to enable checksumming of the uncompressed content
    auto_flush :: specifies whether the library should buffer input data or not.
    store_size :: If True, the size of the uncompressed data will be stored in the frame header.
    '''
    def __init__(self):
        self.jump = 3
        self.compression_level = lz4.frame.COMPRESSIONLEVEL_MINHC
        self.block_size = lz4.frame.BLOCKSIZE_DEFAULT
        self.block_linked = True
        self.content_checksum = False
        self.auto_flush = False
        self.store_size = True

    def compress(self, data: bytes):
        assert (isinstance(data, bytes))
        c_context = lz4.frame.create_compression_context()
        compressed = lz4.frame.compress_begin(
            c_context,
            compression_level=self.compression_level,
            block_size=self.block_size,
            block_linked=self.block_linked,
            content_checksum=self.content_checksum,
            auto_flush=self.auto_flush,
            # store_size=self.store_size
        )
        cur, jump, limit = 0, self.jump, len(data)

        while (True):
            if cur >= limit:
                break
            compressed += lz4.frame.compress_chunk(c_context, data[cur:cur + jump])
            cur = cur + jump

        compressed += lz4.frame.compress_flush(c_context)
        return compressed

    def decompress(self, data):
        assert (isinstance(data, bytes))
        d_context = lz4.frame.create_decompression_context()
        decompressed = bytes()
        cur, jump, limit = 0, self.jump, len(data)

        while (True):
            if cur >= limit:
                break
            decompressed += lz4.frame.decompress_chunk(d_context, data[cur:cur + jump])[0]
            cur = cur + jump

        return decompressed
