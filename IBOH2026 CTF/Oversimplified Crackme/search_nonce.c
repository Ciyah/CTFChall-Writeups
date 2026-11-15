/* Challenge-specific AVX2 BLAKE2s-256 search. Reads Keys 1-5 from solution_keys.txt.
 * Build: gcc -O3 -mavx2 -fopenmp search_nonce.c -o /tmp/search_nonce
 * Run: /tmp/search_nonce
 */
#include <immintrin.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include <omp.h>
typedef __m256i V;
#define ADD _mm256_add_epi32
#define XOR _mm256_xor_si256
#define SET(x) _mm256_set1_epi32(x)
#define R(x,n) _mm256_or_si256(_mm256_srli_epi32(x,n),_mm256_slli_epi32(x,32-n))
#define G(a,b,c,d,x,y) a=ADD(ADD(a,b),x);d=R(XOR(d,a),16);c=ADD(c,d);b=R(XOR(b,c),12);a=ADD(ADD(a,b),y);d=R(XOR(d,a),8);c=ADD(c,d);b=R(XOR(b,c),7)
uint32_t iv[]={0x6A09E667,0xBB67AE85,0x3C6EF372,0xA54FF53A,0x510E527F,0x9B05688C,0x1F83D9AB,0x5BE0CD19};
unsigned char sig[10][16]={{0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15},{14,10,4,8,9,15,13,6,1,12,0,2,11,7,5,3},{11,8,12,0,5,2,15,13,10,14,3,6,7,1,9,4},{7,9,3,1,13,12,11,14,2,6,5,10,4,0,15,8},{9,0,5,7,2,4,10,15,14,1,11,12,6,8,3,13},{2,12,6,10,0,11,8,3,4,13,7,5,15,14,1,9},{12,5,1,15,14,13,4,10,0,7,6,3,9,2,8,11},{13,11,7,14,12,1,3,9,5,0,15,4,8,6,2,10},{6,15,14,9,11,3,0,8,12,2,13,7,1,4,10,5},{10,2,8,4,7,6,1,5,15,11,9,14,3,12,13,0}};
void comp(V*h,V*m,int count,int last){V v[16];for(int i=0;i<8;i++){v[i]=h[i];v[i+8]=SET(iv[i]);}v[12]=XOR(v[12],SET(count));if(last)v[14]=XOR(v[14],SET(-1));for(int r=0;r<10;r++){unsigned char*s=sig[r];G(v[0],v[4],v[8],v[12],m[s[0]],m[s[1]]);G(v[1],v[5],v[9],v[13],m[s[2]],m[s[3]]);G(v[2],v[6],v[10],v[14],m[s[4]],m[s[5]]);G(v[3],v[7],v[11],v[15],m[s[6]],m[s[7]]);G(v[0],v[5],v[10],v[15],m[s[8]],m[s[9]]);G(v[1],v[6],v[11],v[12],m[s[10]],m[s[11]]);G(v[2],v[7],v[8],v[13],m[s[12]],m[s[13]]);G(v[3],v[4],v[9],v[14],m[s[14]],m[s[15]]);}for(int i=0;i<8;i++)h[i]=XOR(h[i],XOR(v[i],v[i+8]));}
int main(){unsigned char p[1024]={0};int len=0;FILE*input=fopen("solution_keys.txt","rb");if(!input){perror("solution_keys.txt");return 1;}for(int i=0;i<5;i++){char line[256];if(!fgets(line,sizeof line,input))return 1;size_t n=strcspn(line,"\r\n");memcpy(p+len,line,n);len+=n;}fclose(input);if(len!=139){fprintf(stderr,"Expected this challenge\'s 139-byte key prefix.\n");return 1;}V base[8],msg[16];for(int i=0;i<8;i++)base[i]=SET(iv[i]^(i==0?0x1010020:0));for(int off=0;off<128;off+=64){for(int i=0;i<16;i++)msg[i]=SET(*(uint32_t*)(p+off+4*i));comp(base,msg,off+64,0);}memmove(p,p+128,len-128);memset(p+len-128,0,64-(len-128));for(int i=0;i<16;i++)msg[i]=SET(*(uint32_t*)(p+4*i));
#pragma omp parallel num_threads(4)
{V m[16],h[8];memcpy(m,msg,sizeof m);int tid=omp_get_thread_num();double start=omp_get_wtime();for(uint64_t n=tid*8;n<0x100000000ULL;n+=32){V ns=_mm256_set_epi32(n+7,n+6,n+5,n+4,n+3,n+2,n+1,n);m[2]=XOR(msg[2],_mm256_slli_epi32(ns,24));m[3]=_mm256_srli_epi32(ns,8);memcpy(h,base,sizeof h);comp(h,m,len+8,1);int mask=_mm256_movemask_ps((__m256)_mm256_cmpeq_epi32(h[0],SET(0)));if(mask){uint32_t out[8][8];for(int i=0;i<8;i++)_mm256_storeu_si256((V*)out[i],h[i]);for(int k=0;k<8;k++)if(mask>>k&1){printf("NONCE %llu hash ",(unsigned long long)(n+k));for(int i=0;i<8;i++)printf("%08x",__builtin_bswap32(out[i][k]));puts("");fflush(stdout);}}if(tid==0&&n&&!(n&0x3ffffff)){fprintf(stderr,"%llu %.1f M/s\n",(unsigned long long)n,n/(omp_get_wtime()-start)/1e6);}}}
}
