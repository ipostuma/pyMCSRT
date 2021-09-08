import numpy as np
import matplotlib.pyplot as plt
import argparse

class read_phits_mesh:
    def __init__(self,mesh_file) -> None:
        
        # tally variables
        self.tallyfound = False
        self.comment = ""
        self.tallytype = ""
        self.xbins = []
        self.ybins = []
        self.zbins = []
        self.ebins = []
        self.part = []
        self.nx,self.ny,self.nz,self.ne,self.p = 0,0,0,1,0
        self.partdict={}
        self.axis = ""

        # read header to set variables
        with open(mesh_file,'r+') as f:
            self.tallytype = next(f)
            for line in f:
                if "title" in line:
                    self.comment = line.split("=")[-1]
                if "nx =" in line:
                    self.nx = int(line.split("#")[0].split()[-1])
                if "ny =" in line:
                    self.ny = int(line.split("#")[0].split()[-1])
                if "nz =" in line:
                    self.nz = int(line.split("#")[0].split()[-1])
                if "ne =" in line:
                    self.ne = int(line.split("#")[0].split()[-1])
                if "axis =" in line:
                    self.axis = line.split("#")[0].split()[-1]
                if "part =" in line:
                    self.part = line.split("=")[-1].split()
                    self.p = len(self.part)
                    for i in range(self.p):
                        self.partdict[self.part[i]]=i
                if ("#newpage:" in line):
                    break
        
        self.result = np.zeros((self.p,
                                self.nx,
                                self.ny,
                                self.nz,
                                self.ne))

        # loop through the input file
        with open(mesh_file,'r+') as f:
            for line in f:
                #if "part. =" in line:
                #    p_id=self.partdict[line.split("part. =")[-1].split()[0]]
                #    y = 0
                if ("hc:  y =" in line) and len(self.part) >= 0:
                    dump_n = self.nx
                    if self.axis == "xy":
                        dump_n = self.nz
                    if self.axis == "xz":
                        dump_n = self.ny
                    for dump_z in range(dump_n):
                        for l_p_id in range(len(self.part)):
                            dump_n2 = self.nz
                            if self.axis == "xy":
                                dump_n2 = self.ny
                            #print(dump_n2)
                            dump_n3 = self.ny
                            if self.axis == "xy":
                                dump_n3 = self.nx
                            dump = []
                            for i in range((dump_n2*dump_n3//10)+1):
                                dump += next(f).split()
                            if self.axis == "xy":
                                self.result[l_p_id,:,:,dump_z,0] = np.rot90(np.array(dump).reshape(dump_n2,dump_n3))
                            if self.axis == "xz":
                                self.result[l_p_id,:,dump_z,:,0] = np.rot90(np.array(dump).reshape(dump_n2,dump_n3))
                            if self.axis == "yz":
                                self.result[l_p_id,dump_z,:,:,0] = np.rot90(np.array(dump).reshape(dump_n2,dump_n3))
                            while True:
                                dump = next(f)
                                if "bitrseed" in dump:
                                    break
                                if "# ( ( data(x,y), x = 1, nx ), y = ny, 1, -1 )" in dump:
                                    next(f)
                                    next(f)
                                    break
                            

        print(self.partdict)



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Extract mesh result in readable format')
    parser.add_argument("file", type=str, nargs=1,
                        help='input file location')
    parser.add_argument("-o", dest='outfile', type=str, nargs=1,
                        help='output file name')
    parser.add_argument('-p','--plot',dest='plot', action='store_true',
                        help='plot info')
    args = parser.parse_args()

    # create an output file with the track count, the poissonian error and the execution time
    if not args.outfile:
        outfile='data.txt'
    else:
        outfile=args.outfile[0]

    # If user wants detailed plot information plot os set to true
    plot = False
    if(args.plot):
        plot = True
        print("plot "+str(plot))

    mesh_file = args.file[0]

    phits_mesh = read_phits_mesh(mesh_file)
    result = phits_mesh.result
    print(result)
    # results  
    print("{}\n{}".format(phits_mesh.comment,phits_mesh.tallytype))
    if plot:
        plot_number = result.shape[0]
        if plot_number >=2:
            fig, ax = plt.subplots(1,plot_number,figsize=(4*plot_number,4))
            fig.suptitle("{} {}".format(phits_mesh.tallytype.strip(),phits_mesh.comment.strip()))
            for i in range(plot_number):
                ax[i].title.set_text("{}".format(phits_mesh.part[i]))
                ax[i].imshow(result[i,:,:,0,0])
        elif plot_number==1:
            fig, ax = plt.subplots(1,1,figsize=(4,4))
            fig.suptitle("{} {}".format(phits_mesh.tallytype.strip(),phits_mesh.comment.strip()))
            ax.set_title("{}".format(phits_mesh.part[0]))
            ax.imshow(result[0,:,:,0,0])
        plt.show()
        plt.close()