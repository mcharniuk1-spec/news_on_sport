from pathlib import Path
from toolkit import Canvas, Rig, icon, transition, lower_third, ticker, particles, counter, poll_bars, bubble
from PIL import Image, ImageChops
from tempfile import TemporaryDirectory

def probe():
    with TemporaryDirectory(dir=Path(__file__).parent) as tmp:
        result=[]
        for i in range(1,13):
            c=Canvas('#a3cedb')
            Rig('#6655b1','#ffd173','#513447').draw(c,265,730,420,i)
            icon(c,'ball',422,505,55,i)
            particles(c,i,265,470)
            lower_third(c,['TEST'])
            ticker(c,'TEST',i)
            poll_bars(c,[counter(0,10,i/12)/10,.7],i)
            bubble(c,['TEST'])
            transition(c,i,12,'ink-splash','page-turn','#a3cedb','#6d50a6')
            p=Path(tmp)/f'f{i:04}.png'
            c.finish().save(p)
            with Image.open(p) as im:
                assert im.mode=='RGB' and im.size==(1080,1920)
                result.append(im.convert('L').resize((108,192)))
        assert all(ImageChops.difference(a,b).getbbox() for a,b in zip(result,result[1:]))
        print('toolkit probe: 12 opaque distinct 1080x1920 frames')
if __name__=='__main__':probe()
