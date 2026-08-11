#!/usr/bin/env python3
"""Publish a Wolf's Buzz/Nostr kind-0 profile picture using that Wolf's OWN key.

Usage:
  publish_wolf_profile.py --wolf <name> [--mapping wolf-profiles.json]

Security model:
  - Reads the Wolf's BUZZ_PRIVATE_KEY from its OWN profile .env (in-process,
    never on argv / stdout / logs). san -> ~/.hermes/.env; others ->
    ~/.hermes/profiles/<wolf>/.env (per the mapping key_env).
  - Each invocation touches exactly ONE Wolf's key and ONLY that Wolf's profile.
  - Prints only public data: wolf name, npub, event id, avatar URL, success.
  - Idempotent: Nostr kind-0 is replaceable; re-publishing the same content
    re-sets the profile without duplicating state.

The `buzz` CLI (maintained Nostr client in the stack) does the signing +
relay publish; we only supply the key via its environment.
"""
import argparse, json, os, subprocess

# --- nsec -> npub (pure stdlib, from hermes-buzz-native-gateway skill) ---
CHARSET = "qpzry9x8gf2tvdw0s3jn54khce6mua7l"
def _poly(v):
    G=[0x3b6a57b2,0x26508e6d,0x1ea119fa,0x3d4233dd,0x2a1462b3]; c=1
    for x in v:
        b=c>>25; c=((c&0x1ffffff)<<5)^x
        for i in range(5): c^=G[i] if ((b>>i)&1) else 0
    return c
def _hexp(h): return [ord(x)>>5 for x in h]+[0]+[ord(x)&31 for x in h]
def _b32d(b):
    p=b.rfind('1'); h=b[:p]; d=[CHARSET.find(x) for x in b[p+1:]]
    assert _poly(_hexp(h)+d)==1; return h,d[:-6]
def _conv(d,f,t,pad=True):
    acc=0;bits=0;r=[];mx=(1<<t)-1
    for v in d:
        acc=(acc<<f)|v;bits+=f
        while bits>=t: bits-=t; r.append((acc>>bits)&mx)
    if pad and bits: r.append((acc<<(t-bits))&mx)
    return r
def _b32e(h,d):
    c=_poly(_hexp(h)+d+[0]*6)^1; cs=[(c>>(5*(5-i)))&31 for i in range(6)]
    return h+'1'+''.join(CHARSET[x] for x in d+cs)
P=0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
Gx=0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798
Gy=0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8
def _inv(a,m): return pow(a,m-2,m)
def _add(p1,p2):
    if p1 is None: return p2
    x1,y1=p1;x2,y2=p2
    if x1==x2 and (y1+y2)%P==0: return None
    lam=((3*x1*x1)*_inv(2*y1,P))%P if p1==p2 else ((y2-y1)*_inv(x2-x1,P))%P
    x3=(lam*lam-x1-x2)%P; return (x3,(lam*(x1-x3)-y1)%P)
def _mul(k,pt):
    r=None
    while k:
        if k&1: r=_add(r,pt)
        pt=_add(pt,pt); k>>=1
    return r
def nsec_to_npub(nsec):
    h,d=_b32d(nsec); assert h=="nsec"
    priv=bytes(_conv(d,5,8,False)); assert len(priv)==32
    pub=_mul(int.from_bytes(priv,"big"),(Gx,Gy))
    pb=pub[0].to_bytes(32,"big")
    return _b32e("npub",_conv(list(pb),8,5))
# --------------------------------------------------------------------------

def env_key(path, name):
    path=os.path.expanduser(path)
    try:
        for l in open(path):
            if l.startswith(name+"="): return l.split("=",1)[1].strip().strip('"').strip("'")
    except Exception: pass
    return None

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--wolf", required=True)
    ap.add_argument("--mapping", default=os.path.join(os.path.dirname(os.path.abspath(__file__)),"wolf-profiles.json"))
    ap.add_argument("--relay", default=None)
    args=ap.parse_args()

    m=json.load(open(args.mapping))
    if args.wolf not in m["wolves"]:
        raise SystemExit(f"wolf '{args.wolf}' not in mapping")
    entry=m["wolves"][args.wolf]
    relay=args.relay or m.get("relay") or os.environ.get("BUZZ_RELAY_URL")

    key=env_key(entry["key_env"],"BUZZ_PRIVATE_KEY")
    if not key:
        raise SystemExit(f"no BUZZ_PRIVATE_KEY at {entry['key_env']}")
    npub=nsec_to_npub(key)

    env=dict(os.environ); env["BUZZ_RELAY_URL"]=relay; env["BUZZ_PRIVATE_KEY"]=key
    cmd=["buzz","users","set-profile",
         "--name",entry["display_name"],
         "--avatar",entry["picture"],
         "--about",entry["about"]]
    r=subprocess.run(cmd,env=env,capture_output=True,text=True,timeout=60)
    out=(r.stdout or r.stderr).strip()
    try:
        o=json.loads(out)
        print(f"wolf={args.wolf} npub={npub} accepted={o.get('accepted')} "
              f"event_id={o.get('event_id')} relay={relay} picture={entry['picture']}")
    except Exception:
        print(f"wolf={args.wolf} npub={npub} raw={out[:200]}")

if __name__=="__main__":
    main()
