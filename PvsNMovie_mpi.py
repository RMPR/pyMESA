import os, sys
import numpy as np
import argparse as arp
import multiprocessing as mpi

#Video & plot 
import matplotlib.pyplot as plt
import matplotlib.cm as cm

#Mesa specifics
import mesaPlot as mp
    
p=arp.ArgumentParser(prog='PvsNVideo',description='Script to generate videos from MESA profile files. It uses mesaPlot')
p.add_argument('--version',action='version',version='%(prog)s 0.1')
p.add_argument('-dir','--folder',help='Folder with the profile*.data files',type=str,default='LOGS')
p.add_argument('-fn','--filename',help='Name of the generated video',type=str,default='PvsNAbunMovie.mp4')
p.add_argument('-fps',help='Framerate of the generated video',type=int,default=10)
p.add_argument('-mencoder',help='Use MEncoder to create video',action='store_true',default=False)
p.add_argument('-t','--title',help='Title of the plot',type=str,default='')
p.add_argument('-age',help='Show star age in the title',action='store_true',default=False)
p.add_argument('-xn','--xname',help='Name of the column to be used as x data',type=str,default='mass')
p.add_argument('-xl','--xlabel',help='Label of the x axis',default=None)
p.add_argument('-yl','--ylabel',help='Label of the y axis',default=None)
p.add_argument('-lim',help='Set the axis limits, both axis have the same limits',nargs=2,type=float)
p.add_argument('-clim',help='Set the colorbar limits',nargs=2,type=float)
p.add_argument('-threads',help='Nuber of threads',type=int,default=4)
args=p.parse_args() #parse arguments

if args.clim:
    cmin=args.clim[0]
    cmax=args.clim[1]
else:
    cmin=-5
    cmax=0


m=mp.MESA() #initialize mesaPlot instance to read and plot data

#find all profiles to import with mesaPlot
m._loadProfileIndex(args.folder)
models=m.prof_ind['model']

try:
    m.loadProfile(f=args.folder,num=models[0])
    x=m.prof.data[args.xname]
except (KeyError,AttributeError):
    raise ValueError(args.xname+"not found as data name")

fig1=plt.figure(1,figsize=(14,12))
ax=fig1.add_axes([0.2,0.15,0.7,0.75])
p=mp.plot()
p._listAbun(m.prof)
p.plotAbunPAndN(m,show=False,fig=fig1,ax=ax,show_title_age=args.age)
xb,xt=ax.get_xlim() #xbottom,xtop
yb,yt=ax.get_ylim() #ybottom,ytop
if args.lim:
    xaxis=ax.set_xlim(amin,amax)
    yaxis=ax.set_ylim(amin,amax)
else:
    xaxis=ax.set_xlim(-0.5,max(xt,yt))
    yaxis=ax.set_ylim(-0.5,max(xt,yt))
cb=plt.get_cmap()
cbar=cm.ScalarMappable(cmap=cb)
clim=cbar.set_clim(vmin=cmin,vmax=cmax)
plt.savefig('_tmp%04d'%(1))

def _saveAbun(iterargs,mesaM=m,mesaP=p,f=args.folder,show_age=args.age,title=args.title,xaxis=xaxis,yaxis=yaxis,cmin=cmin,cmax=cmax):
    i,fig,model_number,thread_num=iterargs
    fig.clf()   
    ax=fig.add_axes([0.2,0.15,0.7,0.75])
    mesaM.loadProfile(num=model_number,f=f)
    mesaP.plotAbunPAndN(m,show=False,fig=fig,ax=ax,show_title_age=show_age)
    fig.suptitle(title)
    ax.set_xlim(xaxis)
    ax.set_ylim(yaxis)
    ax.set_aspect('equal')
    cb=cm.get_cmap()
    cbar=cm.ScalarMappable(cmap=cb)
    clim=cbar.set_clim(vmin=cmin,vmax=cmax)
    plt.figure(thread_num)
    plt.savefig('_tmp%04d'%(i))

i=2
threads=np.arange(args.threads)
iterargs=[[i,fig1,models[i-1],1]]
for k in threads[1:]:
    iterargs.append([i+k,plt.figure(k+1,figsize=(14,12)),models[i-1+k],k+1])

for mod_no in models[1:-args.threads:args.threads]:
    for k in threads:
        iterargs[k][0]=i+k
        iterargs[k][2]=models[i-1+k]
    p=mpi.Pool(processes=args.threads)
    p.map(_saveAbun,iterargs)
    p.close()
    p.join()
    i+=args.threads

for mod_no in models[-args.threads+2:]:
    try: 
        mod_no=models[i-1]
        _saveAbun([i,fig1,mod_no,1])
    except IndexError:
        break
    i+=1

if args.mencoder:
    os.system("opt='vbitrate=2160000:mbd=2:keyint=132:v4mv:vqmin=3:vlelim=-4:vcelim=7:\
          lumi_mask=0.07:dark_mask=0.10:naq:vqcomp=0.7:vqblur=0.2:mpeg_quant'")
    os.system("mencoder 'mf://_tmp*.png' -mf type=png:fps=%d \
          -ovc lavc -lavcopts vcodec=mpeg4:vpass=1:$opt -oac copy -o %s" %(args.fps, args.filename))
else:
    ffmpeg='ffmpeg -framerate %d '%args.fps +'-i _tmp%04d.png '+args.filename
    os.system(ffmpeg)
os.system("rm -rf _tmp*.png")