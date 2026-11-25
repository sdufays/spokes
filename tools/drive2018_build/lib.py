import os,re
OUT='/Users/Sarah/spokes/raw/drive/2018'
def slug(s):
    s=s.lower().replace("’","").replace("'","")
    return re.sub(r'[^a-z0-9]+','-',s).strip('-')[:70]
def w(folder,title,dpath,link,typ,mod,rel,tags,summary,body):
    d=os.path.join(OUT,folder); os.makedirs(d,exist_ok=True)
    fn=f"2018_{slug(title)}.md"
    q=lambda s:s.replace('"','\\"')
    fm=f'---\ntitle: "{q(title)}"\nyear: 2018\ndrive_path: "Spokes 2018/{q(dpath)}"\ndrive_link: "{link}"\ntype: {typ}\nmodified: "{mod}"\nrelevance: {rel}\ntags: [{", ".join(tags)}]\nsummary: "{q(summary)}"\n---\n'
    open(os.path.join(d,fn),'w').write(fm+body.strip()+'\n')
def gd(i): return f"https://docs.google.com/document/d/{i}/edit"
def gs(i): return f"https://docs.google.com/spreadsheets/d/{i}/edit"
def gp(i): return f"https://docs.google.com/presentation/d/{i}/edit"
def gf(i): return f"https://drive.google.com/file/d/{i}/view"
