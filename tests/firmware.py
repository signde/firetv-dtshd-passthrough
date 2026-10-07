#!/usr/bin/env python3
"""Check packaged shell and agent guards against an external firmware corpus."""
from pathlib import Path
import json
import subprocess
import sys
import tempfile
import zipfile

root = Path(__file__).resolve().parents[1]
corpus = Path(sys.argv[1]).resolve()
with zipfile.ZipFile(sys.argv[2]) as z:
    helper = z.read('verify-firmware.sh').decode()
    profiles = {n: z.read(n).decode() for n in z.namelist()
                if n.startswith('firmware/') and n.endswith('.sha256')}
    agent = z.read('runtime.js').decode().split('const cm=new CModule', 1)[0]
    agent += '\n} catch(e) { throw e; }'
expected = {
    'ps7688.4591', 'ps7690.4714', 'ps7690.4716', 'ps7696.5226', 'ps7696.5229',
    'ps7699.4894', 'ps7699.4896', 'ps7702.4965', 'ps7704.5024', 'ps7706.5106',
    'ps7707.5376', 'ps7710.6003', 'ps7711.5272', 'ps7712.5371', 'ps7713.5443',
    'ps7714.5503', 'ps7714.5506', 'ps7714.5507', 'ps7715.5585', 'ps7716.5665',
    'ps7717.5741',
}
paths = [line.split()[1] for line in next(iter(profiles.values())).splitlines()]
cases = []
for folder in sorted(corpus.iterdir()):
    if not folder.is_dir():
        continue
    buffers = {p: (folder/Path(p).name).read_bytes() for p in paths}
    cases.append((folder.name, buffers, folder.name in expected, 'arm'))
base = next(buffers for name, buffers, ok, arch in cases if name == 'ps7702.4965')
for path in paths:
    damaged = dict(base)
    damaged[path] += b'corrupt'
    cases.append(('corrupt-' + Path(path).name, damaged, False, 'arm'))
    mixed = dict(base)
    mixed[path] = (corpus/'ps7299.3051'/Path(path).name).read_bytes()
    cases.append(('mixed-' + Path(path).name, mixed, False, 'arm'))
cases.append(('wrong-arch', base, False, 'arm64'))
with tempfile.TemporaryDirectory(prefix='dtshd-firmware-test-') as tmp:
    tmp = Path(tmp)
    (tmp/'firmware').mkdir()
    (tmp/'verify-firmware.sh').write_text(helper)
    node_cases = []
    for name, buffers, expected_ok, arch in cases:
        folder = tmp/name
        folder.mkdir()
        mapping = {}
        for path, content in buffers.items():
            local = folder/Path(path).name
            local.write_bytes(content)
            mapping[path] = str(local)
        for profile, content in profiles.items():
            translated = ''.join(digest+'  '+mapping[path]+'\n'
                                 for digest, path in (line.split() for line in content.splitlines()))
            (tmp/profile).write_text(translated)
        if arch == 'arm':
            result = subprocess.run(['sh', '-c', '. "$1/verify-firmware.sh"; verify_firmware "$1"',
                                     'sh', str(tmp)])
            assert (result.returncode == 0) == expected_ok, ('shell', name)
        node_cases.append(dict(name=name, mapping=mapping, expected=expected_ok, arch=arch))
    (tmp/'cases.json').write_text(json.dumps(node_cases))
    (tmp/'guard.js').write_text(agent)
    js = r"""
const fs=require('fs'), vm=require('vm'), crypto=require('crypto');
const cases=JSON.parse(fs.readFileSync(process.argv[1]));
const source=fs.readFileSync(process.argv[2],'utf8');
for(const c of cases) {
  let accepted=true;
  try {
    vm.runInNewContext(source, {
      Process:{arch:c.arch,pointerSize:c.arch==='arm'?4:8},
      File:{readAllBytes:path=>fs.readFileSync(c.mapping[path])},
      Checksum:{compute:(algorithm,bytes)=>crypto.createHash(algorithm).update(bytes).digest('hex')},
    });
  } catch(e) {accepted=false;}
  if(accepted!==c.expected) throw Error('agent: '+c.name);
}
console.log('PASS: agent firmware profiles and wrong-architecture rejection');
"""
    subprocess.run(['node', '-e', js, str(tmp/'cases.json'), str(tmp/'guard.js')], check=True)
print('PASS: 21 allowed / 15 rejected firmware sets; corrupt and mixed libraries rejected by shell and agent')
