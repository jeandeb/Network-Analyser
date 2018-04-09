import snap, numpy as np, matplotlib.image as mpimg, matplotlib.pyplot as plt, os

MAX_XTICKS_NUM = 25


def computeDegCorr(graph):
	knn = {}
	for u in graph.Nodes():
		ki = u.GetDeg()

		# Isolated nodes
		if ki == 0:
			continue

		ksum = 0.
		for i in range(ki):
			vid = u.GetNbrNId(i)
			ksum += graph.GetNI(vid).GetDeg()
		ksum = ksum / ki

		if ki not in knn:
			knn[ki] = []
		knn[ki].append(ksum)

	knn_arr = []
	for ki in knn:
		knn_arr.append( (ki, sum(knn[ki]) / len(knn[ki])) )
	knn_ndarr = np.array(knn_arr, dtype=float)

	sorted_ks = np.argsort(knn_ndarr[:, 0])
	knn_ndarr = knn_ndarr[sorted_ks]
	return knn_ndarr

def plotDegCorr(graph, name):
	out_fname = 'degcorr' + name + '.png'
	knn = computeDegCorr(graph)
	plt.clf()
	plt.figure(1)
	plt.plot(knn[:, 0], knn[:, 1], '-x')
	plt.subplots_adjust(left=0.1, bottom=0.075, right=1., top=1., wspace=0., hspace=0.)


	if knn[:, 0].max() > MAX_XTICKS_NUM:
		skip = int(knn[:, 0].max()) / MAX_XTICKS_NUM
		plt.xticks( np.arange(0, knn[:, 0].max() + 1 + skip, skip) )
	else:
		plt.xticks(np.arange(knn[:, 0].max() + 1))

	plt.ylim(knn[:, 1].min(), knn[:, 1].max())
	plt.xlabel('Degree', fontsize=16)
	plt.ylabel('Degree Correlation', fontsize=16)
	plt.yscale('log')
	plt.xscale('log')
	plt.grid(True)
	plt.savefig(out_fname, dpi=300, format='png')
	plt.close()

	return os.path.abspath(out_fname)


def getDegCentr(graph):
	nid = snap.GetMxDegNId(graph)
	CDn = snap.GetDegreeCentr(graph, nid)
	n = graph.GetNodes()

	freeman_nom = 0.

	for NI in graph.Nodes():
		CDi = snap.GetDegreeCentr(graph, NI.GetId())
		freeman_nom += CDn - CDi

	return freeman_nom / (n - 2)