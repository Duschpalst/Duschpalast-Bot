import json

with open('permissions/permission.json') as f:
    permission = json.load(f)

lvl1 = permission["perms"]["lvl1"]
lvl2 = permission["perms"]["lvl2"]


async def get(memb):
    lvl = [0]
    for r in memb.roles:
        if r.id in lvl2:
            lvl.append(2)
        elif r.id in lvl1:
            lvl.append(1)
    return max(lvl)


async def check(memb, lvl):
    return await get(memb) >= lvl
