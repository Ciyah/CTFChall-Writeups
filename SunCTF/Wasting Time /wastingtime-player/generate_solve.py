from pathlib import Path


P = "typedef unsigned long U;long read(int,void*,U),write(int,void*,U);U q[]={"


def make_r(p, logical_length):
    return (
        "};unsigned char s[3001],b[4000];U k;"
        "void d(U x){unsigned char t[21];U n=0;do{t[n++]=48+x-x/10*10;x/=10;}while(x);while(n)s[k++]=t[--n];}"
        "U f(U x,U y){return x<<y|x>>(64-y);}"
        "int main(){U i,j,a,x,y,n;unsigned char*c,*v;"
        f"for(j=0;j<{p};j++)s[k++]=((unsigned char*)q)[j];"
        "for(j=0;j<sizeof(q)/8;j++){d(q[j]);s[k++]=44;}"
        f"for(j={p};j<{logical_length};j++)s[k++]=((unsigned char*)q)[j];"
        "s[k++]=10;read(0,b,4000);"
        "U*h=(U*)b;a=h[2]^11400714819323198485UL;n=k;"
        "v=b+32+9*h[3];"
        "for(i=0;i<n;i++){x=s[h[0]]^v[i];a^=x+1;c=b+32;"
        "for(j=0;j<h[3];j++){int t=*c;y=*(U*)(c+1);"
        "if(t==0)a^=y;else if(t==1)a+=y;else if(t==2)a*=y;"
        "else if(t==3)a=f(a,y);else if(t==4)a^=(x+y+i)*1406734886183297941UL;"
        "else a+=h[2]^y^i;c+=9;}"
        "h[0]+=h[1];if(h[0]>=n)h[0]-=n;}"
        "a=f(a,29)^10323789583279413013UL;k=0;d(a);write(1,s,k);return 0;}"
    )


r = make_r(len(P), 0)
while True:
    new_r = make_r(len(P), len(P + r))
    if new_r == r:
        break
    r = new_r

template = (P + r).encode()
template += bytes((-len(template)) % 8)
words = [int.from_bytes(template[i : i + 8], "little") for i in range(0, len(template), 8)]
source = P + "".join(f"{word}," for word in words) + r
rebuilt = (
    template[: len(P)].decode()
    + "".join(f"{word}," for word in words)
    + template[len(P) : len(P + r)].decode()
)

banned = set("#?%\"'\\")
assert rebuilt == source
assert not (set(source) & banned)
assert len(source.encode()) <= 3000, len(source.encode())
Path("solve.c").write_text(source)
print(f"generated solve.c: {len(source)} bytes, {len(words)} packed template words")
