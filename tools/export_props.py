# Converts selected glTF/GLB models into one compact binary for the game: positions, normals, colours (materials and
# texture colour swatches baked into vertex colours), indices. World transforms of the node tree are applied.
import json, struct, base64, glob, math, os, sys
from PIL import Image
import numpy as np
RAW = sys.argv[1]; OUT = sys.argv[2]
def load(path):
    if path.endswith('.glb'):
        b = open(path,'rb').read(); off = 12; js = None; bins = None
        while off < len(b):
            ln, typ = struct.unpack('<II', b[off:off+8]); chunk = b[off+8:off+8+ln]
            if typ == 0x4E4F534A: js = json.loads(chunk)
            else: bins = chunk
            off += 8 + ln
        buffers = [bins]
    else:
        js = json.load(open(path)); buffers = []
        for bf in js['buffers']:
            u = bf['uri']
            buffers.append(base64.b64decode(u.split(',',1)[1]) if u.startswith('data:') else open(os.path.join(os.path.dirname(path), u),'rb').read())
    return js, buffers
CT = {5120:'b',5121:'B',5122:'h',5123:'H',5125:'I',5126:'f'}; NC = {'SCALAR':1,'VEC2':2,'VEC3':3,'VEC4':4}
def acc(js, bufs, i):
    a = js['accessors'][i]; bv = js['bufferViews'][a['bufferView']]; n = NC[a['type']]; t = CT[a['componentType']]
    sz = struct.calcsize(t); stride = bv.get('byteStride', sz*n); base = bv.get('byteOffset',0) + a.get('byteOffset',0)
    data = bufs[bv['buffer']]
    arr = np.frombuffer(data, dtype=np.dtype(t), count=(a['count']-1)*stride//sz + n, offset=base)
    arr = np.lib.stride_tricks.as_strided(arr, shape=(a['count'], n), strides=(stride, sz)).astype(np.float64)
    if a.get('normalized'): arr = arr / {5121:255,5123:65535,5120:127,5122:32767}[a['componentType']]
    return arr
def trs(n):
    if 'matrix' in n: return np.array(n['matrix']).reshape(4,4).T
    t = n.get('translation',[0,0,0]); r = n.get('rotation',[0,0,0,1]); s = n.get('scale',[1,1,1])
    x,y,z,w = r
    R = np.array([[1-2*(y*y+z*z),2*(x*y-z*w),2*(x*z+y*w)],[2*(x*y+z*w),1-2*(x*x+z*z),2*(y*z-x*w)],[2*(x*z-y*w),2*(y*z+x*w),1-2*(x*x+y*y)]])
    M = np.eye(4); M[:3,:3] = R*np.array(s); M[:3,3] = t; return M
def export(path):
    js, bufs = load(path); tex_cache = {}
    def material_colour(mi, uv):
        if mi is None: return np.ones((len(uv) if uv is not None else 1,3))
        m = js['materials'][mi]; pbr = m.get('pbrMetallicRoughness', {}); f = np.array(pbr.get('baseColorFactor',[1,1,1,1])[:3])
        ti = pbr.get('baseColorTexture')
        if ti is not None and uv is not None:
            src = js['textures'][ti['index']]['source']
            if src not in tex_cache:
                im = js['images'][src]
                if 'uri' in im:
                    u = im['uri']
                    img = Image.open(os.path.join(os.path.dirname(path), u)) if not u.startswith('data:') else Image.open(__import__('io').BytesIO(base64.b64decode(u.split(',',1)[1])))
                else:
                    bv = js['bufferViews'][im['bufferView']]; img = Image.open(__import__('io').BytesIO(bufs[bv['buffer']][bv.get('byteOffset',0):bv.get('byteOffset',0)+bv['byteLength']]))
                tex_cache[src] = np.asarray(img.convert('RGB'), dtype=np.float64)/255
            T = tex_cache[src]; h, w = T.shape[:2]
            px = (np.mod(uv[:,0],1)*(w-1)).round().astype(int); py = (np.mod(uv[:,1],1)*(h-1)).round().astype(int)
            # texture colours are sRGB; base colour factors are linear -> convert factor to sRGB-ish for flat colour use
            return T[py, px] * (f ** (1/2.2))
        return np.tile(f ** (1/2.2), (len(uv) if uv is not None else 1, 1))
    P, N, C, I = [], [], [], []; vo = 0
    def walk(ni, parent):
        nonlocal vo
        n = js['nodes'][ni]; M = parent @ trs(n)
        if 'mesh' in n and 'skin' not in n:
            for pr in js['meshes'][n['mesh']]['primitives']:
                pos = acc(js, bufs, pr['attributes']['POSITION']); cnt = len(pos)
                nor = acc(js, bufs, pr['attributes']['NORMAL']) if 'NORMAL' in pr['attributes'] else np.tile([0,1,0],(cnt,1))
                uv = acc(js, bufs, pr['attributes']['TEXCOORD_0']) if 'TEXCOORD_0' in pr['attributes'] else None
                col = material_colour(pr.get('material'), uv)
                if len(col) == 1: col = np.tile(col[0], (cnt,1))
                idx = acc(js, bufs, pr['indices'])[:,0].astype(int) if 'indices' in pr else np.arange(cnt)
                ph = np.c_[pos, np.ones(cnt)] @ M.T; Nm = np.linalg.inv(M[:3,:3]).T; nn = nor @ Nm.T
                nn /= np.maximum(1e-9, np.linalg.norm(nn, axis=1))[:,None]
                if np.linalg.det(M[:3,:3]) < 0: idx = idx.reshape(-1,3)[:,[0,2,1]].ravel()
                P.append(ph[:,:3]); N.append(nn); C.append(col); I.append(idx + vo); vo += cnt
        for c in n.get('children', []): walk(c, M)
    scene = js['scenes'][js.get('scene',0)]
    for r in scene['nodes']: walk(r, np.eye(4))
    P = np.vstack(P); N = np.vstack(N); C = np.clip(np.vstack(C),0,1); I = np.concatenate(I)
    mn = P.min(0); mx = P.max(0)
    P -= [ (mn[0]+mx[0])/2, mn[1], (mn[2]+mx[2])/2 ]   # centre on x/z, sit on the floor (y=0)
    return P, N, C, I, (mx-mn)
want = {  # name -> source file pattern
 'container_long':'Container_Long.gltf','container_small':'Container_Small.gltf','crate':'Crate.gltf','boxes':'CardboardBoxes_1.gltf',
 'sacks':'SackTrench.gltf','sacks_small':'SackTrench_Small.gltf','barrier':'Barrier_Single.gltf','tires':'Debris_Tires.gltf','pallet':'Pallet.gltf',
 'cone':'TrafficCone.gltf','barrel':'ExplodingBarrel.gltf','streetlight':'StreetLight.gltf','tree1':'Tree_1.gltf','tree2':'Tree_2.gltf','tree3':'Tree_3.gltf',
 'tree4':'Tree_4.gltf','watertank':'WaterTank_Platform.gltf','health':'Health.gltf','ak':'AK.gltf','papers':'Debris_Papers_1.gltf',
 'bld_a':'building-a.glb','bld_c':'building-c.glb','bld_e':'building-e.glb','bld_g':'building-g.glb','bld_j':'building-j.glb','bld_m':'building-m.glb',
 'bld_p':'building-p.glb','bld_s':'building-s.glb','water_tower':'water-tower.glb','chimney':'chimney-large.glb','tank_big':'detail-tank-large.glb',
 'clip':'clip-large.glb'}
index = {}; blob = bytearray()
def put(arr, dt):
    global blob
    while len(blob) % 4: blob.append(0)
    o = len(blob); blob += arr.astype(dt).tobytes(); return o
for name, f in want.items():
    hits = [p for p in glob.glob(f'{RAW}/**/{f}', recursive=True) if 'GLB format' in p or f.endswith('.gltf')]
    if not hits: print('MISSING', name); continue
    P, N, C, I, size = export(hits[0])
    index[name] = {'v':len(P),'i':len(I),'size':[round(float(s),4) for s in size],
                   'pos':put(P,'<f4'),'nor':put(np.round(N*127),'<i1'),'col':put(np.round(C*255),'<u1'),'idx':put(I, '<u2' if len(P)<65536 else '<u4'),'i32':len(P)>=65536}
    print(f"{name:14s} {len(I)//3:6d} tris  size {np.round(size,2)}")
open(os.path.join(OUT,'props.bin'),'wb').write(blob); json.dump(index, open(os.path.join(OUT,'props.json'),'w'))
print('props.bin', len(blob)//1024, 'KB')
