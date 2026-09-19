#include <atomic>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <omp.h>

struct MT {
    uint32_t a[624]; int idx;
    void init(uint64_t seed) {
        a[0]=19650218U;
        for(int i=1;i<624;i++) a[i]=1812433253U*(a[i-1]^(a[i-1]>>30))+i;
        uint32_t key[2]={(uint32_t)seed,(uint32_t)(seed>>32)};
        int i=1,j=0;
        for(int k=624;k;k--) {
            a[i]=(a[i]^((a[i-1]^(a[i-1]>>30))*1664525U))+key[j]+j;
            if(++i>=624){a[0]=a[623];i=1;} if(++j>=2)j=0;
        }
        for(int k=623;k;k--) {
            a[i]=(a[i]^((a[i-1]^(a[i-1]>>30))*1566083941U))-i;
            if(++i>=624){a[0]=a[623];i=1;}
        }
        a[0]=0x80000000U; idx=624;
    }
    uint32_t next() {
        if(idx>=624){
            static const uint32_t mag[2]={0,0x9908b0dfU};
            int k=0; uint32_t y;
            for(;k<227;k++){y=(a[k]&0x80000000U)|(a[k+1]&0x7fffffffU);a[k]=a[k+397]^(y>>1)^mag[y&1];}
            for(;k<623;k++){y=(a[k]&0x80000000U)|(a[k+1]&0x7fffffffU);a[k]=a[k-227]^(y>>1)^mag[y&1];}
            y=(a[623]&0x80000000U)|(a[0]&0x7fffffffU);a[623]=a[396]^(y>>1)^mag[y&1]; idx=0;
        }
        uint32_t y=a[idx++]; y^=y>>11; y^=(y<<7)&0x9d2c5680U; y^=(y<<15)&0xefc60000U; y^=y>>18; return y;
    }
};

int main(int argc,char**argv){
    if(argc!=5){fprintf(stderr,"usage: %s lo hi mode hexprefix\n",argv[0]);return 2;}
    uint64_t lo=strtoull(argv[1],0,10),hi=strtoull(argv[2],0,10); int mode=atoi(argv[3]);
    const char* h=argv[4]; int n=strlen(h)/2; unsigned char want[64];
    for(int i=0;i<n;i++){unsigned x;sscanf(h+2*i,"%2x",&x);want[i]=x;}
    std::atomic<unsigned long long> found{0};
    #pragma omp parallel for schedule(static)
    for(unsigned long long seed=lo;seed<=hi;seed++){
        MT r;r.init(seed); bool ok=true;
        if(mode==0){for(int i=0;i<38;i++)r.next();for(int i=0;i<n;i++)if((r.next()>>24)!=want[i]){ok=false;break;}}
        else {for(int i=0;i<10;i++)r.next();for(int i=0;i<n;i+=4){uint32_t x=r.next();for(int j=0;j<4&&i+j<n;j++)if(((x>>(8*j))&255)!=want[i+j]){ok=false;break;}if(!ok)break;}}
        if(ok){found=seed;printf("MATCH %llu mode %d\n",seed,mode);}
    }
    return found?0:1;
}
