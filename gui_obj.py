
import ttk
import Tkinter as tk
import snap, numpy as np, matplotlib.image as mpimg, matplotlib.pyplot as plt
import gui_utils as gu
import reading_files as rf
from Tkinter import *
from tkFileDialog import askopenfilename
import tkMessageBox
import util
import PIL.Image
import PIL.ImageTk



class NetworkMenu(tk.Tk):

    def __init__(self, *args, **kwargs):

        #INTIALIZING GRAPH CHARACTERISTICS
        self.graph = snap.GenRndGnm(snap.PUNGraph, 10, 10)
        self.graph_name = ""
        self.number_of_nodes = 0
        self.number_of_edges = 0
        
        #CREATING THE ROOT WINDOW
        self.root = tk.Tk()
        self.root.title("Network Analysis GUI")

        #CREATING THE DIPLAYED FRAME
        self.mainframe = ttk.Frame(self.root, padding="3 3 12 12")
        self.mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        self.mainframe.columnconfigure(0, weight=1)
        self.mainframe.rowconfigure(0, weight=1)

        #NETWORK CHOICE 
        ttk.Label(self.mainframe, text="Choose the network:").grid(column=0, row=0, sticky=W)
        ttk.Button(self.mainframe, text="PostgreSQL", command=self.load_sql).grid(column=0, row=1, sticky=W)
        ttk.Button(self.mainframe, text="SNAP File", command=self.open_snap_file).grid(column=0, row=2, sticky=W)
        ttk.Button(self.mainframe, text="Random Network", command=self.random_network).grid(column=0, row=3, sticky=W)
        ttk.Button(self.mainframe, text="Scale-Free Network", command=self.scale_free_network).grid(column=0, row=4, sticky=W)

        #CHARACTERISTICS CHOICE
        ttk.Label(self.mainframe, text="Choose caracteristics:").grid(column=1, row=1, sticky=W)
        ttk.Button(self.mainframe, text="Degree Distribution", command=self.degree_distribution).grid(column=2, row=1, sticky=W)
        ttk.Button(self.mainframe, text="Centrality", command=self.centrality).grid(column=3, row=1, sticky=W)
        ttk.Button(self.mainframe, text="Clustering Coefficient", command=self.clust_coef).grid(column=4, row=1, sticky=W)
        ttk.Button(self.mainframe, text="Degree Correlation", command=self.degree_correlation).grid(column=5, row=1, sticky=W)
        ttk.Button(self.mainframe, text="Connectivity", command=self.connectivity).grid(column=6, row=1, sticky=W)

        #NETWORK CHARACTERISTICS DISPLAY
        ttk.Label(self.mainframe, text="Network Name: ").grid(column=1, row=0, sticky=W)
        ttk.Label(self.mainframe, text=" Number of Nodes: ").grid(column=3, row=0, sticky=W)
        ttk.Label(self.mainframe, text=" Number of Edges: ").grid(column=5, row=0, sticky=W)


        self.nameLabel = tk.Label( self.mainframe, text = "None" ) 
        self.nameLabel.grid( column = 2, row = 0, sticky = W )
        self.nameLabel.pack()

        self.numberOfNodes = tk.Label (self.mainframe, text = "None" )
        self.numberOfNodes.grid( column = 4, row = 0, sticky = W )
        self.numberOfNodes.pack()

        self.numberOfEdges = tk.Label( self.mainframe, text = "None" )
        self.numberOfEdges.grid( column = 6, row = 0, sticky = W )
        self.numberOfEdges.pack()

        for child in self.mainframe.winfo_children(): child.grid_configure(padx=10, pady=10)

    #UPDATE THE NETWORK'S DIPLAYED CHARACTERISTICS
    def add_characteristics( self, graph, graph_name ):

        nodes = str(graph.GetNodes())
        edges = str(graph.GetEdges())

        self.nameLabel.configure( text = graph_name )
        self.numberOfNodes.configure( text = nodes )
        self.numberOfEdges.configure( text = edges )


    #OPEN THE SNAP FILE -> NEEDS TO BE AN EDGE LIST
    def open_snap_file( self ):

        filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file
        self.graph = snap.LoadEdgeList(snap.PUNGraph, filename, 0, 1)

        self.graph_name = filename
        self.add_characteristics(  self.graph, self.graph_name )

    #LOAD THE SQL FILE -> NEEDS TO HAVE THE RIGHT CREDENTIALS
    def load_sql( self ):
  
        d = SQLDialog(self.root)
        self.root.wait_window(d.top)

        dbname = d.dbname
        user = d.user
        password = d.password
        

        self.graph = rf.read_from_sql( dbname, user, password )

        self.graph_name = dbname
        self.add_characteristics(  self.graph, self.graph_name )

    #CREATE A RANDOM NETWORK
    def random_network( self ):
        
        d = RnDialog(self.root)
        self.root.wait_window(d.top)

        nodes = d.nodes
        edges = d.edges

        self.graph = snap.GenRndGnm(snap.PUNGraph, nodes, edges)

        self.graph_name = "Random Network"
        self.add_characteristics( self.graph, self.graph_name )

    #CREATE A SCALE FREE NETWORK
    def scale_free_network( self ):

        d = SfDialog(self.root)
        self.root.wait_window(d.top)

        nodes = d.nodes
        power = d.power
        
        self.graph = snap.GenRndPowerLaw(nodes, power)

        self.graph_name = "Scale-Free Network"
        self.add_characteristics(  self.graph, self.graph_name )

    #COMPUTES THE DEGREE DISTRIBUTION, SHOW THE GRAPH
    def degree_distribution( self ):

        snap.PlotOutDegDistr( self.graph, "Degree_Distribution", " Graph Degree Distribution")
        img = mpimg.imread("outDeg.Degree_Distribution.png")
        plt.figure()
        imgplot = plt.imshow(img)
        plt.show()    
        
    def centrality( self ):
        tkMessageBox.showinfo(message = 'Graph degree centrality: ' + str(util.getDegCentr(self.graph)))

    def clust_coef( self ):
        snap.PlotClustCf( self.graph, "Clust_Coef", "Graph Clustering Coefficient")
        img = mpimg.imread("ccf.Clust_Coef.png")
        plt.figure()
        imgplot = plt.imshow(img)
        plt.show()   


    def degree_correlation( self ):
        plotPath = util.plotDegCorr( self.graph, "Degree_Correlation")
        img = mpimg.imread(plotPath)
        plt.figure()
        imgplot = plt.imshow(img)
        plt.show()    


    def connectivity( self ):
        snap.PlotSccDistr(self.graph, "Connectivity", "Connectivity")
        img = mpimg.imread("scc.Connectivity.png")
        plt.figure()
        imgplot = plt.imshow(img)
        plt.show()  


#THE SQL DIALOG TO ENTER NAME, USER AND PASSWORD
class SQLDialog:

    def __init__(self, parent):

        top = self.top = Toplevel(parent)

        Label(top, text="Database Name").pack()
        self.dbname_entry = Entry(top)
        self.dbname_entry.pack(padx=5)

        Label(top, text="User").pack()
        self.user_entry = Entry(top)
        self.user_entry.pack(padx=5)

        Label(top, text="Password").pack()
        self.password_entry = Entry(top)
        self.password_entry.pack(padx=5)

        b = Button(top, text="Submit", command=self.ok)
        b.pack(pady=5)

    def ok(self):

        self.dbname = str(self.dbname_entry.get())
        self.user = str(self.user_entry.get())
        self.password = str(self.password_entry.get())

        self.top.destroy()

#SIMPLE DIALOG TO ENTER RANDOM NETWORK CHARACTERISTICS
class RnDialog:

    def __init__(self, parent):

        top = self.top = Toplevel(parent)

        Label(top, text="Number of Nodes").pack()
        self.nodes_entry = Entry(top)
        self.nodes_entry.pack(padx=5)

        Label(top, text="Number of Edges").pack()
        self.edges_entry = Entry(top)
        self.edges_entry.pack(padx=5)

        b = Button(top, text="Submit", command=self.ok)
        b.pack(pady=5)

    def ok(self):

        self.nodes = int(self.nodes_entry.get())
        self.edges = int(self.edges_entry.get())

        self.top.destroy()

#SIMPLE DIALOG TO ENTER SCALE FREE CHARACTERISTICS
class SfDialog:

    def __init__(self, parent):

        top = self.top = Toplevel(parent)

        Label(top, text="Number of Nodes").pack()
        self.nodes_entry = Entry(top)
        self.nodes_entry.pack(padx=5)

        Label(top, text="Power Law Numebr").pack()
        self.power_entry = Entry(top)
        self.power_entry.pack(padx=5)

        b = Button(top, text="Submit", command=self.ok)
        b.pack(pady=5)

    def ok(self):

        self.nodes = int(self.nodes_entry.get())
        self.power = float(self.power_entry.get())

        self.top.destroy()

#LAUNCH THE GUI LOOP
app = NetworkMenu()
app.root.mainloop()
        