import numpy as np


def random_direction(n, rng=None):
	"""
	returns an n-dimensional vector with random direction and length n
	"""
	if rng is None:
		rng = np.random.default_rng()

	vector = rng.normal(0,1,n)
	return vector/np.linalg.norm(vector)

def orthonormalise(vectors):
	"""
	Orthonormalise vectors in place (with Gram-Schmidt) and return their norms after orthogonalisation (but before normalisation).
	"""
	norms = []
	for i,vector in enumerate(vectors):
		for j in range(i):
			vector -= np.dot( vector, vectors[j] ) * vectors[j]
		norm = np.linalg.norm(vector)
		vector /= norm
		norms.append(norm)
	
	return np.array(norms)

def orthonormalise_qr(vectors):
	"""
	Return orthonormalised vectors (using `numpy.linalg.qr`) and return their norms after orthogonalisation (but before normalisation).
	"""
	A = np.asarray(vectors).T
	vectors,R = np.linalg.qr(A)
	signs = np.sign(R.diagonal())
	vectors *= signs
	norms = R.diagonal()*signs
	return vectors.T,norms

def rel_dist(x,y):
	x = np.asarray(x)
	y = np.asarray(y)
	return np.linalg.norm(x-y)/np.linalg.norm(np.mean((x,y)))

