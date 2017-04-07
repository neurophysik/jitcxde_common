from __future__ import print_function, division, with_statement
import numpy as np

def random_direction(n):
	vector = np.random.normal(0,1,n)
	return vector/np.linalg.norm(vector)

def orthonormalise(vectors):
	"""
	Orthonormalise vectors (with Gram-Schmidt) and return their norms after orthogonalisation (but before normalisation).
	"""
	norms = []
	for i,vector in enumerate(vectors):
		for j in range(i):
			vector -= np.dot( vector, vectors[j] ) * vectors[j]
		norm = np.linalg.norm(vector)
		vector /= norm
		norms.append(norm)
	
	return np.array(norms)

