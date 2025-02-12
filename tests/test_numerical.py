#!/usr/bin/python3

import unittest

import numpy as np
from numpy.testing import assert_allclose

from jitcxde_common.numerical import orthonormalise, orthonormalise_qr, random_direction, rel_dist


class RandomDirectionTest(unittest.TestCase):
	def test_random_direction(self):
		d = 10
		n = 100000
		n_vectors = np.vstack([random_direction(d) for i in range(n)])
		average = np.average(n_vectors, axis=0)
		assert_allclose( average, np.zeros(d), rtol=0, atol=0.01 )

class OrthonormaliseTest(unittest.TestCase):
	def method(self,vectors):
		norms = orthonormalise(vectors)
		return vectors,norms

	def test_orthonormalise_1(self):
		vectors = [ np.array([3.0,4.0]) ]
		vectors,norms = self.method(vectors)
		assert_allclose( vectors[0], np.array([0.6,0.8]) )
		assert_allclose( norms, np.array([5]) )
	
	def test_orthonormalise_2(self):
		vectors = [ np.array([1.0,0.0]), np.array([0.0,1.0]) ]
		vectors,norms = self.method(vectors)
		assert_allclose( vectors[0], np.array([1.0,0.0]) )
		assert_allclose( vectors[1], np.array([0.0,1.0]) )
		assert_allclose( norms, np.array([1.0,1.0]) )
	
	def test_orthonormalise_3(self):
		vectors = [ np.array([1.0,0.0]), np.array([1.0,1.0]) ]
		vectors,norms = self.method(vectors)
		assert_allclose( vectors[0], np.array([1.0,0.0]) )
		assert_allclose( vectors[1], np.array([0.0,1.0]) )
		assert_allclose( norms, np.array([1.0,1.0]) )
	
	def test_orthonormalise_4(self):
		vectors = [ np.array([1.0,1.0]), np.array([1.0,1.0]) ]
		vectors,norms = self.method(vectors)
		assert_allclose( vectors[0], np.array([np.sqrt(0.5),np.sqrt(0.5)]) )
		assert_allclose( norms, np.array([np.sqrt(2),0.0]) , atol = 1e-10 )
	
	def test_orthonormalise_5(self):
		vectors = [ np.array([1.0,1.0]), np.array([1.0,-1.0]) ]
		vectors,norms = self.method(vectors)
		assert_allclose( vectors[0], np.array([np.sqrt(0.5),np.sqrt(0.5)]) )
		assert_allclose( vectors[1], np.array([np.sqrt(0.5),-np.sqrt(0.5)]) )
		assert_allclose( norms, np.array([np.sqrt(2),np.sqrt(2)]) )
	
	def test_orthonormalise_6(self):
		vectors = [ np.array([1.0,1.0]), np.array([1.0,0.0]) ]
		vectors,norms = self.method(vectors)
		assert_allclose( vectors[0], np.array([np.sqrt(0.5),np.sqrt(0.5)]) )
		assert_allclose( vectors[1], np.array([np.sqrt(0.5),-np.sqrt(0.5)]) )
		assert_allclose( norms, np.array([np.sqrt(2),np.sqrt(0.5)]) )

class OrthonormaliseQRTest(OrthonormaliseTest):
	def method(self,vectors):
		return orthonormalise_qr(vectors)

class OrthonormaliseCompare(unittest.TestCase):
	def test_random_vectors(self):
		rng = np.random.default_rng(seed=42)
		for _ in range(100):
			dims = sorted(rng.integers(1,10,2))
			vectors = rng.random(np.prod(dims))
			vectors_gs = [ vectors[i*dims[1]:(i+1)*dims[1]].copy() for i in range(dims[0]) ]
			vectors_qr,norms_qr = orthonormalise_qr(vectors.reshape(dims).copy())
			norms_gs = orthonormalise(vectors_gs)
			assert_allclose(vectors_gs,vectors_qr)
			assert_allclose(norms_gs,norms_qr)

class RelDistTest(unittest.TestCase):
	def test_reldist_1(self):
		assert_allclose( rel_dist(1,3), 1.0 )
	
	def test_reldist_2(self):
		assert_allclose( rel_dist(1,1+1e-10), 1e-10 )
	
	def test_reldist_3(self):
		assert_allclose( rel_dist([1,1],[1+1e-10,1]), 1e-10 )
	
if __name__ == "__main__":
	unittest.main(buffer=True)
