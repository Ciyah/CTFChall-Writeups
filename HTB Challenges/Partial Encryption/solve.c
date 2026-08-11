#include <immintrin.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static __m128i decrypt_block(__m128i in, unsigned char i) {
    __m128i index = _mm_set1_epi8((char)i);
    __m128i a = _mm_aeskeygenassist_si128(index, 0x00);
    __m128i b = _mm_aeskeygenassist_si128(index, 0x10);
    return _mm_aesdeclast_si128(_mm_xor_si128(in, b), a);
}

int main(int argc, char **argv) {
    if (argc != 3) return 1;
    FILE *in = fopen(argv[1], "rb");
    FILE *out = fopen(argv[2], "wb");
    if (!in || !out) return 2;
    fseek(in, 0, SEEK_END);
    long n = ftell(in);
    rewind(in);
    unsigned char *buf = malloc((size_t)n);
    fread(buf, 1, (size_t)n, in);
    /* .data: RVA 0x4000, raw file offset 0x2600, size 0x908. */
    const long blobs[][2] = {
        {0x000, 0x070}, {0x070, 0x040}, {0x0b0, 0x030},
        {0x0e0, 0x030}, {0x110, 0x030}, {0x140, 0x1a0},
        {0x2e0, 0x1e0}, {0x4c0, 0x270}, {0x730, 0x100}
    };
    for (unsigned b = 0; b < sizeof(blobs) / sizeof(blobs[0]); ++b) {
      for (long off = 0; off < blobs[b][1]; off += 16) {
        long pos = 0x2600 + blobs[b][0] + off;
        __m128i x = _mm_loadu_si128((const __m128i *)(buf + pos));
        x = decrypt_block(x, (unsigned char)(off / 16));
        _mm_storeu_si128((__m128i *)(buf + pos), x);
      }
    }
    fwrite(buf, 1, (size_t)n, out);
    fclose(out);
    fclose(in);
    free(buf);
    return 0;
}
