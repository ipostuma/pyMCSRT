import numpy as np
import matplotlib.pyplot as plt
import argparse

class read_mcnp_mesh:
    def __init__(self,mesh_file,tally_num) -> None:
        self.begin_of_result="{}{:10d}".format("Mesh Tally Number",tally_num)

        # tally variables
        self.tallyfound = False
        self.comment = ""
        self.tallytype = ""
        self.xbins = []
        self.ybins = []
        self.zbins = []
        self.ebins = []
        self.result = []

        # loop through the input files
        with open(mesh_file,'r+') as f:
            for line in f:
                if (self.begin_of_result in line) and (not self.tallyfound):
                    self.tallyfound = True
                    self.comment = ' '.join(next(f).split())
                    self.tallytype = ' '.join(next(f).split())
                if (" Tally bin boundaries:" in line) and self.tallyfound:
                    dumpx = next(f).split()
                    self.xbins = [dumpx[i] for i in range(2,len(dumpx))]
                    dumpy = next(f).split()
                    self.ybins = [dumpy[i] for i in range(2,len(dumpy))]
                    dumpz = next(f).split()
                    self.zbins = [dumpz[i] for i in range(2,len(dumpz))]
                    dumpe = next(f).split()
                    self.ebins = [dumpe[i] for i in range(3,len(dumpe))]

                    next(f)
                    lastlayerlen = len(next(f).split())-1
                    self.result = np.zeros((1,
                                            len(self.xbins)-1,
                                            len(self.ybins)-1,
                                            len(self.zbins)-1,
                                            len(self.ebins)-1,lastlayerlen))

                    print(self.result.shape)

                    for x in range(len(self.xbins)-1):
                        for y in range(len(self.ybins)-1):
                            for z in range(len(self.zbins)-1):
                                for e in range(len(self.ebins)-1):
                                    self.result[0,x,y,z,e] = next(f).split()
                    
                    # when finishing reading the tally, reset variable to false
                    # and break the loop 
                    self.tallyfound = False
                    break

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Extract mesh result in readable format')
    parser.add_argument("file", type=str, nargs=1,
                        help='input file location')
    parser.add_argument('tally', type=int, nargs=1,
                        help='invert color of the image')
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
    tally_num = args.tally[0]

    mcnp_mesh = read_mcnp_mesh(mesh_file,tally_num)

    # results
    if len(mcnp_mesh.result) > 0:    
        print("{}\n{}".format(mcnp_mesh.comment,mcnp_mesh.tallytype))
        print(mcnp_mesh.xbins)
        print(mcnp_mesh.ybins)
        print(mcnp_mesh.zbins)
        print(mcnp_mesh.ebins)
        if plot:
            fig, ax = plt.subplots(1,2,figsize=(8,3))
            ax[0].set_title("YZ {} mesh".format(mcnp_mesh.tallytype))
            ax[0].imshow(mcnp_mesh.result[0,:,:,0,0,-2])
            print(mcnp_mesh.result[0,:,:,0,0,-2])
            ax[1].set_title("YZ {} mesh err".format(mcnp_mesh.tallytype))
            ax[1].imshow(mcnp_mesh.result[0,:,:,0,0,-1])
            plt.show()
            plt.close()
    else:
        print("Sorry tally was not found\n")