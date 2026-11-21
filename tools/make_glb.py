# glTF (with embedded base64 buffer) -> GLB, keeping only the animations the game uses.
# Re-packs the buffer so data used only by dropped animations isn't shipped.
import json, base64, struct, sys
src, dst = sys.argv[1], sys.argv[2]
KEEP = {'Death','HitReact','Idle','Idle_Shoot','Run','Run_Shoot','Walk','Walk_Shoot'}
js = json.load(open(src)); buf = base64.b64decode(js['buffers'][0]['uri'].split(',',1)[1])
js['animations'] = [a for a in js.get('animations',[]) if a['name'] in KEEP]
# which accessors are still used?
used = set()
for m in js['meshes']:
    for p in m['primitives']:
        used.update(p['attributes'].values())
        if 'indices' in p: used.add(p['indices'])
        for t in p.get('targets',[]): used.update(t.values())
for s in js.get('skins',[]):
    if 'inverseBindMatrices' in s: used.add(s['inverseBindMatrices'])
for a in js['animations']:
    for smp in a['samplers']: used.update([smp['input'], smp['output']])
amap = {}; accs = []
for i, a in enumerate(js['accessors']):
    if i in used: amap[i] = len(accs); accs.append(a)
out = bytearray(); bvs = []
for a in accs:  # one bufferView per accessor (simple, valid)
    bv = js['bufferViews'][a['bufferView']]
    start = bv.get('byteOffset',0); data = buf[start:start+bv['byteLength']]
    while len(out) % 4: out.append(0)
    nbv = {'buffer':0,'byteOffset':len(out),'byteLength':len(data)}
    if 'byteStride' in bv: nbv['byteStride'] = bv['byteStride']
    if 'target' in bv: nbv['target'] = bv['target']
    out += data; a['bufferView'] = len(bvs); bvs.append(nbv)
js['accessors'] = accs; js['bufferViews'] = bvs
remap = lambda i: amap[i]
for m in js['meshes']:
    for p in m['primitives']:
        p['attributes'] = {k: remap(v) for k, v in p['attributes'].items()}
        if 'indices' in p: p['indices'] = remap(p['indices'])
        if 'targets' in p: p['targets'] = [{k: remap(v) for k, v in t.items()} for t in p['targets']]
for s in js.get('skins',[]):
    if 'inverseBindMatrices' in s: s['inverseBindMatrices'] = remap(s['inverseBindMatrices'])
for a in js['animations']:
    for smp in a['samplers']: smp['input'] = remap(smp['input']); smp['output'] = remap(smp['output'])
while len(out) % 4: out.append(0)
js['buffers'] = [{'byteLength': len(out)}]
j = json.dumps(js, separators=(',',':')).encode(); j += b' ' * ((4 - len(j) % 4) % 4)
glb = struct.pack('<III', 0x46546C67, 2, 12 + 8 + len(j) + 8 + len(out)) + struct.pack('<II', len(j), 0x4E4F534A) + j + struct.pack('<II', len(out), 0x004E4942) + bytes(out)
open(dst,'wb').write(glb); print(dst, len(glb)//1024, 'KB', [a['name'] for a in js['animations']])
